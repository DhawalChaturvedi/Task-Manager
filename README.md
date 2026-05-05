# Project Manager

A web-based project management app with role-based access control, task tracking, and a dashboard. Built with Django 5 + HTMX + Bootstrap 5.

## Tech Stack

- **Backend:** Django 5.x
- **Frontend:** Django Templates + HTMX + Bootstrap 5
- **Database:** MySQL
- **Auth:** Django built-in session auth
- **Extras:** django-crispy-forms, crispy-bootstrap5, whitenoise

## Features

- **Auth** — signup, login, logout
- **Projects** — create, edit, delete projects; invite and remove members
- **Role-based access** — project-level Admin and Member roles
  - Admins can edit/delete projects, manage members, edit/delete any task
  - Members can view projects, create tasks, and update task status
- **Tasks** — title, description, priority, due date, assignee, status tracking
- **HTMX interactions** — inline task creation and status updates without full page reloads
- **Dashboard** — task counts by status and overdue task list across all your projects

## Project Structure

```
personal-project/
├── venv/                        # Virtual environment
├── requirements.txt
└── config/                      # Django project root
    ├── manage.py
    ├── config/                  # Django settings package
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── apps/
    │   ├── accounts/            # Custom user model, auth views
    │   ├── projects/            # Project & member management
    │   └── tasks/               # Task CRUD and status tracking
    └── templates/
        ├── base.html
        ├── accounts/
        ├── projects/
        ├── tasks/
        └── dashboard/
```

## Setup

### Prerequisites

- Python 3.11+
- MySQL running locally
- `mysql-client` headers (required to build `mysqlclient`)

```bash
brew install mysql-client pkg-config
```

### Installation

```bash
# Clone / download the project, then:
cd personal-project

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Database

```bash
mysql -u root -e "CREATE DATABASE project_manager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

Update `USER` and `PASSWORD` in `config/config/settings.py` to match your MySQL credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'project_manager',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

### Migrations

```bash
cd config
python manage.py migrate
```

### Run

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/auth/signup/` to create your first account.

## URL Reference

| URL | Description |
|---|---|
| `/auth/signup/` | Create an account |
| `/auth/login/` | Log in |
| `/auth/logout/` | Log out |
| `/dashboard/` | Status counts + overdue tasks |
| `/projects/` | List your projects |
| `/projects/create/` | Create a project |
| `/projects/<pk>/` | Project detail + tasks + members |

## Role Permissions

| Action | Admin | Member |
|---|---|---|
| View project + tasks | ✅ | ✅ |
| Create tasks | ✅ | ✅ |
| Update task status | ✅ | ✅ |
| Edit / delete any task | ✅ | ❌ |
| Manage members | ✅ | ❌ |
| Edit / delete project | ✅ | ❌ |
