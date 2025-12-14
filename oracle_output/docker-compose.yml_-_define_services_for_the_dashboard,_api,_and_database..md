```yaml
version: '3.8'

services:
  # Frontend Dashboard
  dashboard:
    build: ./dashboard
    container_name: app-dashboard
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - REACT_APP_API_URL=http://api:8000
    depends_on:
      - api
    networks:
      - app-network
    restart: unless-stopped

  # Backend API
  api:
    build: ./api
    container_name: app-api
    ports:
      - "8000:8000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://postgres:password@db:5432/appdb
      - JWT_SECRET=${JWT_SECRET:-your-secret-key-change-in-production}
    depends_on:
      db:
        condition: service_healthy
    networks:
      - app-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # PostgreSQL Database
  db:
    image: postgres:15-alpine
    container_name: app-db
    environment:
      - POSTGRES_DB=appdb
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - app-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

networks:
  app-network:
    driver: bridge

volumes:
  postgres_data:
```

## Key Features:
- **Dashboard**: React app on port 3000 with API connectivity
- **API**: Node.js backend on port 8000 with health checks
- **Database**: PostgreSQL with persistent storage and initialization script support
- **Network**: Isolated bridge network for secure inter-service communication
- **Dependencies**: Proper service startup ordering with health checks
- **Security**: Environment variables for sensitive configuration
- **Reliability**: Automatic restart policies for production resilience

## Usage:
1. Create `dashboard/` and `api/` directories with respective `Dockerfile`s
2. Place database initialization in `init.sql`
3. Set `JWT_SECRET` in `.env` file for production
4. Run: `docker-compose up -d`