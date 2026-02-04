# Data Model: In-Memory Console Todo Application

**Feature**: `001-console-todo-app`
**Date**: 2026-01-02
**Phase**: Phase 1 - Data Model Design

## Purpose

Define the data structures, entities, and their relationships for the in-memory todo application. This model serves as the contract between layers and provides the foundation for Phase II database migration.

---

## Core Entities

### Todo

Represents a single task item with full lifecycle support (create, update, complete, delete).

**Attributes**:

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `id` | `int` | Yes | Auto-generated | Unique identifier, sequential starting from 1 |
| `title` | `str` | Yes | - | Task description, user-provided, 1-500 characters |
| `completed` | `bool` | Yes | `False` | Completion status (True = done, False = pending) |
| `category` | `Optional[str]` | No | `None` | Optional grouping label (e.g., "work", "personal") |
| `priority` | `str` | Yes | `"medium"` | Priority level: "high", "medium", or "low" |
| `created_at` | `datetime` | Yes | Auto-generated | Timestamp when todo was created |

**Validation Rules**:

1. **id**: Must be positive integer, unique within the session, immutable after creation
2. **title**: Must not be empty after stripping whitespace, max length 500 characters
3. **completed**: Boolean only (True/False)
4. **category**: If provided, must be non-empty string after stripping, max 50 characters, lowercase normalized
5. **priority**: Must be exactly one of ["high", "medium", "low"], case-insensitive input normalized to lowercase
6. **created_at**: Automatically set on creation, immutable, timezone-naive (assumes local time)

**State Transitions**:

```
[Created] ---> completed = False (initial state)
   |
   v
[Incomplete] <---> [Complete]
   |                   |
   |                   |
[Updated]          [Updated]
   |                   |
   v                   v
[Deleted] <-------- [Deleted]
```

**Invariants**:
- Once created, `id` never changes
- `created_at` never changes
- All state transitions preserve `id` and `created_at`
- `completed` can toggle freely between True/False
- `title`, `category`, and `priority` can be updated at any time

---

## Python Implementation Contract

