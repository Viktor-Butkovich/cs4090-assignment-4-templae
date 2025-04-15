import pytest
from pytest_bdd import scenarios, given, when, then

scenarios("../echo.feature")

def echo(message):
    return message

@pytest.fixture
def context():
    return {}

@given("a message 'Hello, World'")
def precondition(context):
    context["message"] = "Hello, World!"


@when("the message is echoed")
def action(context):
    context["result"] = echo(context["message"])


@then("the output should be 'Hello, World'")
def outcome(context):
    assert context["result"] == context["message"]
