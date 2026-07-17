# Interview Prep

A Django-based web application for practicing interview questions, tracking sessions, and reviewing results.

## Features
- User registration and login
- Practice interview questions by section
- Track interview sessions and answers
- View results and feedback

## Project Structure
- accounts/: user authentication and account-related views
- feedback/: feedback handling
- practice/: practice session logic
- questions/: question models and sample data
- templates/: HTML templates for the app
- interview_prep/: Django project settings and URLs   

## Requirements
- Python 3.10+
- Django
- SQLite (default database)

## Setup
1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
   On Windows:
   ```bash
   venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```
4. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Usage
- Open http://127.0.0.1:8000/ in your browser
- Register a new account or log in
- Start practicing interview questions

## Notes
- This project uses Django's built-in admin for managing content
- Sample questions are included through migrations
  
