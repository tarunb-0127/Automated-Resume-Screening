# Automated Resume Screening System

Automated Resume Screening System is a web-based application designed to simplify and accelerate the initial phase of recruitment. The platform enables recruiters to evaluate multiple resumes against a job description in a single action using AI-powered analysis. Each resume is scored based on its relevance to the job description, candidates are ranked accordingly, and automated email notifications are sent with selection status and feedback.

---

## Overview

This application automates resume shortlisting by leveraging a large language model for intelligent matching rather than traditional rule-based or machine learning pipelines. Candidates upload their resumes for a specific job posting, and recruiters initiate the screening process with one click. The system generates a match percentage for each resume and ranks candidates based on suitability.

---

## Core Functionality

- Recruiter job description posting
- Candidate resume upload
- Bulk resume screening with a single action
- AI-based resume and job description matching
- Percentage-based match score generation
- Candidate ranking based on relevance
- Automated email notifications
- Resume improvement feedback for non-shortlisted candidates

---

## Technology Stack

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Django (Python)

### AI Integration
- Gemini 2.0 Flash
- Prompt-driven resume evaluation and feedback generation

### Communication
- Django Email Backend using SMTP

---

## System Workflow

1. The recruiter creates and publishes a job description.
2. Candidates review the job description and upload their resumes.
3. The recruiter triggers the screening process.
4. The backend sends the job description and resume data to the Gemini 2.0 Flash model.
5. The model evaluates relevance and returns a match percentage.
6. Candidates are ranked in descending order of match score.
7. Email notifications are automatically sent:
   - Shortlisted candidates receive a selection notification.
   - Non-shortlisted candidates receive a rejection notification with resume improvement suggestions.

---

## Installation and Setup

Clone the repository:

```bash
git clone https://github.com/tarunb-0127/Automated-Resume-Screening.git
cd Automated-Resume-Screening/scrrening_project
````

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install required dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file in the project root and configure the following variables:

```
DJANGO_SECRET_KEY=your_secret_key
DEBUG=True

EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_password
EMAIL_USE_TLS=True

GEMINI_API_KEY=your_gemini_api_key
```

---

## Running the Application

Apply database migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

Open the application in a browser:

```
http://127.0.0.1:8000/
```

---

## Email Notification Process

* Selected candidates receive an email confirming their shortlisting and next steps.
* Candidates who are not shortlisted receive a rejection email containing AI-generated feedback on how to improve their resume for similar roles.

---

## Project Structure (High-Level)

```
scrrening_project/
├── manage.py
├── screening_app/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/
│   ├── static/
│   └── services/
│       └── gemini_screening.py
├── requirements.txt
└── README.md
```

---

## Potential Enhancements

* User authentication and role management
* Support for multiple concurrent job postings
* Screening analytics and reporting dashboard
* Advanced resume parsing and visualization
* Production deployment configuration

