# Research: In-Memory Console Todo Application

**Feature**: `001-console-todo-app`
**Date**: 2026-01-02
**Phase**: Phase 0 - Technology Research and Decision Documentation

## Purpose

Document technology choices, best practices, and architectural patterns for building a Python in-memory CLI todo application following the Constitution's Phase-Aware Architecture and Simplicity principles.

---

## Research Areas

### 1. Python Version and Compatibility

**Decision**: Use Python 3.13+ with backward compatibility to Python 3.8

**Rationale**:
- User specified Python 3.13+ in requirements
- Constitution mandates Python 3.8+ for maximum compatibility
- Modern Python (3.8+) provides:
  - Type hints for better code documentation
  - Dataclasses (built-in since 3.7) for model definition
  - `typing` module enhancements for static analysis
  - `__future__` annotations for forward compatibility

**Alternatives Considered**:
- Python 3.7: Lacks some typing improvements, nearing EOL
- Python 3.10+: Pattern matching unavailable in 3.8-3.9, reduces compatibility
- Python 2.7: Deprecated, not an option

**Best Practices**:
- Use type hints throughout (`from __future__ import annotations`)
- Test on Python 3.8 minimum to ensure compatibility claims
- Use dataclasses for model definitions (clean, built-in)
- Avoid f-strings if targeting <3.6, but 3.8+ baseline makes this safe

---

### 2. Project Structure and Module Organization

**Decision**: Modular structure with Models/Services/CLI/Lib separation

**Rationale**:
- Constitution Principle IV: Modular Implementation
- Separation of concerns enables independent testing
- Clear boundaries for future migration to FastAPI (Phase II)
- Standard Python package structure with `src/` layout

**Structure Pattern**:
```
src/
├── models/      # Data structures (Todo dataclass)
├── services/    # Business logic (TodoManager)
├── cli/         # User interface (menu, handlers)
└── lib/         # Utilities (validators, formatters)
```

**Alternatives Considered**:
- Flat structure: Poor organization, hard to maintain, violates modular principle
- Single file: Simple but doesn't scale, hard to test, no separation of concerns
- Clean Architecture layers: Over-engineering for Phase I (violates YAGNI)

**Best Practices**:
- Each module has `__init__.py` for package imports
- Entry point at `src/__main__.py` for `python -m src` execution
- Test structure mirrors `src/` structure for clarity
- Use relative imports within package, absolute from tests

---

### 3. Data Storage Pattern

**Decision**: In-memory list-based storage with TodoManager service class

**Rationale**:
- Constitution mandates in-memory only (no persistence)
- Python list provides O(1) append, O(n) search by ID
- TodoManager encapsulates storage and provides CRUD interface
- Simple, testable, meets all performance requirements

**Storage Design**:
- `TodoManager` maintains `List[Todo]` internally
- Auto-increment ID counter for unique todo IDs
- Sequential IDs starting from 1 (user-friendly)
- No need for UUID or hash-based IDs in Phase I

**Alternatives Considered**:
- Dictionary storage (id → todo): More complex, no ordering guarantee
- SQLite in-memory: Violates "zero external dependencies" (sqlite3 is stdlib but adds unnecessary complexity)
- Global variables: Poor testability, violates modular principle

**Best Practices**:
- TodoManager owns the todo list (encapsulation)
- Provide methods: add(), get_all(), get_by_id(), update(), delete(), mark_complete()
- Return copies of todos to prevent external mutation
- Use defensive copying where appropriate

---

### 4. Data Model Design

**Decision**: Use Python `@dataclass` for Todo model with validation

**Rationale**:
- Dataclasses provide clean syntax with minimal boilerplate
- Built-in `__init__`, `__repr__`, `__eq__` methods
- Supports type hints for IDE autocomplete and static analysis
- Easy to extend with `__post_init__` for validation
- Directly maps to Pydantic models in Phase II (FastAPI)

