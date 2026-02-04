# Tasks: Full-Stack Todo Web Application

**Input**: Design documents from `/specs/001-fullstack-todo-web/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/openapi.yaml

**Tests**: This project follows strict TDD (Test-Driven Development). ALL test tasks must be completed BEFORE their corresponding implementation tasks. Tests MUST fail before implementation begins.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story. Each user story represents an independently deliverable increment.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5, US6)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`, `backend/tests/`
- **Frontend**: `frontend/src/`, `frontend/__tests__/`
- Monorepo structure with clear frontend/backend separation

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, directory structure, and basic configuration

- [ ] T001 Create monorepo directory structure (`frontend/`, `backend/`, `specs/`)
- [ ] T002 [P] Initialize backend Python project with `pyproject.toml` and create `backend/requirements.txt`
- [ ] T003 [P] Initialize frontend Next.js 14+ project with TypeScript in `frontend/`
- [ ] T004 [P] Configure backend linting (Black, isort) and create `backend/.flake8`
- [ ] T005 [P] Configure frontend linting (ESLint, Prettier) in `frontend/.eslintrc.json` and `frontend/.prettierrc`
- [ ] T006 [P] Create `.gitignore` for Python, Node.js, and environment files
- [ ] T007 [P] Create environment template files: `backend/.env.example` and `frontend/.env.example`
- [ ] T008 Create root-level `README.md` with project overview and setup instructions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Backend Foundation

- [ ] T009 Install backend dependencies: FastAPI, SQLModel, Uvicorn, Alembic, pytest, python-dotenv in `backend/requirements.txt`
- [ ] T010 Create database configuration in `backend/src/database.py` with engine, session management
- [ ] T011 Create backend configuration loader in `backend/src/config.py` using pydantic-settings
- [ ] T012 Initialize Alembic for migrations in `backend/alembic/` with `alembic init`
- [ ] T013 Configure Alembic `backend/alembic/env.py` to use SQLModel metadata and DATABASE_URL
- [ ] T014 Create initial database migration for `tasks` table in `backend/alembic/versions/001_create_tasks_table.py`
- [ ] T015 Create FastAPI application in `backend/src/main.py` with CORS middleware and startup/shutdown events
- [ ] T016 [P] Create global exception handlers in `backend/src/main.py` for 404, 422, 500 errors
- [ ] T017 [P] Setup pytest configuration in `backend/pytest.ini` and create test fixtures in `backend/tests/conftest.py`

### Frontend Foundation

- [ ] T018 Install frontend dependencies: Next.js 14+, React 18+, TypeScript, Tailwind CSS 3.4+ in `frontend/package.json`
- [ ] T019 Configure Tailwind CSS in `frontend/tailwind.config.ts` and `frontend/postcss.config.js`
- [ ] T020 Create TypeScript configuration in `frontend/tsconfig.json` with strict mode
- [ ] T021 Create root layout in `frontend/src/app/layout.tsx` with metadata and global styles
- [ ] T022 Create global styles with Tailwind imports in `frontend/src/app/globals.css`
- [ ] T023 [P] Create error boundary in `frontend/src/app/error.tsx` for graceful error handling
- [ ] T024 [P] Create loading state in `frontend/src/app/loading.tsx` for suspense fallback
- [ ] T025 [P] Setup Vitest configuration in `frontend/vitest.config.ts` for component testing

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Quick Task Addition (Priority: P1) 🎯 MVP

**Goal**: Enable users to quickly capture tasks by typing a description and submitting it, with immediate feedback and persistent storage.

**Independent Test**: Open application, type "Buy groceries", press Enter or click Add button, verify task appears in list and persists on page refresh.

### Tests for User Story 1 (TDD - Write FIRST, ensure FAIL)

#### Backend Tests

