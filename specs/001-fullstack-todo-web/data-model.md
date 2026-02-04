# Data Model: Full-Stack Todo Web Application

**Feature**: 001-fullstack-todo-web
**Date**: 2026-01-04
**Version**: 1.0.0

## Purpose

This document defines the data entities, database schema, and data validation rules for the Full-Stack Todo Web Application. All model definitions are derived from the feature specification requirements and informed by research decisions.

---

## Entity Overview

The application has a single core entity:

- **Task**: Represents a user's todo item with description, completion status, and timestamps

---

## 1. Task Entity

### 1.1 Entity Definition

**Purpose**: Represents a single todo item that a user wants to track

**Lifecycle**:
1. **Created**: User submits task description via UI
2. **Active**: Task exists in incomplete state
3. **Completed**: User marks task as done (reversible)
4. **Edited**: User modifies description (optional)
5. **Deleted**: User removes task (permanent)

**Business Rules**:
- Task description MUST be non-empty (1-500 characters)
- Task can transition between incomplete and complete states any number of times
- Timestamps are system-managed (not user-editable)
- Task ID is system-generated (UUID v4)

---

### 1.2 Database Schema

**Table Name**: `tasks`

**PostgreSQL Schema**:
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    description VARCHAR(500) NOT NULL CHECK (length(description) >= 1),
    is_completed BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Index for default ordering (newest first)
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);

-- Index for filtering by completion status (future enhancement)
CREATE INDEX idx_tasks_is_completed ON tasks(is_completed);

-- Trigger to auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tasks_updated_at_trigger
    BEFORE UPDATE ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

**Field Definitions**:

| Field | Type | Nullable | Default | Constraints | Purpose |
|-------|------|----------|---------|-------------|---------|
| `id` | UUID | No | gen_random_uuid() | PRIMARY KEY | Unique identifier for task |
| `description` | VARCHAR(500) | No | - | length >= 1, <= 500 | Task content/description |
| `is_completed` | BOOLEAN | No | false | - | Completion status flag |
| `created_at` | TIMESTAMP WITH TIME ZONE | No | CURRENT_TIMESTAMP | - | When task was created |
| `updated_at` | TIMESTAMP WITH TIME ZONE | No | CURRENT_TIMESTAMP | Auto-update trigger | When task was last modified |

**Rationale**:
- **UUID**: Prevents ID enumeration, no collision risk, future-proof for distributed systems
- **VARCHAR(500)**: Matches spec constraint (FR-008), prevents abuse, adequate length
- **TIMESTAMP WITH TIME ZONE**: Portable across timezones, supports future multi-region
- **Check Constraint**: Database-level validation ensures data integrity
- **Indexes**: Support default ordering and future filtering needs
- **Trigger**: Automatically maintains updated_at without application logic

---

### 1.3 SQLModel Definition (Backend)

**File**: `backend/src/models/task.py`

```python
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4


# Base model with shared fields
class TaskBase(SQLModel):
    """Shared fields for Task entity"""
    description: str = Field(
        min_length=1,
        max_length=500,
        description="Task description (1-500 characters)"
    )


# Database table model
class Task(TaskBase, table=True):
    """Task entity - database table model"""
    __tablename__ = "tasks"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        description="Unique task identifier"
    )
    is_completed: bool = Field(
        default=False,
        description="Task completion status"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Task creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last modification timestamp"
    )


# API request model (create)
class TaskCreate(TaskBase):
    """Request model for creating a new task"""
    pass


# API request model (update)
class TaskUpdate(SQLModel):
    """Request model for updating an existing task"""
    description: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=500,
        description="Updated task description (optional)"
    )
    is_completed: Optional[bool] = Field(
        default=None,
        description="Updated completion status (optional)"
    )


# API response model
class TaskRead(TaskBase):
    """Response model for task data"""
    id: UUID
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

**Model Separation Rationale**:
- **TaskBase**: Shared validation logic, DRY principle
- **Task**: Database table with all fields including system-managed ones
- **TaskCreate**: API input for creation (only user-provided fields)
- **TaskUpdate**: API input for updates (all fields optional for PATCH)
- **TaskRead**: API output (excludes nothing, includes all fields for client consumption)

---

### 1.4 TypeScript Definition (Frontend)

**File**: `frontend/src/types/task.ts`

```typescript
/**
 * Task entity - client-side TypeScript definition
 */
