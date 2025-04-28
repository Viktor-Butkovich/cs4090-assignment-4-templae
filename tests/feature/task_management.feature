Feature: Task management
  As a user
  I want to manage tasks in my task list
  So that I can track my tasks


  Scenario: Save task
    Given I have a task list
    When I make any changes to the task list
    Then the task list should be saved
  
  Scenario: Load task
    Given I have a task list
    When I open the app
    Then my task list should be loaded

  Scenario: Filter tasks by category
    Given I have a task list
    When I filter tasks with the Work category
    Then only tasks with the Work category should be displayed
  
  Scenario: Filter tasks by priority
    Given I have a task list
    When I filter tasks with the High priority
    Then only tasks with the High priority should be displayed