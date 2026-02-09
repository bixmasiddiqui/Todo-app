"""Unit tests for validation utilities.

These tests validate the validator functions:
- validate_title()
- validate_priority()
- validate_category()
- validate_todo_id()
- validate_menu_choice()
- validate_confirmation()
"""

import pytest
from src.lib.validators import (
    validate_title,
    validate_priority,
    validate_category,
    validate_todo_id,
    validate_menu_choice,
    validate_confirmation,
)


class TestValidateTitle:
    """Test validate_title() function."""

    def test_valid_title(self):
        """Valid title returns (True, "")."""
        is_valid, error = validate_title("Buy groceries")

        assert is_valid is True
        assert error == ""

    def test_valid_title_with_special_chars(self):
        """Title with special characters is valid."""
        is_valid, error = validate_title("Call @doctor re: appointment #123")

        assert is_valid is True
        assert error == ""

    def test_empty_string_title(self):
        """Empty string title is invalid."""
        is_valid, error = validate_title("")

        assert is_valid is False
        assert "cannot be empty" in error

    def test_whitespace_only_title(self):
        """Whitespace-only title is invalid."""
        is_valid, error = validate_title("   ")

        assert is_valid is False
        assert "cannot be empty" in error

    def test_none_title(self):
        """None title is invalid."""
        is_valid, error = validate_title(None)

        assert is_valid is False
        assert "cannot be empty" in error

    def test_title_max_length(self):
        """Title at 500 characters is valid."""
        valid_title = "x" * 500
        is_valid, error = validate_title(valid_title)

        assert is_valid is True
        assert error == ""

    def test_title_exceeds_max_length(self):
        """Title over 500 characters is invalid."""
        long_title = "x" * 501
        is_valid, error = validate_title(long_title)

        assert is_valid is False
        assert "too long" in error
        assert "500" in error


class TestValidatePriority:
    """Test validate_priority() function."""

    def test_valid_priority_high(self):
        """'high' priority is valid."""
        is_valid, error = validate_priority("high")

        assert is_valid is True
        assert error == ""

    def test_valid_priority_medium(self):
        """'medium' priority is valid."""
        is_valid, error = validate_priority("medium")

        assert is_valid is True
        assert error == ""

    def test_valid_priority_low(self):
        """'low' priority is valid."""
        is_valid, error = validate_priority("low")

        assert is_valid is True
        assert error == ""

    def test_valid_priority_case_insensitive(self):
        """Priority validation is case-insensitive."""
        is_valid1, _ = validate_priority("HIGH")
        is_valid2, _ = validate_priority("Medium")
        is_valid3, _ = validate_priority("LoW")

        assert is_valid1 is True
        assert is_valid2 is True
        assert is_valid3 is True

    def test_empty_priority(self):
        """Empty priority is valid (will default to medium)."""
        is_valid, error = validate_priority("")

        assert is_valid is True
        assert error == ""

    def test_none_priority(self):
        """None priority is valid (will default to medium)."""
        is_valid, error = validate_priority(None)

        assert is_valid is True
        assert error == ""

    def test_invalid_priority(self):
        """Invalid priority value returns error."""
        is_valid, error = validate_priority("urgent")

        assert is_valid is False
        assert "high, medium, or low" in error


class TestValidateCategory:
    """Test validate_category() function."""

    def test_valid_category(self):
        """Valid category returns (True, "")."""
        is_valid, error = validate_category("work")

        assert is_valid is True
        assert error == ""

    def test_valid_category_with_spaces(self):
        """Category with spaces is valid."""
        is_valid, error = validate_category("personal projects")

        assert is_valid is True
        assert error == ""

    def test_empty_category(self):
        """Empty category is valid (optional field)."""
        is_valid, error = validate_category("")

        assert is_valid is True
        assert error == ""

    def test_none_category(self):
        """None category is valid (optional field)."""
        is_valid, error = validate_category(None)

        assert is_valid is True
        assert error == ""

    def test_category_max_length(self):
        """Category at 50 characters is valid."""
        valid_category = "x" * 50
        is_valid, error = validate_category(valid_category)

        assert is_valid is True
        assert error == ""

    def test_category_exceeds_max_length(self):
        """Category over 50 characters is invalid."""
        long_category = "x" * 51
        is_valid, error = validate_category(long_category)

        assert is_valid is False
        assert "too long" in error
        assert "50" in error