- [ ] T026 [P] [US1] Create unit test for Task model validation in `backend/tests/unit/test_task_model.py` (test empty description fails, whitespace-only fails, valid description passes, description trimming)
- [ ] T027 [P] [US1] Create unit test for TaskCreate schema in `backend/tests/unit/test_task_model.py` (test validation rules)
- [ ] T028 [P] [US1] Create integration test for POST /api/todos endpoint in `backend/tests/integration/test_todos_api.py` (test successful creation returns 201, empty description returns 400, description >500 chars returns 400)
- [ ] T029 [P] [US1] Create integration test for GET /api/todos endpoint in `backend/tests/integration/test_todos_api.py` (test empty list returns [], created tasks appear in list, ordering by created_at DESC)

#### Frontend Tests

- [ ] T030 [P] [US1] Create unit test for TaskInput component in `frontend/src/__tests__/components/TaskInput.test.tsx` (test input disabled when empty, Enter key triggers submission, Add button triggers submission, validation message displays)
- [ ] T031 [P] [US1] Create unit test for API client createTask function in `frontend/src/__tests__/lib/api.test.ts` (test request format, response handling, error handling)

**Checkpoint**: All US1 tests written and FAILING - ready for implementation

### Implementation for User Story 1

#### Backend Implementation

- [ ] T032 [US1] Create Task SQLModel entity in `backend/src/models/task.py` with TaskBase, Task, TaskCreate, TaskUpdate, TaskRead schemas
- [ ] T033 [US1] Create TaskService with create_task and list_tasks methods in `backend/src/services/task_service.py`
- [ ] T034 [US1] Create todos router in `backend/src/routers/todos.py` and register with FastAPI app
- [ ] T035 [US1] Implement POST /api/todos endpoint in `backend/src/routers/todos.py` (validate input, call service, return 201 with Location header)
- [ ] T036 [US1] Implement GET /api/todos endpoint in `backend/src/routers/todos.py` (fetch all tasks ordered by created_at DESC, return 200)
- [ ] T037 [US1] Run backend tests for US1 - verify all tests pass (pytest backend/tests/unit/test_task_model.py backend/tests/integration/test_todos_api.py -v)

#### Frontend Implementation

- [ ] T038 [P] [US1] Create Task TypeScript interfaces in `frontend/src/types/task.ts` (Task, TaskCreateRequest, APIError)
- [ ] T039 [P] [US1] Create API client with createTask and getTasks functions in `frontend/src/lib/api.ts`
- [ ] T040 [US1] Create TaskInput component in `frontend/src/components/TaskInput.tsx` (controlled input, validation, submit on Enter/button, loading state, error display)
- [ ] T041 [US1] Create TaskList component in `frontend/src/components/TaskList.tsx` (fetch and display tasks, empty state, loading state, error handling)
- [ ] T042 [US1] Create EmptyState component in `frontend/src/components/EmptyState.tsx` (friendly message guiding users to add first task)
- [ ] T043 [US1] Implement home page in `frontend/src/app/page.tsx` integrating TaskInput and TaskList components
- [ ] T044 [US1] Run frontend tests for US1 - verify all tests pass (npm test -- TaskInput.test.tsx api.test.ts)

**Checkpoint**: User Story 1 complete and independently functional - users can add tasks and see them persist

---

## Phase 4: User Story 2 - Task Completion Tracking (Priority: P1)

**Goal**: Allow users to mark tasks as complete/incomplete with visual feedback (strikethrough), enabling progress tracking.

**Independent Test**: Create a task, click checkbox to mark complete (task shows strikethrough), uncheck to mark incomplete (strikethrough removed), refresh page to verify status persists.

### Tests for User Story 2 (TDD - Write FIRST, ensure FAIL)

#### Backend Tests

- [ ] T045 [P] [US2] Create unit test for TaskUpdate schema in `backend/tests/unit/test_task_model.py` (test optional is_completed field validation)
- [ ] T046 [P] [US2] Create unit test for TaskService update_task method in `backend/tests/unit/test_task_service.py` (test partial update with is_completed only)
- [ ] T047 [P] [US2] Create integration test for PATCH /api/todos/{id} endpoint in `backend/tests/integration/test_todos_api.py` (test mark complete returns 200, mark incomplete returns 200, invalid UUID returns 400, non-existent task returns 404)

