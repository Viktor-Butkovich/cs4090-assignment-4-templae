import pytest
import os
import pandas as pd
import io
from unittest.mock import patch, MagicMock
from tasks import delete_tasks, save_tasks, export_to_csv_bytes


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

@patch("pandas.DataFrame", return_value=MagicMock())
@patch("io.BytesIO", return_value=MagicMock())
def test_export_to_csv_bytes_calls_to_csv(mock_bytes_io, mock_dataframe):
    export_to_csv_bytes(tasks)
    mock_dataframe.assert_called_once_with(tasks)
    mock_dataframe.return_value.to_csv.assert_called_once()
    
def test_export_to_csv_bytes_output():
    csv_bytes = export_to_csv_bytes(tasks)
    csv_buffer = io.BytesIO(csv_bytes)
    csv_buffer.seek(0)
    bytes_df = pd.read_csv(csv_buffer)
    original_df = pd.DataFrame(tasks)
    assert bytes_df.equals(original_df)