class TestValidateTodoId:
    """Test validate_todo_id() function."""

    def test_valid_todo_id(self):
        """Valid numeric ID returns (True, id, "")."""
        is_valid, todo_id, error = validate_todo_id("5")

        assert is_valid is True
        assert todo_id == 5
        assert error == ""

    def test_valid_large_id(self):
        """Large valid ID is accepted."""
        is_valid, todo_id, error = validate_todo_id("999999")

        assert is_valid is True
        assert todo_id == 999999
        assert error == ""

    def test_zero_id(self):
        """ID of zero is invalid."""
        is_valid, todo_id, error = validate_todo_id("0")

        assert is_valid is False
        assert todo_id == 0
        assert "positive number" in error

    def test_negative_id(self):
        """Negative ID is invalid."""
        is_valid, todo_id, error = validate_todo_id("-5")

        assert is_valid is False
        assert todo_id == 0
        assert "positive number" in error

    def test_non_numeric_id(self):
        """Non-numeric input is invalid."""
        is_valid, todo_id, error = validate_todo_id("abc")

        assert is_valid is False
        assert todo_id == 0
        assert "valid number" in error

    def test_empty_string_id(self):
        """Empty string is invalid."""
        is_valid, todo_id, error = validate_todo_id("")

        assert is_valid is False
        assert todo_id == 0
        assert "enter a todo ID" in error

    def test_whitespace_only_id(self):
        """Whitespace-only input is invalid."""
        is_valid, todo_id, error = validate_todo_id("   ")

        assert is_valid is False
        assert todo_id == 0
        assert "enter a todo ID" in error

    def test_float_id(self):
        """Float input is invalid."""
        is_valid, todo_id, error = validate_todo_id("3.14")

        assert is_valid is False
        assert todo_id == 0
        assert "valid number" in error


class TestValidateMenuChoice:
    """Test validate_menu_choice() function."""

    def test_valid_choice_in_range(self):
        """Valid choice in range returns (True, choice, "")."""
        is_valid, choice, error = validate_menu_choice("3", 1, 5)

        assert is_valid is True
        assert choice == 3
        assert error == ""

    def test_valid_choice_at_minimum(self):
        """Choice at minimum boundary is valid."""
        is_valid, choice, error = validate_menu_choice("1", 1, 5)

        assert is_valid is True
        assert choice == 1
        assert error == ""

    def test_valid_choice_at_maximum(self):
        """Choice at maximum boundary is valid."""
        is_valid, choice, error = validate_menu_choice("5", 1, 5)

        assert is_valid is True
        assert choice == 5
        assert error == ""

    def test_choice_below_minimum(self):
        """Choice below minimum is invalid."""
        is_valid, choice, error = validate_menu_choice("0", 1, 5)

        assert is_valid is False
        assert choice == 0
        assert "1-5" in error

    def test_choice_above_maximum(self):
        """Choice above maximum is invalid."""
        is_valid, choice, error = validate_menu_choice("6", 1, 5)

        assert is_valid is False
        assert choice == 0
        assert "1-5" in error

    def test_non_numeric_choice(self):
        """Non-numeric choice is invalid."""
        is_valid, choice, error = validate_menu_choice("abc", 1, 5)

        assert is_valid is False
        assert choice == 0
        assert "number" in error

    def test_empty_choice(self):
        """Empty choice is invalid."""
        is_valid, choice, error = validate_menu_choice("", 1, 5)

        assert is_valid is False
        assert choice == 0
        assert "enter a number" in error

    def test_whitespace_only_choice(self):
        """Whitespace-only choice is invalid."""
        is_valid, choice, error = validate_menu_choice("   ", 1, 5)

        assert is_valid is False
        assert choice == 0
        assert "enter a number" in error


class TestValidateConfirmation:
    """Test validate_confirmation() function."""

    def test_yes_lowercase(self):
        """'yes' returns True."""
        assert validate_confirmation("yes") is True

    def test_yes_uppercase(self):
        """'YES' returns True."""
        assert validate_confirmation("YES") is True

    def test_yes_mixed_case(self):
        """'Yes' returns True."""
        assert validate_confirmation("Yes") is True

    def test_y_lowercase(self):
        """'y' returns True."""
        assert validate_confirmation("y") is True

    def test_y_uppercase(self):
        """'Y' returns True."""
        assert validate_confirmation("Y") is True

    def test_no_lowercase(self):
        """'no' returns False."""
        assert validate_confirmation("no") is False

    def test_no_uppercase(self):
        """'NO' returns False."""
        assert validate_confirmation("NO") is False

    def test_n_lowercase(self):
        """'n' returns False."""
        assert validate_confirmation("n") is False

    def test_n_uppercase(self):
        """'N' returns False."""
        assert validate_confirmation("N") is False

    def test_empty_string(self):
        """Empty string returns False."""
        assert validate_confirmation("") is False

    def test_invalid_response(self):
        """Invalid response returns False."""
        assert validate_confirmation("maybe") is False

    def test_whitespace_yes(self):
        """'yes' with whitespace returns False (exact match required)."""
        assert validate_confirmation("  yes  ") is False
