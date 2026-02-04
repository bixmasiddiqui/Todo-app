# Implementation Plan: Full-Stack Todo Web Application

**Branch**: `001-fullstack-todo-web` | **Date**: 2026-01-04 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-fullstack-todo-web/spec.md`

## Summary

Build a production-ready, full-stack todo web application with clean architecture, persistent storage, and beautiful UI. The system will consist of a Next.js 14+ frontend with TypeScript and Tailwind CSS, a FastAPI backend with Python 3.11+, SQLModel ORM for type-safe database operations, and Neon Postgres for serverless database hosting. The application will support complete CRUD operations (Create, Read, Update, Delete) for todo tasks with mark-complete functionality, input validation, error handling, and responsive design.

**Key Architectural Decisions:**
- Monorepo structure with clear frontend/backend separation
- Server-first data flow using React Server Components
- RESTful JSON API with 5 endpoints
- UUID primary keys for future-proof distributed systems
- Tailwind CSS for rapid, custom UI development
- Zero external UI libraries (clean, unique design)

**Primary User Value:** Enable users to quickly capture, track, and manage tasks with 100% data persistence, sub-2-second response times, and a clean, intuitive interface that works across all devices.

---

## Technical Context

**Language/Version**:
- Frontend: TypeScript 5.x+ with Next.js 14+
- Backend: Python 3.11+

**Primary Dependencies**:
- Frontend: Next.js 14+, React 18+, Tailwind CSS 3.4+
- Backend: FastAPI 0.109+, SQLModel 0.0.14+, Uvicorn, Alembic
- Database Driver: psycopg2 (async via asyncpg for FastAPI)

**Storage**: Neon Postgres (serverless) with connection pooling

**Testing**:
- Frontend: Vitest + React Testing Library
- Backend: pytest + pytest-asyncio

**Target Platform**: Web (modern browsers: Chrome, Firefox, Safari, Edge with JavaScript enabled)

**Project Type**: Web application (monorepo with frontend/backend separation)

**Performance Goals**:
- Initial page load: < 3 seconds
- API response time: < 100ms (p95)
- Task operations: < 2 seconds end-to-end
- Support 100+ concurrent users without degradation

**Constraints**:
- Task description: 500 characters maximum
- No external UI component libraries (Tailwind only)
- Production-ready code from day one (no TODOs or placeholders)
- Clean architecture with zero technical debt

**Scale/Scope**:
- Single-user application (no authentication in Phase II)
- 5 core operations (add, view, edit, delete, mark complete)
- Optimized for up to 1000 tasks loaded
- Typical use case: 50-200 tasks

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase-Aware Architecture ✅ PASS

**Compliance**: This is Phase II of a multi-phase roadmap. Phase I was an in-memory Python console app. This phase builds the full-stack web application as specified in the constitution (Next.js + FastAPI + Postgres).

**Extension Points for Future Phases**:
- Clean API contracts support future AI chatbot integration (Phase III)
- Modular backend services can be containerized for Kubernetes (Phase IV)
- Database schema designed for multi-user support when auth is added (future)

**No Premature Complexity**: Single-user scope avoids auth complexity until Phase III. No over-engineering for unspecified future needs.

---

### Test-First Development (TDD) ✅ PASS

**Commitment**: All implementation will follow strict TDD:
1. Write tests first (unit + integration)
2. Verify tests fail
3. Implement minimum code to pass tests
4. Refactor while keeping tests green

**Test Coverage Targets**:
- Backend: 80%+ coverage (focus on business logic, API endpoints, data validation)
- Frontend: 70%+ coverage (focus on components, user interactions)

**Test Organization**:
- Backend: `backend/tests/unit/` and `backend/tests/integration/`
- Frontend: `frontend/src/__tests__/`

---

### Independent User Stories ✅ PASS

**Story Independence**: All 6 user stories from spec are independently deliverable:
- P1: Quick Task Addition (MVP - can ship with just this)
- P1: Task Completion Tracking (independent of edit/delete)
- P1: Task List Overview (works standalone)
- P2: Task Modification (enhancement to P1 stories)
- P2: Task Deletion (enhancement to P1 stories)
- P3: Responsive Access (progressive enhancement)

**Incremental Value**: Each P1 story delivers usable functionality. P2/P3 enhance but aren't blockers.

---

### Modular Implementation ✅ PASS

**Backend Structure**:
```
backend/src/
├── models/          # SQLModel entities (Task)
├── routers/         # FastAPI route handlers (todos router)
├── services/        # Business logic (task service)
├── database.py      # DB session management
└── main.py          # FastAPI app initialization
```

**Frontend Structure**:
```
frontend/src/
├── app/             # Next.js App Router (pages, layouts)
├── components/      # React components (TaskInput, TaskList, TaskItem)
├── lib/             # Client utilities (API client)
└── types/           # TypeScript types (Task interfaces)
```

**Rationale**: Clear separation of concerns enables independent testing and future migration (e.g., mobile app reusing backend API).

---

### Input Validation & Error Handling ✅ PASS

**Validation Strategy**:
- **Client-Side**: HTML5 + JavaScript validation (UX only, not security)
- **Backend**: Pydantic/SQLModel validation (security boundary)
- **Database**: Check constraints (last line of defense)

**Error Handling**:
- User-friendly messages for all validation errors (FR-009)
- Preserve user input on failure
- Global exception handlers in FastAPI
- Error boundaries in Next.js
- Proper HTTP status codes (FR-012)

**Edge Cases Addressed**:
- Empty/whitespace-only descriptions
- Description exceeding 500 characters
- Database connection failures
- Network errors during API calls
- Invalid UUID formats

---

### Simplicity & YAGNI ✅ PASS

**Avoided Premature Complexity**:
- ❌ No user authentication (not needed for Phase II)
- ❌ No global state library (React Server Components + local state sufficient)
- ❌ No heavy UI frameworks (Tailwind utilities only)
- ❌ No caching layers (Neon Postgres + connection pooling adequate)
- ❌ No message queues (direct API calls sufficient for single-user)
- ❌ No microservices (monorepo with 2 services is appropriate scale)

**Justified Complexity**:
- ✅ Monorepo structure: Simplifies versioning, shared tooling
- ✅ SQLModel: Combines ORM + validation in one layer (reduces boilerplate vs SQLAlchemy + Pydantic separately)
- ✅ UUID primary keys: Standard practice, prevents ID enumeration, future-proof
- ✅ Alembic migrations: Standard for production databases, enables safe schema evolution

---

### Comprehensive Documentation ✅ PASS

**Deliverables** (all created):
- ✅ `spec.md`: User stories, requirements, success criteria
- ✅ `plan.md`: This file - architecture, technical decisions
- ✅ `research.md`: Technology stack decisions, rationale, alternatives
- ✅ `data-model.md`: Entity definitions, database schema, validation rules
- ✅ `contracts/openapi.yaml`: Full API specification with examples
- ✅ `quickstart.md`: Setup guide, development workflow, troubleshooting
- ⏳ `tasks.md`: Will be generated by `/sp.tasks` command (not created by `/sp.plan`)
- ⏳ `README.md`: Will be created during implementation phase
- ⏳ PHRs: Prompt History Records created during execution
- ⏳ ADRs: Architecture Decision Records (if significant decisions warrant)

**Code Documentation Standards**:
- Docstrings for all public functions/classes
- Type annotations throughout (Python + TypeScript)
- Inline comments only for non-obvious logic
- Self-documenting code via clear naming

---

## Project Structure

### Documentation (this feature)

```text
specs/001-fullstack-todo-web/
├── spec.md              # Feature specification (user stories, requirements)
├── plan.md              # This file (architecture, technical decisions)
├── research.md          # Technology stack research and rationale
├── data-model.md        # Entity definitions, database schema
├── quickstart.md        # Setup and development guide
├── contracts/           # API contracts
│   └── openapi.yaml     # OpenAPI 3.1 specification
├── checklists/          # Quality validation checklists
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Implementation tasks (created by /sp.tasks)
```

---

### Source Code (repository root)

**Option Selected: Web Application (Frontend + Backend)**

```text
/
├── frontend/
│   ├── src/
│   │   ├── app/                    # Next.js App Router
│   │   │   ├── layout.tsx          # Root layout with metadata
│   │   │   ├── page.tsx            # Home page (task list)
│   │   │   ├── globals.css         # Global styles + Tailwind imports
│   │   │   ├── error.tsx           # Error boundary
│   │   │   └── loading.tsx         # Loading state
│   │   ├── components/             # React components
│   │   │   ├── TaskInput.tsx       # Task creation form
│   │   │   ├── TaskList.tsx        # Task list container
│   │   │   ├── TaskItem.tsx        # Individual task component
│   │   │   ├── EmptyState.tsx      # No tasks message
│   │   │   └── ErrorMessage.tsx    # Error display component
│   │   ├── lib/                    # Client utilities
│   │   │   ├── api.ts              # API client functions
│   │   │   └── utils.ts            # Helper functions
│   │   └── types/                  # TypeScript types
│   │       └── task.ts             # Task interfaces
│   ├── public/                     # Static assets
│   ├── __tests__/                  # Frontend tests
│   │   ├── components/             # Component tests
│   │   └── lib/                    # Utility tests
│   ├── package.json                # Dependencies, scripts
│   ├── tsconfig.json               # TypeScript config
│   ├── tailwind.config.ts          # Tailwind configuration
│   ├── postcss.config.js           # PostCSS config
│   ├── next.config.js              # Next.js configuration
│   ├── .env.local                  # Environment variables (gitignored)
│   └── .env.example                # Environment template
│
├── backend/
│   ├── src/
│   │   ├── models/                 # SQLModel entities
│   │   │   ├── __init__.py
│   │   │   └── task.py             # Task model + schemas
│   │   ├── routers/                # FastAPI route handlers
│   │   │   ├── __init__.py
│   │   │   └── todos.py            # /api/todos endpoints
│   │   ├── services/               # Business logic
│   │   │   ├── __init__.py
│   │   │   └── task_service.py     # Task CRUD operations
│   │   ├── __init__.py
│   │   ├── database.py             # DB connection, session management
│   │   ├── config.py               # Settings from environment
│   │   └── main.py                 # FastAPI app entry point
│   ├── tests/
│   │   ├── unit/                   # Unit tests
│   │   │   ├── test_models.py      # Model validation tests
│   │   │   └── test_services.py    # Service logic tests
│   │   └── integration/            # Integration tests
│   │       └── test_api.py         # API endpoint tests
│   ├── alembic/                    # Database migrations
│   │   ├── versions/               # Migration files
│   │   ├── env.py                  # Alembic environment
│   │   └── script.py.mako          # Migration template
│   ├── alembic.ini                 # Alembic configuration
│   ├── requirements.txt            # Python dependencies
│   ├── pyproject.toml              # Project metadata
│   ├── .env                        # Environment variables (gitignored)
│   └── .env.example                # Environment template
│
├── .gitignore                      # Git ignore rules
├── README.md                       # Project overview and quick start
└── CLAUDE.md                       # Agent development rules (updated with tech stack)
```

**Structure Decision**: Selected **Option 2 (Web Application)** from plan template because:
1. Feature requires both frontend and backend (not a single-project app)
2. Clear separation enables independent deployment
3. Not a mobile app (no iOS/Android directories needed)
4. Monorepo keeps frontend/backend in sync with shared versioning

---

## Complexity Tracking

**No Constitution Violations** - All complexity is justified by requirements.

This section is not needed as there are no violations requiring justification.

---

## Architecture Details

### 1. System Architecture

**High-Level Flow**:
```
User Browser
     │
     ├─→ Next.js Frontend (localhost:3000)
     │       │
     │       ├─→ Server Components (initial render)
     │       └─→ Client Components (interactions)
     │               │
     │               └─→ API Client (fetch)
     │                       │
     │                       ▼
     └─→ FastAPI Backend (localhost:8000)
                 │
                 ├─→ Request Validation (Pydantic)
                 ├─→ Business Logic (Services)
                 ├─→ ORM Layer (SQLModel)
                 └─→ Database Connection Pool
                         │
                         ▼
                    Neon Postgres Database
