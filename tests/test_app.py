import pytest
from unittest.mock import patch
from app import main

task1 = {"id": 1, "title": "Task 1", "category": "Work", "completed": False, "description": "Task 1 description important", "due_date": "2000-01-15", "priority": "High"}
task2 = {"id": 2, "title": "Task 2 important", "category": "Personal", "completed": True, "description": "Task 2 description", "due_date": "2000-02-25", "priority": "High"}
task3 = {"id": 3, "title": "Task 3", "category": "Personal", "completed": False, "description": "Task 3 description", "due_date": "2000-03-10", "priority": "Medium"}
task4 = {"id": 4, "title": "Task 4 important", "category": "Work", "completed": True, "description": "Task 4 description", "due_date": "2000-04-18", "priority": "High"}
task5 = {"id": 5, "title": "Task 5", "category": "School", "completed": False, "description": "Task 5 description", "due_date": "2000-05-30", "priority": "Low"}
tasks = [task1, task2, task3, task4, task5]

@patch("app.load_tasks", return_value=tasks)
@patch("streamlit.button", return_value=True)
@patch("streamlit.form_submit_button", return_value=True)
@patch("streamlit.text_input", return_value="Hello World")
def test_main(mock_load_tasks, mock_st_button, mock_st_form_submit_button, mock_st_text_input):
    # Note - main is a script that Streamlit uses to re-create the entire app any time any changes are made, updating the UI
    #with patch("app.load_tasks", return_value=mock_tasks):
    main()
