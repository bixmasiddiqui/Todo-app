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
            json={"title": "Buy groceries"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Buy groceries"
        assert data["completed"] is False
        assert data["description"] is None
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_task_with_description(self, client: TestClient):
        """Test task creation with optional description."""
        response = client.post(
            "/api/todos",
            json={"title": "Buy groceries", "description": "Milk, eggs, bread"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Buy groceries"
        assert data["description"] == "Milk, eggs, bread"

    def test_create_task_empty_title(self, client: TestClient):
        """Test task creation with empty title fails."""
        response = client.post(
            "/api/todos",
            json={"title": ""}
        )
        assert response.status_code == 422

    def test_create_task_whitespace_only(self, client: TestClient):
        """Test task creation with whitespace-only title fails."""
        response = client.post(
            "/api/todos",
            json={"title": "   "}
        )
        assert response.status_code == 422

    def test_create_task_too_long(self, client: TestClient):
        """Test task creation with title exceeding 200 chars fails."""
        long_title = "a" * 201
        response = client.post(
            "/api/todos",
            json={"title": long_title}
        )
        assert response.status_code == 422

    def test_get_all_tasks_empty(self, client: TestClient):
        """Test getting all tasks when none exist."""
        response = client.get("/api/todos")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_all_tasks(self, client: TestClient):
        """Test getting all tasks."""
        client.post("/api/todos", json={"title": "Task 1"})
        client.post("/api/todos", json={"title": "Task 2"})
        client.post("/api/todos", json={"title": "Task 3"})

        response = client.get("/api/todos")
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 3
        assert tasks[0]["title"] == "Task 3"
        assert tasks[2]["title"] == "Task 1"

    def test_get_task_by_id_success(self, client: TestClient):
        """Test getting a single task by ID."""
        create_response = client.post(
            "/api/todos",
            json={"title": "Test task"}
        )
        task_id = create_response.json()["id"]

        response = client.get(f"/api/todos/{task_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == "Test task"

    def test_get_task_not_found(self, client: TestClient):
        """Test getting a non-existent task returns 404."""
        fake_uuid = "00000000-0000-0000-0000-000000000000"
        response = client.get(f"/api/todos/{fake_uuid}")
        assert response.status_code == 404

    def test_update_task_title(self, client: TestClient):
        """Test updating a task's title."""
        create_response = client.post(
            "/api/todos",
            json={"title": "Original title"}
        )
        task_id = create_response.json()["id"]

        response = client.patch(
            f"/api/todos/{task_id}",
            json={"title": "Updated title"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated title"
        assert data["completed"] is False

    def test_update_task_completion(self, client: TestClient):
        """Test marking a task as complete."""
        create_response = client.post(
            "/api/todos",
            json={"title": "Task to complete"}
        )
        task_id = create_response.json()["id"]

        response = client.patch(
            f"/api/todos/{task_id}",
            json={"completed": True}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is True
        assert data["title"] == "Task to complete"

    def test_update_task_toggle_completion(self, client: TestClient):
        """Test toggling task completion status."""
        create_response = client.post(
            "/api/todos",
            json={"title": "Toggle test"}
        )
        task_id = create_response.json()["id"]

        response = client.patch(
            f"/api/todos/{task_id}",
            json={"completed": True}
        )
        assert response.json()["completed"] is True

        response = client.patch(
            f"/api/todos/{task_id}",
            json={"completed": False}
        )
        assert response.json()["completed"] is False

    def test_update_task_not_found(self, client: TestClient):
        """Test updating a non-existent task returns 404."""
        fake_uuid = "00000000-0000-0000-0000-000000000000"
        response = client.patch(
            f"/api/todos/{fake_uuid}",
            json={"title": "Updated"}
        )
        assert response.status_code == 404

    def test_update_task_empty_title(self, client: TestClient):
        """Test updating task with empty title fails."""
        create_response = client.post(
            "/api/todos",
            json={"title": "Original"}
        )
        task_id = create_response.json()["id"]

        response = client.patch(
            f"/api/todos/{task_id}",
            json={"title": ""}
        )
        assert response.status_code == 422

    def test_delete_task_success(self, client: TestClient):
        """Test successful task deletion."""
        create_response = client.post(
            "/api/todos",
            json={"title": "Task to delete"}
        )
        task_id = create_response.json()["id"]

        response = client.delete(f"/api/todos/{task_id}")
        assert response.status_code == 204

        get_response = client.get(f"/api/todos/{task_id}")
        assert get_response.status_code == 404

    def test_delete_task_not_found(self, client: TestClient):
        """Test deleting a non-existent task returns 404."""
        fake_uuid = "00000000-0000-0000-0000-000000000000"
        response = client.delete(f"/api/todos/{fake_uuid}")
        assert response.status_code == 404

    def test_delete_task_removes_from_list(self, client: TestClient):
        """Test deleted task doesn't appear in list."""
        client.post("/api/todos", json={"title": "Task 1"})
        create_response = client.post("/api/todos", json={"title": "Task 2"})
        task_id = create_response.json()["id"]
        client.post("/api/todos", json={"title": "Task 3"})

        client.delete(f"/api/todos/{task_id}")

        response = client.get("/api/todos")
        tasks = response.json()
        assert len(tasks) == 2
        titles = [t["title"] for t in tasks]
        assert "Task 2" not in titles
        assert "Task 1" in titles
        assert "Task 3" in titles

    def test_full_workflow(self, client: TestClient):
        """Test complete CRUD workflow."""
        # Create
        create_response = client.post(
            "/api/todos",
            json={"title": "Workflow test task"}
        )
        assert create_response.status_code == 201
        task_id = create_response.json()["id"]

        # Read (single)
        get_response = client.get(f"/api/todos/{task_id}")
        assert get_response.status_code == 200
        assert get_response.json()["title"] == "Workflow test task"

        # Update title
        update_response = client.patch(
            f"/api/todos/{task_id}",
            json={"title": "Updated workflow task"}
        )
        assert update_response.status_code == 200
        assert update_response.json()["title"] == "Updated workflow task"

        # Mark complete
        complete_response = client.patch(
            f"/api/todos/{task_id}",
            json={"completed": True}
        )
        assert complete_response.status_code == 200
        assert complete_response.json()["completed"] is True

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
        assert response.status_code in [200, 405]


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
