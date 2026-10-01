# BharatResolve AI — Production Deployment Guide

**Target Platforms:** Render (Backend) + Vercel (Frontend Next.js)  
**Database:** Managed PostgreSQL (Render / Supabase) or persistent SQLite volume

---

## 1. Prerequisites & Environment Variables

### Backend Configuration (`render.yaml` / `.env`)
```bash
PYTHON_VERSION=3.10.12
PYTHONPATH=./backend
ENV=production
SECRET_KEY=your_production_secret_key_here
ALLOWED_ORIGINS=https://bharatresolve.vercel.app

# LLM Providers (Pick at least one primary)
GEMINI_API_KEY=AIzaSy...
GROQ_API_KEY=gsk_...

# Database Configuration
DATABASE_URL=postgresql://user:password@ep-cool-db.postgres.render.com/bharatresolve
```

### Frontend Configuration (`vercel.json` / `.env.production`)
```bash
NEXT_PUBLIC_API_URL=https://bharatresolve-backend.onrender.com
```

---

## 2. Render Deployment (Backend Service)

1. Connect repository to Render dashboard.
2. Select **Blueprint** deployment using `render.yaml` or create a Web Service manually:
   - **Environment:** Python 3
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. Add Environment Variables in Render Web Console (`GEMINI_API_KEY`, `ALLOWED_ORIGINS`, `DATABASE_URL`).
4. Trigger Manual Deploy or Git push to `main` branch.

---

## 3. Vercel Deployment (Frontend Next.js App)

1. Import repository into Vercel Dashboard.
2. Set Framework Preset to **Next.js**.
3. Set **Root Directory** to `frontend`.
4. Add Environment Variable: `NEXT_PUBLIC_API_URL` pointing to backend Render URL.
5. Click **Deploy**.

---

## 4. Local Production Dry-Run Instructions

To verify production build locally before triggering remote deployments:

### Backend Dry-Run:
```powershell
$env:PYTHONPATH = 'd:\Bharat_Agent\backend'
& 'D:\Computer_Vision\venv\Scripts\python.exe' -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Frontend Production Build Dry-Run:
```powershell
cd d:\Bharat_Agent\frontend
npm run build
npm run start
```