```

**Data Flow for Task Creation**:
1. User types description in `TaskInput` component (Client Component)
2. On submit, client calls `createTask()` from `lib/api.ts`
3. API client sends POST to `http://localhost:8000/api/todos`
4. FastAPI router receives request, validates with Pydantic
5. Service layer executes business logic
6. SQLModel inserts into database via parameterized query
7. Database returns created task with ID and timestamps
8. FastAPI serializes to JSON and returns 201 Created
9. Client receives response, updates UI optimistically
10. Next.js revalidates server component cache for task list

---

### 2. API Design

**Endpoints** (5 total):

| Method | Path | Purpose | Request | Response |
|--------|------|---------|---------|----------|
| GET | `/api/todos` | List all tasks | None | `Task[]` |
| POST | `/api/todos` | Create task | `{description}` | `Task` (201) |
| GET | `/api/todos/{id}` | Get single task | None | `Task` |
| PATCH | `/api/todos/{id}` | Update task | `{description?, is_completed?}` | `Task` |
| DELETE | `/api/todos/{id}` | Delete task | None | 204 No Content |

**Status Codes**:
- **200 OK**: Successful GET, PATCH
- **201 Created**: Successful POST
- **204 No Content**: Successful DELETE
- **400 Bad Request**: Validation error, invalid input
- **404 Not Found**: Task ID doesn't exist
- **422 Unprocessable Entity**: Malformed JSON
- **500 Internal Server Error**: Unexpected server error

