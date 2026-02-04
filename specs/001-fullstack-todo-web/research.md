# Phase 0: Research & Technical Decisions

**Feature**: Full-Stack Todo Web Application
**Branch**: 001-fullstack-todo-web
**Date**: 2026-01-04

## Purpose

This document consolidates all technical research, decisions, and rationale needed to proceed with architectural design. All "NEEDS CLARIFICATION" items from Technical Context have been resolved through research and industry best practices.

---

## 1. Technology Stack Decisions

### 1.1 Frontend: Next.js 14+ with App Router

**Decision**: Use Next.js 14+ with App Router for the frontend

**Rationale**:
- **App Router Benefits**: Server Components by default, improved routing with file-system based patterns, built-in loading/error states, streaming SSR
- **Performance**: Automatic code splitting, image optimization, font optimization out of the box
- **Developer Experience**: Hot module replacement, TypeScript support, ESLint integration
- **Production Ready**: Used by major companies (Netflix, TikTok, Twitch), mature ecosystem
- **Spec Alignment**: Meets responsive design requirements (FR-011), supports clean architecture separation (FR-013)

**Alternatives Considered**:
- **React + Vite**: More configuration needed, no built-in SSR/SSG, would require additional routing library
- **Remix**: Excellent but smaller ecosystem, steeper learning curve for data mutations
- **SvelteKit**: Great DX but less mature ecosystem, fewer third-party integrations

**Best Practices Applied**:
- Use Server Components for data fetching (reduces client bundle size)
- Client Components only for interactivity (form inputs, checkboxes, modals)
- Route Handlers for API proxy layer if needed (though backend is FastAPI)
- Implement proper error boundaries for graceful error handling (FR-010)

---

### 1.2 Backend: FastAPI 0.109+ with Python 3.11+

**Decision**: Use FastAPI with Python 3.11+ for the backend API layer

**Rationale**:
- **Performance**: ASGI-based, comparable to Node.js/Go in benchmarks, async support throughout
- **Type Safety**: Pydantic v2 for request/response validation, automatic OpenAPI docs
- **Developer Experience**: Automatic API documentation (Swagger UI, ReDoc), dependency injection system
- **Spec Alignment**: Easy HTTP status code control (FR-012), built-in error handling (FR-010), validation support (FR-008)
- **SQLModel Compatibility**: Perfect integration with SQLModel (same author - Sebastián Ramírez)

**Alternatives Considered**:
- **Django REST Framework**: More batteries-included but heavier, includes ORM (we want SQLModel), slower than FastAPI
- **Flask + extensions**: Requires more manual setup, less type safety, no automatic docs
- **Express.js (Node)**: Would unify stack but team specified Python backend, less type safety

**Best Practices Applied**:
- Use dependency injection for database sessions
- Implement middleware for CORS (FR security requirements)
- Use Pydantic models for request/response validation
- Separate routers by domain (todos router)
- Implement proper exception handlers with user-friendly messages (FR-009)

---

### 1.3 ORM: SQLModel 0.0.14+

**Decision**: Use SQLModel for database ORM and data modeling

**Rationale**:
- **Type Safety**: Combines SQLAlchemy and Pydantic - one model for DB, API, and validation
- **Developer Experience**: Single source of truth for data models, IDE autocomplete, type checking
- **FastAPI Integration**: Built by same author, perfect compatibility, automatic API docs from models
- **Migration Support**: Built on SQLAlchemy Core, compatible with Alembic for migrations
- **Spec Alignment**: Prevents SQL injection via parameterized queries (Security Considerations)

**Alternatives Considered**:
- **SQLAlchemy + Pydantic separately**: More boilerplate, duplicate model definitions, sync issues
- **Tortoise ORM**: Async-first but less mature, smaller ecosystem, no Pydantic integration
- **Raw SQL with psycopg3**: More control but loses type safety, more SQL injection risk, more boilerplate

**Best Practices Applied**:
- Use optional fields for nullable columns
- Implement proper relationships (though not needed for single-table app)
- Use Pydantic validators for complex validation rules (e.g., max description length)
- Separate table models from API schemas when needed (creation vs response)