**Todo Model**:
```python
@dataclass
class Todo:
    id: int
    title: str
    completed: bool = False
    category: Optional[str] = None
    priority: str = "medium"
    created_at: datetime = field(default_factory=datetime.now)
```

**Alternatives Considered**:
- `namedtuple`: Immutable, less flexible, no default values
- Plain class: More boilerplate, no built-in features
- `typing.TypedDict`: Runtime dict, no IDE support, less safe

**Best Practices**:
- Use `field(default_factory=...)` for mutable defaults
- Add `__post_init__` for validation (e.g., title not empty)
- Use `Optional[T]` for nullable fields
- Provide `from_dict()` and `to_dict()` methods for future serialization

---

### 5. CLI Interface Pattern

**Decision**: Menu-driven interface with numbered options and input prompts

**Rationale**:
- User-friendly for non-technical users (spec requirement SC-007)
- Clear, self-documenting interface (no need to remember commands)
- Easy to extend with new options
- Standard pattern for console applications

**Menu Flow**:
1. Display welcome message (with data persistence warning)
2. Show main menu with numbered options
3. Read user choice
4. Dispatch to appropriate handler
5. Display result/feedback
6. Return to main menu (loop)

**Alternatives Considered**:
- Command-line arguments (e.g., `todo add "Buy milk"`): Less interactive, violates menu requirement
- REPL-style (e.g., `>>> add Buy milk`): More complex parsing, less intuitive
- Natural language: Over-engineering for Phase I, violates YAGNI

**Best Practices**:
- Clear menu numbering (1-9 for options, 0 for exit)
- Show status line (e.g., "3 todos | 1 completed")
- Confirm destructive actions (delete)
- Clear screen between operations (optional, platform-dependent)
- Handle Ctrl+C gracefully (KeyboardInterrupt → exit)

---

### 6. Input Validation Strategy

**Decision**: Validation layer at CLI boundary using dedicated validators

**Rationale**:
- Constitution Principle V: Input Validation & Error Handling
- Validate early (fail fast at input layer)
- Reusable validation functions in `lib/validators.py`
- Clear error messages for each validation failure

**Validation Points**:
- Menu choice: Must be valid number in range
- Todo ID: Must be positive integer, must exist in manager
- Todo title: Must not be empty, reasonable length
- Priority: Must be in ["high", "medium", "low"]
- Category: Any non-empty string (optional)

**Alternatives Considered**:
- Validation in models: Couples data to validation logic
- Validation in services: Services assume clean input from CLI
- No validation: Violates constitution, poor UX

**Best Practices**:
- Return `(valid: bool, error_message: str)` tuples
- Use type guards for runtime type checking
- Provide helpful error messages (e.g., "Invalid choice. Please enter 1-7")
- Handle edge cases (empty input, whitespace, special characters)

---

### 7. Error Handling Pattern

**Decision**: Return-based error handling with `Optional` and tuple returns

**Rationale**:
- Simple, Pythonic approach without exceptions for flow control
- Exceptions reserved for truly exceptional cases (programming errors)
- Clear success/failure paths in code
- Easy to test both paths

**Error Handling Patterns**:
- Services return `Optional[Todo]` or `List[Todo]`
- Validators return `(bool, str)` tuples
- CLI handlers check results and display appropriate messages

**Alternatives Considered**:
- Exception-based flow control: Expensive, harder to read
- Result/Either monad: Over-engineering for Python, violates YAGNI
- Status codes: Less Pythonic, requires documentation

**Best Practices**:
- Use `Optional[T]` for operations that may fail (get_by_id)
- Check `if result is None:` for failures
- Always provide user-friendly error messages
- Log errors to console (no file logging in Phase I)

---

### 8. Testing Strategy

**Decision**: Three-tier testing with pytest (contract, unit, integration)

**Rationale**:
- Constitution Principle II: Test-First Development (NON-NEGOTIABLE)
- Comprehensive coverage at multiple levels
- Contract tests validate data model contracts
- Unit tests verify individual function behavior
- Integration tests validate user story acceptance criteria

