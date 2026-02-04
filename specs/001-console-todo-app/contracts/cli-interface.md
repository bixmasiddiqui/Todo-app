# CLI Interface Contract: In-Memory Console Todo Application

**Feature**: `001-console-todo-app`
**Date**: 2026-01-02
**Type**: User Interface Contract

## Purpose

Define the exact CLI interface behavior, menu structure, user interactions, and feedback messages for the todo application. This contract serves as the specification for implementation and testing.

---

## Application Startup

### Execution Command

```bash
# Using UV
uv run python -m src

# Using Python directly
python -m src
```

### Welcome Screen

```
╔════════════════════════════════════════════════════════════════╗
║                   Todo Manager - Phase I                       ║
║             In-Memory Console Application                      ║
╚════════════════════════════════════════════════════════════════╝

⚠️  NOTE: All todos are stored in memory only.
   Data will be lost when you exit the application.

Press ENTER to continue...
```

**Behavior**:
- Display welcome banner on startup
- Show data persistence warning prominently
- Wait for ENTER key before showing main menu
- Warning ensures user understands in-memory nature (spec requirement SC-010)

---

## Main Menu

### Menu Display

```
════════════════════════════════════════════════════════════════
                         MAIN MENU
════════════════════════════════════════════════════════════════
Status: 3 todos | 1 completed | 2 pending

1. View all todos
2. Add new todo
3. Mark todo complete/incomplete
4. Update todo
5. Delete todo
6. Filter by category or priority
7. Exit

Enter your choice (1-7): _
```

**Elements**:
- Header with visual separator
- **Status line**: Shows total count, completed count, pending count
- **Numbered options**: 1-7 for all operations
- **Exit option**: Always option 7
- **Input prompt**: Clear instruction to enter 1-7

**Status Line Logic**:
- `total todos = count()`
- `completed = count_completed()`
- `pending = total - completed`
- If no todos: `Status: No todos yet`

---

## Operation 1: View All Todos

### Input Flow

```
Enter your choice (1-7): 1
```

### Output - With Todos

```
════════════════════════════════════════════════════════════════
                       ALL TODOS
════════════════════════════════════════════════════════════════

[1] [ ] Buy groceries                     | work   | high
    Created: 2026-01-02 10:30

[2] [X] Finish project report              | work   | medium
    Created: 2026-01-02 09:15

[3] [ ] Call dentist                       | personal | low
    Created: 2026-01-02 08:45

════════════════════════════════════════════════════════════════
Total: 3 todos | 1 completed | 2 pending

Press ENTER to return to menu...
```

**Format Specification**:
- `[ID]` - Todo ID in brackets
- `[ ]` - Checkbox: `[ ]` = incomplete, `[X]` = complete
- Title - Todo title (truncated to 40 chars with "..." if longer)
- Category - Shown after "|", or "none" if not set
- Priority - Shown after "|", displayed as-is (high/medium/low)
- Created timestamp - ISO date format YYYY-MM-DD HH:MM

### Output - No Todos

```
════════════════════════════════════════════════════════════════
                       ALL TODOS
════════════════════════════════════════════════════════════════

No todos yet. Add your first task!

════════════════════════════════════════════════════════════════

Press ENTER to return to menu...
```

**Behavior**:
- Friendly message when list is empty (spec requirement: edge case handling)
- Always return to main menu after ENTER

---

## Operation 2: Add New Todo

### Input Flow

```
Enter your choice (1-7): 2

════════════════════════════════════════════════════════════════
                       ADD NEW TODO
════════════════════════════════════════════════════════════════

Enter todo title: Buy groceries
Enter category (or press ENTER to skip): work
Enter priority (high/medium/low, default: medium): high

✓ Todo added successfully!
  ID: 1
  Title: Buy groceries
  Category: work
  Priority: high

Press ENTER to return to menu...
```

**Input Validation**:

1. **Title validation**:
   - If empty: `✗ Error: Todo title cannot be empty. Please try again.`
   - If > 500 chars: `✗ Error: Title too long (max 500 characters). Please try again.`
   - Re-prompt until valid

2. **Category validation**:
   - Optional field (ENTER to skip)
   - If provided but empty after trim: treat as None
   - If > 50 chars: `✗ Error: Category too long (max 50 characters). Please try again.`
   - Normalized to lowercase automatically