**Error Response Format**:
```json
{
  "error": "Validation Error",
  "detail": "Description cannot be empty",
  "validation_errors": [
    {
      "field": "description",
      "message": "Description cannot be empty or whitespace only"
    }
  ]
}
```

**Full Specification**: See `contracts/openapi.yaml` for complete API documentation with examples.

---

### 3. Database Design

**Schema**:
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    description VARCHAR(500) NOT NULL CHECK (length(description) >= 1),
    is_completed BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);
CREATE INDEX idx_tasks_is_completed ON tasks(is_completed);
```

**Indexes Rationale**:
- `idx_tasks_created_at`: Supports default ordering (newest first)
- `idx_tasks_is_completed`: Future enhancement for filtering completed vs incomplete

**Constraints**:
- Primary key ensures uniqueness
- NOT NULL prevents missing required fields
- Check constraint enforces non-empty descriptions
- Auto-updating trigger for `updated_at`

**Full Schema Details**: See `data-model.md` for complete entity definitions, validation rules, and migration strategy.

---

### 4. Frontend Architecture

**Component Hierarchy**:
```
Page (Server Component)
└── TaskList
    ├── TaskInput (Client Component)
    └── Task Items (mix of Server + Client)
        ├── TaskItem (Client Component for interactivity)
        ├── EditMode (Client Component)
        └── DeleteConfirmation (Client Component)