export interface Task {
  /** Unique task identifier (UUID v4) */
  id: string;

  /** Task description (1-500 characters) */
  description: string;

  /** Task completion status */
  is_completed: boolean;

  /** Task creation timestamp (ISO 8601) */
  created_at: string;

  /** Last modification timestamp (ISO 8601) */
  updated_at: string;
}

/**
 * Request payload for creating a new task
 */
export interface TaskCreateRequest {
  /** Task description (1-500 characters, non-empty) */
  description: string;
}

/**
 * Request payload for updating an existing task (partial update)
 */
export interface TaskUpdateRequest {
  /** Updated task description (optional) */
  description?: string;

  /** Updated completion status (optional) */
  is_completed?: boolean;
}

/**
 * API error response structure
 */
export interface APIError {
  /** Error type/code */
  error: string;

  /** Human-readable error message */
  detail: string;

  /** Validation errors (if applicable) */
  validation_errors?: Array<{
    field: string;
    message: string;
  }>;
}
```

**Type Definitions Rationale**:
- **Matches Backend**: Field names and types mirror SQLModel definitions
- **ISO 8601 Timestamps**: String format for JSON serialization (parsed to Date when needed)
- **Optional Fields**: TaskUpdateRequest uses optionals for PATCH semantics
- **Error Types**: Structured error responses for type-safe error handling

---

## 2. Data Validation Rules

### 2.1 Backend Validation (Pydantic/SQLModel)

**Task Description Validation**:
```python
from pydantic import validator

class TaskBase(SQLModel):
    description: str = Field(min_length=1, max_length=500)

    @validator('description')
    def description_not_empty_or_whitespace(cls, v):
        if not v or v.strip() == '':
            raise ValueError('Description cannot be empty or whitespace only')
        return v.strip()  # Remove leading/trailing whitespace
```

**Validation Rules**:
| Field | Rule | Error Message |
|-------|------|---------------|
| description | 1-500 characters | "Description must be between 1 and 500 characters" |
| description | Non-empty after trim | "Description cannot be empty or whitespace only" |
| is_completed | Boolean type | "Completion status must be true or false" |
| id (on update/delete) | Valid UUID | "Invalid task ID format" |

**HTTP Status Codes for Validation Errors**:
- **400 Bad Request**: Validation failure (description too long, empty, invalid type)
- **404 Not Found**: Task ID doesn't exist
- **422 Unprocessable Entity**: Pydantic validation error (malformed JSON)

---

### 2.2 Frontend Validation (Client-Side UX)

**Note**: Client-side validation is for UX only, NOT security. Backend always validates.

**Task Input Validation**:
```typescript
// Example validation function
function validateTaskDescription(description: string): string | null {
  const trimmed = description.trim();

  if (trimmed.length === 0) {
    return "Task description cannot be empty";
  }

  if (trimmed.length > 500) {
    return `Description is too long (${trimmed.length}/500 characters)`;
  }

  return null; // Valid
}
```

**UI Validation Feedback**:
- Show character count (e.g., "245/500")
- Disable submit button when description is empty
- Show inline error message on blur if invalid
- Preserve user input on validation failure
- Re-enable editing with error message, don't clear input

---

## 3. Data Relationships

**Current State**: Single entity application with no relationships

**Future Considerations** (out of scope for Phase II):
- **Users**: One-to-many relationship (User has many Tasks)
- **Categories**: Many-to-many relationship (Task can have many Categories)
- **Tags**: Many-to-many relationship (Task can have many Tags)
- **Subtasks**: One-to-many hierarchical relationship (Task can have many Subtasks)

**Database Design Philosophy**:
- Start simple with single table
- Add foreign keys only when needed
- Use indexes strategically for query patterns
- Avoid premature normalization

---

## 4. Data Access Patterns

### 4.1 Common Queries

**List All Tasks** (default ordering: newest first):
```sql
SELECT id, description, is_completed, created_at, updated_at
FROM tasks
ORDER BY created_at DESC;
```

**Get Single Task by ID**:
```sql
SELECT id, description, is_completed, created_at, updated_at
FROM tasks
WHERE id = $1;
```

**Create New Task**:
```sql
INSERT INTO tasks (description)
VALUES ($1)
RETURNING id, description, is_completed, created_at, updated_at;
```

**Update Task** (partial update):
```sql
UPDATE tasks
SET description = COALESCE($2, description),
    is_completed = COALESCE($3, is_completed)
