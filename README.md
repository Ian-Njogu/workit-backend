# JobBoard Backend

A Django REST Framework backend for the JobBoard application, providing REST endpoints that mirror the existing MSW mocks.

## Features

- **Authentication**: JWT-based authentication with SimpleJWT
- **Role-based Access Control**: Separate permissions for clients and workers
- **Job Management**: Create, view, and manage jobs with status transitions
- **Worker Profiles**: Browse and filter worker profiles
- **Applications**: Apply to jobs, accept/reject applications
- **CORS Support**: Configured for frontend integration
- **Database**: PostgreSQL with SQLite fallback for development

## Project Structure

```
jobboard-backend/
├── apps/
│   ├── users/          # User management and authentication
│   ├── workers/        # Worker profiles and browsing
│   ├── jobs/          # Job creation and management
│   └── applications/  # Job applications and management
├── jobboard_backend/  # Django project settings
├── manage.py
├── requirements.txt
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.8+
- pip
- PostgreSQL (optional, SQLite fallback available)

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd jobboard-backend
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/api/`

## Environment Configuration

Copy `env.example` to `.env` and configure:

```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL)
DB_NAME=jobboard_db
DB_USER=jobboard_user
DB_PASSWORD=your-db-password
DB_HOST=127.0.0.1
DB_PORT=5432

# Force SQLite for development
USE_SQLITE=True

# CORS for frontend
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

## API Endpoints

### Authentication

- **POST** `/api/auth/login` - Login and get JWT tokens
- **POST** `/api/auth/refresh` - Refresh access token

### Workers

- **GET** `/api/workers/` - List workers (with filtering)
- **GET** `/api/workers/{id}/` - Get worker details

**Query Parameters:**
- `category` - Filter by category
- `location` - Filter by location
- `available` - Filter by availability
- `min_hourly_rate` - Minimum hourly rate
- `max_hourly_rate` - Maximum hourly rate
- `min_rating` - Minimum rating
- `page` - Page number for pagination
- `page_size` - Items per page

### Jobs

- **GET** `/api/jobs/` - List jobs (filtered by client_id or worker_id)
- **POST** `/api/jobs/` - Create new job
- **GET** `/api/jobs/{id}/` - Get job details
- **PATCH** `/api/jobs/{id}/` - Update job (status transitions)
- **GET** `/api/jobs/feed/` - Get job feed for workers
- **POST** `/api/jobs/{id}/applications/` - Apply to a job

**Job Status Transitions:**
- `pending` → `accepted` → `in_progress` → `completed`
- `pending` → `cancelled` (at any time)

### Applications

- **GET** `/api/applications/` - List applications (filtered by client_id or job_id)
- **GET** `/api/applications/{id}/` - Get application details
- **POST** `/api/applications/{id}/accept/` - Accept application
- **POST** `/api/applications/{id}/reject/` - Reject application

## API Examples

### Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "client@example.com", "password": "password123"}'
```

Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "email": "client@example.com",
    "name": "John Client",
    "role": "client"
  }
}
```

### Create Job

```bash
curl -X POST http://localhost:8000/api/jobs/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Website Development",
    "category": "Web Development",
    "description": "Need a modern website built",
    "location": "Remote",
    "budget": "5000.00",
    "deadline": "2024-02-01"
  }'
```

### Get Workers

```bash
curl -X GET "http://localhost:8000/api/workers/?category=Web%20Development&location=Remote" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Apply to Job

```bash
curl -X POST http://localhost:8000/api/jobs/1/applications/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I can help with your website development project",
    "quote": "4500.00"
  }'
```

### Accept Application

```bash
curl -X POST http://localhost:8000/api/applications/1/accept/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Database Models

### User
- `id`, `email`, `name`, `role` (client/worker), `password`, `created_at`

### WorkerProfile
- `user` (FK), `category`, `location`, `hourly_rate`, `rating`, `review_count`, `skills`, `portfolio`, `available`

### Job
- `id`, `client` (FK), `worker` (FK, nullable), `title`, `category`, `description`, `location`, `budget`, `deadline`, `status`, `created_at`

### Application
- `id`, `job` (FK), `worker` (FK), `message`, `quote`, `status`, `created_at`

## Permissions

- **Clients**: Create jobs, view their jobs, manage applications to their jobs
- **Workers**: View job feed, apply to jobs, view assigned jobs, update job status
- **Object-level**: Users can only modify their own resources

## Development

### Running Tests

```bash
python manage.py test
```

### Creating Sample Data

```bash
python manage.py shell
```

```python
from apps.users.models import User
from apps.workers.models import WorkerProfile
from apps.jobs.models import Job

# Create sample users
client = User.objects.create_user(
    email='client@example.com',
    password='password123',
    name='John Client',
    role='client'
)

worker = User.objects.create_user(
    email='worker@example.com',
    password='password123',
    name='Jane Worker',
    role='worker'
)

# Create worker profile
profile = WorkerProfile.objects.create(
    user=worker,
    category='Web Development',
    location='Remote',
    hourly_rate=50.00
)

# Create sample job
job = Job.objects.create(
    client=client,
    title='Website Development',
    category='Web Development',
    description='Need a modern website built',
    location='Remote',
    budget=5000.00
)
```

## Production Deployment

1. **Set production environment variables:**
   ```bash
   DEBUG=False
   SECRET_KEY=your-production-secret-key
   USE_SQLITE=False
   # Configure PostgreSQL connection
   ```

2. **Collect static files:**
   ```bash
   python manage.py collectstatic
   ```

3. **Use a production WSGI server like Gunicorn:**
   ```bash
   pip install gunicorn
   gunicorn jobboard_backend.wsgi:application
   ```

## Frontend Integration

The backend is designed to work with the existing frontend. To integrate:

1. **Set frontend environment variables:**
   ```bash
   VITE_API_URL=http://localhost:8000
   VITE_USE_REAL_API=true
   ```

2. **Configure axios interceptors for JWT authentication**

3. **Gradually migrate pages from MSW to real API**

## Troubleshooting

### Common Issues

1. **Database connection errors**: Check your database settings in `.env`
2. **CORS errors**: Verify `CORS_ALLOWED_ORIGINS` includes your frontend URL
3. **JWT errors**: Check token expiration and refresh logic
4. **Permission errors**: Verify user roles and object ownership

### Logs

Check Django logs for detailed error information:
```bash
python manage.py runserver --verbosity=2
```

## Contributing

1. Follow the existing code style
2. Add tests for new functionality
3. Update documentation for API changes
4. Ensure all migrations are backward compatible

## License

This project is part of the JobBoard application.
