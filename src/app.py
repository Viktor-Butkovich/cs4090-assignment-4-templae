import streamlit as st
import subprocess
import pandas as pd
from datetime import datetime
from tasks import (
    add_task,
    load_tasks,
    save_tasks,
    filter_tasks_by_priority,
    filter_tasks_by_category,
    delete_tasks,
    export_to_csv_bytes,
    get_num_pages,
    get_paginated_tasks,
)


def run_script(script):
    return subprocess.run(script.split(), capture_output=True, text=True)

def display_test_output(result):
    if result.returncode == 0:
        st.success("All tests passed!")
    else:
        st.error("Some tests failed. Check the output below.")
    st.sidebar.text_area("Test Output", result.stdout + result.stderr)

def main():
    st.title("To-Do Application")

    # Load existing tasks
    tasks = load_tasks()

    # Sidebar for adding new tasks
    st.sidebar.header("Add New Task")

    # Task creation form
    with st.sidebar.form("new_task_form"):
        task_title = st.text_input("Task Title")
        task_description = st.text_area("Description")
        task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        task_category = st.selectbox(
            "Category", ["Work", "Personal", "School", "Other"]
        )
        task_due_date = st.date_input("Due Date")
        submit_button = st.form_submit_button("Add Task")

        if submit_button and task_title:
            tasks = add_task(tasks, task_title, task_description, task_priority, task_category, task_due_date.strftime("%Y-%m-%d"))
            save_tasks(tasks)
            st.sidebar.success("Task added successfully!")

    for button_label, script in [
        ("Run Unit Tests (All Functionality)", "python -m pytest --cov src --cov-report term-missing -s --cov-report=html"),
        ("Run Unit Tests (pytest-cov)", "python -m pytest --cov src --cov-report term-missing -s"),
        ("Run BDD Tests", "python -m pytest tests/feature/steps --cov-report term-missing -s --cov-report=html -vv"),
    ]:
        if st.sidebar.button(button_label):
            with st.spinner(f"Running unit tests..."):
                result = run_script(script)
                display_test_output(result)

    # Main area to display tasks
    st.header("Your Tasks")

    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        filter_category = st.selectbox(
            "Filter by Category",
            ["All"] + list(set([task["category"] for task in tasks])),
        )
    with col2:
        filter_priority = st.selectbox(
            "Filter by Priority", ["All", "High", "Medium", "Low"]
        )

    show_completed = st.checkbox("Show Completed Tasks")

    # Apply filters
    filtered_tasks = tasks.copy()
    if filter_category != "All":
        filtered_tasks = filter_tasks_by_category(filtered_tasks, filter_category)
    if filter_priority != "All":
        filtered_tasks = filter_tasks_by_priority(filtered_tasks, filter_priority)
    if not show_completed:
        filtered_tasks = [task for task in filtered_tasks if not task["completed"]]

    # Display tasks
    tasks_per_page = 5
    current_page = st.number_input(
        "Page", min_value=1, max_value=get_num_pages(filtered_tasks, tasks_per_page), value=1, step=1, format="%d"
    )
    
    for task in get_paginated_tasks(current_page, filtered_tasks, tasks_per_page):
        col1, col2 = st.columns([4, 1])
        with col1:
            if task["completed"]:
                st.markdown(f"~~**{task['title']}**~~")
            else:
                st.markdown(f"**{task['title']}**")
            st.write(task["description"])
            st.caption(
                f"Due: {task['due_date']} | Priority: {task['priority']} | Category: {task['category']}"
            )
        with col2:
            if st.button(
                "Complete" if not task["completed"] else "Undo",
                key=f"complete_{task['id']}",
            ):
                for t in tasks:
                    if t["id"] == task["id"]:
                        t["completed"] = not t["completed"]
                        save_tasks(tasks)
                        st.rerun()
            if st.button("Delete", key=f"delete_{task['id']}"):
                tasks = [t for t in tasks if t["id"] != task["id"]]
                save_tasks(tasks)
                st.rerun()

    if st.button("Delete all tasks"):
        delete_tasks()
        st.rerun()
    
    st.download_button(
        label="Download CSV",
        data=export_to_csv_bytes(tasks),
        file_name="tasks.csv",
        mime="text/csv",
    )

if __name__ == "__main__":
    main()
