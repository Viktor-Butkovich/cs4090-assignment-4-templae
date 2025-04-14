import pytest
from datetime import datetime
from unittest.mock import patch, mock_open
from tasks import generate_unique_id, save_tasks, load_tasks, filter_tasks_by_category, filter_tasks_by_completion, search_tasks, filter_tasks_by_priority, get_overdue_tasks

@pytest.mark.parametrize(
    "tasks, expected_id",
    [
        ([], 1),
        ([{"id": 1}], 2),
        ([{"id": 2}, {"id": 4}, {"id": 1}], 5),
    ]
)
def test_generate_unique_id(tasks, expected_id): # Calls the function with different inputs and corresponding expected outputs
    assert generate_unique_id(tasks) == expected_id

def test_save_tasks():
    tasks = [{"id": 1, "title": "Task 1"}, {"id": 2, "title": "Task 2"}]
    file_path = "mock_tasks.json"

    with patch("builtins.open", mock_open()) as mocked_file:
        with patch("json.dump") as mocked_json_dump:
            save_tasks(tasks, file_path)

            # Assert that the correct file was opened and received the correct JSON content
            mocked_file.assert_called_once_with(file_path, "w")
            mocked_json_dump.assert_called_once_with(tasks, mocked_file(), indent=2)

def test_load_tasks_successful():
    tasks = [{"id": 1, "title": "Task 1"}, {"id": 2, "title": "Task 2"}]
    file_path = "mock_tasks.json"

    with patch("builtins.open", mock_open(read_data='[{"id": 1, "title": "Task 1"}, {"id": 2, "title": "Task 2"}]')) as mocked_file:
        with patch("json.load") as mocked_json_load:
            mocked_json_load.return_value = tasks
            loaded_tasks = load_tasks(file_path)

            # Assert that the correct file was opened and the correct data was loaded

            mocked_file.assert_called_once_with(file_path, "r")
            mocked_json_load.assert_called_once_with(mocked_file.return_value)

def test_load_tasks_file_not_found():
    file_path = "non_existent_file.json"

    with patch("builtins.open", side_effect=FileNotFoundError):
        tasks = load_tasks(file_path)

        assert tasks == []

def test_load_tasks_json_decode_error(capfd):
    file_path = "corrupted_file.json"

    with patch("builtins.open", mock_open(read_data='[{"id": 1')):
        tasks = load_tasks(file_path)
        assert tasks == []

    output = capfd.readouterr() # Captures stdout and stderr
    # Assert correct stdout text
    assert "Warning: corrupted_file.json contains invalid JSON. Creating new tasks list." in output.out



task1 = {"id": 1, "title": "Task 1", "category": "Work", "completed": False, "description": "Task 1 description important", "due_date": "2000-01-15", "priority": "High"}
task2 = {"id": 2, "title": "Task 2 important", "category": "Personal", "completed": True, "description": "Task 2 description", "due_date": "2000-02-25", "priority": "High"}
task3 = {"id": 3, "title": "Task 3", "category": "Personal", "completed": False, "description": "Task 3 description", "due_date": "2000-03-10", "priority": "Medium"}
task4 = {"id": 4, "title": "Task 4 important", "category": "Work", "completed": True, "description": "Task 4 description", "due_date": "2000-04-18", "priority": "High"}
task5 = {"id": 5, "title": "Task 5", "category": "School", "completed": False, "description": "Task 5 description", "due_date": "2000-05-30", "priority": "Low"}
tasks = [task1, task2, task3, task4, task5]

@pytest.mark.parametrize(
    "category, expected",
    [
        ("Work", [task1, task4]),
        ("Personal", [task2, task3]),
        ("School", [task5]),
        ("Fitness", []),
        ("invalid", []),
    ]
)
def test_filter_tasks_by_category(category, expected):
    assert filter_tasks_by_category(tasks, category) == expected

@pytest.mark.parametrize(
    "completed, expected",
    [
        (True, [task2, task4]),
        (False, [task1, task3, task5]),
        (None, [task2, task4]), # Default behavior is True
    ]
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
    ]
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
    ]
)
def test_filter_tasks_by_priority(priority, expected):
    assert filter_tasks_by_priority(tasks, priority) == expected

@pytest.mark.parametrize(
    "tasks, expected, date",
    [
        (tasks, [task1, task3, task5], "2001-01-01"),
        (tasks, [], "2000-01-01"),
        (tasks, [task1], "2000-03-01"),
    ]
)
def test_get_overdue_tasks(tasks, expected, date):
    with patch("tasks.datetime") as mock_datetime:
        # mock_datetime.datetime.now.return_value = datetime.strptime(date, "%Y-%m-%d")
        mock_datetime.now.return_value = datetime.strptime(date, "%Y-%m-%d")
        mock_datetime.strptime = datetime.strptime
        mock_datetime.date = datetime.date
        assert get_overdue_tasks(tasks) == expected
