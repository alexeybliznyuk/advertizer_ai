# Content Generation Service

A FastAPI-based service for managing content generation, templates, and usage tracking.

## Features

- **Content Block Management**: Create and manage content blocks with tags and audience targeting
- **Template Management**: Create and manage content generation templates
- **Usage Tracking**: Track content generation usage and statistics
- **Generation Context**: Manage generation contexts and parameters
- **Generated Content**: Store and retrieve generated content with status tracking

## Architecture

```
sender-service/
├── alembic/                 # Database migrations
├── controller/              # FastAPI controllers and endpoints
├── models/                  # SQLAlchemy database models
├── repository/              # Database access layer
├── schemas/                 # Pydantic request/response schemas
├── service/                 # Business logic layer
├── settings/                # Configuration and environment
├── main.py                  # Application entry point
├── Dockerfile               # Container configuration
└── pyproject.toml          # Python dependencies
```

## Database Models

### Core Models
- **ContentBlock**: Content blocks with titles, descriptions, and tags
- **Template**: Content generation templates with parameters
- **GenerationConstant**: Constants for content generation
- **GenerationContext**: Context for content generation
- **Generated**: Generated content with status tracking
- **Usage**: Usage tracking and statistics

### Enums
- **ActionType**: Types of actions (CREATE, UPDATE, DELETE)
- **GeneratedType**: Types of generated content
- **GenerationStatus**: Status of content generation

## API Endpoints

### Health Check
- `GET /health` - Service health status

### Content Blocks
- `POST /content-blocks` - Create a new content block
- `GET /content-blocks` - Get all content blocks

### Templates
- `POST /templates` - Create a new template
- `GET /templates` - Get all templates

## Development

### Prerequisites
- Python 3.11+
- PostgreSQL
- Docker (optional)

### Local Development
1. Install dependencies:
   ```bash
   pip install -e .
   ```

2. Set up environment variables:
   ```bash
   cp settings/sender-service.env.example settings/sender-service.env
   # Edit the .env file with your database credentials
   ```

3. Run database migrations:
   ```bash
   alembic upgrade head
   ```

4. Start the service:
   ```bash
   python main.py
   ```

### Docker Development
1. Build and start services:
   ```bash
   docker-compose -f ../../docker-compose.dev.yml up sender-db sender-service
   ```

2. Run migrations:
   ```bash
   docker exec -it sender-service alembic upgrade head
   ```

## Environment Variables

Required environment variables in `settings/sender-service.env`:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/sender_db

# Service
SERVICE_NAME=sender-service
SERVICE_VERSION=1.0.0
```

## Database Migrations

The service uses Alembic for database migrations:

```bash
# Generate a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migrations
alembic downgrade -1
```

## Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=.
```

## Deployment

The service can be deployed using Docker:

```bash
# Build image
docker build -t sender-service .

# Run container
docker run -p 8000:8000 sender-service
```

## Monitoring

- Health check endpoint: `GET /health`
- Service logs are available via Docker logs
- Database connection status is monitored automatically 