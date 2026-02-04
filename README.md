# Full-Stack Todo Web Application - Phase II

A modern, production-ready todo management application built with Next.js, FastAPI, and PostgreSQL.

## Overview

This is a **full-stack web application** with a clean, responsive UI, RESTful API, and persistent database storage. Built following Test-Driven Development (TDD) and Spec-Driven Development methodologies.

### Features (Phase II - COMPLETE ✨)

**Core Functionality:**
- ✅ Add new tasks with real-time validation (empty check, 500 char limit)
- ✅ View all tasks in a beautiful, modern interface
- ✅ Mark tasks as complete/incomplete with visual feedback
- ✅ **Edit tasks inline** (double-click or click edit button)
- ✅ Delete tasks with double-click confirmation
- ✅ Persistent storage with PostgreSQL
- ✅ RESTful API with automatic documentation

**UI/UX Features:**
- ✅ Modern, gradient-based design with dark mode support
- ✅ Smooth animations and transitions
- ✅ Character count indicator (turns orange near limit)
- ✅ Progress bar showing completion status
- ✅ Responsive design (mobile-first, 320px to 1920px+)
- ✅ Loading states and optimistic UI updates
- ✅ Toast notifications for errors
- ✅ Empty state with helpful guidance
- ✅ Keyboard shortcuts (Enter to submit, Escape to cancel edit)

**Developer Features:**
- ✅ Comprehensive test suite (38 backend tests, frontend tests)
- ✅ Input validation at all layers (frontend, backend, database)
- ✅ Error handling with rollback on failure
- ✅ Type safety throughout (TypeScript + Python type hints)
- ✅ Production-ready deployment configuration
- ✅ Security: No exposed API keys, CORS configured, parameterized queries

### Tech Stack

**Frontend:**
- Next.js 14 (App Router)
- React 18
- TypeScript
- Tailwind CSS
- Vitest (testing)

**Backend:**
- FastAPI (Python 3.11+)
- SQLModel (ORM)
- PostgreSQL (Neon)
- Alembic (migrations)
- pytest (testing)

**Deployment:**
- Railway (Backend + PostgreSQL)
- Vercel (Frontend)
- Docker containerization

## Quick Start

### Prerequisites

- **Python 3.11+** - Backend runtime
- **Node.js 18+** - Frontend runtime
- **PostgreSQL** - Database (Neon recommended)
- **Git** - Version control

### Local Development Setup

See **[STARTUP.md](./STARTUP.md)** for detailed local development instructions.

**Quick version:**

1. **Backend Setup:**
   ```bash
   cd backend
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   # Create .env with DATABASE_URL
   alembic upgrade head
   uvicorn src.main:app --reload --port 8000
   ```

2. **Frontend Setup:**
   ```bash
   cd frontend
   npm install
   # Create .env.local with NEXT_PUBLIC_API_URL
   npm run dev
   ```

3. **Access:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/docs

### Production Deployment

See **[DEPLOYMENT.md](./DEPLOYMENT.md)** for complete deployment guide.

**Quick deploy:**
- **Backend**: Railway (includes PostgreSQL database)
- **Frontend**: Vercel
- **Cost**: $0/month on free tiers

Push to GitHub and connect to Railway + Vercel for automatic deployments!

## Project Structure

```
.
├── backend/                 # FastAPI Backend
│   ├── src/
│   │   ├── main.py          # FastAPI application
│   │   ├── config.py        # Settings & environment
│   │   ├── database.py      # Database connection
│   │   ├── models.py        # SQLModel models
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── services/        # Business logic
│   │   └── routers/         # API endpoints
│   ├── tests/               # Backend tests
│   ├── alembic/             # Database migrations
│   ├── Dockerfile           # Docker configuration
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Environment template
│
├── frontend/                # Next.js Frontend
│   ├── src/
│   │   ├── app/             # App Router pages
│   │   │   ├── layout.tsx   # Root layout
│   │   │   ├── page.tsx     # Home page
│   │   │   ├── error.tsx    # Error boundary
│   │   │   └── loading.tsx  # Loading state
│   │   ├── components/      # React components
│   │   │   ├── TaskInput.tsx
│   │   │   └── TaskList.tsx
│   │   ├── lib/             # API client
│   │   │   └── api.ts
│   │   └── types/           # TypeScript types
│   │       └── task.ts
│   ├── package.json         # Dependencies
│   ├── tailwind.config.ts   # Tailwind configuration
│   └── .env.example         # Environment template
│
├── specs/                   # Design documentation
│   └── 002-fullstack-todo-app/
│       ├── spec.md          # Feature specification
│       ├── plan.md          # Architecture plan
│       ├── tasks.md         # Task breakdown
│       ├── data-model.md    # Database schema
│       └── contracts/
│           └── openapi.yaml # API specification
│
├── STARTUP.md               # Local development guide
├── DEPLOYMENT.md            # Production deployment guide
└── README.md                # This file
```

