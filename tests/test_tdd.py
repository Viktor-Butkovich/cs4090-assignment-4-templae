import pytest
import os
from unittest.mock import patch, MagicMock
from tasks import delete_tasks, save_tasks


@patch("os.remove")
@patch("os.path.exists", return_value=True)
def test_delete_tasks_calls_os_remove(mock_path_exists, mock_remove):
    task_file = "test_tasks.json"

    delete_tasks(task_file)

    mock_remove.assert_called_once_with(task_file)

@patch("os.remove")
@patch("os.path.exists", return_value=False)
def test_delete_tasks_file_missing(mock_path_exists, mock_remove):
    task_file = "invalid_file"

    delete_tasks(task_file)

    mock_remove.assert_not_called()

def test_delete_tasks_removes_file():
    task_file = "test_tasks.json"
    if os.path.exists(task_file):
        os.remove(task_file)
    save_tasks([{"id": 1, "title": "Task 1"}, {"id": 2, "title": "Task 2"}], task_file)
    assert os.path.exists(task_file)
    delete_tasks(task_file)
    assert not os.path.exists(task_file)
