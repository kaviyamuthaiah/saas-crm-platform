# 🚀 SaaS Platform – Multi-Tenant Django Application

A production-ready multi-tenant SaaS platform built with Django, PostgreSQL, and Bootstrap 5.
Features Projects/Tasks management, CRM (Leads & Contacts), role-based access, and per-tenant workspace isolation.

---

## 📁 Project Structure

```
saas_platform/
├── apps/
│   ├── accounts/          # Custom User model, auth views (login, register, profile)
│   ├── dashboard/         # Aggregated stats dashboard
│   ├── projects/          # Projects + Tasks CRUD
│   ├── crm/               # Leads + Contacts CRUD
│   └── tenants/           # Tenant model, middleware, settings, team management
├── saas_platform/         # Django project config (settings, urls, wsgi)
├── static/
│   ├── css/main.css       # Complete design system
│   └── js/main.js         # Sidebar toggle, alerts, tooltips
├── templates/
│   ├── base.html          # Sidebar + topbar shell
│   ├── auth_base.html     # Split-panel auth layout
│   ├── accounts/          # Login, register, profile
│   ├── dashboard/         # Dashboard with stat cards + charts
│   ├── projects/          # Project & Task CRUD templates
│   ├── crm/               # Lead & Contact CRUD templates
│   ├── tenants/           # Settings, members, invite
│   └── partials/          # Reusable fragments (pagination)
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── Procfile
```

---

## ⚙️ Local Setup (Step-by-Step)

### 1. Prerequisites
- Python 3.10+
- PostgreSQL 14+ running locally (or use Docker)
- `pip` and optionally `virtualenv`

### 2. Clone & create virtual environment
```bash
git clone <your-repo-url>
cd saas_platform

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
```
Edit `.env`:
```
DEBUG=True
SECRET_KEY=your-very-secret-key-here
DB_NAME=saas_platform
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Create the PostgreSQL database
```bash
psql -U postgres -c "CREATE DATABASE saas_platform;"
```

### 6. Run migrations
```bash
python manage.py migrate
```

### 7. Create a superuser (optional, for Django admin)
```bash
python manage.py createsuperuser
```
> Note: The superuser created this way won't have a tenant. Use the `/accounts/register/` page to create a full workspace account.

### 8. Collect static files (development)
```bash
python manage.py collectstatic --noinput
```

### 9. Start the development server
```bash
python manage.py runserver
```

Visit → **http://127.0.0.1:8000**

---

## 🐳 Docker Compose (Quickest Start)

```bash
cp .env.example .env
docker-compose up --build
```
Visits → http://localhost:8000

---

## 🧩 Multi-Tenancy Architecture

This project uses **row-based multi-tenancy**:

- Every data model (`Project`, `Task`, `Lead`, `Contact`) has a `tenant` FK.
- `TenantMiddleware` reads `request.user.tenant` and attaches it to every request as `request.tenant`.
- `TenantQuerysetMixin` automatically filters `.get_queryset()` to `tenant=request.tenant`.
- `TenantFormMixin` stamps `tenant` on new objects before saving.
- No data from Tenant A is ever accessible to Tenant B.

### Creating a new workspace
Navigate to `/accounts/register/` — this creates a **new Tenant** and assigns the registering user as its **Admin**.

### Inviting team members
As a tenant Admin, go to **Settings → Team → Invite Member**.

---

## 🔐 Role-Based Access

| Role  | Capabilities |
|-------|-------------|
| Admin | Full CRUD on all data + Settings + Team management |
| User  | Full CRUD on Projects, Tasks, CRM (no Settings access) |

---

## 🚢 Deployment

### Heroku / Railway / Render
```bash
# Set environment variables on your platform:
SECRET_KEY=<strong-random-key>
DEBUG=False
DATABASE_URL=postgres://...
ALLOWED_HOSTS=yourapp.herokuapp.com

# Deploy
git push heroku main
heroku run python manage.py migrate
```

### VPS (Ubuntu + Nginx + Gunicorn)
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations and collect static
python manage.py migrate
python manage.py collectstatic --noinput

# Start with Gunicorn
gunicorn saas_platform.wsgi --bind 127.0.0.1:8000 --workers 3 --daemon

# Configure Nginx to proxy_pass to 127.0.0.1:8000
# and serve /static/ from staticfiles/
```

Sample Nginx block:
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /path/to/saas_platform/staticfiles/;
    }

    location /media/ {
        alias /path/to/saas_platform/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🛠 Tech Stack

| Layer      | Technology              |
|------------|-------------------------|
| Backend    | Django 4.2              |
| Database   | PostgreSQL + psycopg2   |
| Frontend   | Bootstrap 5 + Chart.js  |
| Forms      | django-crispy-forms     |
| Static     | WhiteNoise              |
| Production | Gunicorn                |
