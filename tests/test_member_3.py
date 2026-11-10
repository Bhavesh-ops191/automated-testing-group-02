from playwright.sync_api import Page, expect

URL = "https://demo.playwright.dev/todomvc/"


def test_add_task(page: Page):
    page.goto(URL)

    task_input = page.get_by_placeholder(
        "What needs to be done?",
        exact=True,
    )
    task_items = page.locator(".todo-list li")
    task_labels = task_items.locator("label")

    expect(task_items).to_have_count(0)
    page.screenshot(
        path="docs/evidence/member-3/guided-add-task-before.png",
        full_page=True,
    )

    task_input.fill("Read testing notes")
    expect(task_input).to_have_value("Read testing notes")
    page.screenshot(
        path="docs/evidence/member-3/guided-add-task-during.png",
        full_page=True,
    )
    task_input.press("Enter")

    expect(task_items).to_have_count(1)
    expect(task_labels).to_have_text(["Read testing notes"])
    expect(task_input).to_have_value("")
    page.screenshot(
        path="docs/evidence/member-3/guided-add-task-after.png",
        full_page=True,
    )