WHERE id = $1
RETURNING id, description, is_completed, created_at, updated_at;
```

**Delete Task**:
```sql
DELETE FROM tasks
WHERE id = $1;
```

**Performance Expectations**:
- List all tasks: < 50ms for up to 1000 tasks (with index)
- Single task lookup: < 10ms (primary key index)
- Insert: < 20ms
- Update: < 20ms
- Delete: < 20ms

---

### 4.2 Query Optimization

**Current Indexes**:
1. **Primary Key (id)**: Automatic B-tree index for lookups
2. **created_at DESC**: Supports default ordering
3. **is_completed**: Future filtering (completed vs incomplete tabs)

**Query Guidelines**:
- Always use parameterized queries (SQL injection prevention)
- Use RETURNING clause to fetch updated data in single round-trip
- Use COALESCE for partial updates (PATCH semantics)
- Avoid SELECT *; specify fields explicitly for clarity and forward compatibility

---

## 5. Migration Strategy

### 5.1 Alembic Configuration

**Migration Files Location**: `backend/alembic/versions/`

**Initial Migration** (001_create_tasks_table.py):
```python
"""create tasks table

Revision ID: 001
Revises:
Create Date: 2026-01-04

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create tasks table
    op.create_table(
        'tasks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('description', sa.String(500), nullable=False),
        sa.Column('is_completed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.CheckConstraint('length(description) >= 1', name='description_not_empty')
    )

    # Create indexes
    op.create_index('idx_tasks_created_at', 'tasks', ['created_at'], postgresql_ops={'created_at': 'DESC'})
    op.create_index('idx_tasks_is_completed', 'tasks', ['is_completed'])

    # Create updated_at trigger
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    op.execute("""
        CREATE TRIGGER tasks_updated_at_trigger
            BEFORE UPDATE ON tasks
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column();
    """)


def downgrade() -> None:
    # Drop trigger first
    op.execute("DROP TRIGGER IF EXISTS tasks_updated_at_trigger ON tasks;")
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column;")

    # Drop indexes
    op.drop_index('idx_tasks_is_completed', table_name='tasks')
    op.drop_index('idx_tasks_created_at', table_name='tasks')

    # Drop table
    op.drop_table('tasks')
```

**Migration Commands**:
```bash
# Generate new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Show current migration version
alembic current
```

---

### 5.2 Schema Evolution Guidelines

**Future Schema Changes**:
1. **Adding Fields**: Use `ALTER TABLE ADD COLUMN` with appropriate defaults
2. **Removing Fields**: Deprecated first, remove in next major version
3. **Renaming Fields**: Create new field, migrate data, remove old field (three migrations)
4. **Index Changes**: Can be done online in Postgres 11+

**Backwards Compatibility**:
- API models should handle missing fields gracefully
- Database defaults allow old code to work with new schema
- Frontend types should use optional fields for new additions

---

## 6. Data Integrity Constraints

### 6.1 Database-Level Constraints

**Enforced by PostgreSQL**:
- **Primary Key**: Uniqueness of task IDs
- **NOT NULL**: Required fields cannot be null
- **Check Constraint**: Description length >= 1
- **Default Values**: is_completed defaults to false
- **Timestamps**: Automatic creation and update tracking

**Rationale**: Database constraints provide last line of defense against data corruption, even if application logic fails.

---

### 6.2 Application-Level Validation

**Enforced by SQLModel/Pydantic**:
- Type validation (string, boolean, UUID)
- Length validation (1-500 characters)
- Whitespace trimming
- Custom validators for business rules

**Rationale**: Application validation provides better error messages and fails fast before database interaction.

---

## 7. Testing Data Models

### 7.1 Model Tests (Unit Tests)

**File**: `backend/tests/unit/test_models.py`

**Test Cases**:
```python
import pytest
from uuid import UUID
from src.models.task import Task, TaskCreate, TaskUpdate

def test_task_create_valid():
    """Valid task creation should succeed"""
    task_data = TaskCreate(description="Buy groceries")
    assert task_data.description == "Buy groceries"

def test_task_create_empty_description_fails():
    """Empty description should raise validation error"""
    with pytest.raises(ValueError):
        TaskCreate(description="")

def test_task_create_whitespace_only_fails():
    """Whitespace-only description should raise validation error"""
    with pytest.raises(ValueError):
        TaskCreate(description="   ")

def test_task_create_too_long_fails():
    """Description > 500 chars should raise validation error"""
    with pytest.raises(ValueError):
        TaskCreate(description="x" * 501)

def test_task_update_partial():
    """Partial update should allow optional fields"""
    update_data = TaskUpdate(description="Updated task")
    assert update_data.description == "Updated task"
    assert update_data.is_completed is None  # Not provided

def test_task_whitespace_trimmed():
    """Leading/trailing whitespace should be trimmed"""
    task_data = TaskCreate(description="  Buy milk  ")
    assert task_data.description == "Buy milk"
```

---

### 7.2 Integration Tests (Database)

**File**: `backend/tests/integration/test_database.py`

**Test Cases**:
- Task can be inserted and retrieved
- UUID is auto-generated
- Timestamps are auto-populated
- updated_at changes on UPDATE
- Check constraint prevents empty descriptions
- Indexes are created correctly

---

## 8. Data Model Summary

**Entity Count**: 1 (Task)

**Database Tables**: 1 (tasks)

**Total Fields**: 5 per task
- **System-Managed**: id, created_at, updated_at (3 fields)
- **User-Provided**: description, is_completed (2 fields)

**Indexes**: 3
- Primary key on id
- B-tree on created_at (DESC)
- B-tree on is_completed

**Constraints**: 4
- Primary key constraint
- NOT NULL constraints (4 fields)
- Check constraint (description length)
- Unique constraint (via primary key)

**Model Files**:
- `backend/src/models/task.py` (SQLModel definitions)
- `frontend/src/types/task.ts` (TypeScript definitions)
- `backend/alembic/versions/001_create_tasks_table.py` (Migration)

---

## 9. Data Model Evolution

**Version 1.0 (Current)**: Single-user, single-entity system

**Future Enhancements** (not in Phase II):
- **v1.1**: Add User entity, foreign key in Task
- **v1.2**: Add Category entity, many-to-many with Task
- **v1.3**: Add Tag entity, many-to-many with Task
- **v1.4**: Add Subtask entity, hierarchical relationship
- **v2.0**: Add Project entity, task grouping

**Migration Path**: Each version adds tables/columns without breaking existing functionality

---

**Data Model Version**: 1.0.0
**Last Updated**: 2026-01-04
**Next Review**: After Phase II implementation (before Phase III planning)
