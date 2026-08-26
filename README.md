# Soundora

Soundora is a Django REST Framework backend for a music platform. It provides user authentication (email and SMS verification), music catalog management, artist panels, playlists, likes, and automatic metadata extraction from uploaded audio files.

---


- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Environment Variables](#environment-variables)
- [Getting Started](#getting-started)
  - [Option A: Docker (Recommended)](#option-a-docker-recommended)
  - [Option B: Local Python Setup](#option-b-local-python-setup)
- [Database Migrations](#database-migrations)
- [API Documentation](#api-documentation)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Data Models](#data-models)
- [Background Tasks (Celery)](#background-tasks-celery)
- [Management Commands](#management-commands)
- [Development Tools](#development-tools)
- [Production Deployment](#production-deployment)
- [Contributing](#contributing)

---

## Features

- **User management** — Custom user model with email login, Iranian phone number validation, and profile management
- **Dual verification** — Email activation (Djoser) or SMS verification via Kavenegar
- **JWT authentication** — Access/refresh tokens with rotation and blacklisting (Simple JWT)
- **Music catalog** — Browse, filter, search, and paginate music tracks
- **Automatic metadata extraction** — Title, album, cover art, and artist auto-filled from MP3, FLAC, OGG, and M4A files using Mutagen
- **Artist panel** — Verified artists can upload and manage their own music
- **Playlists** — Users create public or private playlists with multiple tracks
- **Likes** — Toggle like/unlike on music tracks
- **Platform analytics** — Middleware tracks visitor OS statistics (Windows, Mac, iPhone, Android, Other)
- **API documentation** — Interactive Swagger UI and ReDoc
- **Containerized deployment** — Docker Compose for development and production with Nginx, Gunicorn, PostgreSQL, Redis, and Celery

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.13 |
| Framework | Django 5.2 |
| API | Django REST Framework 3.16 |
| Authentication | Simple JWT, Djoser |
| Database | PostgreSQL 16 |
| Cache / Broker | Redis |
| Task Queue | Celery |
| Metadata | Mutagen |
| SMS | Kavenegar API (Can be changed) |
| API Docs | drf-yasg (Swagger / ReDoc) |
| Production Server | Gunicorn + Nginx |
| Containerization | Docker, Docker Compose |

---

## Project Structure

```
Soundora/
├── app/                        # Core music application
│   ├── api/v1/                 # REST API (views, serializers, filters, permissions)
│   ├── migrations/
│   ├── templates/admin/        # Custom admin os stats report templates
│   ├── admin.py
│   ├── middleware.py           # OS statistics tracking middleware
│   ├── models.py               # Music, Album, Category, PlayList, Like, Stats
│   └── utils.py                # Audio metadata extraction (Mutagen)
├── core/                       # Django project configuration
│   ├── settings/
│   │   ├── base.py             # Shared settings
│   │   ├── dev.py              # Development settings
│   │   └── prod.py             # Production settings
│   ├── celery.py
│   ├── urls.py                 # Root URL routing + Swagger/ReDoc
│   └── wsgi.py
├── users/                      # User & artist management
│   ├── api/v1/                 # Auth & profile API
│   ├── api/sms.py              # SMS API
│   ├── management/commands/    # Custom management commands
│   ├── models.py               # User, Artist
│   └── signals.py              # Auto-set is_artist on Artist creation
├── media/                      # Uploaded music files and cover images
├── docker-compose-dev.yml      # Development stack
├── docker-compose-prod.yml     # Production stack
├── default.conf                # Nginx configuration
├── Dockerfile
├── manage.py
├── requirements.txt
└── pytest.ini
```

---

## Prerequisites

- **Docker & Docker Compose** (recommended), or:
- Python 3.13+
- PostgreSQL 16
- Redis

---

## Environment Variables

Create a `.env` file in the project root. The file is gitignored and must be created manually.

```env
SECRET_KEY=django-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost
API_BASE_URL=http://127.0.0.1:81


POSTGRES_DB_DEV=soundora
POSTGRES_USER_DEV=alidb
POSTGRES_PASSWORD_DEV=ali72387238
POSTGRES_HOST_DEV=postgres_db
POSTGRES_PORT_DEV=5432



POSTGRES_DB=soundora
POSTGRES_USER=alidb
POSTGRES_PASSWORD=ali72387238
POSTGRES_HOST=postgres_db
POSTGRES_PORT=5432

REDIS_HOST=redis
REDIS_PORT=6379
```

For SMS verification, set your Kavenegar API key in `users/api/sms.py`:

```python
api = KavenegarAPI("YOUR_API_KEY")
```
It can also be changed to any other SMS API provider.
---

## Getting Started

### Option A: Docker (Recommended)

#### Development

```bash
docker compose -f docker-compose-dev.yml up --build
```

This starts:

| Service | Port | Description |
|---------|------|-------------|
| Django backend | 8000 | Development server |
| PostgreSQL | 5432 | Database |
| Redis | 6379 | Cache & Celery broker |
| Celery worker | — | Background task processor |
| smtp4dev | 5001 (UI), 25 (SMTP) | Local email testing |
| pgAdmin | 8080 | Database GUI |

Apply migrations inside the backend container:

```bash
docker exec -it django python manage.py migrate
docker exec -it django python manage.py createsuperuser
```

#### Production

```bash
docker compose -f docker-compose-prod.yml up --build -d
```

Production stack adds:

| Service | Port | Description |
|---------|------|-------------|
| Nginx | 81 | Reverse proxy — `http://127.0.0.1:81/` |
| Gunicorn | 8000 (internal) | WSGI application server |
| pgAdmin | 8081 | Database GUI |

---

### Option B: Local Python Setup

```bash
# 1. Clone and enter the project
git clone <repository-url>
cd Soundora

# 2. Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env (see Environment Variables section)
# Ensure PostgreSQL and Redis are running locally

# 5. Run migrations
python manage.py migrate

# 6. Create a superuser
python manage.py createsuperuser

# 7. Start the development server
python manage.py runserver

# 8. (Optional) Start Celery worker in a separate terminal
celery -A core worker --loglevel=info
```

Default settings module for local development: `core.settings.dev` (set in `manage.py`).

---

## Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## API Documentation

Once the server is running, interactive API docs are available at:

| URL | Description |
|-----|-------------|
| `http://localhost:8000/swagger/` | Swagger UI |
| `http://localhost:8000/redoc/` | ReDoc |
| `http://localhost:8000/swagger/output.json` | OpenAPI schema (JSON) |



---

## API Endpoints

All API endpoints are prefixed with `/user/api/v1/` (users) or `/core/api/v1/` (music). Unless marked otherwise, endpoints require a JWT access token in the `Authorization` header.

### Users & Authentication (`/user/api/v1/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/user/api/v1/test/` | Test endpoint |
| `POST` | `/user/api/v1/register/` | Register a new user |
| `POST` | `/user/api/v1/token/login/` | Log in and obtain JWT tokens |
| `POST` | `/user/api/v1/token/refresh-v1` | Refresh access token (Simple JWT) |
| `POST` | `/user/api/v1/token/refresh-v2` | Refresh access token (custom view) |
| `GET` | `/user/api/v1/me/` | Get current user profile |
| `POST` | `/user/api/v1/sms-verification/` | Verify account via SMS code |
| `POST` | `/user/api/v1/resend-sms-verification/` | Resend SMS verification code |
| `POST` | `/user/api/v1/reset_password/` | Request password reset |
| `POST` | `/user/api/v1/reset_password_confirm/` | Confirm password reset |
| `POST` | `/user/api/v1/email-verification/` | Activate account via email link |
| `POST` | `/user/api/v1/resend-email-verification/` | Resend activation email |

### Music (`/core/api/v1/`) — Authenticated users

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/core/api/v1/music/` | List music tracks (filter, search, order, paginate) |
| `GET` | `/core/api/v1/music/{id}/` | Retrieve a single track with details |

### Artist Panel (`/core/api/v1/artist/`) — Verified artists only

Full CRUD on the artist's own music:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/core/api/v1/artist/` | List the artist's own tracks |
| `POST` | `/core/api/v1/artist/` | Upload a new track (auto metadata extraction) |
| `GET` | `/core/api/v1/artist/{id}/` | Retrieve one of the artist's tracks |
| `PUT` | `/core/api/v1/artist/{id}/` | Update a track |
| `PATCH` | `/core/api/v1/artist/{id}/` | Partially update a track |
| `DELETE` | `/core/api/v1/artist/{id}/` | Delete a track |

### Playlists (`/core/api/v1/playlists/`) — Authenticated users

Public playlists are visible to everyone; owners have full control over their own playlists:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/core/api/v1/playlists/` | List public + own playlists |
| `POST` | `/core/api/v1/playlists/` | Create a playlist |
| `GET` | `/core/api/v1/playlists/{id}/` | Retrieve a playlist |
| `PUT` | `/core/api/v1/playlists/{id}/` | Update an owned playlist |
| `PATCH` | `/core/api/v1/playlists/{id}/` | Partially update an owned playlist |
| `DELETE` | `/core/api/v1/playlists/{id}/` | Delete an owned playlist |

### Likes (`/core/api/v1/`) — Authenticated users

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/core/api/v1/toggle-like/{music_id}` | Toggle like/unlike on a track |

### Other URLs

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/admin/` | Django admin panel |
| `GET` | `/api-auth/` | DRF browsable API login/logout |
| `GET` | `/media/...` | Uploaded media files (music, cover images) |

---

## Authentication

Soundora uses **JWT Bearer tokens** for API authentication.

| Token | Lifetime | Notes |
|-------|----------|-------|
| Access token | 15 minutes | Sent in `Authorization` header |
| Refresh token | 10 days | Used to obtain new access tokens |

Features:

- Refresh token rotation enabled
- Old refresh tokens blacklisted after rotation
- Users must be both `is_active` and `is_verified` to log in
- Artists must be verified (`is_verified=True`) to access the artist panel

---

## Data Models

### User (`users.User`)

Custom user with email as the login field. Key fields: `username`, `email`, `phone_number` (Iran format `09XXXXXXXXX`), `avatar`, `is_artist`, `is_verified`, `notifications`.

### Artist (`users.Artist`)

One-to-one with User. Fields: `category`, `played_time`, `website`, `location` (country), `rating` (0–5), `is_suspended`. Creating an Artist automatically sets `user.is_artist = True`.

### Music (`app.Music`)

Core track model. Supports automatic metadata extraction on upload for title, album, cover image, and artist. Fields: `title`, `category` (M2M), `artist` (M2M), `album` (FK), `cover_image`, `lyrics`, `file`, `is_published`.

### PlayList (`app.PlayList`)

User-owned playlists with `title`, `description`, `is_public`, and a M2M relation to `Music`.

### Like (`app.Like`)

Unique `(user, music)` pairs. Use the toggle-like endpoint to like or unlike.

### Stats (`app.Stats`)

Single-row OS visit counter tracked by middleware: `win`, `mac`, `iphone`, `android`, `other`.

---

## Background Tasks (Celery)

Celery is configured with Redis as both broker and result backend.

```bash
# Start a worker
celery -A core worker --loglevel=info
```

Configuration (from `core/settings/base.py`):

- Broker: `redis://{REDIS_HOST}:{REDIS_PORT}/0`
- Result backend: `redis://{REDIS_HOST}:{REDIS_PORT}/1`
- Timezone: `Asia/Tehran`

---

## Management Commands

### Seed fake data

```bash
python manage.py insert_data
```

Creates 5 users/artists and 10 music tracks using Faker (development only).

---

## Development Tools

### Code formatting (Black)

```bash
black .
```

### Linting (Flake8)

```bash
flake8 .
```


## Production Deployment

1. Set all required environment variables in `.env`
2. Set `DJANGO_SETTINGS_MODULE=core.settings.prod` (configured automatically in `docker-compose-prod.yml`)
3. Build and start the production stack:

```bash
docker compose -f docker-compose-prod.yml up --build -d
```

4. Run migrations:

```bash
docker exec -it django python manage.py migrate
docker exec -it django python manage.py collectstatic --noinput
```

Production architecture:

```
Client → Nginx (host :81 → HTTP) → Gunicorn (backend:8000) → PostgreSQL
                              ↓
                         Celery Worker → Redis
```

Nginx serves `/static/` and `/media/` directly. All other requests are proxied to Gunicorn. Maximum upload size is 100 MB.
---

## License

This project is under MIT License.