#### Frontend Tests

- [ ] T048 [P] [US2] Create unit test for TaskItem component completion toggle in `frontend/src/__tests__/components/TaskItem.test.tsx` (test checkbox state, strikethrough styling, optimistic update, error rollback)
- [ ] T049 [P] [US2] Create unit test for API client updateTask function in `frontend/src/__tests__/lib/api.test.ts` (test PATCH request with is_completed field)

**Checkpoint**: All US2 tests written and FAILING - ready for implementation

### Implementation for User Story 2

#### Backend Implementation

- [ ] T050 [US2] Implement TaskService update_task method in `backend/src/services/task_service.py` (handle partial updates with COALESCE, return updated task or raise TaskNotFoundError)
- [ ] T051 [US2] Implement PATCH /api/todos/{id} endpoint in `backend/src/routers/todos.py` (validate UUID, call service, return 200 or 404)
- [ ] T052 [US2] Run backend tests for US2 - verify all tests pass (pytest backend/tests/unit/test_task_service.py backend/tests/integration/test_todos_api.py::test_patch_task_completion -v)

#### Frontend Implementation

- [ ] T053 [P] [US2] Add updateTask function to API client in `frontend/src/lib/api.ts` (PATCH request with partial TaskUpdateRequest)
- [ ] T054 [US2] Create TaskItem component in `frontend/src/components/TaskItem.tsx` (checkbox, description display, completion styles, optimistic update, error handling)
- [ ] T055 [US2] Update TaskList component in `frontend/src/components/TaskList.tsx` to render TaskItem components for each task
- [ ] T056 [US2] Add strikethrough and color styling for completed tasks using Tailwind classes in `frontend/src/components/TaskItem.tsx`
- [ ] T057 [US2] Run frontend tests for US2 - verify all tests pass (npm test -- TaskItem.test.tsx)

**Checkpoint**: User Story 2 complete - users can mark tasks complete/incomplete with visual feedback

---

## Phase 5: User Story 3 - Task List Overview (Priority: P1)

**Goal**: Display all tasks in a clean, readable list format with visual distinction between completed and incomplete tasks.

**Independent Test**: Add several tasks with different completion states, verify all display correctly with appropriate visual hierarchy, empty state shows when no tasks exist.

### Tests for User Story 3 (TDD - Write FIRST, ensure FAIL)

#### Backend Tests

- [ ] T058 [P] [US3] Create integration test for GET /api/todos with multiple tasks in `backend/tests/integration/test_todos_api.py` (test ordering by created_at DESC, mixed completion states)
- [ ] T059 [P] [US3] Create unit test for TaskService list_tasks filtering (if implementing) in `backend/tests/unit/test_task_service.py`

#### Frontend Tests

- [ ] T060 [P] [US3] Create integration test for TaskList component with mixed states in `frontend/src/__tests__/components/TaskList.test.tsx` (test rendering multiple tasks, completed vs incomplete visual distinction, empty state rendering)
- [ ] T061 [P] [US3] Create unit test for EmptyState component in `frontend/src/__tests__/components/EmptyState.test.tsx` (test message clarity, call-to-action presence)

**Checkpoint**: All US3 tests written and FAILING - ready for implementation

### Implementation for User Story 3

#### Backend Implementation

- [ ] T062 [US3] Verify TaskService list_tasks returns tasks ordered by created_at DESC in `backend/src/services/task_service.py`
- [ ] T063 [US3] Run backend tests for US3 - verify all tests pass (pytest backend/tests/integration/test_todos_api.py::test_list_tasks_ordering -v)

#### Frontend Implementation