**Test Organization**:
- `tests/contract/`: Todo model validation, immutability checks
- `tests/unit/`: TodoManager methods, validators, formatters
- `tests/integration/`: User story flows (P1-P4), end-to-end scenarios

**Alternatives Considered**:
- unittest (stdlib): More verbose, less readable than pytest
- doctest: Good for examples, poor for comprehensive tests
- No tests: Violates constitution (non-negotiable)

**Best Practices**:
- One test file per module under test
- Use `pytest.parametrize` for multiple test cases
- Use fixtures for common setup (TodoManager instance)
- Test both happy paths and error paths
- Integration tests use no mocks (test real flow)

---

### 9. Development Workflow Tools

**Decision**: UV for package management, pytest for testing, mypy for type checking (optional)

**Rationale**:
- UV specified in requirements (fast, modern Python package manager)
- pytest is industry standard for Python testing
- mypy provides static type checking (optional, aids development)
- No linting required (YAGNI for Phase I, can add later)

**UV Benefits**:
- Fast dependency resolution
- `pyproject.toml` configuration
- Virtual environment management
- Compatible with pip ecosystem

**Alternatives Considered**:
- pip + venv: Slower, manual environment management
- Poetry: Feature-rich but overkill for simple project
- Conda: Heavier, more suited for data science

**Best Practices**:
- Define project in `pyproject.toml`
- Lock dependencies (UV handles this)
- Use `uv run` for executing code
- Use `uv run pytest` for running tests

---

### 10. User Experience Design

**Decision**: Friendly, conversational menu with visual feedback

**Rationale**:
- Spec success criteria SC-007: Self-explanatory interface
- Console apps need extra attention to UX (no graphics)
- Visual indicators improve usability (✓ for complete, ✗ for incomplete)
- Status line provides context (todo count, completion stats)

**UX Elements**:
- Welcome message explaining in-memory nature
- Clear menu with descriptions (not just "1. Add")
- Status indicators (✓ ✗ or [X] [ ] for completion)
- Confirmation messages ("✓ Todo added successfully!")
- Friendly error messages ("Todo not found. Please check the ID.")
- Progress feedback (e.g., "3 of 5 completed")

**Alternatives Considered**:
- Minimal output: Poor UX, violates self-explanatory requirement
- Colored output: Platform-dependent, adds complexity
- ASCII art: Distracting, unprofessional

**Best Practices**:
- Use emojis sparingly (may not render on all terminals)
- Keep output concise (80-character width)
- Show relative timestamps ("Created 2 minutes ago") for better UX (future enhancement)
- Provide "no todos yet" message instead of empty list

---

## Summary of Key Decisions

| Area | Decision | Rationale |
|------|----------|-----------|
| Python Version | 3.13+ (compatible to 3.8) | User requirement + Constitution compatibility |
| Data Model | `@dataclass` for Todo | Clean, Pythonic, extensible to Phase II |
| Storage | In-memory list in TodoManager | Simple, fast, meets requirements |
| CLI Pattern | Menu-driven numbered options | User-friendly, self-documenting |
| Validation | CLI boundary validation layer | Fail fast, clear errors, reusable |
| Error Handling | `Optional` and tuple returns | Simple, testable, Pythonic |
| Testing | pytest with 3 tiers | TDD requirement, comprehensive coverage |
| Package Manager | UV | User specified, modern, fast |
| Module Structure | Models/Services/CLI/Lib | Constitution mandates modular design |
| UX Design | Friendly menu with feedback | Self-explanatory requirement |

---

## Open Questions (Resolved)

All technical decisions have been finalized. No open questions remaining. Proceed to Phase 1 (Design).

---

**Research Status**: ✅ COMPLETE

All unknowns resolved. Ready for Phase 1 design artifacts (data-model.md, contracts/, quickstart.md).