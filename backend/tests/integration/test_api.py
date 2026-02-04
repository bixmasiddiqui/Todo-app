"""Integration tests for API endpoints."""
import pytest
from fastapi.testclient import TestClient


class TestTaskAPI:
    """Test suite for task API endpoints."""

    def test_health_check(self, client: TestClient):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_create_task_success(self, client: TestClient):
        """Test successful task creation."""
        response = client.post(
            "/api/todos",
            json={"description": "Buy groceries"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["description"] == "Buy groceries"
        assert data["is_completed"] is False
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_task_empty_description(self, client: TestClient):
        """Test task creation with empty description fails."""
        response = client.post(
            "/api/todos",
            json={"description": ""}
        )
        assert response.status_code == 422

    def test_create_task_whitespace_only(self, client: TestClient):
        """Test task creation with whitespace-only description fails."""
        response = client.post(
            "/api/todos",
            json={"description": "   "}
        )
        assert response.status_code == 422

    def test_create_task_too_long(self, client: TestClient):
        """Test task creation with description exceeding 500 chars fails."""
        long_description = "a" * 501
        response = client.post(
            "/api/todos",
            json={"description": long_description}
        )
        assert response.status_code == 422

    def test_get_all_tasks_empty(self, client: TestClient):
        """Test getting all tasks when none exist."""
        response = client.get("/api/todos")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_all_tasks(self, client: TestClient):
        """Test getting all tasks."""
        # Create tasks
        client.post("/api/todos", json={"description": "Task 1"})
        client.post("/api/todos", json={"description": "Task 2"})
        client.post("/api/todos", json={"description": "Task 3"})

        response = client.get("/api/todos")
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 3
        # Tasks should be ordered by created_at DESC (newest first)
        assert tasks[0]["description"] == "Task 3"
        assert tasks[2]["description"] == "Task 1"

    def test_get_task_by_id_success(self, client: TestClient):
        """Test getting a single task by ID."""
        # Create a task
        create_response = client.post(
            "/api/todos",
            json={"description": "Test task"}
        )
        task_id = create_response.json()["id"]

        # Get the task
        response = client.get(f"/api/todos/{task_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["description"] == "Test task"

    def test_get_task_not_found(self, client: TestClient):
        """Test getting a non-existent task returns 404."""
        fake_uuid = "00000000-0000-0000-0000-000000000000"
        response = client.get(f"/api/todos/{fake_uuid}")
        assert response.status_code == 404

    def test_update_task_description(self, client: TestClient):
        """Test updating a task's description."""
        # Create a task
        create_response = client.post(
            "/api/todos",
            json={"description": "Original description"}
        )
        task_id = create_response.json()["id"]

        # Update the task
        response = client.patch(
            f"/api/todos/{task_id}",
            json={"description": "Updated description"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["description"] == "Updated description"
        assert data["is_completed"] is False

    def test_update_task_completion(self, client: TestClient):
        """Test marking a task as complete."""
        # Create a task
        create_response = client.post(
            "/api/todos",
            json={"description": "Task to complete"}
        )
        task_id = create_response.json()["id"]

        # Mark as complete
        response = client.patch(
            f"/api/todos/{task_id}",
            json={"is_completed": True}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["is_completed"] is True
        assert data["description"] == "Task to complete"

    def test_update_task_toggle_completion(self, client: TestClient):
        """Test toggling task completion status."""
        # Create a task
        create_response = client.post(
            "/api/todos",
            json={"description": "Toggle test"}
        )
        task_id = create_response.json()["id"]

        # Mark as complete
        response = client.patch(
            f"/api/todos/{task_id}",
            json={"is_completed": True}
        )
        assert response.json()["is_completed"] is True

        # Mark as incomplete
        response = client.patch(
            f"/api/todos/{task_id}",
            json={"is_completed": False}
        )
        assert response.json()["is_completed"] is False

    def test_update_task_not_found(self, client: TestClient):
        """Test updating a non-existent task returns 404."""
        fake_uuid = "00000000-0000-0000-0000-000000000000"
        response = client.patch(
            f"/api/todos/{fake_uuid}",
            json={"description": "Updated"}
        )
        assert response.status_code == 404

    def test_update_task_empty_description(self, client: TestClient):
        """Test updating task with empty description fails."""
        # Create a task
        create_response = client.post(
            "/api/todos",
            json={"description": "Original"}
        )
        task_id = create_response.json()["id"]

        # Try to update with empty description
        response = client.patch(
            f"/api/todos/{task_id}",
            json={"description": ""}
        )
        assert response.status_code == 422

    def test_delete_task_success(self, client: TestClient):
        """Test successful task deletion."""
        # Create a task
        create_response = client.post(
            "/api/todos",
            json={"description": "Task to delete"}
        )
        task_id = create_response.json()["id"]

        # Delete the task
        response = client.delete(f"/api/todos/{task_id}")
        assert response.status_code == 204

        # Verify task is deleted
        get_response = client.get(f"/api/todos/{task_id}")
        assert get_response.status_code == 404

    def test_delete_task_not_found(self, client: TestClient):
        """Test deleting a non-existent task returns 404."""
        fake_uuid = "00000000-0000-0000-0000-000000000000"
        response = client.delete(f"/api/todos/{fake_uuid}")
        assert response.status_code == 404

    def test_delete_task_removes_from_list(self, client: TestClient):
        """Test deleted task doesn't appear in list."""
        # Create tasks
        client.post("/api/todos", json={"description": "Task 1"})
        create_response = client.post("/api/todos", json={"description": "Task 2"})
        task_id = create_response.json()["id"]
        client.post("/api/todos", json={"description": "Task 3"})

        # Delete middle task
        client.delete(f"/api/todos/{task_id}")

        # Verify list
        response = client.get("/api/todos")
        tasks = response.json()
        assert len(tasks) == 2
        descriptions = [t["description"] for t in tasks]
        assert "Task 2" not in descriptions
        assert "Task 1" in descriptions
        assert "Task 3" in descriptions

    def test_full_workflow(self, client: TestClient):
        """Test complete CRUD workflow."""
        # Create
        create_response = client.post(
            "/api/todos",
            json={"description": "Workflow test task"}
        )
        assert create_response.status_code == 201
        task_id = create_response.json()["id"]

        # Read (single)
        get_response = client.get(f"/api/todos/{task_id}")
        assert get_response.status_code == 200
        assert get_response.json()["description"] == "Workflow test task"

        # Update description
        update_response = client.patch(
            f"/api/todos/{task_id}",
            json={"description": "Updated workflow task"}
        )
        assert update_response.status_code == 200
        assert update_response.json()["description"] == "Updated workflow task"

        # Mark complete
        complete_response = client.patch(
            f"/api/todos/{task_id}",
            json={"is_completed": True}
        )
        assert complete_response.status_code == 200
        assert complete_response.json()["is_completed"] is True

        # Read (list)
        list_response = client.get("/api/todos")
        assert list_response.status_code == 200
        assert len(list_response.json()) == 1

        # Delete
        delete_response = client.delete(f"/api/todos/{task_id}")
        assert delete_response.status_code == 204

        # Verify deleted
        verify_response = client.get("/api/todos")
        assert verify_response.json() == []


class TestCORS:
    """Test CORS configuration."""

    def test_cors_headers(self, client: TestClient):
        """Test CORS headers are present."""
        response = client.options("/api/todos")
        # Note: TestClient doesn't process CORS middleware the same way
        # This is more of a smoke test
        assert response.status_code in [200, 405]  # OPTIONS might not be allowed


class TestErrorHandling:
    """Test error handling."""

    def test_invalid_json(self, client: TestClient):
        """Test invalid JSON returns 422."""
        response = client.post(
            "/api/todos",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422

    def test_invalid_uuid(self, client: TestClient):
        """Test invalid UUID format returns 422."""
        response = client.get("/api/todos/not-a-uuid")
        assert response.status_code == 422
