# Tasks: In-Memory Console Todo Application

**Input**: Design documents from `/specs/001-console-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/cli-interface.md

**Tests**: Test tasks included below (TDD workflow enforced per Constitution Principle II)

**Organization**: Tasks grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below follow plan.md structure

---

## Phase 1: Setup (Shared Infrastructure) ✅ COMPLETE

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directory structure (src/, tests/, specs/)
- [X] T002 Initialize pyproject.toml with UV configuration for Python 3.13+
- [X] T003 [P] Create src/__init__.py and src/__main__.py entry point
- [X] T004 [P] Create all module __init__.py files (models/, services/, cli/, lib/)
- [X] T005 [P] Create tests directory structure (contract/, integration/, unit/)
- [X] T006 [P] Create .gitignore for Python project (\_\_pycache\_\_, .venv/, .pytest_cache/)
- [X] T007 [P] Create README.md with project overview and quick-start instructions

---

## Phase 2: Foundational (Blocking Prerequisites) ✅ COMPLETE

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T008 Create Todo dataclass in src/models/todo.py with all 6 attributes
- [X] T009 Add \_\_post_init\_\_ validation to Todo dataclass (title, priority, category rules)
- [X] T010 [P] Add to_dict() and from_dict() methods to Todo class
- [X] T011 Create TodoManager class skeleton in src/services/todo_manager.py
- [X] T012 [P] Add _todos list and _next_id counter to TodoManager \_\_init\_\_
- [X] T013 [P] Create input validation utilities in src/lib/validators.py
- [X] T014 [P] Create display formatting utilities in src/lib/formatters.py

**Checkpoint**: ✅ Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - View and Add Basic Todos (Priority: P1) 🎯 MVP

**Goal**: Users can add todos and view their list - delivers core value proposition

**Independent Test**: Launch app, add 2-3 todos with different titles, view list, confirm todos appear with correct details (ID, title, status)

### Tests for User Story 1 (TDD: Write tests FIRST, ensure they FAIL) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T015 [P] [US1] Contract test for Todo model validation in tests/contract/test_todo_model.py
- [ ] T016 [P] [US1] Unit test for TodoManager.add() in tests/unit/test_todo_manager.py
- [ ] T017 [P] [US1] Unit test for TodoManager.get_all() in tests/unit/test_todo_manager.py
- [ ] T018 [P] [US1] Integration test for add/view workflow in tests/integration/test_p1_add_view.py

### Implementation for User Story 1

- [ ] T019 [P] [US1] Implement TodoManager.add(title, category, priority) in src/services/todo_manager.py
- [ ] T020 [P] [US1] Implement TodoManager.get_all() in src/services/todo_manager.py
- [ ] T021 [P] [US1] Implement TodoManager.count() in src/services/todo_manager.py
- [ ] T022 [US1] Create menu display function in src/cli/menu.py (depends on T021 for status line)
- [ ] T023 [P] [US1] Create add_todo_handler() in src/cli/handlers.py
- [ ] T024 [P] [US1] Create view_todos_handler() in src/cli/handlers.py
- [ ] T025 [P] [US1] Implement format_todo_list() in src/lib/formatters.py
- [ ] T026 [P] [US1] Implement validate_title() in src/lib/validators.py
- [ ] T027 [P] [US1] Implement validate_priority() in src/lib/validators.py
- [ ] T028 [US1] Wire up menu options 1 (View) and 2 (Add) in src/__main__.py main loop
- [ ] T029 [US1] Add welcome screen with data persistence warning in src/__main__.py
- [ ] T030 [US1] Add graceful exit handler (Ctrl+C) in src/__main__.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently (MVP COMPLETE!)

---

## Phase 4: User Story 2 - Mark Todos Complete/Incomplete (Priority: P2)

**Goal**: Users can track progress by marking todos as complete or incomplete

**Independent Test**: Add several todos, mark some complete, view list to confirm status changes ([ ] vs [X]), toggle status back to incomplete

### Tests for User Story 2 (TDD: Write tests FIRST) ⚠️

- [ ] T031 [P] [US2] Unit test for TodoManager.mark_complete() in tests/unit/test_todo_manager.py
- [ ] T032 [P] [US2] Unit test for TodoManager.count_completed() in tests/unit/test_todo_manager.py
- [ ] T033 [P] [US2] Integration test for mark complete workflow in tests/integration/test_p2_complete.py

### Implementation for User Story 2

- [ ] T034 [P] [US2] Implement TodoManager.mark_complete(id, completed) in src/services/todo_manager.py
- [ ] T035 [P] [US2] Implement TodoManager.count_completed() in src/services/todo_manager.py
- [ ] T036 [P] [US2] Create mark_complete_handler() in src/cli/handlers.py
- [ ] T037 [P] [US2] Update format_todo_list() to show [ ] vs [X] in src/lib/formatters.py
- [ ] T038 [P] [US2] Implement validate_todo_id() in src/lib/validators.py
- [ ] T039 [US2] Wire up menu option 3 (Mark complete/incomplete) in src/__main__.py
- [ ] T040 [US2] Update status line in menu to show completed count (depends on T035)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update and Delete Todos (Priority: P3)

**Goal**: Users can edit todo titles and remove tasks they no longer need (full CRUD complete)

**Independent Test**: Add todos, update titles, delete specific todos by ID, confirm changes reflected in list

### Tests for User Story 3 (TDD: Write tests FIRST) ⚠️

- [ ] T041 [P] [US3] Unit test for TodoManager.get_by_id() in tests/unit/test_todo_manager.py
- [ ] T042 [P] [US3] Unit test for TodoManager.update() in tests/unit/test_todo_manager.py
- [ ] T043 [P] [US3] Unit test for TodoManager.delete() in tests/unit/test_todo_manager.py
- [ ] T044 [P] [US3] Integration test for update/delete workflow in tests/integration/test_p3_update_delete.py

### Implementation for User Story 3

- [ ] T045 [P] [US3] Implement TodoManager.get_by_id(id) in src/services/todo_manager.py
- [ ] T046 [P] [US3] Implement TodoManager.update(id, title, category, priority) in src/services/todo_manager.py
- [ ] T047 [P] [US3] Implement TodoManager.delete(id) in src/services/todo_manager.py
- [ ] T048 [P] [US3] Create update_todo_handler() in src/cli/handlers.py
- [ ] T049 [P] [US3] Create delete_todo_handler() with confirmation in src/cli/handlers.py
- [ ] T050 [P] [US3] Implement validate_confirmation() in src/lib/validators.py
- [ ] T051 [US3] Wire up menu options 4 (Update) and 5 (Delete) in src/__main__.py

**Checkpoint**: All core CRUD operations complete - full todo manager functionality

---

## Phase 6: User Story 4 - Categorize and Prioritize Todos (Priority: P4)

**Goal**: Users can organize todos with categories and priorities, and filter/sort accordingly

**Independent Test**: Add todos with various categories ("work", "personal") and priorities ("high", "low"), view filtered lists, confirm organization works

### Tests for User Story 4 (TDD: Write tests FIRST) ⚠️

- [ ] T052 [P] [US4] Unit test for TodoManager.get_by_category() in tests/unit/test_todo_manager.py
- [ ] T053 [P] [US4] Unit test for TodoManager.get_by_priority() in tests/unit/test_todo_manager.py
- [ ] T054 [P] [US4] Integration test for filter workflow in tests/integration/test_p4_categorize.py

### Implementation for User Story 4

- [ ] T055 [P] [US4] Implement TodoManager.get_by_category(category) in src/services/todo_manager.py
- [ ] T056 [P] [US4] Implement TodoManager.get_by_priority(priority) in src/services/todo_manager.py
- [ ] T057 [P] [US4] Create filter_todos_handler() with sub-menu in src/cli/handlers.py
- [ ] T058 [P] [US4] Implement validate_category() in src/lib/validators.py
- [ ] T059 [US4] Wire up menu option 6 (Filter by category/priority) in src/__main__.py

**Checkpoint**: All user stories complete - enhanced todo manager with professional features

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final validation

- [ ] T060 [P] Add comprehensive docstrings to all public functions/classes
- [ ] T061 [P] Add type hints throughout codebase (models, services, cli, lib)
- [ ] T062 [P] Create unit tests for validators in tests/unit/test_validators.py
- [ ] T063 [P] Create unit tests for formatters in tests/unit/test_formatters.py
- [ ] T064 Run full test suite and ensure 100% pass rate
- [ ] T065 Test with 1000+ todos to validate performance (SC-005: <2s display time)
- [ ] T066 Manual testing of all 8 edge cases from spec.md
- [ ] T067 [P] Update README.md with complete usage instructions and examples
- [ ] T068 Verify all success criteria (SC-001 through SC-010) are met
- [ ] T069 Final constitution compliance check (all 7 principles validated)
- [ ] T070 Create quickstart validation script per quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds on Todo model but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Uses existing TodoManager structure
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Optional enhancement, no dependencies

### Within Each User Story

- **Tests FIRST** (TDD mandate): Write and run tests, ensure they FAIL
- Models before services (Todo dataclass → TodoManager methods)
- Services before CLI handlers (TodoManager → handlers)
- Handlers before main loop wiring (handlers → menu integration)
- Story complete before moving to next priority

### Parallel Opportunities

- **Setup tasks** marked [P] can run in parallel (T003-T007)
- **Foundational tasks** marked [P] can run in parallel within Phase 2 (T010, T012, T013, T014)
- **Once Foundational completes**, all user stories can start in parallel (different teams can work US1-US4 simultaneously)
- **Within each story**, all [P] tasks can run in parallel:
  - All tests for a story can be written in parallel
  - Models/services/handlers for a story can be developed in parallel after tests
- **Polish tasks** marked [P] can run in parallel (T060-T063, T067)

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (TDD: write these FIRST):
Task T015: Contract test for Todo model
Task T016: Unit test for TodoManager.add()
Task T017: Unit test for TodoManager.get_all()
Task T018: Integration test for add/view workflow

# After tests written and FAILING, launch implementation tasks in parallel:
Task T019: Implement TodoManager.add()
Task T020: Implement TodoManager.get_all()
Task T021: Implement TodoManager.count()
Task T023: Create add_todo_handler()
Task T024: Create view_todos_handler()
Task T025: Implement format_todo_list()
Task T026: Implement validate_title()
Task T027: Implement validate_priority()

# Sequential tasks (depend on parallel tasks completing):
Task T022: Create menu display (depends on T021)
Task T028: Wire up menu options (depends on T023, T024)
Task T029: Add welcome screen (depends on T028)
Task T030: Add exit handler (depends on T028)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T007)
2. Complete Phase 2: Foundational (T008-T014) - CRITICAL GATE
3. Complete Phase 3: User Story 1 (T015-T030)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deliverable: Working todo app with add/view functionality

**This is the Minimum Viable Product** - delivers immediate value as a basic task tracker.

### Incremental Delivery (Recommended)

1. **MVP (P1)**: Complete Phase 1 + Phase 2 + Phase 3 → Deploy/Demo
   - Users can add and view todos
   - Validates core architecture
   - Gets early feedback

2. **Enhanced (P1+P2)**: Add Phase 4 → Deploy/Demo
   - Users can mark todos complete/incomplete
   - Adds progress tracking
   - Increases user satisfaction

3. **Full CRUD (P1+P2+P3)**: Add Phase 5 → Deploy/Demo
   - Users can update and delete todos
   - Complete task lifecycle management
   - Production-ready core functionality

4. **Professional (P1+P2+P3+P4)**: Add Phase 6 → Deploy/Demo
   - Users can categorize and filter todos
   - Professional-grade organization
   - Complete feature set

5. **Polished (All)**: Add Phase 7 → Final Release
   - Documentation complete
   - All tests passing
   - Performance validated
   - Constitution compliant

### Parallel Team Strategy

With multiple developers:

1. **Team completes Setup + Foundational together** (T001-T014)
2. **Once Foundational is done**:
   - Developer A: User Story 1 (T015-T030)
   - Developer B: User Story 2 (T031-T040)
   - Developer C: User Story 3 (T041-T051)
   - Developer D: User Story 4 (T052-T059)
3. **Stories complete and integrate independently**
4. **Team completes Polish together** (T060-T070)

---

## Task Count Summary

| Phase | Task Range | Count | Can Parallelize |
|-------|-----------|-------|-----------------|
| Setup | T001-T007 | 7 | Yes (5 tasks) |
| Foundational | T008-T014 | 7 | Yes (4 tasks) |
| User Story 1 (P1) | T015-T030 | 16 | Yes (12 tasks) |
| User Story 2 (P2) | T031-T040 | 10 | Yes (7 tasks) |
| User Story 3 (P3) | T041-T051 | 11 | Yes (7 tasks) |
| User Story 4 (P4) | T052-T059 | 8 | Yes (5 tasks) |
| Polish | T060-T070 | 11 | Yes (4 tasks) |
| **TOTAL** | T001-T070 | **70 tasks** | **44 parallelizable** |

**Test Tasks**: 14 total (T015-T018, T031-T033, T041-T044, T052-T054)
**Implementation Tasks**: 56 total (all others)

**MVP Scope** (User Story 1 only): 30 tasks (T001-T030)
**Full Feature Set** (All User Stories): 59 tasks (T001-T059)
**Production Ready** (Including Polish): 70 tasks (T001-T070)

---

## Notes

- **[P] tasks** = different files, no dependencies - can run in parallel
- **[Story] label** maps task to specific user story for traceability
- **Each user story is independently completable and testable**
- **TDD Mandate**: Write tests FIRST (T015-T018, T031-T033, T041-T044, T052-T054), ensure they FAIL, THEN implement
- **Verify tests fail before implementing** (Constitution Principle II: NON-NEGOTIABLE)
- **Commit after each task or logical group** for clean history
- **Stop at any checkpoint to validate story independently**
- **Avoid**: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## TDD Workflow Reminder (NON-NEGOTIABLE)

Per Constitution Principle II, ALL implementation MUST follow strict TDD:

1. **RED**: Write test, run test, **ensure it FAILS**
2. **Get user approval**: Show failing test output
3. **GREEN**: Implement minimum code to pass test
4. **REFACTOR**: Improve code quality while keeping tests green
5. **Repeat** for next task

**Example for T015-T019**:
```bash
# 1. RED: Write contract test for Todo model (T015)
# Run: pytest tests/contract/test_todo_model.py
# Expected: FAIL (Todo class doesn't exist yet)

# 2. Get approval from user to proceed

# 3. GREEN: Implement Todo dataclass (T008, T009)
# Run: pytest tests/contract/test_todo_model.py
# Expected: PASS

# 4. REFACTOR: Clean up validation logic if needed
# Run: pytest tests/contract/test_todo_model.py
# Expected: Still PASS

# Repeat for T016-T030...
```

**Never write implementation before tests fail!**

---

**Tasks Status**: ✅ COMPLETE - Ready for `/sp.implement` command

**Next Command**: `/sp.implement` to execute tasks following TDD workflow
