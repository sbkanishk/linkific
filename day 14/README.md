# 🚀 Day 14: Django Fundamentals & E-commerce Store Setup

This project is a foundational Django application translating our previous FastAPI e-commerce database into Django's powerful ORM and MVT architecture.

## 🛠️ Quickstart Guide

**1. Set up the Sandbox**
Create and activate your isolated virtual environment:
- `python -m venv venv`
- `venv\Scripts\activate` *(Windows)*

**2. Install Dependencies**
Install the Django framework:
- `pip install django`

**3. Initialize the Project & App**
Create the core control center and the specific store module:
- `django-admin startproject core .`
- `python manage.py startapp store`

**4. Wire it Together**
Add the new app to the project by opening `core/settings.py` and adding `"store",` to the bottom of the `INSTALLED_APPS` list.

**5. Build the Database (Django ORM)**
Translate the Python models into SQL tables:
- `python manage.py makemigrations`
- `python manage.py migrate`

**6. Create the Admin Master Key**
Set up credentials to access the built-in dashboard:
- `python manage.py createsuperuser`

**7. Launch the Server**
Fire up the application:
- `python manage.py runserver`

## 🌟 Key Accomplishments
- Successfully transitioned an E-commerce schema (Categories, Products, Carts, Orders, Reviews) from SQLAlchemy to Django ORM.
- Registered all models to the built-in Django Admin dashboard.
- Implemented the **MVT** (Model-View-Template) pattern to render dynamic database data to an HTML webpage.