3. **Priority validation**:
   - Default to "medium" if ENTER pressed
   - If invalid: `✗ Error: Priority must be high, medium, or low. Please try again.`
   - Case-insensitive (HIGH, High, high all accepted)
   - Re-prompt until valid

**Success Feedback**:
- Green checkmark (✓) for success
- Show all attributes of created todo
- Display auto-assigned ID

**Error Feedback**:
- Red X (✗) for errors
- Clear, actionable error message
- Re-prompt for corrected input

---

## Operation 3: Mark Todo Complete/Incomplete

### Input Flow

```
Enter your choice (1-7): 3

════════════════════════════════════════════════════════════════
                   MARK TODO COMPLETE/INCOMPLETE
════════════════════════════════════════════════════════════════

Enter todo ID: 1

Current status: Incomplete [ ]
New status: Complete [X]

✓ Todo marked as complete!

Press ENTER to return to menu...
```

**Input Validation**:

1. **ID validation**:
   - If not a number: `✗ Error: Invalid input. Please enter a valid number.`
   - If todo not found: `✗ Error: Todo ID not found. Please check the ID and try again.`

**Behavior**:
- Auto-toggle: If incomplete → mark complete, if complete → mark incomplete
- Show both current and new status for clarity
- Success message confirms action

**Toggle Logic**:
- Current `completed = False` → Set to `True`
- Current `completed = True` → Set to `False`

---

## Operation 4: Update Todo

### Input Flow

```
Enter your choice (1-7): 4

════════════════════════════════════════════════════════════════
                       UPDATE TODO
════════════════════════════════════════════════════════════════

Enter todo ID to update: 1

Current todo:
  Title: Buy groceries
  Category: work
  Priority: high

Enter new title (or press ENTER to keep current): Buy milk and eggs
Enter new category (or press ENTER to keep current): personal
Enter new priority (or press ENTER to keep current): medium

✓ Todo updated successfully!

Updated todo:
  Title: Buy milk and eggs
  Category: personal
  Priority: medium

Press ENTER to return to menu...
```

**Input Validation**:

1. **ID validation**: Same as mark complete operation
2. **Title validation**: If provided, same rules as add operation. ENTER = keep current.
3. **Category validation**: If provided, same rules as add operation. ENTER = keep current.
4. **Priority validation**: If provided, same rules as add operation. ENTER = keep current.

**Behavior**:
- Show current values before prompting for updates
- ENTER on any field = keep current value (no change)
- Only update fields where user provides new value
- Show before/after comparison

**Edge Cases**:
- If todo not found: `✗ Error: Todo ID not found.`
- If all fields skipped (all ENTER): `ℹ️ No changes made.`

---

## Operation 5: Delete Todo

### Input Flow

```
Enter your choice (1-7): 5

════════════════════════════════════════════════════════════════
                       DELETE TODO
════════════════════════════════════════════════════════════════

Enter todo ID to delete: 1

Todo to delete:
  [1] [ ] Buy groceries | work | high

Are you sure you want to delete this todo? (yes/no): yes

✓ Todo deleted successfully!

Press ENTER to return to menu...
```

**Input Validation**:

1. **ID validation**: Same as other operations
2. **Confirmation validation**:
   - Accept: "yes", "y", "YES", "Y" (case-insensitive)
   - Reject: "no", "n", "NO", "N", or anything else
   - If rejected: `ℹ️ Delete cancelled. Todo was not removed.`

**Behavior**:
- **Confirmation required** (destructive operation)
- Show full todo details before confirmation
- Clear success/cancellation message

**Security Note**:
- Confirmation prevents accidental deletions
- User-friendly (spec requirement: clear feedback)

---

## Operation 6: Filter by Category or Priority

### Input Flow

```
Enter your choice (1-7): 6

════════════════════════════════════════════════════════════════
                       FILTER TODOS
════════════════════════════════════════════════════════════════

Filter by:
1. Category
2. Priority
3. Back to main menu

Enter your choice (1-3): 1

Enter category name: work

════════════════════════════════════════════════════════════════
                   TODOS - Category: work
════════════════════════════════════════════════════════════════

[1] [ ] Buy groceries                     | work   | high
    Created: 2026-01-02 10:30

[2] [X] Finish project report              | work   | medium
    Created: 2026-01-02 09:15

════════════════════════════════════════════════════════════════
Total: 2 todos in category 'work'

Press ENTER to return to menu...
```