```

**State Management**:
- **Server State**: React Server Components fetch from API, cache responses
- **Client State**: useState for form inputs, edit mode, loading states
- **No Global State**: Not needed for single-entity app

**Styling Approach**:
- Tailwind utility classes for all styling
- No CSS modules, styled-components, or external UI libraries
- Custom design inspired by linear.app and height.app
- Responsive classes (sm:, md:, lg:) for mobile-first design

**Performance Optimizations**:
- Server Components reduce client JavaScript bundle
- Streaming SSR for fast initial render
- Optimistic UI updates for perceived speed
- Debounced input validation

---

### 5. Backend Architecture

**Layered Architecture**:
```
Routers (API Endpoints)
    ↓
Services (Business Logic)
    ↓
Models (Data Layer)
    ↓
Database (Persistence)
```

**Layer Responsibilities**:
- **Routers**: HTTP handling, request/response serialization, status codes
- **Services**: Business logic, validation coordination, transaction management
- **Models**: Data definitions, SQLModel schemas, database mapping
- **Database**: Connection pooling, session management, query execution

**Dependency Injection**:
```python
# Database session injected into route handlers
@router.get("/api/todos")
async def list_tasks(db: Session = Depends(get_db)):
    return task_service.list_all(db)
```

**Error Handling**:
- Global exception handlers for common errors (404, 422, 500)
- Custom exceptions for domain errors (TaskNotFound, ValidationError)
- Logging with structured output for debugging

---

### 6. Security Implementation

**Input Validation**:
- Pydantic models validate type, length, format
- Custom validators trim whitespace, enforce business rules
- Database check constraints as last line of defense

**SQL Injection Prevention**:
- SQLModel uses parameterized queries exclusively
- Never construct raw SQL from user input

**CORS Configuration**:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Production**: Restrict to actual frontend domain, no wildcards.

**XSS Protection**:
- React escapes output by default
- Never use `dangerouslySetInnerHTML`
- Validate and sanitize all user inputs

**Environment Security**:
- Credentials in .env files (gitignored)
- No secrets in code or version control
- HTTPS in production (TLS encryption)

---

## Implementation Workflow

### Phase 0: Research ✅ COMPLETED

**Deliverable**: `research.md`

**Outcomes**:
- All technology choices researched and justified
- Alternatives considered and documented
- Best practices identified for each technology
- All "NEEDS CLARIFICATION" items resolved

**Status**: Complete - see `research.md`

---

### Phase 1: Design & Contracts ✅ COMPLETED

**Deliverable**: `data-model.md`, `contracts/openapi.yaml`, `quickstart.md`

**Outcomes**:
- Database schema designed with indexes and constraints
- API contracts defined with full OpenAPI 3.1 spec
- SQLModel models defined with validation
- TypeScript types defined for frontend
- Quickstart guide created with setup instructions

**Status**: Complete - all artifacts generated

---

### Phase 2: Tasks Generation (Next Step)

**Command**: `/sp.tasks`

**Expected Output**: `tasks.md` with dependency-ordered implementation tasks

**Task Categories**:
1. Backend setup (FastAPI app, database connection, migrations)
2. Backend models and services (Task entity, CRUD operations)
3. Backend API endpoints (5 routes with tests)
4. Frontend setup (Next.js app, Tailwind configuration)
5. Frontend components (TaskInput, TaskList, TaskItem)
6. Frontend integration (API client, error handling)
7. End-to-end testing (manual + automated)
8. Documentation finalization (README, deployment guide)

**Workflow**: Each task will follow TDD cycle (write test → fail → implement → pass → refactor)

---

## Risk Analysis

### Technical Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Neon database connection issues | High | Provide fallback connection string, implement retry logic, document troubleshooting in quickstart.md |
| CORS configuration errors | Medium | Detailed CORS setup in quickstart, test with actual frontend requests during development |
| TypeScript/Python type mismatches | Medium | Keep TypeScript types in sync with SQLModel schemas, use OpenAPI spec as source of truth |
| Performance degradation with many tasks | Low | Indexes on created_at, test with 1000+ tasks, plan for pagination if needed |
| State sync issues (client/server) | Low | Server is source of truth, optimistic updates with revalidation, error rollback |

---

### Development Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Environment setup complexity | Medium | Comprehensive quickstart.md, provide .env.example files, troubleshooting section |
| Testing coverage gaps | Medium | Require tests before implementation (TDD), track coverage metrics, gate PRs on coverage |
| Scope creep (adding features) | High | Strict adherence to spec, explicit out-of-scope list, defer enhancements to future phases |
| Inconsistent code style | Low | ESLint + Prettier for frontend, Black + isort for backend, pre-commit hooks |

---

## Success Metrics

**Definition of Done** (from spec.md Success Criteria):

1. ✅ **Performance**: Task operations complete in under 2 seconds (SC-001)
2. ✅ **Core Workflow**: Add/complete/delete workflow under 30 seconds (SC-002)
3. ✅ **Persistence**: 100% data reliability, no loss on refresh (SC-003)
4. ✅ **Responsive**: Works on 320px to 1920px without scrolling (SC-004)
5. ✅ **Feedback**: All actions provide feedback within 200ms (SC-005)
6. ✅ **Error Handling**: Graceful error messages, retry capability (SC-006)
7. ✅ **Usability**: 95% of users understand empty state without help (SC-007)
8. ✅ **Scalability**: 100+ concurrent users supported (SC-008)
9. ✅ **Stability**: Zero unhandled exceptions during normal use (SC-009)
10. ✅ **Performance**: 1000 tasks remain performant and readable (SC-010)

**Quality Gates**:
- All tests passing (unit + integration)
- 80%+ backend coverage, 70%+ frontend coverage
- No TypeScript errors
- No linter errors/warnings
- Manual testing of all user stories completed
- Quickstart guide successfully used by fresh developer

---

## Next Steps

### Immediate Actions

1. **Review Planning Artifacts**:
   - Read `research.md`, `data-model.md`, `contracts/openapi.yaml`, `quickstart.md`
   - Verify architecture aligns with requirements
   - Ask questions or request clarifications if needed

2. **Generate Implementation Tasks**:
   - Run `/sp.tasks` to generate `tasks.md`
   - Review task breakdown and dependencies
   - Confirm task ordering makes sense

3. **Begin Implementation**:
   - Run `/sp.implement` to execute tasks
   - Follow TDD workflow strictly
   - Update documentation as code evolves

---

### Follow-Up Documentation

**After Implementation**:
- Create `README.md` at project root with overview and quick start
- Document deployment process for production
- Create ADRs for any significant architectural decisions made during implementation
- Update constitution if patterns emerge that should be standardized

---

## Architectural Decision Records (ADR)

**Significant Decisions Made**:

Based on the three-part test (impact, alternatives, scope), the following decisions may warrant ADRs:

1. **Monorepo Structure with Frontend/Backend Separation**
   - Long-term impact: Affects deployment, versioning, tooling
   - Alternatives: Separate repos, single fullstack project, Turborepo
   - Cross-cutting: Influences CI/CD, developer workflow, deployment strategy
   - **Recommendation**: Create ADR if this pattern is adopted for future features

2. **SQLModel for ORM + Validation**
   - Long-term impact: Affects all data layer code, migrations, API contracts
   - Alternatives: SQLAlchemy + Pydantic separately, Tortoise ORM, raw SQL
   - Cross-cutting: Touches models, services, API responses, tests
   - **Recommendation**: Create ADR if significant (established pattern for project)

3. **UUID Primary Keys**
   - Long-term impact: Affects all entities, API contracts, database design
   - Alternatives: Auto-increment integers, composite keys
   - Cross-cutting: Influences security, scalability, future multi-region support
   - **Recommendation**: Create ADR if this becomes standard for all entities

**ADR Creation**:
If user approves, run `/sp.adr <decision-title>` to document these decisions with rationale and tradeoffs.

---

**Plan Version**: 1.0.0
**Status**: Complete - Ready for `/sp.tasks`
**Constitution Compliance**: ✅ All gates passed
**Artifacts Generated**: research.md, data-model.md, contracts/openapi.yaml, quickstart.md, plan.md
**Next Command**: `/sp.tasks`
