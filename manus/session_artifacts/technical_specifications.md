# Constitution Service Technical Specifications

## Service Architecture

### Technology Stack
- **Runtime**: Node.js 22.19.0 LTS
- **Language**: TypeScript 5.9.2
- **Web Framework**: Express.js 5.1.0
- **Database**: PostgreSQL 14+ with pgvector extension
- **Database Client**: pg 8.16.3
- **Testing**: Jest 29.x with Supertest
- **Build Tool**: TypeScript Compiler (tsc)

### System Requirements
- **Memory**: Minimum 512MB RAM
- **CPU**: 1 vCPU minimum
- **Storage**: 1GB minimum for application and logs
- **Network**: HTTP/HTTPS access on configurable port (default 3000)

## Database Design

### Schema Definition
```sql
CREATE TABLE constitutions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    rules JSONB
);
```

### Data Types and Constraints
- **id**: Auto-incrementing primary key
- **name**: Required string, max 255 characters
- **description**: Optional text field, unlimited length
- **rules**: JSONB for flexible rule storage and querying

### Indexing Strategy
```sql
-- Primary key index (automatic)
-- Consider adding for performance:
CREATE INDEX idx_constitutions_name ON constitutions(name);
CREATE INDEX idx_constitutions_rules ON constitutions USING GIN(rules);
```

## API Specification

### Base URL
- Development: `http://localhost:3000`
- Production: `https://your-domain.com`

### Content Type
- Request: `application/json`
- Response: `application/json`

### Endpoints

#### POST /constitutions
**Purpose**: Create a new constitution

**Request Body**:
```typescript
interface CreateConstitutionRequest {
  name: string;           // Required, max 255 chars
  description?: string;   // Optional
  rules: object;          // Required, any valid JSON object
}
```

**Response**: `201 Created`
```typescript
interface ConstitutionResponse {
  id: number;
  name: string;
  description: string | null;
  rules: object;
}
```

**Error Responses**:
- `400 Bad Request`: Invalid input data
- `500 Internal Server Error`: Database or server error

#### GET /constitutions
**Purpose**: Retrieve all constitutions

**Response**: `200 OK`
```typescript
interface ConstitutionResponse[] {
  id: number;
  name: string;
  description: string | null;
  rules: object;
}
```

#### GET /constitutions/:id
**Purpose**: Retrieve a specific constitution

**Parameters**:
- `id`: Integer, constitution ID

**Response**: `200 OK`
```typescript
interface ConstitutionResponse {
  id: number;
  name: string;
  description: string | null;
  rules: object;
}
```

**Error Responses**:
- `404 Not Found`: Constitution not found
- `500 Internal Server Error`: Database or server error

#### PUT /constitutions/:id
**Purpose**: Update an existing constitution

**Parameters**:
- `id`: Integer, constitution ID

**Request Body**:
```typescript
interface UpdateConstitutionRequest {
  name: string;           // Required
  description?: string;   // Optional
  rules: object;          // Required
}
```

**Response**: `200 OK`
```typescript
interface ConstitutionResponse {
  id: number;
  name: string;
  description: string | null;
  rules: object;
}
```

#### DELETE /constitutions/:id
**Purpose**: Delete a constitution

**Parameters**:
- `id`: Integer, constitution ID

**Response**: `200 OK`
```json
"Constitution was deleted!"
```

## Error Handling

### Error Response Format
```typescript
interface ErrorResponse {
  error: string;
  message: string;
  statusCode: number;
}
```

### HTTP Status Codes
- `200 OK`: Successful operation
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server or database error

### Logging Strategy
- All requests logged with timestamp, method, URL, and response status
- Errors logged with full stack trace
- Database operations logged for debugging
- Structured logging format for production monitoring

## Security Considerations

### Current Implementation
- **Authentication**: None (development only)
- **Authorization**: None (development only)
- **Input Validation**: Basic Express.js JSON parsing
- **Database**: Trust authentication (development only)

### Production Security Requirements
- **Authentication**: JWT or API key based
- **Authorization**: Role-based access control
- **Input Validation**: Schema validation with Joi or similar
- **Database**: Encrypted connections, proper user credentials
- **Rate Limiting**: Implement request rate limiting
- **CORS**: Configure appropriate CORS policies
- **HTTPS**: Enforce HTTPS in production

## Performance Characteristics

### Database Connection Pooling
```typescript
const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'postgres',
  password: '',
  port: 5432,
  max: 20,          // Maximum connections in pool
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});
```

### Expected Performance
- **Throughput**: 1000+ requests/second (single instance)
- **Latency**: <100ms for simple CRUD operations
- **Concurrent Connections**: 20 database connections
- **Memory Usage**: ~50MB base + ~1MB per concurrent request

## Monitoring and Observability

### Health Checks
Implement health check endpoint:
```typescript
app.get('/health', async (req, res) => {
  try {
    await pool.query('SELECT 1');
    res.json({ status: 'healthy', database: 'connected' });
  } catch (error) {
    res.status(503).json({ status: 'unhealthy', database: 'disconnected' });
  }
});
```

### Metrics to Track
- Request count by endpoint
- Response time percentiles (p50, p95, p99)
- Error rate by endpoint
- Database connection pool utilization
- Memory and CPU usage

### Logging Configuration
```typescript
// Production logging setup
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' }),
    new winston.transports.Console({
      format: winston.format.simple()
    })
  ]
});
```

## Deployment Configuration

### Environment Variables
```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@host:port/database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_password

# Application Configuration
NODE_ENV=production
PORT=3000
LOG_LEVEL=info

# Security Configuration
JWT_SECRET=your_jwt_secret
API_KEY=your_api_key
```

### Docker Configuration
```dockerfile
FROM node:22-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY dist/ ./dist/

EXPOSE 3000

CMD ["node", "dist/index.js"]
```

### Process Management
```bash
# Using PM2
pm2 start dist/index.js --name constitution-service --instances 2

# Using systemd
[Unit]
Description=Constitution Service
After=network.target

[Service]
Type=simple
User=app
WorkingDirectory=/app
ExecStart=/usr/bin/node dist/index.js
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## Testing Strategy

### Unit Tests
- All API endpoints tested with mocked database
- Error handling scenarios covered
- Input validation tested
- Database connection handling tested

### Integration Tests
- End-to-end API testing with real database
- Database transaction testing
- Connection pool testing
- Performance testing under load

### Test Coverage
- Current: 100% of API endpoints
- Target: 90%+ code coverage
- Automated testing in CI/CD pipeline

## Scalability Considerations

### Horizontal Scaling
- Stateless service design enables multiple instances
- Database connection pooling per instance
- Load balancer required for multiple instances

### Vertical Scaling
- Memory usage scales with concurrent requests
- CPU usage minimal for CRUD operations
- Database performance is primary bottleneck

### Caching Strategy
- Consider Redis for frequently accessed constitutions
- Database query result caching
- Application-level caching for static data

## Backup and Recovery

### Database Backup
```bash
# Daily backup
pg_dump $DATABASE_URL > constitution_backup_$(date +%Y%m%d).sql

# Point-in-time recovery setup
# Configure PostgreSQL WAL archiving
```

### Application Recovery
- Blue-green deployment strategy
- Automated health checks
- Rollback procedures documented
- Configuration backup and versioning
