# AI-Powered Quiz App

## Overview
A fullstack quiz app with AI-generated questions using Next.js (frontend), Django REST (backend), PostgreSQL (DB via Supabase), and Google Gemini (free AI).

**Core Features**:
- User auth (register/login).
- Create quizzes: Topic, 5-20 questions, difficulty (AI generates MCQs).
- Take quizzes with progress.
- View results/review answers.
- Quiz history/retakes.

**Tech Decisions**:
- **DB Models**: User → Quiz (topic, etc.) → Question (text, options, correct) → Result (score, answers).
- **API**: RESTful endpoints (e.g., /api/quizzes/create/) with JWT auth.
- **AI**: Google Gemini (gemini-1.5-flash) for free generation—prompt for JSON MCQs.
- **Auth**: Django built-in + simplejwt.
- **Error Handling**: Try-except for AI/network; validate inputs.

**Challenges & Solutions**:
- AI Output: Prompt engineered for strict JSON; stripped markdown.
- Deployment: Supabase password encoding for DATABASE_URL (used urllib.parse.quote).
- CORS: Added frontend URLs to django-cors-headers.
- Free Tier Limits: Render sleeps (wakes on request); Gemini rate limits (handled in views).
- Skipped: Advanced features (e.g., real-time) for MVP focus.

**Trade-offs**:
- Gemini over OpenAI: Free, but rate-limited.
- Supabase: Easy free Postgres, but password encoding needed for special chars.
- JWT: Stateless, scalable.

## Local Setup
1. **Backend** (`cd backend`):
   - `python -m venv venv && source venv/bin/activate` (Windows: `venv\Scripts\activate`).
   - `pip install -r requirements.txt`.
   - Set `.env`: `GEMINI_API_KEY=your-key`, `DATABASE_URL=postgresql://postgres:[encoded-password]@db.[ref].supabase.co:5432/postgres`.
   - `python manage.py migrate`.
   - `python manage.py createsuperuser`.
   - `python manage.py runserver`.

2. **Frontend** (`cd frontend`):
   - `npm install`.
   - Set `.env.local`: `NEXT_PUBLIC_API_BASE=http://localhost:8000`.
   - `npm run dev`.

3. Test: http://localhost:3000/login → Create/take quizzes.

## Deployment
- **Backend**: Render.com (free tier) at https://your-backend.onrender.com.
  - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`.
  - Start Command: `gunicorn quiz_backend.wsgi:application`.
  - Env Vars: `DATABASE_URL` (encoded Supabase URI), `GEMINI_API_KEY`, `DJANGO_SECRET_KEY`, `DEBUG=False`.
  - Procfile: `web: gunicorn quiz_backend.wsgi --log-file -`.
  - runtime.txt: `python-3.10.12`.

- **Frontend**: Vercel (free) at https://your-frontend.vercel.app.
  - Env: `NEXT_PUBLIC_API_BASE=https://your-backend.onrender.com`.

- **DB**: Supabase (free) – Connection via encoded DATABASE_URL.

## How to Scale/Improve
- Add caching (Redis) for AI calls.
- Rate limiting on API.
- Switch to paid AI for unlimited.
- Tests: Add Django tests/pytest.

Repo Structure:
- backend/: Django project.
- frontend/: Next.js app.
- README.md: This file.