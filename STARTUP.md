\ Todo App - Startup Guide

This guide will help you set up and run the Full-Stack Todo Web Application.

## Prerequisites

- **Python 3.11+** - Backend runtime
- **Node.js 18+** - Frontend runtime
- **PostgreSQL** (Neon or local) - Database
- **Git** - Version control

## Project Structure

```
hack02/
├── backend/          # FastAPI backend
│   ├── src/          # Source code
│   ├── tests/        # Tests
│   ├── alembic/      # Database migrations
│   └── requirements.txt
├── frontend/         # Next.js frontend
│   ├── src/
│   │   ├── app/      # App Router pages
│   │   ├── components/  # React components
│   │   ├── lib/      # API client
│   │   └── types/    # TypeScript types
│   └── package.json
└── README.md
```

## Setup Instructions

### 1. Database Setup

#### Option A: Using Neon (Recommended)

1. Create a free account at https://neon.tech
2. Create a new project
3. Copy the connection string (format: `postgresql://username:password@host/database`)

#### Option B: Local PostgreSQL

1. Install PostgreSQL locally
2. Create a database: `createdb todo_db`
3. Connection string: `postgresql://localhost:5432/todo_db`

### 2. Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a Python virtual environment:
   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment:
   - **Windows**: `.venv\Scripts\activate`
   - **macOS/Linux**: `source .venv/bin/activate`

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create `.env` file in the `backend/` directory:
   ```env
   DATABASE_URL=postgresql://username:password@host:5432/database
   CORS_ORIGINS=http://localhost:3000
   ENVIRONMENT=development
   ```

6. Run database migrations:
   ```bash
   alembic upgrade head
   ```

7. Start the backend server:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

   The backend will be available at: http://localhost:8000
   API documentation at: http://localhost:8000/docs

### 3. Frontend Setup

1. Open a **new terminal** and navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create `.env.local` file in the `frontend/` directory:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

   The frontend will be available at: http://localhost:3000

## Running the Application

### First Time Setup

1. **Start Backend** (Terminal 1):
   ```bash
   cd backend
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # macOS/Linux
   uvicorn src.main:app --reload --port 8000
   ```

2. **Start Frontend** (Terminal 2):
   ```bash
   cd frontend
   npm run dev
   ```

3. **Open Browser**:
   - Navigate to http://localhost:3000
   - You should see the Todo App with an input field

### Daily Development

You need to run both servers simultaneously:

**Terminal 1 - Backend:**
```bash
cd backend
.venv\Scripts\activate  # Windows
uvicorn src.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Features Implemented (Phase 3 - US1)

✅ **Quick Task Addition**
- Add new tasks with a simple input field
- View all tasks in a clean list
- Mark tasks as complete/incomplete
- Delete tasks
- Real-time UI updates

## Testing the Application

### Manual Testing

1. Open http://localhost:3000
2. Type a task in the input field (e.g., "Buy groceries")
3. Click "Add Task"
4. The task should appear in the list below
5. Click the checkbox to mark it complete
6. Click "Delete" to remove the task

### Backend API Testing

Visit http://localhost:8000/docs to access the interactive API documentation (Swagger UI).

Available endpoints:
- `POST /api/todos` - Create a task
- `GET /api/todos` - Get all tasks
- `GET /api/todos/{id}` - Get a specific task
- `PATCH /api/todos/{id}` - Update a task
- `DELETE /api/todos/{id}` - Delete a task

### Running Automated Tests

**Backend Tests:**
```bash
cd backend
pytest
```

**Frontend Tests:**
```bash
cd frontend
npm run test
```

## Troubleshooting

### Backend Issues

**"ModuleNotFoundError" or import errors:**
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

**"Could not connect to database":**
- Verify DATABASE_URL in `.env` is correct
- Check database server is running
- Test connection: `psql <your-database-url>`

**"Port 8000 already in use":**
- Kill the process: `taskkill /F /IM python.exe` (Windows) or `pkill -f uvicorn` (macOS/Linux)
- Or use a different port: `uvicorn src.main:app --reload --port 8001`

### Frontend Issues

**"Module not found" errors:**
- Delete `node_modules/` and `.next/`
- Reinstall: `npm install`

**API connection errors:**
- Verify backend is running on port 8000
- Check `.env.local` has correct `NEXT_PUBLIC_API_URL`
- Verify CORS is configured (should be automatic)

**"Port 3000 already in use":**
- The dev server will prompt you to use port 3001
- Or kill the process and restart

## Next Steps

After Phase 3 (US1) is complete, you can proceed with:

- **Phase 4 (US2)**: Task Completion Toggle - already implemented! ✅
- **Phase 5 (US3)**: Task Deletion - already implemented! ✅
- **Phase 6 (US4)**: Task List Display with Sorting
- **Phase 7 (US5)**: Task Editing
- **Phase 8 (US6)**: Task Filtering

## Development Commands Reference

### Backend
```bash
# Activate virtual environment
.venv\Scripts\activate              # Windows
source .venv/bin/activate           # macOS/Linux

# Run server
uvicorn src.main:app --reload --port 8000

# Run tests
pytest

# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Frontend
```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Run production server
npm start

# Run tests
npm run test

# Run linter
npm run lint
```

## Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Ensure both backend and frontend servers are running
4. Check browser console for errors (F12 → Console tab)
5. Check backend logs in the terminal

## Architecture Overview

### Backend (FastAPI)
- **Framework**: FastAPI with async support
- **ORM**: SQLModel (combines SQLAlchemy + Pydantic)
- **Database**: PostgreSQL (Neon or local)
- **Migrations**: Alembic
- **Testing**: pytest with TestClient

### Frontend (Next.js)
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Testing**: Vitest + React Testing Library
- **State Management**: React hooks (useState, useEffect)

### API Communication
- RESTful JSON API
- CORS enabled for local development
- Error handling with proper HTTP status codes
- Request/response validation with Pydantic
