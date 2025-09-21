# Constitution Service Deployment Checklist

## Pre-Deployment Requirements

### ✅ Completed in Current Session
- [x] Service implementation complete
- [x] Database schema created
- [x] API endpoints functional
- [x] Test suite passing (5/5 tests)
- [x] Documentation created
- [x] Code committed locally
- [x] Integration with app-agents repository

### ⏳ Pending Actions

#### Git Repository
- [ ] Resolve GitHub authentication
- [ ] Push commits to remote repository
- [ ] Verify GitHub Actions workflows (if any)
- [ ] Create pull request if using feature branch workflow

#### Database Setup
- [ ] Provision PostgreSQL 14+ in production environment
- [ ] Install pgvector extension
- [ ] Create production database and user
- [ ] Run schema creation script:
  ```sql
  CREATE TABLE constitutions (
      id SERIAL PRIMARY KEY,
      name VARCHAR(255) NOT NULL,
      description TEXT,
      rules JSONB
  );
  ```
- [ ] Configure database connection security
- [ ] Set up database backups

#### Environment Configuration
- [ ] Create production environment variables:
  - `DATABASE_URL` or individual DB connection params
  - `NODE_ENV=production`
  - `PORT` (if different from 3000)
- [ ] Update `src/db.ts` for production configuration
- [ ] Configure SSL/TLS for database connections
- [ ] Set up logging configuration

#### Service Deployment
- [ ] Choose hosting platform (AWS, GCP, Azure, Railway, etc.)
- [ ] Configure deployment pipeline
- [ ] Set up health checks
- [ ] Configure monitoring and alerting
- [ ] Set up load balancing (if needed)
- [ ] Configure HTTPS/SSL certificates

#### Security Hardening
- [ ] Replace trust authentication with proper credentials
- [ ] Implement input validation and sanitization
- [ ] Add rate limiting
- [ ] Configure CORS policies
- [ ] Set up API authentication/authorization
- [ ] Implement request logging and audit trails

#### Testing and Validation
- [ ] Run integration tests against production database
- [ ] Perform load testing
- [ ] Validate API endpoints in production
- [ ] Test error handling and recovery
- [ ] Verify monitoring and alerting

## Deployment Commands Reference

### Local Development
```bash
cd services/constitution-service
npm install
npm run build
npm start
```

### Production Deployment (Example)
```bash
# Build for production
npm run build

# Start with production environment
NODE_ENV=production npm start

# Or using PM2 for process management
pm2 start dist/index.js --name constitution-service
```

### Database Migration
```bash
# Connect to production database
psql $DATABASE_URL

# Create table
CREATE TABLE constitutions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    rules JSONB
);

# Verify table creation
\dt constitutions
```

## Monitoring and Maintenance

### Health Check Endpoint
Consider adding a health check endpoint:
```typescript
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});
```

### Logging
Implement structured logging for production:
```typescript
import winston from 'winston';

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});
```

### Metrics to Monitor
- API response times
- Database connection pool status
- Error rates by endpoint
- Request volume
- Database query performance

## Rollback Plan

### Database Rollback
- Keep database backups before schema changes
- Document rollback procedures
- Test rollback scenarios

### Service Rollback
- Maintain previous service version
- Use blue-green deployment strategy
- Have automated rollback triggers

## Post-Deployment Verification

### Functional Tests
```bash
# Test all endpoints
curl -X GET http://your-domain/constitutions
curl -X POST http://your-domain/constitutions -H "Content-Type: application/json" -d '{"name":"Test","description":"Test constitution","rules":{}}'
```

### Performance Tests
- Load testing with expected traffic
- Database performance under load
- Memory and CPU usage monitoring

## Integration with Existing Agents

### Next Steps After Deployment
1. Update agent configurations to use Constitution Service
2. Implement constitution-based behavior in agents
3. Create constitution templates for different agent types
4. Set up constitution versioning and change management

## Documentation Updates

### Post-Deployment
- [ ] Update service documentation with production URLs
- [ ] Create API documentation (OpenAPI/Swagger)
- [ ] Update main repository README
- [ ] Create deployment runbooks
- [ ] Document troubleshooting procedures
