Feature: Task management
  As a user
  I want to manage tasks in my task list
  So that I can track my tasks


  Scenario: Add task
    Given I have filled the new task form
    When I click the Add Task button
    Then the task should be added to the task list