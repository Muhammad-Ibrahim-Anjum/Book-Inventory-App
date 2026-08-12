# Book Inventory App

A Django-based book inventory application for managing authors, books, and borrowing records.

## Project setup

### 1. Create a virtual environment

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Apply database migrations

```bash
python manage.py migrate
```

### 4. Run the development server

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

## Optional admin setup

Create a superuser if you want to access the admin panel:

```bash
python manage.py createsuperuser
```

## Project dependencies

The current requirements file includes:

- Django
- django-crispy-forms
- crispy-bootstrap5
