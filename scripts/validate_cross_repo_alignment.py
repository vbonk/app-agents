#!/usr/bin/env python3
"""
Cross-Repository Alignment Validation Script

Validates that schemas, configurations, and standards are aligned across:
- saas-ecosystem-architecture
- app-agents  
- saas-spec-driven-development
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import subprocess
# import yaml  # Optional dependency
from dataclasses import dataclass
from datetime import datetime

@dataclass
class AlignmentIssue:
    severity: str  # 'error', 'warning', 'info'
    category: str
    message: str
    repository: str
    file_path: Optional[str] = None
    fix_suggestion: Optional[str] = None

class CrossRepoAlignmentValidator:
    """Validates alignment across the three core repositories"""
    
    def __init__(self, workspace_path: str = "/Users/tony/Projects"):
        self.workspace_path = Path(workspace_path)
        self.issues: List[AlignmentIssue] = []
        
        # Repository paths
        self.repos = {
            'saas-ecosystem-architecture': self.workspace_path / 'saas-ecosystem-architecture',
            'app-agents': self.workspace_path / 'app-agents',
            'saas-spec-driven-development': self.workspace_path / 'saas-spec-driven-development'
        }
        
    def validate_repository_existence(self) -> bool:
        """Check that all required repositories exist"""
        all_exist = True
        
        for repo_name, repo_path in self.repos.items():
            if not repo_path.exists():
                self.issues.append(AlignmentIssue(
                    severity='error',
                    category='repository',
                    message=f"Repository {repo_name} not found at {repo_path}",
                    repository=repo_name,
                    fix_suggestion=f"Clone repository or update path configuration"
                ))
                all_exist = False
            else:
                self.issues.append(AlignmentIssue(
                    severity='info',
                    category='repository',
                    message=f"Repository {repo_name} found",
                    repository=repo_name
                ))
        
        return all_exist
    
    def validate_prisma_schemas(self) -> bool:
        """Validate Prisma schema alignment across repositories"""
        schema_files = {}
        
        # Find Prisma schema files
        for repo_name, repo_path in self.repos.items():
            if not repo_path.exists():
                continue
                
            schema_paths = list(repo_path.rglob("schema.prisma"))
            if schema_paths:
                schema_files[repo_name] = schema_paths[0]
            else:
                self.issues.append(AlignmentIssue(
                    severity='warning',
                    category='schema',
                    message=f"No Prisma schema found in {repo_name}",
                    repository=repo_name,
                    fix_suggestion="Create schema.prisma file if database integration is needed"
                ))
        
        # Validate schema consistency
        if len(schema_files) > 1:
            self._compare_prisma_schemas(schema_files)
        
        return len(self.get_issues_by_severity('error')) == 0
    
    def _compare_prisma_schemas(self, schema_files: Dict[str, Path]):
        """Compare Prisma schemas for consistency"""
        schemas = {}
        
        # Read all schemas
        for repo_name, schema_path in schema_files.items():
            try:
                with open(schema_path, 'r') as f:
                    schemas[repo_name] = f.read()
            except Exception as e:
                self.issues.append(AlignmentIssue(
                    severity='error',
                    category='schema',
                    message=f"Failed to read schema in {repo_name}: {e}",
                    repository=repo_name,
                    file_path=str(schema_path)
                ))
        
        # Check for agent-related models
        agent_models = ['Agent', 'AgentMemory', 'AgentTool', 'AgentMetric']
        primary_repo = 'saas-ecosystem-architecture'
        
        if primary_repo in schemas:
            primary_schema = schemas[primary_repo]
            
            for model in agent_models:
                if f"model {model}" not in primary_schema:
                    self.issues.append(AlignmentIssue(
                        severity='error',
                        category='schema',
                        message=f"Missing {model} model in primary schema",
                        repository=primary_repo,
                        file_path=str(schema_files[primary_repo]),
                        fix_suggestion=f"Add {model} model to primary schema"
                    ))
        
        # Check secondary repos reference primary models
        for repo_name, schema_content in schemas.items():
            if repo_name == primary_repo:
                continue
                
            if 'postgresql' not in schema_content.lower():
                self.issues.append(AlignmentIssue(
                    severity='error',
                    category='schema',
                    message=f"Schema in {repo_name} not using PostgreSQL",
                    repository=repo_name,
                    file_path=str(schema_files[repo_name]),
                    fix_suggestion="Update datasource to use PostgreSQL"
                ))
    
    def validate_package_dependencies(self) -> bool:
        """Validate package.json dependencies for consistency"""
        package_files = {}
        
        for repo_name, repo_path in self.repos.items():
            if not repo_path.exists():
                continue
                
            package_path = repo_path / "package.json"
            if package_path.exists():
                try:
                    with open(package_path, 'r') as f:
                        package_files[repo_name] = json.load(f)
                except Exception as e:
                    self.issues.append(AlignmentIssue(
                        severity='error',
                        category='dependencies',
                        message=f"Failed to read package.json in {repo_name}: {e}",
                        repository=repo_name,
                        file_path=str(package_path)
                    ))
        
        # Check for critical dependencies
        critical_deps = ['prisma', '@prisma/client']
        
        for repo_name, package_data in package_files.items():
            all_deps = {**package_data.get('dependencies', {}), **package_data.get('devDependencies', {})}
            
            for dep in critical_deps:
                if dep not in all_deps:
                    self.issues.append(AlignmentIssue(
                        severity='warning',
                        category='dependencies',
                        message=f"Missing {dep} dependency in {repo_name}",
                        repository=repo_name,
                        fix_suggestion=f"Add {dep} to dependencies"
                    ))
        
        return len(self.get_issues_by_severity('error')) == 0
    
    def validate_environment_alignment(self) -> bool:
        """Validate environment variable alignment"""
        env_files = {}
        
        for repo_name, repo_path in self.repos.items():
            if not repo_path.exists():
                continue
                
            env_example = repo_path / ".env.example"
            if env_example.exists():
                try:
                    with open(env_example, 'r') as f:
                        env_files[repo_name] = f.read()
                except Exception as e:
                    self.issues.append(AlignmentIssue(
                        severity='error',
                        category='environment',
                        message=f"Failed to read .env.example in {repo_name}: {e}",
                        repository=repo_name,
                        file_path=str(env_example)
                    ))
        
        # Check for required environment variables
        required_vars = ['DATABASE_URL', 'NEXTAUTH_SECRET', 'NEXTAUTH_URL']
        
        for repo_name, env_content in env_files.items():
            for var in required_vars:
                if var not in env_content:
                    self.issues.append(AlignmentIssue(
                        severity='warning',
                        category='environment',
                        message=f"Missing {var} in {repo_name} .env.example",
                        repository=repo_name,
                        fix_suggestion=f"Add {var} to .env.example"
                    ))
        
        return True
    
    def validate_documentation_alignment(self) -> bool:
        """Validate documentation references and alignment"""
        # Check for CLAUDE.md files
        for repo_name, repo_path in self.repos.items():
            if not repo_path.exists():
                continue
                
            claude_md = repo_path / "CLAUDE.md"
            if not claude_md.exists():
                self.issues.append(AlignmentIssue(
                    severity='warning',
                    category='documentation',
                    message=f"Missing CLAUDE.md in {repo_name}",
                    repository=repo_name,
                    fix_suggestion="Create CLAUDE.md with repository-specific guidance"
                ))
            else:
                # Check for PostgreSQL references
                try:
                    with open(claude_md, 'r') as f:
                        content = f.read()
                    
                    if 'sqlite' in content.lower() and 'postgresql' not in content.lower():
                        self.issues.append(AlignmentIssue(
                            severity='error',
                            category='documentation',
                            message=f"CLAUDE.md in {repo_name} references SQLite but not PostgreSQL",
                            repository=repo_name,
                            file_path=str(claude_md),
                            fix_suggestion="Update documentation to reflect PostgreSQL standardization"
                        ))
                except Exception as e:
                    self.issues.append(AlignmentIssue(
                        severity='error',
                        category='documentation',
                        message=f"Failed to read CLAUDE.md in {repo_name}: {e}",
                        repository=repo_name,
                        file_path=str(claude_md)
                    ))
        
        return True
    
    def validate_git_coordination(self) -> bool:
        """Validate Git coordination and branch alignment"""
        for repo_name, repo_path in self.repos.items():
            if not repo_path.exists():
                continue
                
            try:
                # Check current branch
                result = subprocess.run(
                    ['git', 'branch', '--show-current'],
                    cwd=repo_path,
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    branch = result.stdout.strip()
                    self.issues.append(AlignmentIssue(
                        severity='info',
                        category='git',
                        message=f"{repo_name} on branch: {branch}",
                        repository=repo_name
                    ))
                else:
                    self.issues.append(AlignmentIssue(
                        severity='warning',
                        category='git',
                        message=f"Could not determine branch for {repo_name}",
                        repository=repo_name
                    ))
                
                # Check for uncommitted changes
                result = subprocess.run(
                    ['git', 'status', '--porcelain'],
                    cwd=repo_path,
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0 and result.stdout.strip():
                    self.issues.append(AlignmentIssue(
                        severity='warning',
                        category='git',
                        message=f"Uncommitted changes in {repo_name}",
                        repository=repo_name,
                        fix_suggestion="Commit or stash changes before coordination"
                    ))
                    
            except Exception as e:
                self.issues.append(AlignmentIssue(
                    severity='error',
                    category='git',
                    message=f"Git validation failed for {repo_name}: {e}",
                    repository=repo_name
                ))
        
        return True
    
    def get_issues_by_severity(self, severity: str) -> List[AlignmentIssue]:
        """Get issues filtered by severity"""
        return [issue for issue in self.issues if issue.severity == severity]
    
    def get_issues_by_category(self, category: str) -> List[AlignmentIssue]:
        """Get issues filtered by category"""
        return [issue for issue in self.issues if issue.category == category]
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive alignment report"""
        return {
            "validation_timestamp": datetime.utcnow().isoformat(),
            "repositories_checked": list(self.repos.keys()),
            "summary": {
                "total_issues": len(self.issues),
                "errors": len(self.get_issues_by_severity('error')),
                "warnings": len(self.get_issues_by_severity('warning')),
                "info": len(self.get_issues_by_severity('info'))
            },
            "categories": {
                "repository": len(self.get_issues_by_category('repository')),
                "schema": len(self.get_issues_by_category('schema')),
                "dependencies": len(self.get_issues_by_category('dependencies')),
                "environment": len(self.get_issues_by_category('environment')),
                "documentation": len(self.get_issues_by_category('documentation')),
                "git": len(self.get_issues_by_category('git'))
            },
            "issues": [
                {
                    "severity": issue.severity,
                    "category": issue.category,
                    "message": issue.message,
                    "repository": issue.repository,
                    "file_path": issue.file_path,
                    "fix_suggestion": issue.fix_suggestion
                }
                for issue in self.issues
            ]
        }
    
    def run_full_validation(self) -> bool:
        """Run all validation checks"""
        print("🔍 Running cross-repository alignment validation...")
        
        validators = [
            ("Repository Existence", self.validate_repository_existence),
            ("Prisma Schemas", self.validate_prisma_schemas),
            ("Package Dependencies", self.validate_package_dependencies),
            ("Environment Alignment", self.validate_environment_alignment),
            ("Documentation Alignment", self.validate_documentation_alignment),
            ("Git Coordination", self.validate_git_coordination)
        ]
        
        all_passed = True
        
        for name, validator in validators:
            print(f"  📋 Validating {name}...")
            try:
                result = validator()
                if not result:
                    all_passed = False
                    print(f"  ❌ {name} validation failed")
                else:
                    print(f"  ✅ {name} validation passed")
            except Exception as e:
                print(f"  💥 {name} validation error: {e}")
                all_passed = False
        
        return all_passed

