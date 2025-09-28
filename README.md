# AI-Powered Quiz App - Backend

## Overview
This is the Django REST Framework-based backend for an AI-powered quiz application, integrated with a PostgreSQL database (Neon.tech) and Google Gemini API for question generation. It provides RESTful APIs for user authentication, quiz creation, and result tracking.

## How to Run the Project Locally

1. **Set Up Environment**:
   - Navigate to the `backend/` directory.
   - Create a virtual environment: `python -m venv venv` (Windows: `venv\Scripts\activate`).
   - Activate it: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows).

2. **Install Dependencies**:
   - Install required packages: `pip install -r requirements.txt`.

3. **Configure Environment Variables**:
   - Create a `.env` file in `backend/` with:
DATABASE_URL=postgresql://neondb_owner:[ENCODED_PASSWORD]@ep-bold-resonance-adez0ouu-pooler.c-2.us-east-1.aws.neon.tech/test?sslmode=require
GEMINI_API_KEY=your-gemini-api-key
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
text- Replace `[ENCODED_PASSWORD]` with the URL-encoded Neon database password (use `urllib.parse.quote` for special chars).

4. **Apply Migrations**:
- Run: `python manage.py migrate` to set up the database schema.

5. **Create Superuser**:
- Run: `python manage.py createsuperuser` to create an admin account.

6. **Run the Server**:
- Start the development server: `python manage.py runserver`.
- Access at `http://localhost:8000/admin/` or test APIs (see API structure below).

## Database Design Decisions
- **Models**:
- `User`: Extends Django's default user model for authentication (username, email, password).
- `Quiz`: Stores quiz metadata (topic, num_questions, difficulty, created_at, user).
- `Question`: Contains quiz questions (text, options A-D, correct_option) linked to a Quiz.
- `Result`: Tracks user quiz attempts (score, answers, quiz, user, timestamp).
- **Rationale**: Normalized structure for scalability; foreign keys ensure data integrity. Neon.tech chosen for free tier reliability over Supabase (DNS issues).
- **Indexes**: Added on `Quiz.user` and `Result.user` for efficient user-specific queries.

## API Structure
- **Base URL**: `http://localhost:8000` (or Render URL in production).
- **Endpoints**:
- `POST /api/register/`: Register a new user (requires username, password, email).
- `POST /api/login/`: Authenticate user (returns JWT tokens).
- `GET /api/quizzes/`: List user's quizzes (requires JWT).
- `POST /api/quizzes/create/`: Create a quiz (requires topic, num_questions, difficulty, JWT).
- `GET /api/quizzes/{id}/`: Fetch quiz details and questions (requires JWT).
- `POST /api/quizzes/{id}/submit/`: Submit quiz answers (requires answers dict, JWT).
- `GET /api/results/`: Fetch user’s quiz results (requires JWT).
- **Authentication**: JWT-based using `rest_framework_simplejwt`.
- **CORS**: Configured with `corsheaders` to allow frontend origins (e.g., `localhost:3000`, Vercel URL).

## Challenges Faced and How They Were Solved
- **Database Connection Issues**: Initial Supabase DNS errors (`No such host`) resolved by switching to Neon.tech, which provided stable connectivity.
- **Gunicorn Deployment Failure**: "command not found" on Render fixed by adding `gunicorn` to `requirements.txt`.
- **ALLOWED_HOSTS Error**: DisallowedHost on Render solved by adding `quizbackend-xxmv.onrender.com` to `ALLOWED_HOSTS` in `settings.py`.
- **Neon Password Authentication**: Incorrect password issue resolved by copying the exact URI from Neon dashboard.

## Features Implemented vs. Skipped
- **Implemented**:
- User authentication (register/login) with JWT.
- Quiz creation with AI-generated questions via Gemini API.
- Quiz taking and result tracking.
- Admin panel for manual oversight.
- Reason: Core MVP functionality to validate the concept.
- **Skipped**:
- Real-time quiz collaboration (requires WebSockets, skipped for simplicity).
- Advanced analytics (e.g., user progress trends, skipped for MVP scope).
- Email notifications (requires SMTP setup, deferred for future).
- Reason: Focused on minimal viable product; scalability features planned for later iterations.

## Deployment
- **Platform**: Render.com (free tier).
- **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`.
- **Start Command**: `gunicorn quizbackend.wsgi:application`.
- **Env Vars**: `DATABASE_URL`, `GEMINI_API_KEY`, `DJANGO_SECRET_KEY`, `DEBUG=False`.
- **Runtime**: `python-3.10.12` (recommended for compatibility).

**Repo Structure**:
- `quizbackend/`: Django project folder.
- `quizzes/`: Main app with models, views, and serializers.
- `manage.py`: Django management script.
- `README.md`: This file.