**Sub-Menu Options**:
1. Filter by category (user enters category name)
2. Filter by priority (user enters priority level)
3. Back to main menu (cancel operation)

**Filter by Priority Flow**:

```
Enter your choice (1-3): 2

Enter priority (high/medium/low): high

════════════════════════════════════════════════════════════════
                   TODOS - Priority: high
════════════════════════════════════════════════════════════════

[1] [ ] Buy groceries                     | work   | high

════════════════════════════════════════════════════════════════
Total: 1 todo with priority 'high'

Press ENTER to return to menu...
```

**Validation**:
- Category: Any non-empty string, case-insensitive match
- Priority: Must be high/medium/low, case-insensitive
- If no matches: `No todos found with {filter criteria}.`

---

## Operation 7: Exit

### Input Flow

```
Enter your choice (1-7): 7

════════════════════════════════════════════════════════════════
                       GOODBYE!
════════════════════════════════════════════════════════════════

⚠️  Remember: All todos have been discarded (in-memory only).

Thank you for using Todo Manager!

════════════════════════════════════════════════════════════════
```

**Behavior**:
- Display goodbye message
- Remind user about data loss (in-memory warning)
- Clean exit (no errors, exit code 0)
- Handle Ctrl+C gracefully (same goodbye message)

---

## Error Handling

### Invalid Menu Choice

```
Enter your choice (1-7): 99

✗ Error: Invalid choice. Please enter a number between 1 and 7.

Press ENTER to try again...
```

### Non-Numeric Input

```
Enter your choice (1-7): abc

✗ Error: Invalid input. Please enter a number between 1 and 7.

Press ENTER to try again...
```

### Keyboard Interrupt (Ctrl+C)

```
^C

════════════════════════════════════════════════════════════════
                       GOODBYE!
════════════════════════════════════════════════════════════════

⚠️  Remember: All todos have been discarded (in-memory only).

Thank you for using Todo Manager!

════════════════════════════════════════════════════════════════
```

**Behavior**:
- Catch `KeyboardInterrupt` exception
- Treat same as menu option 7 (Exit)
- Display goodbye message
- Clean exit

---

## UI Standards

### Consistent Elements

1. **Visual Separators**: `════` lines (64 chars) for section headers
2. **Success Symbol**: ✓ (checkmark) for successful operations
3. **Error Symbol**: ✗ (X mark) for errors
4. **Info Symbol**: ℹ️ (info) for informational messages
5. **Warning Symbol**: ⚠️ (warning triangle) for important notes

### Message Templates

```python
SUCCESS_TEMPLATE = "✓ {message}"
ERROR_TEMPLATE = "✗ Error: {message}"
INFO_TEMPLATE = "ℹ️ {message}"
WARNING_TEMPLATE = "⚠️  {message}"
```

### Prompt Standards

- **Menu prompts**: `Enter your choice (1-N): _`
- **Text input**: `Enter {field}: _`
- **Confirmation**: `Are you sure? (yes/no): _`
- **Optional input**: `Enter {field} (or press ENTER to skip): _`
- **Default value**: `Enter {field} (default: {value}): _`

---

## Accessibility Considerations

1. **No color dependency**: Use symbols (✓ ✗ [ ] [X]) not just colors
2. **Clear labeling**: All options numbered and described
3. **Explicit prompts**: Tell user exactly what input is expected
4. **Error recovery**: Always re-prompt on error, don't crash
5. **Consistent structure**: Same layout across all screens

---

## Performance Requirements

From spec success criteria:

- **SC-001**: Add todo confirmation < 5 seconds ✓ (instant)
- **SC-002**: View list display < 2 seconds ✓ (instant even with 1000 todos)
- **SC-003**: Mark complete ≤ 2 interactions ✓ (menu choice + ID)
- **SC-004**: Update/delete ≤ 3 interactions ✓ (menu + ID + new value/confirm)
- **SC-007**: Self-explanatory interface ✓ (numbered menu, clear prompts)

All requirements met by this interface design.

---

## Contract Status

✅ **COMPLETE**

All user interactions defined, error handling specified, UI standards established. Ready for implementation.

**Next Steps**: Generate quickstart guide with usage examples.
