import pytest
from playwright.sync_api import Page, expect

def test_create_note(page: Page):
    """Test creating a new note through the UI"""
    # Navigate to the application
    page.goto("http://localhost:3000")

    # Wait for the app to load
    page.wait_for_selector("#app")

    # Click the create button (floating action button)
    create_button = page.locator("button[aria-label*='create'], button:has-text('+')").first
    create_button.click()

    # Wait for the panel to open
    page.wait_for_selector("[data-testid='create-panel'], .fixed.inset-0")

    # Fill in the note details
    title_input = page.locator("input[placeholder*='Title'], input[placeholder*='标题']").first
    content_input = page.locator("textarea[placeholder*='content'], textarea[placeholder*='写下你的想法']").first

    title_input.fill("E2E Test Note")
    content_input.fill("This note was created during end-to-end testing")

    # Select a color (optional)
    color_buttons = page.locator("button[title*='Blue'], button[aria-label*='Blue']").first
    if color_buttons.count() > 0:
        color_buttons.click()

    # Save the note
    save_button = page.locator("button:has-text('Save'), button:has-text('保存')").first
    save_button.click()

    # Wait for panel to close
    page.wait_for_selector("[data-testid='create-panel'], .fixed.inset-0", state="hidden")

    # Verify the note appears in the list
    note_cards = page.locator("[data-testid='note-card'], .note-card")
    expect(note_cards.first).to_contain_text("E2E Test Note")

def test_create_note_validation(page: Page):
    """Test note creation validation"""
    page.goto("http://localhost:3000")

    # Click create button
    create_button = page.locator("button[aria-label*='create'], button:has-text('+')").first
    create_button.click()

    # Wait for panel
    page.wait_for_selector("[data-testid='create-panel'], .fixed.inset-0")

    # Try to save without title and content
    save_button = page.locator("button:has-text('Save'), button:has-text('保存')").first

    # Button should be disabled when validation fails
    expect(save_button).to_be_disabled()

    # Fill only content, no title
    content_input = page.locator("textarea[placeholder*='content'], textarea[placeholder*='写下你的想法']").first
    content_input.fill("Content without title")

    # Button should still be disabled
    expect(save_button).to_be_disabled()

    # Fill title
    title_input = page.locator("input[placeholder*='Title'], input[placeholder*='标题']").first
    title_input.fill("Valid Title")

    # Button should now be enabled
    expect(save_button).to_be_enabled()

def test_note_list_display(page: Page):
    """Test that notes are displayed correctly in the list"""
    page.goto("http://localhost:3000")

    # Wait for app to load
    page.wait_for_selector("#app")

    # Check if there's an empty state or note list
    empty_state = page.locator("text=No notes yet, text=暂无笔记").first
    note_list = page.locator("[data-testid='note-list'], .grid").first

    # One of them should be visible
    expect(empty_state.or_(note_list)).to_be_visible()

def test_panel_close_functionality(page: Page):
    """Test that the create panel can be closed"""
    page.goto("http://localhost:3000")

    # Click create button
    create_button = page.locator("button[aria-label*='create'], button:has-text('+')").first
    create_button.click()

    # Wait for panel
    page.wait_for_selector("[data-testid='create-panel'], .fixed.inset-0")

    # Click cancel button
    cancel_button = page.locator("button:has-text('Cancel'), button:has-text('取消')").first
    cancel_button.click()

    # Panel should close
    page.wait_for_selector("[data-testid='create-panel'], .fixed.inset-0", state="hidden")

    # Or click outside the panel
    create_button.click()
    page.wait_for_selector("[data-testid='create-panel'], .fixed.inset-0")

    # Click on backdrop (outside panel)
    page.locator(".fixed.inset-0").first.click()

    # Panel should close
    page.wait_for_selector("[data-testid='create-panel'], .fixed.inset-0", state="hidden")