- [ ] T064 [P] [US3] Enhance TaskList component in `frontend/src/components/TaskList.tsx` with proper visual hierarchy (spacing, borders, grouping)
- [ ] T065 [P] [US3] Add loading skeleton in TaskList component for better perceived performance
- [ ] T066 [US3] Implement responsive layout in TaskList using Tailwind responsive classes (sm:, md:, lg:)
- [ ] T067 [US3] Add scroll behavior for long task lists (virtualization if >100 tasks, or smooth scrolling)
- [ ] T068 [US3] Run frontend tests for US3 - verify all tests pass (npm test -- TaskList.test.tsx EmptyState.test.tsx)

**Checkpoint**: User Story 3 complete - users have clear overview of all tasks with proper visual design

---

## Phase 6: User Story 4 - Task Modification (Priority: P2)

**Goal**: Allow users to edit task descriptions after creation by clicking edit button or double-clicking task.

**Independent Test**: Create task, click edit button or double-click, modify text, save (verify update persists), cancel edit (verify original text unchanged).

### Tests for User Story 4 (TDD - Write FIRST, ensure FAIL)

#### Backend Tests

- [ ] T069 [P] [US4] Create unit test for TaskUpdate schema with description field in `backend/tests/unit/test_task_model.py` (test validation, whitespace trimming)
- [ ] T070 [P] [US4] Create integration test for PATCH /api/todos/{id} with description update in `backend/tests/integration/test_todos_api.py` (test successful update returns 200, empty description returns 400, description >500 chars returns 400)

#### Frontend Tests

- [ ] T071 [P] [US4] Create unit test for TaskItem edit mode in `frontend/src/__tests__/components/TaskItem.test.tsx` (test double-click activates edit, edit button activates edit, Escape cancels, Enter saves, validation on save)
- [ ] T072 [P] [US4] Create unit test for API client updateTask with description field in `frontend/src/__tests__/lib/api.test.ts`

**Checkpoint**: All US4 tests written and FAILING - ready for implementation

### Implementation for User Story 4

#### Backend Implementation

- [ ] T073 [US4] Verify TaskService update_task handles description updates in `backend/src/services/task_service.py` (partial update with description validation)
- [ ] T074 [US4] Run backend tests for US4 - verify all tests pass (pytest backend/tests/integration/test_todos_api.py::test_patch_task_description -v)

#### Frontend Implementation

- [ ] T075 [US4] Add edit mode state and handlers to TaskItem component in `frontend/src/components/TaskItem.tsx` (double-click listener, edit button, cancel button, save button)
- [ ] T076 [US4] Implement inline editing UI in TaskItem (replace text with input field, maintain styling, focus input on edit activation)
- [ ] T077 [US4] Add keyboard shortcuts in TaskItem (Enter to save, Escape to cancel, Tab navigation)
- [ ] T078 [US4] Implement client-side validation in TaskItem edit mode (prevent empty, show character count, disable save when invalid)
- [ ] T079 [US4] Add optimistic update with error rollback in TaskItem save handler
- [ ] T080 [US4] Run frontend tests for US4 - verify all tests pass (npm test -- TaskItem.test.tsx --grep edit)

**Checkpoint**: User Story 4 complete - users can edit task descriptions with inline editing

---

## Phase 7: User Story 5 - Task Deletion (Priority: P2)

**Goal**: Enable users to permanently delete tasks with confirmation to prevent accidental deletion.

**Independent Test**: Create task, click delete button, confirm deletion in modal, verify task removed from list and does not reappear on refresh.

### Tests for User Story 5 (TDD - Write FIRST, ensure FAIL)

#### Backend Tests

- [ ] T081 [P] [US5] Create unit test for TaskService delete_task method in `backend/tests/unit/test_task_service.py` (test successful deletion, non-existent task raises error)
- [ ] T082 [P] [US5] Create integration test for DELETE /api/todos/{id} endpoint in `backend/tests/integration/test_todos_api.py` (test successful deletion returns 204, invalid UUID returns 400, non-existent task returns 404)
- [ ] T083 [P] [US5] Create integration test for delete then list in `backend/tests/integration/test_todos_api.py` (verify deleted task does not appear in GET /api/todos)

#### Frontend Tests

