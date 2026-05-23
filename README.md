========================================================================
                       PREPNOVA PLATFORM - README
========================================================================

PrepNova is a premium placement preparation portal built with Django.
It features modules for Aptitude tests, Coding challenges with an online
compiler, sequential Mock Test rounds, and an interactive Resume Builder.

------------------------------------------------------------------------
1. System Requirements & Dependencies
------------------------------------------------------------------------
* Python 3.10 or higher
* PostgreSQL (recommended for production) or SQLite (for local testing)
* Major browsers (Chrome, Firefox, Safari, Edge)

All python dependencies are listed in `requirements.txt`:
* Django>=6.0.5
* whitenoise>=6.6.0
* gunicorn>=21.2.0
* psycopg2-binary>=2.9.9

------------------------------------------------------------------------
2. Local Development Setup
------------------------------------------------------------------------
Follow these steps to run the application locally:

a) Clone the project repository and navigate to the project directory.

b) Create a virtual environment:
   python -m venv venv

c) Activate the virtual environment:
   - On Windows (Command Prompt):
     venv\Scripts\activate.bat
   - On Windows (PowerShell):
     venv\Scripts\Activate.ps1
   - On macOS/Linux:
     source venv/bin/activate

d) Install the required dependencies:
   pip install -r requirements.txt

e) Run database migrations:
   python manage.py migrate

f) Collect static files (generates WhiteNoise manifest):
   python manage.py collectstatic --noinput

g) Create a superuser account (admin access):
   python manage.py createsuperuser

h) Run the development server:
   python manage.py runserver

i) Open your browser and navigate to: http://127.0.0.1:8000/

------------------------------------------------------------------------
3. Running the Test Suite
------------------------------------------------------------------------
The codebase includes 16 automated tests covering authentication flow,
public pages, test completions, resume generation, and mock test locks.

Before running tests, ensure static files are collected to satisfy WhiteNoise
manifest requirements:
   python manage.py collectstatic --noinput
   python manage.py test

------------------------------------------------------------------------
4. Environment Variables Configuration
------------------------------------------------------------------------
For production deployment, create a `.env` file in the project root
and configure the following environment variables:

  SECRET_KEY=your-highly-secure-random-secret-key
  DEBUG=False
  ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
  DATABASE_URL=postgres://user:password@host:port/database_name

Ensure `SECRET_KEY` is kept private and never committed to version control.

------------------------------------------------------------------------
5. Production Deployment Best Practices
------------------------------------------------------------------------
* Database: Switch from SQLite to PostgreSQL by configuring DATABASE_URL.
* Security:
  - Set DEBUG=False.
  - Set ALLOWED_HOSTS to your server domain names.
  - Set SECURE_SSL_REDIRECT=True in settings.py to enforce HTTPS.
  - Enable SESSION_COOKIE_SECURE=True and CSRF_COOKIE_SECURE=True.
* Static Files: WhiteNoise is pre-configured to compress and cache static files.
  Always run `python manage.py collectstatic --noinput` as part of your
  deployment build process.
* Server WSGI: Use Gunicorn to serve the WSGI application:
  gunicorn protal.wsgi:application --bind 0.0.0.0:8000

------------------------------------------------------------------------
6. License & Author Info
------------------------------------------------------------------------
Created by Koushik Prabhu for placement success. All rights reserved.
========================================================================
