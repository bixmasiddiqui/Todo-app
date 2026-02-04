# Quickstart Guide: Full-Stack Todo Web Application

**Feature**: 001-fullstack-todo-web
**Version**: 1.0.0
**Last Updated**: 2026-01-04

## Overview

This guide will help you set up and run the Full-Stack Todo Web Application in under 10 minutes.

**What you'll build:**
- Next.js frontend (React with TypeScript)
- FastAPI backend (Python async API)
- Neon Postgres database (serverless)
- Complete CRUD operations for todo tasks

---

## Prerequisites

Before starting, ensure you have these installed:

| Tool | Version | Check Command | Install Link |
|------|---------|---------------|--------------|
| **Node.js** | 18.x or higher | `node --version` | [nodejs.org](https://nodejs.org/) |
| **npm** | 9.x or higher | `npm --version` | Comes with Node.js |
| **Python** | 3.11 or higher | `python --version` | [python.org](https://www.python.org/) |
| **uv** | Latest | `uv --version` | `pip install uv` |
| **Git** | Any recent | `git --version` | [git-scm.com](https://git-scm.com/) |

**Optional but recommended:**
- **VS Code** with Python and TypeScript extensions
- **Postman** or **curl** for API testing
- **PostgreSQL client** (e.g., pgAdmin, DBeaver) for database inspection

---

## Step 1: Clone and Setup Repository

```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Checkout the feature branch
git checkout 001-fullstack-todo-web

# Verify you're on the correct branch
git branch --show-current
# Should output: 001-fullstack-todo-web
```

---

## Step 2: Set Up Neon Postgres Database

### 2.1 Create Neon Account and Database

1. Go to [neon.tech](https://neon.tech/) and sign up (free tier available)
2. Create a new project (e.g., "todo-app")
3. Create a new database (e.g., "todos_db")
4. Copy the connection string from the Neon dashboard

**Connection string format:**
```
postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/database?sslmode=require
```

### 2.2 Test Database Connection (Optional)

```bash
# Using psql (if installed)
psql "postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/database?sslmode=require"

# Or using Python
python -c "import psycopg2; conn = psycopg2.connect('YOUR_CONNECTION_STRING'); print('Connected successfully!')"
```

---

## Step 3: Set Up Backend (FastAPI)

### 3.1 Navigate to Backend Directory

```bash
cd backend
```

### 3.2 Create Environment File

Create a `.env` file in the `backend/` directory:

```bash
# backend/.env
DATABASE_URL=postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/database?sslmode=require
CORS_ORIGINS=http://localhost:3000
ENVIRONMENT=development
```

**Important:** Never commit `.env` files to version control!

### 3.3 Install Dependencies

```bash
# Using uv (recommended - faster)
uv pip install -r requirements.txt

# OR using pip
pip install -r requirements.txt
```

**Expected dependencies** (from `requirements.txt`):
```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlmodel==0.0.14
psycopg2-binary==2.9.9
python-dotenv==1.0.0
pydantic[email]==2.5.3
alembic==1.13.1
```

### 3.4 Run Database Migrations

```bash
# Generate initial migration (if not exists)
alembic revision --autogenerate -m "create tasks table"

# Apply migrations
alembic upgrade head

# Verify migration status
alembic current
```

**Expected output:**
```
INFO  [alembic.runtime.migration] Running upgrade  -> 001, create tasks table
```

### 3.5 Start Backend Server

```bash
# Development mode with auto-reload
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# OR using the run script (if provided)
python -m src.main
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process using StatReload
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 3.6 Verify Backend is Running

Open your browser or use curl:

```bash
# Test API root
curl http://localhost:8000/

# Check API docs (Swagger UI)
# Open in browser: http://localhost:8000/docs

# Test health endpoint (if implemented)
curl http://localhost:8000/health

# List tasks (should return empty array initially)
curl http://localhost:8000/api/todos
# Expected: []
```

---

## Step 4: Set Up Frontend (Next.js)

### 4.1 Open New Terminal

Keep the backend server running. Open a new terminal window/tab.

### 4.2 Navigate to Frontend Directory

```bash
cd frontend
```

### 4.3 Create Environment File

Create a `.env.local` file in the `frontend/` directory:

```bash
# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 4.4 Install Dependencies

```bash
npm install
```

**Expected dependencies** (from `package.json`):
```json
{
  "dependencies": {
    "next": "^14.1.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/node": "^20.11.5",
    "@types/react": "^18.2.48",
    "@types/react-dom": "^18.2.18",
    "autoprefixer": "^10.4.17",
    "postcss": "^8.4.33",
    "tailwindcss": "^3.4.1",
    "typescript": "^5.3.3"
  }
}
```

### 4.5 Start Frontend Development Server

```bash
npm run dev
```

**Expected output:**
```
  ▲ Next.js 14.1.0
  - Local:        http://localhost:3000
  - Network:      http://192.168.x.x:3000

 ✓ Ready in 2.5s
```

### 4.6 Open Application in Browser

Navigate to [http://localhost:3000](http://localhost:3000)

**Expected UI:**
- Clean, modern interface
- Input field for adding tasks
- Empty state message (since no tasks exist yet)

---

## Step 5: Verify Everything Works

### 5.1 Test Task Creation

1. In the browser (http://localhost:3000), enter a task description (e.g., "Buy groceries")
2. Press Enter or click the Add button
3. Verify the task appears in the list immediately

### 5.2 Test Task Completion

1. Click the checkbox next to a task
2. Verify the task shows completed status (strikethrough text)
3. Uncheck the checkbox
4. Verify the task returns to incomplete status

### 5.3 Test Task Editing

1. Click the edit button (or double-click the task)
2. Modify the task description
3. Save changes
4. Verify the updated description persists

### 5.4 Test Task Deletion

1. Click the delete button next to a task
2. Confirm deletion (if confirmation dialog appears)
3. Verify the task is removed from the list

### 5.5 Test Persistence

1. Create several tasks with different completion states
2. Refresh the browser page (Ctrl+R or Cmd+R)
3. Verify all tasks remain with correct states

---

## Step 6: Development Workflow

### Running Both Servers Concurrently

**Option 1: Separate Terminals**
- Terminal 1: `cd backend && uvicorn src.main:app --reload`
- Terminal 2: `cd frontend && npm run dev`

**Option 2: Using Process Managers** (optional)
- Install `concurrently`: `npm install -g concurrently`
- Create root-level script in `package.json`:
  ```json
  {
    "scripts": {
      "dev": "concurrently \"cd backend && uvicorn src.main:app --reload\" \"cd frontend && npm run dev\""
    }
  }
  ```
- Run: `npm run dev` from project root

---

## Common Issues and Solutions

### Issue: Backend Won't Start - Database Connection Error

**Symptoms:**
```
psycopg2.OperationalError: could not connect to server
```

**Solutions:**
1. Verify `DATABASE_URL` in `backend/.env` is correct
2. Check if Neon database is active (not suspended)
3. Verify network connectivity
4. Test connection string using `psql` or Python script

---

### Issue: Frontend Can't Reach Backend API

**Symptoms:**
```
Failed to fetch
Network Error
CORS Error
```

**Solutions:**
1. Verify backend is running on http://localhost:8000
2. Check `NEXT_PUBLIC_API_URL` in `frontend/.env.local`
3. Verify CORS configuration in backend (should allow http://localhost:3000)
4. Check browser console for detailed error messages

---

### Issue: Migrations Fail

**Symptoms:**
```
Target database is not up to date
Migration failed
```

**Solutions:**
1. Check if database exists and is accessible
2. Verify Alembic configuration in `alembic.ini`
3. Run `alembic current` to check migration status
4. If stuck, rollback and retry: `alembic downgrade -1` then `alembic upgrade head`

---

### Issue: TypeScript Errors in Frontend

**Symptoms:**
```
Type 'X' is not assignable to type 'Y'
Cannot find module
```

**Solutions:**
1. Ensure dependencies are installed: `npm install`
2. Check TypeScript version: `npx tsc --version`
3. Restart TypeScript server in VS Code: Cmd+Shift+P → "TypeScript: Restart TS Server"
4. Verify type definitions in `frontend/src/types/task.ts`

---

## Project Structure Reference

After setup, your project should look like this:

```
project-root/
├── backend/
│   ├── src/
│   │   ├── models/
│   │   │   └── task.py
│   │   ├── routers/
│   │   │   └── todos.py
│   │   ├── services/
│   │   │   └── task_service.py
│   │   ├── database.py
│   │   └── main.py
│   ├── tests/
│   ├── alembic/
│   ├── alembic.ini
│   ├── requirements.txt
│   ├── .env (gitignored)
│   └── pyproject.toml
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   └── globals.css
│   │   ├── components/
│   │   │   ├── TaskInput.tsx
│   │   │   ├── TaskList.tsx
│   │   │   └── TaskItem.tsx
│   │   ├── lib/
│   │   │   └── api.ts
│   │   └── types/
│   │       └── task.ts
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── .env.local (gitignored)
│   └── next.config.js
│
├── specs/
│   └── 001-fullstack-todo-web/
│       ├── spec.md
│       ├── plan.md
│       ├── research.md
│       ├── data-model.md
│       ├── quickstart.md (this file)
│       └── contracts/
│           └── openapi.yaml
│
├── .gitignore
└── README.md
```

---

## API Endpoints Quick Reference

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| GET | `/api/todos` | List all tasks | None |
| POST | `/api/todos` | Create new task | `{description: string}` |
| GET | `/api/todos/{id}` | Get single task | None |
| PATCH | `/api/todos/{id}` | Update task | `{description?: string, is_completed?: boolean}` |
| DELETE | `/api/todos/{id}` | Delete task | None |

**Full API documentation:** http://localhost:8000/docs

---

## Testing the API with Curl

```bash
# Create a task
curl -X POST http://localhost:8000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"description": "Buy groceries"}'

# List all tasks
curl http://localhost:8000/api/todos

# Get single task (replace {id} with actual UUID)
curl http://localhost:8000/api/todos/{id}

# Update task description
curl -X PATCH http://localhost:8000/api/todos/{id} \
  -H "Content-Type: application/json" \
  -d '{"description": "Buy groceries and prepare dinner"}'

# Mark task complete
curl -X PATCH http://localhost:8000/api/todos/{id} \
  -H "Content-Type: application/json" \
  -d '{"is_completed": true}'

# Delete task
curl -X DELETE http://localhost:8000/api/todos/{id}
```

---

## Running Tests

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_models.py

# Run tests in verbose mode
pytest -v

# View coverage report
# Open htmlcov/index.html in browser
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm test -- --coverage
```

---

## Environment Variables Reference

### Backend (.env)

| Variable | Required | Example | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | `postgresql://...` | Neon Postgres connection string |
| `CORS_ORIGINS` | Yes | `http://localhost:3000` | Allowed CORS origins (comma-separated) |
| `ENVIRONMENT` | No | `development` | Environment name (development/production) |

### Frontend (.env.local)

| Variable | Required | Example | Description |
|----------|----------|---------|-------------|
| `NEXT_PUBLIC_API_URL` | Yes | `http://localhost:8000` | Backend API base URL |

---

## Next Steps

After verifying everything works:

1. **Explore the Code**: Review `backend/src/` and `frontend/src/` to understand the implementation
2. **Review Documentation**: Read `plan.md`, `research.md`, and `data-model.md` in `specs/001-fullstack-todo-web/`
3. **Run Tests**: Execute backend and frontend test suites
4. **Customize UI**: Modify Tailwind classes in frontend components to personalize the design
5. **Add Features**: Implement optional enhancements (filtering, sorting, etc.)

---

## Production Deployment Checklist

Before deploying to production:

- [ ] Update `CORS_ORIGINS` to include production frontend URL
- [ ] Set `ENVIRONMENT=production` in backend
- [ ] Use production Neon database (not development database)
- [ ] Enable HTTPS for both frontend and backend
- [ ] Set up proper error logging and monitoring
- [ ] Configure rate limiting on API endpoints
- [ ] Run database backups regularly
- [ ] Review and update security headers
- [ ] Test with production database connection
- [ ] Set up CI/CD pipeline

---

## Support and Resources

**Documentation:**
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Next.js Docs](https://nextjs.org/docs)
- [SQLModel Docs](https://sqlmodel.tiangolo.com/)
- [Neon Docs](https://neon.tech/docs/introduction)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)

**API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI Spec: `specs/001-fullstack-todo-web/contracts/openapi.yaml`

**Issue Reporting:**
- Check `CLAUDE.md` for development guidelines
- Review existing issues in project tracker
- Include error messages, logs, and steps to reproduce

---

**Version**: 1.0.0 | **Last Updated**: 2026-01-04
**Estimated Setup Time**: 10 minutes