### Todo Dataclass

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Todo:
    """
    Represents a single todo item.

    Attributes:
        id: Unique identifier (auto-assigned by TodoManager)
        title: Task description (required, non-empty)
        completed: Completion status (default False)
        category: Optional grouping label
        priority: Priority level (high/medium/low, default medium)
        created_at: Creation timestamp (auto-set)
    """
    id: int
    title: str
    completed: bool = False
    category: Optional[str] = None
    priority: str = "medium"
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate todo attributes after initialization."""
        # Validate title
        if not self.title or not self.title.strip():
            raise ValueError("Todo title cannot be empty")
        if len(self.title) > 500:
            raise ValueError("Todo title cannot exceed 500 characters")

        # Validate priority
        if self.priority.lower() not in ["high", "medium", "low"]:
            raise ValueError(f"Priority must be high, medium, or low (got '{self.priority}')")
        self.priority = self.priority.lower()

        # Normalize category
        if self.category is not None:
            self.category = self.category.strip()
            if not self.category:
                self.category = None
            elif len(self.category) > 50:
                raise ValueError("Category cannot exceed 50 characters")
            else:
                self.category = self.category.lower()

    def to_dict(self) -> dict:
        """Convert todo to dictionary for serialization (future use)."""
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed,
            "category": self.category,
            "priority": self.priority,
            "created_at": self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Todo':
        """Create todo from dictionary (future use for Phase II persistence)."""
        data_copy = data.copy()
        if "created_at" in data_copy and isinstance(data_copy["created_at"], str):
            data_copy["created_at"] = datetime.fromisoformat(data_copy["created_at"])
        return cls(**data_copy)
```

---

## Storage Model

### TodoManager

The `TodoManager` class encapsulates all in-memory storage and provides the service layer API.

**Internal State**:
- `_todos: List[Todo]` - Ordered list of all todos (private)
- `_next_id: int` - Counter for generating unique IDs (private)

**Operations Contract**:

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `add()` | `title: str, category: Optional[str], priority: str` | `Todo` | Create new todo, auto-assign ID |
| `get_all()` | - | `List[Todo]` | Return all todos (in creation order) |
| `get_by_id()` | `id: int` | `Optional[Todo]` | Find todo by ID, None if not found |
| `update()` | `id: int, title: Optional[str], category: Optional[str], priority: Optional[str]` | `Optional[Todo]` | Update todo fields, None if ID invalid |
| `delete()` | `id: int` | `bool` | Remove todo, True if deleted, False if not found |
| `mark_complete()` | `id: int, completed: bool` | `Optional[Todo]` | Toggle completion status, None if ID invalid |
| `get_by_category()` | `category: str` | `List[Todo]` | Filter todos by category |
| `get_by_priority()` | `priority: str` | `List[Todo]` | Filter todos by priority |
| `count()` | - | `int` | Total number of todos |
| `count_completed()` | - | `int` | Number of completed todos |

**Guarantees**:
- IDs are sequential: first todo gets ID 1, second gets ID 2, etc.
- IDs are never reused (even after deletion)
- `get_all()` returns todos in creation order (oldest first)
- All getters return copies (external mutation doesn't affect internal state)
- All mutating operations are atomic (no partial updates)

---

## Data Relationships

### Current (Phase I)

**No relationships** - Single entity (Todo) with no foreign keys or references. Simple flat list structure.

### Future (Phase II)

Potential relationships for web application phase:

```
User (1) <----> (N) Todo
   - User can have many todos
   - Todo belongs to one user
   - FK: todo.user_id -> user.id

Todo (1) <----> (N) Tag
   - Todo can have many tags
   - Tag can belong to many todos
   - Junction: todo_tags (todo_id, tag_id)

Category -> Enum/Table
   - Categories become enumerated type or reference table
   - Ensures consistency across users
```

**Phase I Decision**: Keep flat structure. No user association. Category as simple string. Prepare for migration by keeping clean model boundaries.

---

## Data Migration Path (Phase I → Phase II)

### Mapping to SQLModel/Pydantic

Current `@dataclass` design maps cleanly to SQLModel:

```python
# Phase I (current)
@dataclass
class Todo:
    id: int
    title: str
    ...

# Phase II (future)
class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=500)
    user_id: int = Field(foreign_key="user.id")
    ...
```

**Migration Strategy**:
- Add `user_id` field (foreign key to User table)
- Convert `created_at` to UTC timezone-aware
- Add `updated_at` timestamp for audit trail
- Normalize categories to separate Category table
- Add indexes on `user_id`, `completed`, `created_at`

**Backward Compatibility**:
- Current `to_dict()`/`from_dict()` methods prepare for JSON serialization
- Validation logic stays in model (moves to Pydantic validators)
- Service layer (TodoManager) becomes SQLModel CRUD operations
- CLI layer unchanged (still calls same service methods)

---

## Validation Summary

### Model-Level Validation (Todo.__post_init__)
- Title: Not empty, ≤ 500 chars
- Priority: One of [high, medium, low]
- Category: If provided, not empty, ≤ 50 chars

### Service-Level Validation (TodoManager)
- ID existence: Verify todo exists before update/delete/mark_complete
- Duplicate prevention: Not needed (list-based, no uniqueness constraints)

### CLI-Level Validation (lib/validators.py)
- User input parsing: String → int for IDs
- Menu choice validation: 1-7 range
- Empty input handling: Re-prompt for required fields
- Type conversion: All CLI input arrives as strings

---

## Data Integrity Rules

1. **Uniqueness**: Todo IDs must be unique within session (enforced by auto-increment)
2. **Immutability**: `id` and `created_at` never change after creation
3. **Referential Integrity**: Not applicable (no relationships in Phase I)
4. **Type Safety**: Python type hints + runtime validation in `__post_init__`
5. **Defensive Copying**: TodoManager returns copies to prevent external mutation

---

## Performance Characteristics

### Time Complexity

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| Add todo | O(1) | Append to list |
| Get all todos | O(n) | Return full list |
| Get by ID | O(n) | Linear search (acceptable for <1000 todos) |
| Update | O(n) | Find by ID + update |
| Delete | O(n) | Find by ID + remove |
| Mark complete | O(n) | Find by ID + update |
| Filter by category | O(n) | Linear scan |
| Count | O(1) | Length of list |

**Optimization Notes**:
- For Phase I (10-100 todos), O(n) operations are instant
- Spec requires handling 1000+ todos: O(n) acceptable (< 2s requirement easily met)
- Phase II can use database indexes for O(log n) or O(1) lookups
- No premature optimization needed (violates YAGNI)

### Space Complexity

- O(n) where n = number of todos
- Each Todo: ~200 bytes (rough estimate: int + str + bool + datetime)
- 1000 todos: ~200 KB in memory (negligible)
- 10,000 todos: ~2 MB in memory (still trivial)

**Phase I is memory-efficient** even at scale. No concerns.

---

## Data Model Status

✅ **COMPLETE**

All entities defined, validation rules specified, migration path documented. Ready for implementation.

**Next Steps**: Generate CLI contracts and quickstart guide.