## Development Workflow

This project follows **Spec-Driven Development** with strict TDD:

1. **Specify** (`/sp.specify`): Define user stories and requirements
2. **Plan** (`/sp.plan`): Design architecture and technical approach
3. **Tasks** (`/sp.tasks`): Generate implementation task list
4. **Implement** (`/sp.implement`): Execute tasks with TDD workflow
   - **RED**: Write test, ensure it fails
   - **GREEN**: Implement minimum code to pass
   - **REFACTOR**: Improve code quality
5. **Commit & PR**: Version control with meaningful commits

### Constitution Principles

All development follows the [Todo Management System Constitution](./. specify/memory/constitution.md):

- **Phase-Aware Architecture**: Simple now, extensible for future phases
- **Test-First Development** (NON-NEGOTIABLE): TDD for all code
- **Independent User Stories**: Incremental delivery (P1→P2→P3→P4)
- **Modular Implementation**: Clean separation (Models/Services/CLI/Lib)
- **Input Validation & Error Handling**: User-friendly error messages
- **Simplicity & YAGNI**: No over-engineering
- **Comprehensive Documentation**: All artifacts tracked

## API Documentation

Once the backend is running, visit **http://localhost:8000/docs** for interactive API documentation.

### Available Endpoints

- `POST /api/todos` - Create a new task
- `GET /api/todos` - Get all tasks
- `GET /api/todos/{id}` - Get specific task
- `PATCH /api/todos/{id}` - Update task
- `DELETE /api/todos/{id}` - Delete task
- `GET /health` - Health check

### Example API Usage

```bash
# Create a task
curl -X POST http://localhost:8000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"description": "Buy groceries"}'

# Get all tasks
curl http://localhost:8000/api/todos

# Mark task as complete
curl -X PATCH http://localhost:8000/api/todos/{task-id} \
  -H "Content-Type: application/json" \
  -d '{"is_completed": true}'

# Delete a task
curl -X DELETE http://localhost:8000/api/todos/{task-id}
```

## Documentation

- **[STARTUP.md](./STARTUP.md)** - Local development setup guide
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Production deployment guide (Railway + Vercel)
- **Specification**: `specs/002-fullstack-todo-app/spec.md` - User stories and requirements
- **Architecture Plan**: `specs/002-fullstack-todo-app/plan.md` - Technical design
- **Task List**: `specs/002-fullstack-todo-app/tasks.md` - Implementation breakdown
- **Data Model**: `specs/002-fullstack-todo-app/data-model.md` - Database schema
- **API Contract**: `specs/002-fullstack-todo-app/contracts/openapi.yaml` - OpenAPI specification

## Contributing

This is a learning project following the Spec-Driven Development methodology. All work is done through the Claude Code agent following strict TDD practices.

## License

[Your License Here]

## Acknowledgments

- Built with [Claude Code](https://claude.com/claude-code)
- Following [Spec-Kit Plus](https://github.com/anthropics/specify) methodology
- Powered by [UV](https://github.com/astral-sh/uv) for Python packaging

## Testing

### Backend Tests
```bash
cd backend
pytest
pytest --cov=src --cov-report=term-missing
```

### Frontend Tests
```bash
cd frontend
npm run test
```

---

## Screenshots

![Todo App Interface](docs/screenshots/app-screenshot.png)
*Modern, clean interface built with Next.js and Tailwind CSS*

---

## Roadmap

### ✅ Completed (MVP - Phase II)
- Phase 1: Project Setup
- Phase 2: Infrastructure (Backend + Frontend)
- Phase 3 (US1): Quick Task Addition with full CRUD

### 🚧 In Progress
- Phase 4 (US2): Task Completion Toggle *(actually already implemented!)*
- Phase 5 (US3): Task Deletion *(actually already implemented!)*

### 📋 Planned
- Phase 6 (US4): Task List Display with Sorting
- Phase 7 (US5): Task Editing (inline editing)
- Phase 8 (US6): Task Filtering (All/Active/Completed)
- Phase 9: Integration Testing
- Phase 10: Deployment & Documentation

---

**Current Status**: ✅ **MVP Complete - Ready for Deployment**
**Next Milestone**: Deploy to Production (Railway + Vercel)
