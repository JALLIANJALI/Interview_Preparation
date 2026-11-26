# Interview Prep

A Django-based web application for practicing interview questions, tracking sessions, and reviewing results.

## Features
- User registration and login
- Practice interview questions by section
- Track interview sessions and answers
- View results and feedback

## Project Structure
```text

interview_prep/
├── accounts/           # User authentication and account management
├── feedback/           # Feedback handling and related logic
├── practice/           # Interview practice sessions and user progress
├── questions/          # Question models, views, and sample data
├── templates/          # HTML templates for the user interface
├── interview_prep/     # Django project settings and URL configuration
├── manage.py           # Django management entry point
├── db.sqlite3          # Local SQLite database
└── README.md           # Project documentation
```

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
  
