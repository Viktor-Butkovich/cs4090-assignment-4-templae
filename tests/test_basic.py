from unittest.mock import patch, mock_open
from tasks import (
    save_tasks,
    load_tasks,
)


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

    with patch(
        "builtins.open",
        mock_open(
            read_data='[{"id": 1, "title": "Task 1"}, {"id": 2, "title": "Task 2"}]'
        ),
    ) as mocked_file:
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

    output = capfd.readouterr()  # Captures stdout and stderr
    # Assert correct stdout text
    assert (
        "Warning: corrupted_file.json contains invalid JSON. Creating new tasks list."
        in output.out
    )
