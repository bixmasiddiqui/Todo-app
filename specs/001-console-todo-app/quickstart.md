# Quickstart Guide: In-Memory Console Todo Application

**Feature**: `001-console-todo-app`
**Date**: 2026-01-02
**Audience**: Developers, testers, and end users

## Purpose

Get up and running with the Todo Manager application in under 5 minutes. This guide covers installation, first use, and common workflows.

---

## Prerequisites

- **Python**: Version 3.8 or higher (3.13+ recommended)
- **UV**: Modern Python package manager ([installation](https://github.com/astral-sh/uv))
- **Terminal**: Any terminal with 80-character width minimum
- **Operating System**: Windows, macOS, or Linux

### Check Your Environment

```bash
# Check Python version
python --version
# Should output: Python 3.8.0 or higher

# Check UV installation
uv --version
# Should output: uv X.Y.Z
```

If UV is not installed:
```bash
# Install UV (macOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install UV (Windows PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

## Installation

### 1. Clone or Download the Project

```bash
# If using Git
git clone <repository-url>
cd <repository-name>

# Or download and extract ZIP, then cd into directory
```

### 2. Install Dependencies

```bash
# UV automatically creates virtual environment and installs dependencies
uv sync
```

**What this does**:
- Creates a virtual environment (.venv/)
- Installs pytest for testing
- No other external dependencies (Python stdlib only)

---

## Running the Application

### Start the Todo Manager

```bash
# Using UV (recommended)
uv run python -m src

# Or activate virtual environment first
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
python -m src
```

### First Time Experience

You'll see the welcome screen:

```
╔════════════════════════════════════════════════════════════════╗
║                   Todo Manager - Phase I                       ║
║             In-Memory Console Application                      ║
╚════════════════════════════════════════════════════════════════╝

⚠️  NOTE: All todos are stored in memory only.
   Data will be lost when you exit the application.

Press ENTER to continue...
```

**Press ENTER** to proceed to the main menu.

---

## Your First Todo

### Step 1: View the Empty List

```
Enter your choice (1-7): 1
```

You'll see:
```
No todos yet. Add your first task!
```

Press ENTER to return to the main menu.

### Step 2: Add Your First Todo

```
Enter your choice (1-7): 2

Enter todo title: Buy groceries
Enter category (or press ENTER to skip): personal
Enter priority (high/medium/low, default: medium): high

✓ Todo added successfully!
  ID: 1
  Title: Buy groceries
  Category: personal
  Priority: high
```

Press ENTER to return to the main menu.

### Step 3: View Your Todo

```
Enter your choice (1-7): 1
```

You'll see:
```
[1] [ ] Buy groceries                     | personal | high
    Created: 2026-01-02 10:30
```

---

## Common Workflows

### Workflow 1: Daily Task Management

**Morning - Add Tasks**
```
1. Choose option 2 (Add new todo)
2. Enter: "Finish project report" | work | high
3. Enter: "Call dentist" | personal | low
4. Enter: "Review pull requests" | work | medium
```

**Throughout Day - Mark Complete**
```
1. Choose option 3 (Mark complete)
2. Enter ID of completed task
3. See status change from [ ] to [X]
```

**Evening - Review**
```
1. Choose option 1 (View all todos)
2. See completed vs. pending status
3. Choose option 7 (Exit) when done
```

### Workflow 2: Focused Work Session

**Filter by Priority**
```
1. Choose option 6 (Filter todos)
2. Choose option 2 (Filter by priority)
3. Enter: high
4. See only high-priority tasks
5. Complete tasks one by one
```

**Filter by Category**
```
1. Choose option 6 (Filter todos)
2. Choose option 1 (Filter by category)
3. Enter: work
4. Focus on work tasks only
```

### Workflow 3: Task Updates

**Fix a Typo**
```
1. Choose option 4 (Update todo)
2. Enter ID of todo to fix
3. Enter corrected title
4. Press ENTER to skip category/priority (keep current)
```

**Change Priority**
```
1. Choose option 4 (Update todo)
2. Enter ID of todo
3. Press ENTER to skip title (keep current)
4. Press ENTER to skip category (keep current)
5. Enter new priority (e.g., "high")
```

### Workflow 4: Cleanup

**Delete Completed Tasks**
```
1. Choose option 1 (View all) to see IDs
2. Note IDs of completed tasks [X]
3. Choose option 5 (Delete todo)
4. Enter ID
5. Confirm with "yes"
6. Repeat for other completed tasks
```

---

## Menu Reference

| Option | Action | Inputs | Example |
|--------|--------|--------|---------|
| 1 | View all todos | None | See full list |
| 2 | Add new todo | Title, Category (opt), Priority (opt) | "Buy milk" \| personal \| high |
| 3 | Mark complete/incomplete | Todo ID | 1 |
| 4 | Update todo | Todo ID, new values | Update ID 1 → new title |
| 5 | Delete todo | Todo ID, confirmation | Delete ID 1 → yes |
| 6 | Filter todos | Category or Priority | work OR high |
| 7 | Exit | None | Quit application |

---

## Tips and Tricks

### Productivity Tips

1. **Use categories consistently**: Stick to 3-5 categories (work, personal, home, shopping, health)
2. **Prioritize ruthlessly**: Only truly urgent tasks should be "high"
3. **Review regularly**: Check list at start and end of day
4. **Delete liberally**: Remove completed tasks to keep list focused
5. **Empty input shortcuts**: Press ENTER to skip optional fields quickly

### Keyboard Shortcuts

- **ENTER**: Continue/Skip optional field
- **Ctrl+C**: Exit application (same as option 7)
- **ESC**: Not supported (use menu navigation)

### Common Mistakes

**Mistake**: Entering "1" instead of "yes" for confirmations
- **Solution**: Type "yes" or "y" for confirmations

**Mistake**: Forgetting todo ID
- **Solution**: Choose option 1 to view list and see IDs

**Mistake**: Typing priority as "1" instead of "high"
- **Solution**: Use words: high, medium, or low

**Mistake**: Expecting data to persist after exit
- **Solution**: Remember this is Phase I - in-memory only!

---

## Troubleshooting

### Issue: "Command not found: uv"

**Solution**: Install UV package manager
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh  # macOS/Linux
# Or use PowerShell script for Windows
```

### Issue: "ModuleNotFoundError: No module named 'src'"

**Solution**: Run from project root directory
```bash
# Ensure you're in the correct directory
ls src/  # Should show __main__.py and subdirectories

# Run with correct command
uv run python -m src
```

### Issue: "ValueError: Priority must be high, medium, or low"

**Solution**: Use exact words (case-insensitive)
```
✓ Correct: high, medium, low, HIGH, Medium, Low
✗ Incorrect: 1, 2, 3, urgent, normal
```

### Issue: "Todo ID not found"

**Solution**: View list first to confirm ID exists
```
1. Choose option 1 (View all todos)
2. Note the ID in brackets [1] [2] [3]
3. Use that exact number
```

### Issue: Application crashes on invalid input

**Solution**: This shouldn't happen! If it does, report a bug.
- Expected behavior: Clear error message + re-prompt
- Actual crashes violate spec requirement SC-008

---

## Example Session

Here's a complete example session:

```
$ uv run python -m src

[Welcome screen displays]
Press ENTER to continue...

════════════════════════════════════════════════════════════════
Status: No todos yet

1. View all todos
2. Add new todo
3. Mark todo complete/incomplete
4. Update todo
5. Delete todo
6. Filter by category or priority
7. Exit

Enter your choice (1-7): 2

Enter todo title: Finish project report
Enter category (or press ENTER to skip): work
Enter priority (high/medium/low, default: medium): high

✓ Todo added successfully!
  ID: 1
  ...

Press ENTER...

Enter your choice (1-7): 2

Enter todo title: Buy groceries
Enter category: personal
Enter priority: medium

✓ Todo added successfully!
  ID: 2
  ...

Press ENTER...

Enter your choice (1-7): 1

[1] [ ] Finish project report             | work     | high
[2] [ ] Buy groceries                      | personal | medium

Press ENTER...

Enter your choice (1-7): 3

Enter todo ID: 1

Current status: Incomplete [ ]
New status: Complete [X]

✓ Todo marked as complete!

Press ENTER...

Enter your choice (1-7): 1

[1] [X] Finish project report             | work     | high
[2] [ ] Buy groceries                      | personal | medium

Total: 2 todos | 1 completed | 1 pending

Press ENTER...

Enter your choice (1-7): 7

════════════════════════════════════════════════════════════════
                       GOODBYE!
════════════════════════════════════════════════════════════════

⚠️  Remember: All todos have been discarded (in-memory only).

Thank you for using Todo Manager!
```

---

## Running Tests

### Run All Tests

```bash
# Using UV
uv run pytest

# Or with activated virtual environment
pytest
```

### Run Specific Test Suite

```bash
# Contract tests (data model)
uv run pytest tests/contract/

# Unit tests (services and utilities)
uv run pytest tests/unit/

# Integration tests (user stories)
uv run pytest tests/integration/
```

### Test with Coverage

```bash
uv run pytest --cov=src --cov-report=term-missing
```

**Expected Output**:
- All tests should pass (green dots)
- Coverage should be > 90% for all modules
- No errors or warnings

---

## Development Workflow

### Test-Driven Development (TDD)

This project follows strict TDD:

1. **Red**: Write failing test first
2. **Green**: Implement minimum code to pass
3. **Refactor**: Improve code quality

Example:
```bash
# 1. Write test in tests/unit/test_todo_manager.py
# 2. Run test - should fail
uv run pytest tests/unit/test_todo_manager.py::test_add_todo

# 3. Implement feature in src/services/todo_manager.py
# 4. Run test again - should pass
uv run pytest tests/unit/test_todo_manager.py::test_add_todo

# 5. Refactor if needed, ensure test still passes
```

### Project Structure Overview

```
src/
├── models/           # Todo dataclass
├── services/         # TodoManager (business logic)
├── cli/              # Menu and user interaction
└── lib/              # Utilities (validators, formatters)

tests/
├── contract/         # Model contract tests
├── unit/             # Service and utility tests
└── integration/      # User story end-to-end tests
```

---

## Next Steps

After mastering the basics:

1. **Explore filtering**: Try filtering by different categories and priorities
2. **Stress test**: Add 100+ todos to test performance (should handle 1000+ per spec)
3. **Review tests**: Read test files to understand expected behavior
4. **Phase II preview**: Check constitution.md for web app roadmap

---

## Support and Feedback

- **Documentation**: See `specs/001-console-todo-app/` for detailed specs
- **Issues**: Report bugs via GitHub issues (if applicable)
- **Feature Requests**: See Phase II roadmap in constitution.md

---

## Important Reminders

⚠️  **Data Persistence**: ALL TODOS ARE LOST WHEN YOU EXIT. This is Phase I behavior by design.

✅ **Phase II Preview**: Web app with database persistence coming in future phase

🧪 **Testing**: This app was built using Test-Driven Development - all features have comprehensive tests

📋 **Spec-Driven**: Every feature traces back to requirements in spec.md

---

**Quickstart Complete!** You're ready to use the Todo Manager. Enjoy tracking your tasks! 🎯