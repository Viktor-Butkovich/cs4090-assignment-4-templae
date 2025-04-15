Feature: Echo Task
  As a user
  I want to see an echo of my input
  So that I know the BDD framework is working

  Scenario: Display echoed message
    Given a message 'Hello, World'
    When the message is echoed
    Then the output should be 'Hello, World'