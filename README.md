# TalentHub - Web-Based Recruitment Management System

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Django](https://img.shields.io/badge/Django-6.0-green)
![Database](https://img.shields.io/badge/Database-SQLite-lightgrey)

## About

TalentHub is a full-stack recruitment management system built for Neotech Company to streamline the hiring process. It provides a dedicated portal for job seekers to discover and apply for roles, and a separate employer dashboard for posting jobs, reviewing applications, and managing candidates  -all in one place.

---

## Features

**For Applicants**
- Register, build a profile, and upload a CV
- Browse and apply for open job listings
- Track application status in real time
- Save jobs for later and manage skills

**For Employers**
- Post and manage job listings
- Review applications and update candidate status
- Search and filter candidates by skills and location
- View application reports and analytics

**For Admins**
- Full system oversight via Django admin panel
- User and content management

---

## Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Backend    | Python 3.8+ / Django 6.0          |
| Frontend   | HTML5, CSS3, Bootstrap 5          |
| Database   | SQLite (development) / MySQL (production) |
| Icons      | Font Awesome 6                    |

---

## Getting Started

### Prerequisites

- Python 3.8+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/wangoimwangi/job_seeker.git
   cd job_seeker
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv env
   env\Scripts\activate        # Windows
   source env/bin/activate     # macOS / Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser** (optional, for admin access)
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Visit the app**
   ```
   http://127.0.0.1:8000/
   ```

---

## Project Structure

```
job_seeker/
├── job_seeker/          # Core app — models, views, forms, URLs
├── jobs/                # Project settings and root URL configuration
├── templates/           # HTML templates (applicant, staff, shared)
├── static/              # CSS, JavaScript, images
├── media/               # User-uploaded files (CVs, cover letters)
├── requirements.txt
└── manage.py
```

---

## License

This project was developed for academic purposes and is not intended for commercial use.