- [ ] T084 [P] [US5] Create unit test for TaskItem delete functionality in `frontend/src/__tests__/components/TaskItem.test.tsx` (test delete button click, confirmation modal display, confirm action, cancel action)
- [ ] T085 [P] [US5] Create unit test for API client deleteTask function in `frontend/src/__tests__/lib/api.test.ts` (test DELETE request, 204 response handling)

**Checkpoint**: All US5 tests written and FAILING - ready for implementation

### Implementation for User Story 5

#### Backend Implementation

- [ ] T086 [US5] Implement GET /api/todos/{id} endpoint in `backend/src/routers/todos.py` (fetch single task, return 200 or 404)
- [ ] T087 [US5] Implement TaskService delete_task method in `backend/src/services/task_service.py` (delete by ID, raise TaskNotFoundError if not found)
- [ ] T088 [US5] Implement DELETE /api/todos/{id} endpoint in `backend/src/routers/todos.py` (validate UUID, call service, return 204 or 404)
- [ ] T089 [US5] Run backend tests for US5 - verify all tests pass (pytest backend/tests/unit/test_task_service.py backend/tests/integration/test_todos_api.py::test_delete_task -v)

#### Frontend Implementation

- [ ] T090 [P] [US5] Add deleteTask function to API client in `frontend/src/lib/api.ts` (DELETE request, handle 204 response)
- [ ] T091 [US5] Add delete button to TaskItem component in `frontend/src/components/TaskItem.tsx` (trash icon, confirm modal trigger)
- [ ] T092 [US5] Implement simple confirmation dialog/modal (native confirm or custom modal with confirm/cancel buttons)
- [ ] T093 [US5] Implement optimistic deletion in TaskList (remove from UI immediately, rollback on error)
- [ ] T094 [US5] Handle empty state after deleting last task (TaskList shows EmptyState component)
- [ ] T095 [US5] Run frontend tests for US5 - verify all tests pass (npm test -- TaskItem.test.tsx api.test.ts --grep delete)

**Checkpoint**: User Story 5 complete - users can delete tasks with confirmation

---

## Phase 8: User Story 6 - Responsive Access Across Devices (Priority: P3)

**Goal**: Ensure application works seamlessly across all devices (desktop, tablet, mobile) with appropriate touch targets and layouts.

**Independent Test**: Access application from different screen sizes (320px mobile, 768px tablet, 1920px desktop), verify all core features work, buttons/inputs are appropriately sized for touch.

### Tests for User Story 6 (TDD - Write FIRST, ensure FAIL)

#### Frontend Tests

- [ ] T096 [P] [US6] Create responsive layout test for TaskList in `frontend/src/__tests__/components/TaskList.test.tsx` (test mobile, tablet, desktop viewports)
- [ ] T097 [P] [US6] Create responsive layout test for TaskItem in `frontend/src/__tests__/components/TaskItem.test.tsx` (test touch target sizes, button spacing at different viewports)
- [ ] T098 [P] [US6] Create responsive layout test for TaskInput in `frontend/src/__tests__/components/TaskInput.test.tsx` (test mobile input sizing, button accessibility)

**Checkpoint**: All US6 tests written and FAILING - ready for implementation

### Implementation for User Story 6

#### Frontend Implementation

- [ ] T099 [P] [US6] Add responsive utility classes in `frontend/src/app/globals.css` (touch target sizes, spacing scales)
- [ ] T100 [US6] Implement mobile-first responsive layout in TaskList using Tailwind breakpoints (padding, spacing, max-width)
- [ ] T101 [US6] Implement responsive TaskItem layout (stack edit/delete buttons on mobile, inline on desktop)
- [ ] T102 [US6] Implement responsive TaskInput (full-width on mobile, constrained on desktop, appropriate button sizing)
- [ ] T103 [US6] Add touch-friendly interactions (larger touch targets, adequate spacing, no hover-only features)
- [ ] T104 [US6] Test on actual devices or browser dev tools across breakpoints (320px, 768px, 1024px, 1920px)
- [ ] T105 [US6] Run frontend tests for US6 - verify all tests pass (npm test -- --grep responsive)

