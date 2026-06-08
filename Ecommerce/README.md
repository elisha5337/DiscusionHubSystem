# Ecommerce — Render Deployment Guide

This document explains how to deploy this Django project to Render.

## Prerequisites

- A Render account.
- (Recommended) A PostgreSQL database on Render or another provider.
- (Optional) An S3 bucket for media if your app accepts uploads.

## Important environment variables

- `SECRET_KEY` — your Django secret key (required in production).
- `DATABASE_URL` — database URL (e.g., provided by Render Postgres or local Postgres).
- `DATABASE_SSL_REQUIRE` — optional, `True` when using SSL connections to Postgres.
- `DEBUG` — set to `False` in production.
- `ALLOWED_HOSTS` — comma-separated hosts.
- `CORS_ORIGIN_ALLOW_ALL` — optional, `True`/`False`.
- `USE_S3` — set to `True` to enable S3 media storage.
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_STORAGE_BUCKET_NAME`, `AWS_S3_REGION_NAME` — required when `USE_S3=True`.

## Build & Start commands (Render)

- **Build command:**

```
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
```

- **Start command:**

```
gunicorn Ecommerce.wsgi:application --workers 3 --bind 0.0.0.0:$PORT
```

## Deploy steps

1. Push your repo to GitHub (or connect Render to your repo).
2. In Render, create a new **Web Service**; point it to this repository and branch.
3. Use the build and start commands above.
4. In the Render Dashboard, set environment variables listed above.
5. If you use Postgres, create a Render Postgres instance and paste the `DATABASE_URL` into Render service env vars.
6. If you use S3 for media, set `USE_S3=True` and the AWS env vars.

## Local testing tips

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
set SECRET_KEY=unsafe-local-dev-key
set DEBUG=True
python manage.py migrate
python manage.py runserver
```

## Notes & Recommendations

- Do not commit secrets to the repo. Use Render environment variables for secrets.
- For media/uploads use S3 or Render Persistent Volumes; the local `media/` folder is ephemeral on Render.
- Monitor logs in the Render dashboard for runtime errors.

If you want, I can:

- Add S3-backed static files (instead of WhiteNoise),
- Enforce stricter production checks (e.g., disallow DEBUG on production), or
- Create a Git branch and commit these changes for you.

---

## Render Deployment Checklist (detailed)

Follow these steps to deploy this project to Render with PostgreSQL and optional S3 media storage.

1. Connect your Git repository to Render and create a new **Web Service**.

2. In the Render service settings, set these environment variables (required in production):
   - `SECRET_KEY` — a strong secret (required when `DEBUG=False`).
   - `DATABASE_URL` — Postgres connection string (example: `postgres://user:pass@host:5432/dbname`).
   - `DEBUG` — set to `False` in production.
   - `ALLOWED_HOSTS` — comma-separated hosts your app will serve (example: `example.com,api.example.com`).
   - `CORS_ORIGIN_ALLOW_ALL` — optional `True`/`False`.

   Optional for S3 media:
   - `USE_S3=True`
   - `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_STORAGE_BUCKET_NAME`, `AWS_S3_REGION_NAME`

3. If using Render Postgres, create a Render Postgres instance and paste the provided `DATABASE_URL` into the Web Service env var.

4. The `render.yaml` already contains build and start commands. The build step runs:

   ```bash
   pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
   ```

   Make sure `requirements.txt` contains `gunicorn`, `dj-database-url`, `whitenoise`, and `psycopg2-binary` (it does).

5. The start command uses Gunicorn:

   ```bash
   gunicorn Ecommerce.wsgi:application --workers 3 --bind 0.0.0.0:$PORT
   ```

6. Media files: Render's filesystem is ephemeral. Use S3 for uploads or Render Persistent Volumes. If you use S3, set `USE_S3=True` and AWS env vars above.

7. Health checks (optional): configure Render health check path to `/` or a small view that returns 200 OK.

8. After deployment, check Render logs for migration and `collectstatic` output. If `collectstatic` fails due to missing static assets, run `python manage.py collectstatic` locally to debug.

## Quick local test with environment variables (PowerShell)

```powershell
$env:SECRET_KEY="unsafe-local-dev-key"
$env:DEBUG="True"
$env:DATABASE_URL="sqlite:///db.sqlite3"
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

If you'd like, I can also add a small healthcheck endpoint or create a `Dockerfile` for Render.
