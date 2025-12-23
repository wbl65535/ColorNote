import pytest
from playwright.sync_api import Page, expect

def test_complete_crud_workflow(page: Page):
    """Test the complete CRUD workflow: Create, Read, Update, Delete"""
    page.goto("http://localhost:3000")

    # Wait for app to load
    page.wait_for_selector("#app")

    # === CREATE ===
    # Click create button
    create_button = page.locator("button[aria-label*='create'], button:has-text('+')").first
    create_button.click()

    # Wait for create panel
    page.wait_for_selector("[data-testid='create-panel'], .fixed.inset-0")

    # Fill note details
    title_input = page.locator("input[placeholder*='Title'], input[placeholder*='标题']").first
    content_input = page.locator("textarea[placeholder*='content'], textarea[placeholder*='写下你的想法']").first

    test_title = "CRUD Test Note"
    test_content = "This note will go through the complete CRUD workflow"

    title_input.fill(test_title)
    content_input.fill(test_content)

    # Select blue color
    blue_button = page.locator("button[title*='Blue'], button[aria-label*='Blue']")
    if blue_button.count() > 0:
        blue_button.click()

    # Save the note
    save_button = page.locator("button:has-text('Save'), button:has-text('保存')").first
    save_button.click()

    # Wait for panel to close
    page.wait_for_selector("[data-testid='create-panel'], .fixed.inset-0", state="hidden")

    # === READ ===
    # Verify note appears in list
    note_cards = page.locator("[data-testid='note-card'], .note-card")
    created_note = note_cards.locator(f"text={test_title}").first
    expect(created_note).to_be_visible()

    # === UPDATE ===
    # Click the note to edit
    created_note.click()

    # Wait for edit panel
    page.wait_for_selector("[data-testid='edit-panel'], .fixed.inset-0")

    # Modify the content
    title_input = page.locator("input[placeholder*='Title'], input[placeholder*='标题']").first
    content_input = page.locator("textarea[placeholder*='content'], textarea[placeholder*='写下你的想法']").first

    title_input.clear()
    title_input.fill("Updated CRUD Test Note")

    content_input.clear()
    content_input.fill("This note has been updated through the CRUD workflow")

    # Change to green color
    green_button = page.locator("button[title*='Green'], button[aria-label*='Green']")
    if green_button.count() > 0:
        green_button.click()

    # Save changes
    update_button = page.locator("button:has-text('Update'), button:has-text('更新')").first
    update_button.click()

    # Wait for panel to close
    page.wait_for_selector("[data-testid='edit-panel'], .fixed.inset-0", state="hidden")

    # Verify changes in list
    updated_note = note_cards.locator("text=Updated CRUD Test Note").first
    expect(updated_note).to_be_visible()

    # === DELETE ===
    # Click the note again to open edit panel
    updated_note.click()

    # Wait for edit panel
    page.wait_for_selector("[data-testid='edit-panel'], .fixed.inset-0")

    # Click delete button
    delete_button = page.locator("button:has-text('delete'), button[aria-label*='delete']").first
    delete_button.click()

    # Confirm deletion in modal
    confirm_button = page.locator("button:has-text('Delete'), button:has-text('删除')").first
    confirm_button.click()

    # Wait for modal to close and panel to close
    page.wait_for_selector("[data-testid='delete-modal'], .fixed.inset-0", state="hidden")
    page.wait_for_selector("[data-testid='edit-panel'], .fixed.inset-0", state="hidden")

    # Verify note is removed from list
    deleted_note = page.locator("text=Updated CRUD Test Note")
    expect(deleted_note).not_to_be_visible()

def test_multiple_notes_crud(page: Page):
    """Test CRUD operations with multiple notes"""
    page.goto("http://localhost:3000")

    # Create multiple notes
    note_data = [
        {"title": "Note Alpha", "content": "First note in series"},
        {"title": "Note Beta", "content": "Second note in series"},
        {"title": "Note Gamma", "content": "Third note in series"}
    ]

    for i, data in enumerate(note_data):
        # Click create
        create_button = page.locator("button[aria-label*='create'], button:has-text('+')").first
        create_button.click()

        page.wait_for_selector("[data-testid='create-panel'], .fixed.inset-0")

        # Fill details
        title_input = page.locator("input[placeholder*='Title'], input[placeholder*='标题']").first
        content_input = page.locator("textarea[placeholder*='content'], textarea[placeholder*='写下你的想法']").first

        title_input.fill(data["title"])
        content_input.fill(data["content"])

        # Save
        save_button = page.locator("button:has-text('Save'), button:has-text('保存')").first
        save_button.click()

        page.wait_for_selector("[data-testid='create-panel'], .fixed.inset-0", state="hidden")

    # Verify all notes are visible
    for data in note_data:
        note_card = page.locator(f"text={data['title']}")
        expect(note_card).to_be_visible()

    # Verify order (newest first)
    note_cards = page.locator("[data-testid='note-card'], .note-card")
    expect(note_cards.nth(0)).to_contain_text("Note Gamma")  # Newest
    expect(note_cards.nth(1)).to_contain_text("Note Beta")   # Middle
    expect(note_cards.nth(2)).to_contain_text("Note Alpha")  # Oldest

def test_crud_error_handling(page: Page):
    """Test error handling in CRUD operations"""
    page.goto("http://localhost:3000")

    # Test create with network error simulation (if possible)
    # Test update of non-existent note (if UI allows)
    # Test delete of non-existent note (if UI allows)

    # For now, test basic validation
    create_button = page.locator("button[aria-label*='create'], button:has-text('+')").first
    create_button.click()

    page.wait_for_selector("[data-testid='create-panel'], .fixed.inset-0")

    # Try to save without required fields
    save_button = page.locator("button:has-text('Save'), button:has-text('保存')").first

    # Button should be disabled
    expect(save_button).to_be_disabled()

    # Fill content but not title
    content_input = page.locator("textarea[placeholder*='content'], textarea[placeholder*='写下你的想法']").first
    content_input.fill("Content without title")

    # Button should still be disabled
    expect(save_button).to_be_disabled()

def test_crud_ui_state_management(page: Page):
    """Test UI state management during CRUD operations"""
    page.goto("http://localhost:3000")

    # Create a note
    create_button = page.locator("button[aria-label*='create'], button:has-text('+')").first
    create_button.click()

    page.wait_for_selector("[data-testid='create-panel'], .fixed.inset-0")

    # Fill and save
    title_input = page.locator("input[placeholder*='Title'], input[placeholder*='标题']").first
    content_input = page.locator("textarea[placeholder*='content'], textarea[placeholder*='写下你的想法']").first

    title_input.fill("State Test Note")
    content_input.fill("Testing UI state management")

    save_button = page.locator("button:has-text('Save'), button:has-text('保存')").first
    save_button.click()

    # Panel should close
    page.wait_for_selector("[data-testid='create-panel'], .fixed.inset-0", state="hidden")

    # FAB should be visible again
    expect(create_button).to_be_visible()

    # Note should be in list
    note_card = page.locator("text=State Test Note")
    expect(note_card).to_be_visible()