**Checkpoint**: User Story 6 complete - application is fully responsive across all devices

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements, documentation, and production readiness

### Code Quality & Cleanup

- [ ] T106 [P] Run backend linter and formatter (black backend/src backend/tests && isort backend/src backend/tests)
- [ ] T107 [P] Run frontend linter and formatter (npm run lint && npm run format in frontend/)
- [ ] T108 [P] Remove any console.log, debugger statements, or commented-out code
- [ ] T109 [P] Verify no TODO or FIXME comments remain in production code
- [ ] T110 Review all error messages for user-friendliness and actionability

### Testing & Quality Assurance

- [ ] T111 Run full backend test suite with coverage (pytest backend/tests --cov=backend/src --cov-report=html --cov-report=term)
- [ ] T112 Verify backend test coverage meets 80%+ target, add tests for gaps if needed
- [ ] T113 Run full frontend test suite with coverage (npm test -- --coverage in frontend/)
- [ ] T114 Verify frontend test coverage meets 70%+ target, add tests for gaps if needed
- [ ] T115 [P] Manual end-to-end testing following quickstart.md instructions
- [ ] T116 [P] Test all edge cases from spec.md (database connection loss, long descriptions, thousands of tasks, etc.)

### Performance & Optimization

- [ ] T117 [P] Verify database indexes are created correctly (idx_tasks_created_at, idx_tasks_is_completed)
- [ ] T118 [P] Test with 1000+ tasks to ensure UI remains performant
- [ ] T119 [P] Verify API response times meet <100ms p95 target using browser dev tools
- [ ] T120 [P] Verify initial page load meets <3s target using Lighthouse or WebPageTest

### Documentation

- [ ] T121 Update root README.md with final setup instructions, architecture overview, and usage examples
- [ ] T122 [P] Document all environment variables in .env.example files with descriptions
- [ ] T123 [P] Verify quickstart.md is accurate and up-to-date with actual implementation
- [ ] T124 [P] Add inline code documentation (docstrings for backend functions, JSDoc comments for frontend utilities)
- [ ] T125 [P] Create API documentation using FastAPI's automatic docs (verify /docs and /redoc endpoints work)

### Production Readiness

- [ ] T126 Configure production environment settings (remove debug mode, set proper CORS origins)
- [ ] T127 [P] Verify all secrets use environment variables, nothing hardcoded
- [ ] T128 [P] Create deployment guide documenting backend deployment (Render/Railway/Vercel) and frontend deployment (Vercel/Netlify)
- [ ] T129 Test production build of frontend (npm run build && npm run start in frontend/)
- [ ] T130 Test backend with production settings (ENVIRONMENT=production)

---

## Dependencies & Execution Order

### Phase Dependencies

1. **Setup (Phase 1)**: No dependencies - can start immediately
2. **Foundational (Phase 2)**: Depends on Setup completion - **BLOCKS all user stories**
3. **User Stories (Phase 3-8)**: All depend on Foundational phase completion
   - **US1 (P1)**: Can start after Foundational - MVP foundation
   - **US2 (P1)**: Can start after Foundational - Independent of US1
   - **US3 (P1)**: Can start after Foundational - Enhances US1+US2
   - **US4 (P2)**: Can start after Foundational - Independent implementation
   - **US5 (P2)**: Can start after Foundational - Independent implementation
   - **US6 (P3)**: Should start after US1-US3 for best testing - Enhances all stories
4. **Polish (Phase 9)**: Depends on all desired user stories being complete

### User Story Dependencies

**Independent Stories** (can implement in any order after Foundational):
- US1 (Quick Task Addition) - Foundation for all CRUD
- US2 (Task Completion Tracking) - Uses US1 components but independently testable
- US3 (Task List Overview) - Enhances US1+US2 display
- US4 (Task Modification) - Adds editing capability
- US5 (Task Deletion) - Adds deletion capability
- US6 (Responsive Access) - Cross-cutting enhancement

