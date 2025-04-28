import pytest
from unittest.mock import patch, mock_open, MagicMock
from pytest_bdd import scenarios, given, when, then
from src.app import (
    add_task,
    save_tasks,
    load_tasks,
    filter_tasks_by_category,
    filter_tasks_by_priority,
)

scenarios("../task_management.feature")


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
        "task1": task1,
        "task2": task2,
        "task3": task3,
        "task4": task4,
        "task5": task5,
        "tasks": [task1, task2, task3, task4, task5],
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
        mock_datetime.now.return_value.strftime.return_value = context["added_task"][
            "created_at"
        ]
        context["result"] = add_task(
            context["tasks"],
            context["title"],
            context["description"],
            context["priority"],
            context["category"],
            context["due_date"],
        )


@then("the task should be added to the task list")
def outcome(context):
    assert context["result"] == context["expected"]


@given("I have a task list")
def precondition(context):
    context["file_path"] = "mock_tasks.json"


@when("I make any changes to the task list")
def action(context):
    with patch("builtins.open", mock_open()) as mocked_file:
        with patch("json.dump") as mocked_json_dump:
            save_tasks(context["tasks"], context["file_path"])
            context["mocked_file"] = mocked_file
            context["mocked_json_dump"] = mocked_json_dump


@then("the task list should be saved")
def outcome(context):
    context["mocked_file"].assert_called_once_with(context["file_path"], "w")
    context["mocked_json_dump"].assert_called_once_with(
        context["tasks"], context["mocked_file"](), indent=2
    )


@when("I open the app")
def action(context):
    with patch(
        "builtins.open", mock_open(read_data=str(context["tasks"]))
    ) as mocked_file:
        with patch("json.load") as mocked_json_load:
            mocked_json_load.return_value = context["tasks"]
            loaded_tasks = load_tasks(context["file_path"])
            context["loaded_tasks"] = loaded_tasks
            context["mocked_file"] = mocked_file
            context["mocked_json_load"] = mocked_json_load


@then("my task list should be loaded")
def outcome(context):
    assert context["loaded_tasks"] == context["tasks"]
    context["mocked_file"].assert_called_once_with(context["file_path"], "r")
    context["mocked_json_load"].assert_called_once_with(
        context["mocked_file"].return_value
    )


@when("I filter tasks with the Work category")
def action(context):
    context["filtered_tasks"] = filter_tasks_by_category(context["tasks"], "Work")


@then("only tasks with the Work category should be displayed")
def outcome(context):
    assert context["filtered_tasks"] == [context["task1"], context["task4"]]


@when("I filter tasks with the High priority")
def action(context):
    context["filtered_tasks"] = filter_tasks_by_priority(context["tasks"], "High")


@then("only tasks with the High priority should be displayed")
def outcome(context):
    assert context["filtered_tasks"] == [
        context["task1"],
        context["task2"],
        context["task4"],
    ]
