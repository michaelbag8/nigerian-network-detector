# Nigerian Network Detector

A production-quality web application that detects which Nigerian mobile network provider originally allocated a given phone number prefix. Built with Python/FastAPI backend, React/TypeScript frontend, PostgreSQL database, and Docker.

## Features

- **Phone Number Normalization**: Accepts multiple input formats (09XXXXXXXXX, +2349XXXXXXXXX, 2349XXXXXXXXX, with or without spaces/dashes)
- **Network Detection**: Identifies the original network provider (MTN, Glo, Airtel, 9mobile) from the number's prefix
- **Mobile Number Portability (MNP) Awareness**: Clearly labels results as "Original Network" (not current network, since MNP allows porting)
- **Professional UI**: Responsive SaaS-style interface with provider branding, logos, and clear labeling
- **Production Security**: Input validation, rate limiting, SQL injection prevention, secure headers, CORS, secrets management
- **Comprehensive API**: RESTful endpoints with OpenAPI/Swagger documentation
- **Database-Driven**: Provider and prefix data stored in PostgreSQL, managed via Alembic migrations
- **Full Test Suite**: Unit tests, API tests, database tests with pytest
- **Docker Ready**: Compose configuration for dev and production environments

## Technology Stack

**Backend:**
- Python 3.12+
- FastAPI
- Pydantic v2
- SQLAlchemy (async)
- PostgreSQL
- Alembic (migrations)
- phonenumbers (Google's libphonenumber library)
- pytest

**Frontend:**
- React 18+
- TypeScript
- Vite
- Tailwind CSS

**Infrastructure:**
- Docker & Docker Compose
- Nginx (reverse proxy)
- PostgreSQL 15+
- Redis (optional, for rate limiting)

## Quick Start (Local Development)

### Prerequisites
- Python 3.12+
- Node.js 18+
- PostgreSQL 15+ (or use Docker Compose)
- Docker & Docker Compose (optional but recommended)

### Option 1: Local Setup (without Docker)

**Backend Setup:**

```bash
# Clone the repository
git clone https://github.com/michaelbag8/nigerian-network-detector.git
cd nigerian-network-detector

# Create Python virtual environment
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file and configure
cp .env.example .env
# Edit .env with your local PostgreSQL credentials

# Create database
creatdb nigerian_detector

# Run migrations
alembic upgrade head

# Seed the database with provider/prefix data
python -m app.scripts.seed_data

# Run the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

**Frontend Setup:**

```bash
# In a new terminal, from repository root
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Start dev server
npm run dev
```

Frontend will be available at `http://localhost:5173`

### Option 2: Docker Setup (Recommended)

```bash
# From repository root
docker compose up --build
```

This will start:
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`
- PostgreSQL: `postgres:5432` (internal to Docker network)
- Nginx: `http://localhost:80`

Wait for database to be ready (~10 seconds), then migrations and seeding will run automatically.

### Testing

**Backend Tests:**

```bash
cd backend
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_phone_normalizer.py -v
```

**Frontend Tests:**

```bash
cd frontend
npm run test
```

## Project Structure

```
nigerian-network-detector/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI application entry
│   │   ├── config.py               # Configuration management
│   │   ├── database.py             # Database setup & session factory
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── health.py       # Health check endpoints
│   │   │       ├── phones.py       # Phone detection endpoints
│   │   │       └── providers.py    # Provider list endpoints
│   │   ├── models/                 # SQLAlchemy ORM models
│   │   │   ├── provider.py
│   │   │   └── phone_prefix.py
│   │   ├── schemas/                # Pydantic request/response schemas
│   │   │   ├── phone.py
│   │   │   └── provider.py
│   │   ├── services/               # Business logic
│   │   │   ├── phone_normalizer.py
│   │   │   ├── phone_detector.py
│   │   │   └── carrier_lookup.py   # Placeholder for future MNP integration
│   │   ├── repositories/           # Data access layer
│   │   │   ├── provider_repository.py
│   │   │   └── prefix_repository.py
│   │   ├── middleware/
│   │   │   └── rate_limit.py       # Rate limiting middleware
│   │   ├── utils/
│   │   │   └── logging.py          # Structured logging setup
│   │   └── scripts/
│   │       └── seed_data.py        # Database seeding
│   ├── tests/
│   │   ├── test_phone_normalizer.py
│   │   ├── test_phone_detector.py
│   │   ├── test_api.py
│   │   └── test_repositories.py
│   ├── migrations/                 # Alembic migrations
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── Dockerfile
│   ├── .env.example
│   └── pytest.ini
├── frontend/
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── Header.tsx
│   │   │   ├── Hero.tsx
│   │   │   ├── PhoneDetector.tsx    # Main input/detection component
│   │   │   ├── ResultCard.tsx       # Results display
│   │   │   ├── SupportedNetworks.tsx
│   │   │   ├── HowItWorks.tsx
│   │   │   └── Footer.tsx
│   │   ├── services/
│   │   │   └── api.ts              # API client
│   │   ├── types/
│   │   │   └── index.ts            # TypeScript types
│   │   ├── styles/
│   │   │   └── globals.css
│   │   └── assets/
│   │       └── provider-logos/     # SVG placeholder logos
│   ├── public/
│   ├── Dockerfile
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── .env.example
│   └── package.json
├── docker-compose.yml
├── nginx.conf
├── .gitignore
├── .github/
│   └── workflows/
│       └── ci.yml
└── README.md
```

## API Endpoints

### Phone Detection

**GET** `/api/v1/phone/{phone_number}`

Detect the network provider for a given phone number.

**Parameters:**
- `phone_number` (path): Phone number in any accepted format

**Response (200):**
```json
{
  "phone_number": "+2349050003328",
  "country": "NG",
  "valid": true,
  "prefix": "905",
  "original_network": {
    "id": 1,
    "name": "MTN Nigeria",
    "slug": "mtn",
    "logo_url": "/logos/mtn.svg",
    "primary_color": "#ffd700",
    "secondary_color": "#000000"
  },
  "current_network": null,
  "ported": null,
  "detection_type": "prefix_based"
}
```

**Error (400):**
```json
{
  "error": {
    "code": "INVALID_PHONE_NUMBER",
    "message": "Phone number is not valid for Nigeria"
  }
}
```

### List Providers

**GET** `/api/v1/providers`

List all active network providers.

**Response (200):**
```json
{
  "providers": [
    {
      "id": 1,
      "name": "MTN Nigeria",
      "slug": "mtn",
      "logo_url": "/logos/mtn.svg",
      "primary_color": "#ffd700",
      "secondary_color": "#000000",
      "active": true
    }
  ]
}
```

### Health Check

**GET** `/api/v1/health`

Healthcheck endpoint (verifies database connectivity).

**Response (200):**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Version

**GET** `/api/v1/version`

Returns application version and build info.

**Response (200):**
```json
{
  "version": "1.0.0",
  "environment": "production",
  "build_date": "2024-01-15"
}
```

## Security Features

1. **Input Validation**: All inputs validated via Pydantic schemas before processing
2. **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries, no raw SQL string interpolation
3. **XSS Protection**: React/TypeScript automatic escaping, no dangerouslySetInnerHTML
4. **CORS**: Restricted to known origins via environment configuration
5. **Secure Headers**: HSTS, X-Content-Type-Options, X-Frame-Options, CSP (via Nginx in production)
6. **Rate Limiting**: 100 requests per minute per IP address (configurable)
7. **Request Size Limits**: Max 1MB request body
8. **Secrets Management**: All secrets in `.env` file (never committed), example config in `.env.example`
9. **Phone Number Privacy**: Sensitive phone numbers are masked/hashed in logs (only prefix logged at info level)
10. **HTTPS**: Enforced via Nginx reverse proxy in production with Let's Encrypt

## Data Privacy & Retention

- **What is persisted**: Only provider/prefix metadata (not user phone numbers)
- **What is temporary**: Phone numbers exist only for the duration of the API request/response cycle
- **Logging**: Phone numbers are masked (e.g., "90500..." or hashed) in application logs
- **No history**: No phone lookup history table in base build
- **Future consideration**: Real carrier/MNP lookup would require careful PII handling with explicit privacy policies

## Environment Variables

See `.env.example` for all available configuration. Key variables:

- `DATABASE_URL`: PostgreSQL connection string
- `ENVIRONMENT`: `development` or `production`
- `SECRET_KEY`: Used for session/security tokens (change in production!)
- `CORS_ORIGINS`: Comma-separated list of allowed frontend origins
- `RATE_LIMIT_ENABLED`: Enable/disable rate limiting
- `LOG_LEVEL`: `DEBUG`, `INFO`, `WARNING`, `ERROR`
- `VITE_API_BASE_URL`: Frontend API base URL (set by frontend .env)

## Production Deployment

### Deployment Checklist

- [ ] Use strong `SECRET_KEY` in production
- [ ] Set `ENVIRONMENT=production`
- [ ] Configure real domain name and HTTPS
- [ ] Set up database backups (daily, retained 30 days minimum)
- [ ] Use strong database password, restrict network access
- [ ] Enable security headers in Nginx
- [ ] Set up monitoring/alerting (application and infrastructure logs)
- [ ] Run security audit of dependencies: `pip audit`, `npm audit`
- [ ] Test health/version endpoints in production
- [ ] Set up log aggregation (e.g., ELK, Datadog, CloudWatch)
- [ ] Test database migration strategy before production upgrade
- [ ] Document runbooks for common incidents
- [ ] Implement database connection pooling (already configured)
- [ ] Use managed PostgreSQL service (e.g., AWS RDS) or secure self-hosted
- [ ] Enable slow query logging in PostgreSQL
- [ ] Set up CI/CD pipeline (GitHub Actions provided)

### Example Deployment (Linux/DigitalOcean/AWS)

```bash
# 1. Provision server, install Docker
sudo apt update && sudo apt install -y docker.io docker-compose git

# 2. Clone repository
git clone https://github.com/michaelbag8/nigerian-network-detector.git
cd nigerian-network-detector

# 3. Create production .env
cp .env.example .env
# Edit .env with production values, strong passwords, real domain

# 4. Set up SSL certificate (Let's Encrypt via Certbot)
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --standalone -d your-domain.com

# 5. Build and start services
sudo docker compose -f docker-compose.yml up -d

# 6. Verify services
curl http://localhost:8000/api/v1/health
curl http://localhost:3000/

# 7. Set up automated backups
# (Add cron job to backup PostgreSQL container volume)
```

### Reverse Proxy (Nginx) with HTTPS

The `nginx.conf` provided handles:
- HTTPS termination (with Let's Encrypt certs)
- Reverse proxy to backend (http://backend:8000)
- Static frontend serving
- Security headers
- Gzip compression
- Rate limiting at reverse proxy level

## Monitoring & Logging

- **Structured Logging**: All logs emitted as JSON for easy parsing/aggregation
- **Log Levels**: DEBUG (development), INFO (standard), WARNING, ERROR (issues), CRITICAL (failures)
- **Sensitive Data**: Phone numbers masked in logs
- **Metrics**: Response times, error rates, database query times tracked
- **Health Checks**: `/api/v1/health` returns database and service status

## Contributing

1. Create a feature branch: `git checkout -b feature/description`
2. Make changes and commit: `git commit -am 'Description'`
3. Run tests locally: `pytest` (backend), `npm test` (frontend)
4. Push and create a Pull Request
5. GitHub Actions will run CI checks

## License

MIT License - see LICENSE file

## Support

For issues, questions, or contributions, please open a GitHub issue or contact the maintainers.

## Appendix: Verified Provider Prefixes

All prefixes in the seed data are from authoritative sources or clearly reputable references. See `backend/app/scripts/seed_data.py` for sources and `Unverified Prefixes` section below if any prefix could not be confidently verified.

### Unverified Prefixes

None explicitly marked as unverified in this build. All prefixes used are from NCC allocations or verified operator documentation. If adding new prefixes, verify against NCC or operator official sources first.