**Recommended Order** (by priority):
1. US1 → US2 → US3 (All P1 - Core functionality)
2. US4 → US5 (Both P2 - Enhanced functionality)
3. US6 (P3 - Polish)

### Within Each User Story (TDD Cycle)

1. **Tests FIRST**: Write all test tasks for the story, ensure they FAIL
2. **Backend Implementation**: Models → Services → Endpoints → Run tests (must pass)
3. **Frontend Implementation**: Types → API Client → Components → Run tests (must pass)
4. **Integration**: Connect frontend to backend, verify end-to-end functionality
5. **Story Complete**: Checkpoint reached, story independently testable

### Parallel Opportunities

**Setup Phase (Phase 1)**:
- T002 (backend setup) || T003 (frontend setup)
- T004 (backend linting) || T005 (frontend linting)
- T006 (gitignore) || T007 (env templates) || T008 (README)

**Foundational Phase (Phase 2)**:
- Backend tasks (T009-T017) can run in parallel with Frontend tasks (T018-T025)
- Within backend: T016 (exception handlers) || T017 (pytest config)
- Within frontend: T023 (error boundary) || T024 (loading state) || T025 (vitest config)

**User Story Tests** (within each story):
- All test tasks marked [P] within a story can run in parallel
- Example US1: T026 || T027 || T028 || T029 (backend tests), T030 || T031 (frontend tests)

**User Story Implementation** (within each story):
- Backend models marked [P] can run in parallel
- Frontend components marked [P] can run in parallel
- Different user stories can be worked on in parallel (after Foundational complete)

---

## Parallel Example: User Story 1

```bash
# After Foundational phase complete, launch all US1 tests in parallel:
Task T026: Unit test for Task model validation (backend)
Task T027: Unit test for TaskCreate schema (backend)
Task T028: Integration test for POST /api/todos (backend)
Task T029: Integration test for GET /api/todos (backend)
Task T030: Unit test for TaskInput component (frontend)
Task T031: Unit test for API client createTask (frontend)

# Verify all tests FAIL, then launch parallel implementation tasks:
Task T038: Create Task TypeScript interfaces (frontend)
Task T039: Create API client functions (frontend)

# Then sequential tasks:
Task T032 → T033 → T034 → T035 → T036 → T037 (backend chain)
Task T040 → T041 → T042 → T043 → T044 (frontend chain)
```

---

## Parallel Example: Multiple User Stories

```bash
# After Foundational complete, if multiple developers available:
Developer A: Complete US1 (Tasks T026-T044)
Developer B: Complete US2 (Tasks T045-T057)
Developer C: Complete US4 (Tasks T069-T080)

# Each developer follows TDD within their story:
# 1. Write tests → ensure FAIL
# 2. Implement backend → tests pass
# 3. Implement frontend → tests pass
# 4. Integration test
# 5. Story complete and independently functional
```

---

## Implementation Strategy

### MVP First (User Story 1-3 Only)

**Minimum Viable Product Path**:

1. Complete Phase 1: Setup (Tasks T001-T008)
2. Complete Phase 2: Foundational (Tasks T009-T025) - **CRITICAL BLOCKER**
3. Complete Phase 3: US1 - Quick Task Addition (Tasks T026-T044)
4. **STOP and VALIDATE**: Test US1 independently (can add tasks, they persist)
5. Complete Phase 4: US2 - Task Completion Tracking (Tasks T045-T057)
6. **STOP and VALIDATE**: Test US1+US2 together (add tasks, mark complete)
7. Complete Phase 5: US3 - Task List Overview (Tasks T058-T068)
8. **STOP and VALIDATE**: Test full MVP (add, view, complete with good UX)
9. **Deploy MVP** or proceed to enhanced features (US4, US5, US6)

**MVP Delivers**:
- Users can add tasks ✅
- Users can view all tasks ✅
- Users can mark tasks complete ✅
- Data persists in database ✅
- Clean, functional UI ✅

### Incremental Delivery