def main():
    """Main validation entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate cross-repository alignment")
    parser.add_argument("--workspace", default="/Users/tony/Projects", help="Workspace path")
    parser.add_argument("--output", help="Output report file path")
    parser.add_argument("--fix", action="store_true", help="Attempt to fix issues automatically")
    
    args = parser.parse_args()
    
    validator = CrossRepoAlignmentValidator(args.workspace)
    success = validator.run_full_validation()
    
    # Generate report
    report = validator.generate_report()
    
    # Output results
    print(f"\n📊 Validation Summary:")
    print(f"  Total Issues: {report['summary']['total_issues']}")
    print(f"  Errors: {report['summary']['errors']}")
    print(f"  Warnings: {report['summary']['warnings']}")
    print(f"  Info: {report['summary']['info']}")
    
    if report['summary']['errors'] > 0:
        print(f"\n❌ Critical errors found:")
        for issue in validator.get_issues_by_severity('error'):
            print(f"  • {issue.repository}: {issue.message}")
            if issue.fix_suggestion:
                print(f"    💡 Fix: {issue.fix_suggestion}")
    
    if report['summary']['warnings'] > 0:
        print(f"\n⚠️  Warnings:")
        for issue in validator.get_issues_by_severity('warning'):
            print(f"  • {issue.repository}: {issue.message}")
    
    # Save report
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"📄 Report saved to: {args.output}")
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()