import pytest
from unittest.mock import patch, MagicMock
from pytest_bdd import scenarios, given, when, then
from datetime import datetime
from app import add_task

scenarios("../add_task.feature")

@pytest.fixture
def context():
    task1 = {
        "id": 1,
        "title": "Task 1",
        "category": "Work",
        "completed": False,
        "description": "Task 1 description important",
        "due_date": "2000-01-15",
        "priority": "High",
    }
    task2 = {
        "id": 2,
        "title": "Task 2 important",
        "category": "Personal",
        "completed": True,
        "description": "Task 2 description",
        "due_date": "2000-02-25",
        "priority": "High",
    }
    task3 = {
        "id": 3,
        "title": "Task 3",
        "category": "Personal",
        "completed": False,
        "description": "Task 3 description",
        "due_date": "2000-03-10",
        "priority": "Medium",
    }
    task4 = {
        "id": 4,
        "title": "Task 4 important",
        "category": "Work",
        "completed": True,
        "description": "Task 4 description",
        "due_date": "2000-04-18",
        "priority": "High",
    }
    task5 = {
        "id": 5,
        "title": "Task 5",
        "category": "School",
        "completed": False,
        "description": "Task 5 description",
        "due_date": "2000-05-30",
        "priority": "Low",
    }
    return {
        "tasks": [task1, task2, task3, task4, task5]
    }

@given("I have filled the new task form")
def precondition(context):
    context["precondition"] = "Hello, World!"
    context["title"] = "Task 6"
    context["description"] = "Task 6 description"
    context["priority"] = "High"
    context["category"] = "Work"
    context["due_date"] = "2000-06-15"
    context["added_task"] = {
        "id": 6,
        "title": "Task 6",
        "category": "Work",
        "completed": False,
        "description": "Task 6 description",
        "due_date": "2000-06-15",
        "priority": "High",
        "created_at": MagicMock(),
    }
    context["expected"] = context["tasks"] + [context["added_task"]]


@when("I click the Add Task button")
def action(context):
    with patch("tasks.datetime") as mock_datetime:
        mock_datetime.now.return_value = MagicMock()
        mock_datetime.now.return_value.strftime.return_value = context["added_task"]["created_at"]
        context["result"] = add_task(context["tasks"], context["title"], context["description"], context["priority"], context["category"], context["due_date"])


@then("the task should be added to the task list")
def outcome(context):
    assert context["result"] == context["expected"]

# The created at is incorrect
# We need to modify the test tasks to have created_at, and we need to mock created_at to get the correct timestamp on the generated task