**Delivery Milestones**:

1. **Foundation** (Phases 1-2): Project structure + infrastructure ready
2. **MVP** (Phases 3-5): Core task management functional → **Deploy v1.0**
3. **Enhanced** (Phases 6-7): Add edit and delete → **Deploy v1.1**
4. **Polished** (Phases 8-9): Responsive + production-ready → **Deploy v1.2**

Each milestone is independently deployable and adds value without breaking previous functionality.

### Parallel Team Strategy

**With 3 Developers**:

1. **All Together**: Complete Setup (Phase 1) and Foundational (Phase 2)
2. **Split User Stories** (after Foundational):
   - Dev A: US1 (T026-T044) - Quick Task Addition
   - Dev B: US2 (T045-T057) + US3 (T058-T068) - Completion + Overview
   - Dev C: US4 (T069-T080) + US5 (T081-T095) - Edit + Delete
3. **Reconvene**: US6 (T096-T105) - Responsive (requires all features complete)
4. **All Together**: Polish (Phase 9) - Final QA and deployment prep

Each developer owns their user story end-to-end (tests + backend + frontend), ensuring story independence.

---

## TDD Workflow Reminders

**For Every Task Marked "Test"**:

1. Write the test (unit or integration)
2. Run the test → **MUST FAIL** (proves test is actually testing something)
3. Take screenshot or note of failure
4. Mark test task complete
5. Proceed to implementation task

**For Every Implementation Task**:

1. Implement minimum code to pass the test
2. Run tests → **MUST PASS**
3. Refactor if needed (while keeping tests green)
4. Mark implementation task complete
5. Commit changes with descriptive message

**Red-Green-Refactor Cycle**:
- 🔴 **Red**: Test fails (proves it's testing correctly)
- 🟢 **Green**: Implementation passes test (proves code works)
- 🔵 **Refactor**: Clean up code (while tests stay green)

---

## Task Summary

**Total Tasks**: 130

**By Phase**:
- Phase 1 (Setup): 8 tasks
- Phase 2 (Foundational): 17 tasks (Backend: 9, Frontend: 8)
- Phase 3 (US1 - Quick Task Addition): 19 tasks (Tests: 6, Backend: 6, Frontend: 7)
- Phase 4 (US2 - Completion Tracking): 13 tasks (Tests: 5, Backend: 3, Frontend: 5)
- Phase 5 (US3 - Task List Overview): 11 tasks (Tests: 4, Backend: 2, Frontend: 5)
- Phase 6 (US4 - Task Modification): 12 tasks (Tests: 4, Backend: 2, Frontend: 6)
- Phase 7 (US5 - Task Deletion): 15 tasks (Tests: 5, Backend: 4, Frontend: 6)
- Phase 8 (US6 - Responsive Access): 10 tasks (Tests: 3, Frontend: 7)
- Phase 9 (Polish & Cross-Cutting): 25 tasks

**By User Story**:
- US1 (P1): 19 tasks
- US2 (P1): 13 tasks
- US3 (P1): 11 tasks
- US4 (P2): 12 tasks
- US5 (P2): 15 tasks
- US6 (P3): 10 tasks

**Parallel Opportunities**: 45 tasks marked [P] can run in parallel with other tasks

**Test Tasks**: 27 test tasks (must complete and FAIL before implementation)

**MVP Scope** (Phases 1-5): 68 tasks covering Setup, Foundational, US1, US2, US3

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- **TDD is MANDATORY**: Tests written FIRST, must FAIL before implementation
- Verify tests fail before implementing (proves test works)
- Verify tests pass after implementing (proves implementation works)
- Commit after each task or logical group of related tasks
- Stop at any checkpoint to validate story independently
- Backend uses pytest, frontend uses Vitest + React Testing Library
- Target: 80%+ backend coverage, 70%+ frontend coverage
- All tasks include exact file paths for clarity
- Dependencies clearly marked (sequential vs parallel)
- MVP delivers core value (US1-US3), enhanced features follow (US4-US6)
