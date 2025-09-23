#!/usr/bin/env python3
"""
SQLite to PostgreSQL Migration Tool
Migrates all agent data from SQLite databases to PostgreSQL/Prisma
"""

import asyncio
import sqlite3
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import asyncpg
from dataclasses import dataclass

@dataclass
class MigrationResult:
    agent_id: str
    success: bool
    records_migrated: int
    errors: List[str]
    duration_seconds: float

class SQLiteToPostgresMigrator:
    """Migrates agent data from SQLite to PostgreSQL with Prisma compatibility"""
    
    def __init__(self, postgres_url: str, dry_run: bool = False):
        self.postgres_url = postgres_url
        self.dry_run = dry_run
        self.migration_log: List[str] = []
        
    async def connect_postgres(self) -> asyncpg.Connection:
        """Establish PostgreSQL connection"""
        try:
            conn = await asyncpg.connect(self.postgres_url)
            self.log("Connected to PostgreSQL successfully")
            return conn
        except Exception as e:
            self.log(f"Failed to connect to PostgreSQL: {e}")
            raise

    def find_sqlite_databases(self, base_path: str = "./agents") -> List[Path]:
        """Find all SQLite database files in agent directories"""
        sqlite_files = []
        base_path = Path(base_path)
        
        # Common SQLite file patterns
        patterns = ["*.db", "*.sqlite", "*.sqlite3", "memory.db", "agent_memory.db"]
        
        for pattern in patterns:
            sqlite_files.extend(base_path.rglob(pattern))
            
        self.log(f"Found {len(sqlite_files)} SQLite databases")
        return sqlite_files

    def extract_agent_memory(self, sqlite_path: Path) -> List[Dict[str, Any]]:
        """Extract memory records from SQLite database"""
        try:
            conn = sqlite3.connect(str(sqlite_path))
            cursor = conn.cursor()
            
            # Get table schema
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            
            memory_records = []
            
            # Common table patterns for agent memory
            memory_tables = ['memory', 'agent_memory', 'memories', 'conversation_memory']
            
            for table in tables:
                if any(pattern in table.lower() for pattern in memory_tables):
                    cursor.execute(f"SELECT * FROM {table}")
                    columns = [description[0] for description in cursor.description]
                    
                    for row in cursor.fetchall():
                        record = dict(zip(columns, row))
                        record['source_table'] = table
                        record['migrated_at'] = datetime.utcnow().isoformat()
                        memory_records.append(record)
            
            conn.close()
            self.log(f"Extracted {len(memory_records)} memory records from {sqlite_path}")
            return memory_records
            
        except Exception as e:
            self.log(f"Error extracting from {sqlite_path}: {e}")
            return []

    def extract_agent_tools(self, sqlite_path: Path) -> List[Dict[str, Any]]:
        """Extract tool registry from SQLite database"""
        try:
            conn = sqlite3.connect(str(sqlite_path))
            cursor = conn.cursor()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            
            tool_records = []
            tool_tables = ['tools', 'agent_tools', 'tool_registry']
            
            for table in tables:
                if any(pattern in table.lower() for pattern in tool_tables):
                    cursor.execute(f"SELECT * FROM {table}")
                    columns = [description[0] for description in cursor.description]
                    
                    for row in cursor.fetchall():
                        record = dict(zip(columns, row))
                        record['source_table'] = table
                        record['migrated_at'] = datetime.utcnow().isoformat()
                        tool_records.append(record)
            
            conn.close()
            return tool_records
            
        except Exception as e:
            self.log(f"Error extracting tools from {sqlite_path}: {e}")
            return []

    def extract_agent_metrics(self, sqlite_path: Path) -> List[Dict[str, Any]]:
        """Extract performance metrics from SQLite database"""
        try:
            conn = sqlite3.connect(str(sqlite_path))
            cursor = conn.cursor()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            
            metric_records = []
            metric_tables = ['metrics', 'performance', 'agent_metrics', 'execution_log']
            
            for table in tables:
                if any(pattern in table.lower() for pattern in metric_tables):
                    cursor.execute(f"SELECT * FROM {table}")
                    columns = [description[0] for description in cursor.description]
                    
                    for row in cursor.fetchall():
                        record = dict(zip(columns, row))
                        record['source_table'] = table
                        record['migrated_at'] = datetime.utcnow().isoformat()
                        metric_records.append(record)
            
            conn.close()
            return metric_records
            
        except Exception as e:
            self.log(f"Error extracting metrics from {sqlite_path}: {e}")
            return []

    async def insert_agent_data(self, conn: asyncpg.Connection, agent_id: str, 
                              memories: List[Dict], tools: List[Dict], 
                              metrics: List[Dict]) -> MigrationResult:
        """Insert extracted data into PostgreSQL"""
        start_time = datetime.now()
        errors = []
        total_records = 0
        
        try:
            async with conn.transaction():
                # Ensure agent exists
                agent_exists = await conn.fetchval(
                    "SELECT EXISTS(SELECT 1 FROM agents WHERE id = $1)", agent_id
                )
                
                if not agent_exists:
                    # Create basic agent record
                    await conn.execute("""
                        INSERT INTO agents (id, name, version, description, category, status, created_at)
                        VALUES ($1, $2, $3, $4, $5, $6, $7)
                    """, agent_id, f"Migrated Agent {agent_id}", "1.0.0", 
                    f"Agent migrated from SQLite", "OPERATIONAL", "ACTIVE", datetime.utcnow())
                
                # Insert memories
                for memory in memories:
                    try:
                        await conn.execute("""
                            INSERT INTO agent_memories (id, agent_id, content, metadata, embedding, created_at)
                            VALUES (gen_random_uuid(), $1, $2, $3, NULL, $4)
                        """, agent_id, json.dumps(memory), json.dumps(memory.get('metadata', {})), 
                        datetime.utcnow())
                        total_records += 1
                    except Exception as e:
                        errors.append(f"Memory insert error: {e}")
                
                # Insert tools
                for tool in tools:
                    try:
                        await conn.execute("""
                            INSERT INTO agent_tools (id, agent_id, name, description, configuration, created_at)
                            VALUES (gen_random_uuid(), $1, $2, $3, $4, $5)
                        """, agent_id, tool.get('name', 'Unknown Tool'), 
                        tool.get('description', ''), json.dumps(tool), datetime.utcnow())
                        total_records += 1
                    except Exception as e:
                        errors.append(f"Tool insert error: {e}")
                
                # Insert metrics
                for metric in metrics:
                    try:
                        await conn.execute("""
                            INSERT INTO agent_metrics (id, agent_id, metric_name, value, metadata, timestamp)
                            VALUES (gen_random_uuid(), $1, $2, $3, $4, $5)
                        """, agent_id, metric.get('metric_name', 'migrated_metric'),
                        float(metric.get('value', 0)), json.dumps(metric), datetime.utcnow())
                        total_records += 1
                    except Exception as e:
                        errors.append(f"Metric insert error: {e}")
                
        except Exception as e:
            errors.append(f"Transaction error: {e}")
        
        duration = (datetime.now() - start_time).total_seconds()
        return MigrationResult(
            agent_id=agent_id,
            success=len(errors) == 0,
            records_migrated=total_records,
            errors=errors,
            duration_seconds=duration
        )

    def identify_agent_from_path(self, sqlite_path: Path) -> Optional[str]:
        """Extract agent ID from file path"""
        # Try to identify agent from directory structure
        path_parts = sqlite_path.parts
        
        # Look for common patterns
        for i, part in enumerate(path_parts):
            if part == 'agents' and i + 1 < len(path_parts):
                # Next part might be category, then agent name
                if i + 2 < len(path_parts):
                    return f"{path_parts[i+1]}_{path_parts[i+2]}"
                else:
                    return path_parts[i+1]
        
        # Fallback to parent directory name
        return sqlite_path.parent.name

    async def migrate_single_agent(self, conn: asyncpg.Connection, 
                                 sqlite_path: Path) -> MigrationResult:
        """Migrate a single agent's SQLite database to PostgreSQL"""
        agent_id = self.identify_agent_from_path(sqlite_path)
        
        self.log(f"Migrating agent: {agent_id} from {sqlite_path}")
        
        if self.dry_run:
            self.log(f"DRY RUN: Would migrate {agent_id}")
            return MigrationResult(agent_id, True, 0, [], 0.0)
        
        # Extract data
        memories = self.extract_agent_memory(sqlite_path)
        tools = self.extract_agent_tools(sqlite_path)
        metrics = self.extract_agent_metrics(sqlite_path)
        
        # Insert into PostgreSQL
        result = await self.insert_agent_data(conn, agent_id, memories, tools, metrics)
        
        if result.success:
            self.log(f"Successfully migrated {agent_id}: {result.records_migrated} records")
        else:
            self.log(f"Failed to migrate {agent_id}: {result.errors}")
        
        return result

    async def migrate_all_agents(self, base_path: str = "./agents") -> List[MigrationResult]:
        """Migrate all agent databases to PostgreSQL"""
        self.log("Starting SQLite to PostgreSQL migration")
        
        # Find all SQLite databases
        sqlite_files = self.find_sqlite_databases(base_path)
        
        if not sqlite_files:
            self.log("No SQLite databases found")
            return []
        
        # Connect to PostgreSQL
        conn = await self.connect_postgres()
        
        try:
            results = []
            for sqlite_file in sqlite_files:
                result = await self.migrate_single_agent(conn, sqlite_file)
                results.append(result)
            
            # Summary
            successful = sum(1 for r in results if r.success)
            total_records = sum(r.records_migrated for r in results)
            
            self.log(f"Migration complete: {successful}/{len(results)} agents migrated")
            self.log(f"Total records migrated: {total_records}")
            
            return results
            
        finally:
            await conn.close()

    def create_backup_script(self, sqlite_files: List[Path]) -> str:
        """Generate backup script for SQLite files"""
        backup_script = "#!/bin/bash\n"
        backup_script += "# Backup SQLite files before migration\n"
        backup_script += f"mkdir -p ./backups/sqlite_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}\n"
        
        for sqlite_file in sqlite_files:
            backup_script += f"cp {sqlite_file} ./backups/sqlite_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}/\n"
        
        return backup_script

    def log(self, message: str):
        """Log migration progress"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        self.migration_log.append(log_message)

    def save_migration_report(self, results: List[MigrationResult]):
        """Save detailed migration report"""
        report = {
            "migration_date": datetime.utcnow().isoformat(),
            "total_agents": len(results),
            "successful_migrations": sum(1 for r in results if r.success),
            "total_records_migrated": sum(r.records_migrated for r in results),
            "results": [
                {
                    "agent_id": r.agent_id,
                    "success": r.success,
                    "records_migrated": r.records_migrated,
                    "duration_seconds": r.duration_seconds,
                    "errors": r.errors
                }
                for r in results
            ],
            "migration_log": self.migration_log
        }
        
        report_path = f"migration_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.log(f"Migration report saved to: {report_path}")

async def main():
    """Main migration entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Migrate SQLite agent data to PostgreSQL")
    parser.add_argument("--postgres-url", required=True, help="PostgreSQL connection URL")
    parser.add_argument("--agents-path", default="./agents", help="Path to agents directory")
    parser.add_argument("--dry-run", action="store_true", help="Perform dry run without actual migration")
    parser.add_argument("--backup", action="store_true", help="Create backup script for SQLite files")
    
    args = parser.parse_args()
    
    migrator = SQLiteToPostgresMigrator(args.postgres_url, args.dry_run)
    
    if args.backup:
        sqlite_files = migrator.find_sqlite_databases(args.agents_path)
        backup_script = migrator.create_backup_script(sqlite_files)
        with open("backup_sqlite.sh", "w") as f:
            f.write(backup_script)
        print("Backup script created: backup_sqlite.sh")
        return
    
    try:
        results = await migrator.migrate_all_agents(args.agents_path)
        migrator.save_migration_report(results)
        
        # Exit with error code if any migrations failed
        if any(not r.success for r in results):
            sys.exit(1)
            
    except Exception as e:
        print(f"Migration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())