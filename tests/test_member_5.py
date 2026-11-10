import pytest
from playwright.sync_api import Page, expect

URL = "https://demo.playwright.dev/todomvc/"
LOGIN_URL = "https://the-internet.herokuapp.com/login"


# ---------- Guided cases (supplied code) ----------

def test_add_task(page: Page):
    page.goto(URL)

    task_input = page.get_by_placeholder(
        "What needs to be done?",
        exact=True,
    )
    task_items = page.locator(".todo-list li")
    task_labels = task_items.locator("label")

    expect(task_items).to_have_count(0)

    task_input.fill("Read testing notes")
    task_input.press("Enter")

    expect(task_items).to_have_count(1)
    expect(task_labels).to_have_text(["Read testing notes"])
    expect(task_input).to_have_value("")


def test_complete_task(page: Page):
    page.goto(URL)

    task_input = page.get_by_placeholder(
        "What needs to be done?",
        exact=True,
    )
    task_items = page.locator(".todo-list li")

    expect(task_items).to_have_count(0)

    task_input.fill("Practise automated testing")
    task_input.press("Enter")

    expect(task_items).to_have_count(1)

    checkbox = task_items.first.get_by_role("checkbox")
    checkbox.check()
    expect(checkbox).to_be_checked()

    page.get_by_role("link", name="Completed", exact=True).click()

    expect(task_items).to_have_count(1)
    expect(task_items.locator("label")).to_have_text(
        ["Practise automated testing"]
    )


@pytest.mark.parametrize(
    "task_text",
    ["", " ", "   "],
    ids=["empty", "one-space", "three-spaces"],
)
def test_blank_task_is_not_added(page: Page, task_text: str):
    page.goto(URL)

    task_input = page.get_by_placeholder(
        "What needs to be done?",
        exact=True,
    )
    task_items = page.locator(".todo-list li")

    expect(task_items).to_have_count(0)

    task_input.fill(task_text)
    task_input.press("Enter")

    expect(task_items).to_have_count(0)


def test_login_with_correct_details(page: Page):
    page.goto(LOGIN_URL)

    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").fill("SuperSecretPassword!")
    page.get_by_role("button", name="Login").click()

    expect(
        page.get_by_role(
            "heading",
            name="Secure Area",
            exact=True,
        )
    ).to_be_visible()


def test_login_with_incorrect_password(page: Page):
    page.goto(LOGIN_URL)

    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").fill("WrongPassword123")
    page.get_by_role("button", name="Login").click()

    expect(
        page.get_by_text("Your password is invalid!")
    ).to_be_visible()

    expect(
        page.get_by_role("button", name="Login")
    ).to_be_visible()


def add_task(page: Page, task_name: str):
    task_input = page.get_by_placeholder(
        "What needs to be done?",
        exact=True,
    )
    task_input.fill(task_name)
    task_input.press("Enter")


def test_add_two_tasks(page: Page):
    page.goto(URL)
    task_items = page.locator(".todo-list li")

    expect(task_items).to_have_count(0)

    add_task(page, "Read the instructions")
    add_task(page, "Practise the examples")

    expect(task_items).to_have_count(2)
    expect(task_items.locator("label")).to_have_text(
        ["Read the instructions", "Practise the examples"]
    )


# ---------- Member 5 additional tests ----------
# Scenario 1: cancelling an edit with Escape keeps the original name.
# Scenario 2: login rejection for an incorrect USERNAME (valid password).
# Confirm both with your group and record them in docs/test-plan.md.

def test_escape_cancels_task_edit(page: Page):
    page.goto(URL)
    task_items = page.locator(".todo-list li")
    task_labels = task_items.locator("label")

    add_task(page, "Original task name")
    add_task(page, "Second task name")
    expect(task_items).to_have_count(2)

    # Start editing the first task by double-clicking its label.
    task_labels.first.dblclick()
    edit_box = task_items.first.locator(".edit")
    expect(edit_box).to_be_visible()

    edit_box.fill("Changed but cancelled")
    edit_box.press("Escape")

    # The original name must remain and the draft text must not appear.
    expect(task_items).to_have_count(2)
    expect(task_labels).to_have_text(
        ["Original task name", "Second task name"]
    )
    expect(page.get_by_text("Changed but cancelled")).to_have_count(0)

    page.screenshot(
        path="docs/evidence/member-5/extra-test-1-escape-cancel-edit.png",
        full_page=True,
    )


def test_login_with_incorrect_username(page: Page):
    page.goto(LOGIN_URL)

    page.get_by_label("Username").fill("notauser")
    page.get_by_label("Password").fill("SuperSecretPassword!")
    page.get_by_role("button", name="Login").click()

    expect(page.get_by_text("Your username is invalid!")).to_be_visible()
    expect(
        page.get_by_role("heading", name="Secure Area", exact=True)
    ).to_have_count(0)
    expect(page.get_by_role("button", name="Login")).to_be_visible()

    page.screenshot(
        path="docs/evidence/member-5/extra-test-2-wrong-username.png",
        full_page=True,
    )
