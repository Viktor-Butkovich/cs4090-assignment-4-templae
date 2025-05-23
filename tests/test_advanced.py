import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
from src.tasks import (
    generate_unique_id,
    filter_tasks_by_category,
    filter_tasks_by_completion,
    search_tasks,
    filter_tasks_by_priority,
    get_overdue_tasks,
)


@pytest.mark.parametrize(
    "tasks, expected_id",
    [
        ([], 1),
        ([{"id": 1}], 2),
        ([{"id": 2}, {"id": 4}, {"id": 1}], 5),
    ],
)
def test_generate_unique_id(
    tasks, expected_id
):  # Calls the function with different inputs and corresponding expected outputs
    assert generate_unique_id(tasks) == expected_id


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
tasks = [task1, task2, task3, task4, task5]


@pytest.mark.parametrize(
    "category, expected",
    [
        ("Work", [task1, task4]),
        ("Personal", [task2, task3]),
        ("School", [task5]),
        ("Fitness", []),
        ("invalid", []),
    ],
)
def test_filter_tasks_by_category(category, expected):
    assert filter_tasks_by_category(tasks, category) == expected


@pytest.mark.parametrize(
    "completed, expected",
    [
        (True, [task2, task4]),
        (False, [task1, task3, task5]),
        (None, [task2, task4]),  # Default behavior is True
    ],
)
def test_filter_tasks_by_completion(completed, expected):
    if completed is None:
        assert filter_tasks_by_completion(tasks) == expected
    else:
        assert filter_tasks_by_completion(tasks, completed) == expected


@pytest.mark.parametrize(
    "query, expected",
    [
        ("important", [task1, task2, task4]),
        ("Task 1", [task1]),
        ("invalid", []),
    ],
)
def test_search_tasks(query, expected):
    assert search_tasks(tasks, query) == expected


@pytest.mark.parametrize(
    "priority, expected",
    [
        ("High", [task1, task2, task4]),
        ("Medium", [task3]),
        ("Low", [task5]),
        ("invalid", []),
    ],
)
def test_filter_tasks_by_priority(priority, expected):
    assert filter_tasks_by_priority(tasks, priority) == expected


@pytest.mark.parametrize(
    "tasks, expected, date",
    [
        (tasks, [task1, task3, task5], "2001-01-01"),
        (tasks, [], "2000-01-01"),
        (tasks, [task1], "2000-03-01"),
    ],
)
def test_get_overdue_tasks(tasks, expected, date):
    with patch("src.tasks.datetime") as mock_datetime:
        # mock_datetime.datetime.now.return_value = datetime.strptime(date, "%Y-%m-%d")
        mock_datetime.now.return_value = datetime.strptime(date, "%Y-%m-%d")
        mock_datetime.strptime = datetime.strptime
        mock_datetime.date = datetime.date
        assert get_overdue_tasks(tasks) == expected


@patch("src.app.load_tasks", return_value=tasks)
@patch("src.app.save_tasks")
@patch("src.app.delete_tasks")
@patch("src.app.subprocess.run")
@patch("src.app.get_paginated_tasks", return_value=tasks)
def test_main(
    mock_get_paginated_tasks,
    mock_subprocess,
    mock_delete_tasks,
    mock_save_tasks,
    mock_load_tasks,
):
    with patch("src.app.st") as mock_streamlit:
        mock_streamlit.columns.return_value = [MagicMock(), MagicMock()]

        from src.app import (
            main,
        )  # Must be imported here for st module to mock correctly

        # Run test as if all buttons pressed and all forms filled
        # Note - main is a script that Streamlit uses to re-create the entire app any time any changes are made, updating the UI
        main()