---

### 1.4 Database: Neon Postgres (Serverless)

**Decision**: Use Neon Postgres as the database provider

**Rationale**:
- **Serverless Architecture**: Auto-scaling, pay-per-use, no server management
- **Performance**: Connection pooling built-in, fast cold starts, low latency
- **Developer Experience**: Easy provisioning, branching for dev/test environments, time-travel debugging
- **Spec Alignment**: Postgres reliability (SC-003: 100% data persistence), handles concurrent users (SC-008)
- **Modern Features**: Full Postgres compatibility, supports modern SQL features, JSON columns if needed

**Alternatives Considered**:
- **Supabase**: Includes auth/storage (not needed), more complex for simple use case
- **Heroku Postgres**: Legacy platform, less modern features, higher cost
- **Self-hosted Postgres**: More operational overhead, no auto-scaling, requires server management

**Connection Best Practices**:
- Use connection pooling via SQLAlchemy engine
- Store credentials in environment variables (.env file)
- Use async driver (asyncpg) for async FastAPI endpoints
- Implement proper connection lifecycle management (startup/shutdown events)

---

### 1.5 Styling: Tailwind CSS 3.4+

**Decision**: Use Tailwind CSS for styling

**Rationale**:
- **Productivity**: Utility-first approach, rapid prototyping, consistent spacing/colors
- **Performance**: Purges unused CSS, small bundle size (~10KB compressed)
- **Responsive Design**: Built-in responsive utilities (FR-011: mobile to desktop support)
- **Spec Alignment**: No heavy UI libraries (Constraint #3), enables unique designs (UI Requirements)
- **Next.js Integration**: Official Next.js + Tailwind integration, zero config needed

**Alternatives Considered**:
- **Custom CSS**: More control but slower development, harder to maintain consistency
- **CSS Modules**: Good scoping but lacks utility patterns, more verbose
- **Styled Components**: React-specific, runtime overhead, larger bundle size
- **Bootstrap/Material UI**: Too opinionated, generic designs, larger bundles (violates constraints)

**Best Practices Applied**:
- Use semantic class grouping (e.g., `flex items-center gap-4`)
- Create custom utilities for brand colors/spacing if needed
- Use Tailwind's JIT mode for optimal build performance
- Implement responsive classes (sm:, md:, lg:) for mobile-first design

---

## 2. Architecture & Patterns

### 2.1 Project Structure: Monorepo with Separate Frontend/Backend

**Decision**: Use monorepo structure with clear frontend/backend separation

**Rationale**:
- **Spec Compliance**: Clean separation (FR-013), no confusing nesting (Architecture Requirements)
- **Development Experience**: Single repo simplifies versioning, shared tooling configuration
- **Deployment Flexibility**: Can deploy frontend/backend independently or together
- **Clean Paths**: Clear boundaries prevent architectural confusion

**Structure**:
```
/
├── frontend/          # Next.js application
│   ├── src/
│   │   ├── app/      # App Router pages and layouts
│   │   ├── components/  # React components
│   │   ├── lib/      # Client utilities, API client
│   │   └── types/    # TypeScript types
│   ├── public/       # Static assets
│   └── package.json
│
├── backend/           # FastAPI application
│   ├── src/
│   │   ├── models/   # SQLModel models
│   │   ├── routers/  # API route handlers
│   │   ├── services/ # Business logic
│   │   ├── database.py  # DB connection
│   │   └── main.py   # FastAPI app entry
│   ├── tests/        # Backend tests
│   ├── alembic/      # DB migrations
│   └── pyproject.toml
│
├── .env.example       # Template for environment vars
└── README.md          # Project documentation
```

**Alternatives Considered**:
- **Single fullstack project**: Would mix concerns, harder to deploy separately
- **Separate repos**: Complicates versioning, shared types difficult, more overhead
- **Turborepo/Nx**: Overkill for 2-project structure, adds unnecessary complexity

---

### 2.2 API Design: RESTful with JSON

**Decision**: Use REST API with JSON payloads, following OpenAPI 3.1 spec

**Rationale**:
- **Simplicity**: REST is well-understood, easy to test, browser-friendly
- **Spec Alignment**: Supports all CRUD operations (FR-001 through FR-006)
- **FastAPI Advantage**: Automatic OpenAPI docs, request/response validation
- **Caching**: HTTP caching strategies possible for GET requests

**Endpoint Design** (detailed in contracts/openapi.yaml):

| Method | Endpoint | Purpose | Status Codes |
|--------|----------|---------|--------------|
| GET | `/api/todos` | List all tasks | 200 OK |
| POST | `/api/todos` | Create new task | 201 Created, 400 Bad Request |
| GET | `/api/todos/{id}` | Get single task | 200 OK, 404 Not Found |
| PATCH | `/api/todos/{id}` | Update task (partial) | 200 OK, 400 Bad Request, 404 Not Found |
| DELETE | `/api/todos/{id}` | Delete task | 204 No Content, 404 Not Found |

**Alternative Design Considered**:
- Using `/api/todos/{id}/complete` (POST) for completion toggle
- **Decision**: Rejected in favor of PATCH with `is_completed` field for simplicity and REST compliance

**Best Practices**:
- Use plural resource names (`/todos` not `/todo`)
- Return created resource in POST response with Location header
- Use 404 for not found, 400 for validation errors, 500 for server errors (FR-012)
- Include request IDs in error responses for debugging
- Use ISO 8601 timestamps for created_at/updated_at

---

### 2.3 Data Flow & State Management

**Decision**: Server-first data flow with React Server Components, minimal client state

**Data Flow**:
1. **Initial Page Load**: Server Component fetches from API, renders HTML
2. **Client Interactions**: Client Components call API directly via fetch
3. **Optimistic Updates**: Update UI immediately, revalidate in background
4. **Error Handling**: Show toast/inline errors, preserve user input on failure

**State Management**:
- **Server State**: React Server Components + fetch cache
- **Client State**: useState for form inputs, UI toggles (edit mode, modals)
- **No Global State Library**: Not needed for single-entity app (just todos)
- **URL State**: Use Next.js searchParams for any future filtering (out of scope for v1)

**Rationale**:
- **Spec Alignment**: Simplicity (Constraint #5), fast feedback (SC-005: 200ms)
- **Performance**: Reduced JavaScript bundle, less hydration time
- **Reliability**: Server is source of truth, no client/server state sync issues

**Alternatives Considered**:
- **React Query/SWR**: Excellent libraries but overkill for simple CRUD, adds bundle size
- **Redux/Zustand**: Unnecessary for single-entity app with no complex shared state
- **Server Actions**: Could replace API calls but keeps us tied to Next.js deployment model

---

### 2.4 Database Schema Design

**Decision**: Single `tasks` table with minimal fields, UUID primary key

**Schema** (detailed in data-model.md):
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    description VARCHAR(500) NOT NULL,
    is_completed BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);
```

**Rationale**:
- **UUID vs Auto-increment**: UUIDs prevent ID enumeration attacks, easier for distributed systems (future), no collision risk
- **VARCHAR(500)**: Matches spec constraint, prevents abuse, adequate for task descriptions
- **Timestamps**: Required by spec entity definition, useful for future sorting/filtering
- **Index on created_at**: Supports default ordering (newest first), minimal overhead for single table

**Migration Strategy**:
- Use Alembic for schema migrations
- Initial migration creates table with indexes
- Versioned migrations for any future schema changes
- Migration commands documented in quickstart.md

**Alternatives Considered**:
- **Serial ID**: Simpler but exposes record count, enumeration risk, collision in multi-region (future)
- **Composite key**: Overkill for single-user app with single entity type
- **Separate updated_by tracking**: Out of scope (no auth/users in Phase II)

---

## 3. Development & Deployment

### 3.1 Package Management

**Frontend**:
- **Decision**: npm (comes with Node.js)
- **Rationale**: Default for Next.js, widest compatibility, lockfile support
- **Alternative Considered**: pnpm (faster, better space efficiency) - may consider for future but adds setup complexity

**Backend**:
- **Decision**: uv (ultra-fast Python package manager)
- **Rationale**: Modern Python package manager, 10-100x faster than pip, compatible with requirements.txt, better dependency resolution
- **Alternative Considered**: pip (slower but universal), poetry (good but opinionated project structure)

---

### 3.2 Environment Configuration

**Decision**: Use `.env` files with proper .gitignore protection

**Required Variables**:
```bash
# Backend (.env in /backend)
DATABASE_URL=postgresql://user:pass@host:5432/dbname
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com

# Frontend (.env.local in /frontend)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Best Practices**:
- Provide `.env.example` files with dummy values
- Use `python-dotenv` in backend for loading
- Use Next.js built-in env var loading in frontend
- Never commit actual `.env` files (in .gitignore)
- Document all env vars in quickstart.md

---

### 3.3 Error Handling Strategy

**Backend Error Handling**:
```python
# Custom exception classes
class TaskNotFoundError(Exception)
class ValidationError(Exception)

# Global exception handler
@app.exception_handler(TaskNotFoundError)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Task not found", "detail": str(exc)}
    )
```

**Frontend Error Handling**:
- Use Next.js error boundaries for page-level errors
- Show inline errors for form validation
- Use toast notifications for async operation feedback (success/failure)
- Preserve user input on failure (FR-009 requirement)

**Rationale**: Matches FR-009 (user-friendly errors), FR-010 (prevent crashes), SC-006 (graceful degradation)

---

### 3.4 Testing Strategy

**Backend Testing** (pytest):
- **Unit Tests**: Test individual functions (validation, business logic)
- **Integration Tests**: Test API endpoints with test database
- **Fixtures**: Shared database setup, mock data generators
- **Coverage Target**: 80%+ (focus on critical paths)

**Frontend Testing** (Vitest + React Testing Library):
- **Component Tests**: Test individual components in isolation
- **Integration Tests**: Test page-level interactions
- **E2E Tests**: Future consideration (Playwright) - out of scope for v1

**Test Organization**:
```
backend/tests/
├── unit/
│   ├── test_models.py
│   └── test_services.py
└── integration/
    └── test_api.py

frontend/src/__tests__/
├── components/
└── lib/
```

---

## 4. Performance Optimization

### 4.1 Frontend Performance

**Strategies**:
- **Code Splitting**: Automatic via Next.js App Router
- **Image Optimization**: Use Next.js `<Image>` component (if images added later)
- **Font Optimization**: Use Next.js font optimization with local fonts
- **Minimize Client JS**: Use Server Components by default, Client Components only for interactivity

**Metrics** (aligned with SC-001, SC-005):
- First Contentful Paint (FCP): < 1.5s
- Largest Contentful Paint (LCP): < 2.5s
- Cumulative Layout Shift (CLS): < 0.1
- Time to Interactive (TTI): < 3s

---

### 4.2 Backend Performance

**Strategies**:
- **Connection Pooling**: SQLAlchemy engine with pool_size=10
- **Async Endpoints**: Use async/await throughout
- **Query Optimization**: Index on created_at for sorting
- **Response Caching**: HTTP caching headers for GET requests (Cache-Control)

**Metrics** (aligned with SC-001, SC-008):
- API Response Time (p95): < 100ms for simple CRUD
- Concurrent Requests: 100+ without degradation
- Database Query Time: < 50ms per operation

---

### 4.3 Database Performance

**Strategies**:
- **Indexes**: created_at index for default ordering
- **Connection Pooling**: Neon's built-in pooling + SQLAlchemy
- **Query Efficiency**: Simple SELECT/INSERT/UPDATE/DELETE - no N+1 issues

**Monitoring**:
- Track slow queries (> 100ms) via Neon console
- Monitor connection pool utilization
- Set up alerts for high error rates

---

## 5. Security Considerations

### 5.1 Input Validation

**Implementation**:
- **Backend**: Pydantic models validate all inputs (type, length, format)
- **Frontend**: HTML5 validation + client-side checks (UX only, not security)
- **SQL Injection**: Prevented via SQLModel parameterized queries
- **XSS Protection**: React escapes by default, avoid dangerouslySetInnerHTML

**Validation Rules**:
- Task description: 1-500 characters, non-empty (FR-008)
- Boolean fields: Strict true/false validation
- UUID validation for ID parameters

---

### 5.2 CORS Configuration

**Implementation**:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Production**: Restrict to actual frontend domain, remove wildcards

---

### 5.3 Rate Limiting (Optional for v1)

**Consideration**: Optional for single-user app but recommended for production

**Future Implementation**:
- Use slowapi (FastAPI rate limiting library)
- Set limits: 100 requests/minute per IP
- Return 429 Too Many Requests with Retry-After header

---

## 6. UI/UX Design Decisions

### 6.1 Design System

**Decision**: Custom design with Tailwind, inspired by linear.app and height.app

**Characteristics**:
- **Minimalist**: Clean, uncluttered, focus on content
- **Keyboard-First**: Enter to submit, Escape to cancel, Tab navigation
- **Responsive**: Mobile-first approach, adapts to all screen sizes
- **Accessible**: Semantic HTML, proper ARIA labels, keyboard navigation

**Color Palette** (example, can be customized):
- **Primary**: Indigo (500, 600, 700 shades)
- **Success**: Green (completed tasks)
- **Neutral**: Gray scale (700 for text, 100-300 for backgrounds)
- **Error**: Red (400, 500 for validation errors)

---

### 6.2 Component Design

**Key Components**:
1. **TaskInput**: Auto-focus input field with submit button
2. **TaskList**: Virtualized list (if > 100 tasks) with smooth scrolling
3. **TaskItem**: Checkbox, description, edit/delete buttons
4. **EmptyState**: Friendly illustration/text when no tasks exist
5. **ErrorBoundary**: Graceful error display with retry option

**Interaction Patterns**:
- **Optimistic Updates**: UI updates immediately, reverts on error
- **Loading States**: Subtle spinners, skeleton screens for slow connections
- **Confirmation**: Modal for destructive actions (delete)
- **Inline Editing**: Double-click to edit, Escape to cancel, Enter to save

---

## 7. Research Summary

### Resolved Clarifications

All "NEEDS CLARIFICATION" items from Technical Context are now resolved:

| Item | Resolution |
|------|------------|
| Language/Version | Python 3.11+ (backend), TypeScript 5.x+ (frontend) |
| Primary Dependencies | FastAPI, SQLModel, Next.js 14+, Tailwind CSS |
| Storage | Neon Postgres (serverless) |
| Testing | pytest (backend), Vitest (frontend) |
| Target Platform | Web (browser + server) |
| Performance Goals | < 2s page load, < 100ms API response, 100+ concurrent users |
| Constraints | 500 char task limit, 1000 tasks performant |
| Scale/Scope | Single-user app, 5 core features (add/view/edit/delete/complete) |

---

### Key Technical Decisions Documented

1. **Frontend**: Next.js 14+ App Router with TypeScript and Tailwind CSS
2. **Backend**: FastAPI 0.109+ with Python 3.11+
3. **ORM**: SQLModel 0.0.14+ for type-safe database operations
4. **Database**: Neon Postgres with UUID primary keys, indexed created_at
5. **API Design**: RESTful JSON API with 5 endpoints, proper HTTP status codes
6. **Architecture**: Monorepo with clear frontend/backend separation
7. **State Management**: Server-first with React Server Components, minimal client state
8. **Styling**: Tailwind CSS utility-first approach
9. **Error Handling**: Global exception handlers, user-friendly messages
10. **Testing**: pytest for backend, Vitest for frontend, 80%+ coverage target

---

### Next Steps

Phase 0 (Research) is complete. Ready to proceed to **Phase 1**:
1. Generate `data-model.md` with entity definitions and database schema
2. Generate `contracts/openapi.yaml` with full API specification
3. Generate `quickstart.md` with setup and development instructions
4. Update agent context with technology stack

All technical unknowns are resolved. Implementation can proceed with confidence.
