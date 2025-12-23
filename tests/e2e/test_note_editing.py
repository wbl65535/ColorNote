import pytest
from playwright.sync_api import Page, expect

def test_edit_note_functionality(page: Page):
    """Test the complete note editing workflow"""
    page.goto("http://localhost:3000")

    # Wait for app to load
    page.wait_for_selector("#app")

    note_cards = page.locator("[data-testid='note-card'], .note-card")

    if note_cards.count() == 0:
        # Create a note first if none exist
        create_button = page.locator("button[aria-label*='create'], button:has-text('+')").first
        create_button.click()

        page.wait_for_selector("[data-testid='create-panel'], .fixed.inset-0")

        title_input = page.locator("input[placeholder*='Title'], input[placeholder*='标题']").first
        content_input = page.locator("textarea[placeholder*='content'], textarea[placeholder*='写下你的想法']").first

        title_input.fill("Note to Edit")
        content_input.fill("This note will be edited")

        save_button = page.locator("button:has-text('Save'), button:has-text('保存')").first
        save_button.click()

        page.wait_for_selector("[data-testid='create-panel'], .fixed.inset-0", state="hidden")

    # Now edit the first note
    note_cards = page.locator("[data-testid='note-card'], .note-card")
    first_card = note_cards.first

    # Store original content
    original_title = first_card.locator("h3").text_content()

    # Click to edit
    first_card.click()

    # Wait for edit panel
    page.wait_for_selector("[data-testid='edit-panel'], .fixed.inset-0")

    # Modify content
    title_input = page.locator("input[placeholder*='Title'], input[placeholder*='标题']").first
    content_input = page.locator("textarea[placeholder*='content'], textarea[placeholder*='写下你的想法']").first

    title_input.clear()
    title_input.fill("Edited Note Title")

    content_input.clear()
    content_input.fill("This note has been edited through E2E testing")

    # Change color
    color_buttons = page.locator("button[title*='Green'], button[aria-label*='Green']")
    if color_buttons.count() > 0:
        color_buttons.first.click()

    # Save changes
    save_button = page.locator("button:has-text('Update'), button:has-text('更新')").first
    save_button.click()

    # Wait for panel to close
    page.wait_for_selector("[data-testid='edit-panel'], .fixed.inset-0", state="hidden")

    # Verify changes in the list
    updated_card = page.locator("[data-testid='note-card'], .note-card").first
    expect(updated_card).to_contain_text("Edited Note Title")

def test_edit_panel_validation(page: Page):
    """Test validation in the edit panel"""
    page.goto("http://localhost:3000")

    note_cards = page.locator("[data-testid='note-card'], .note-card")

    if note_cards.count() > 0:
        # Click first note to edit
        note_cards.first.click()

        page.wait_for_selector("[data-testid='edit-panel'], .fixed.inset-0")

        # Clear title field
        title_input = page.locator("input[placeholder*='Title'], input[placeholder*='标题']").first
        title_input.clear()

        # Save button should be disabled
        save_button = page.locator("button:has-text('Update'), button:has-text('更新')").first
        expect(save_button).to_be_disabled()

        # Fill title back
        title_input.fill("Valid Title")
        expect(save_button).to_be_enabled()

def test_cancel_edit_operation(page: Page):
    """Test canceling an edit operation"""
    page.goto("http://localhost:3000")

    note_cards = page.locator("[data-testid='note-card'], .note-card")

    if note_cards.count() > 0:
        first_card = note_cards.first
        original_title = first_card.locator("h3").text_content()

        # Click to edit
        first_card.click()

        page.wait_for_selector("[data-testid='edit-panel'], .fixed.inset-0")

        # Modify title
        title_input = page.locator("input[placeholder*='Title'], input[placeholder*='标题']").first
        title_input.clear()
        title_input.fill("Modified Title")

        # Cancel instead of save
        cancel_button = page.locator("button:has-text('Cancel'), button:has-text('取消')").first
        cancel_button.click()

        # Panel should close
        page.wait_for_selector("[data-testid='edit-panel'], .fixed.inset-0", state="hidden")

        # Title should be unchanged
        expect(first_card).to_contain_text(original_title)

def test_color_selection_in_edit(page: Page):
    """Test color selection functionality in edit mode"""
    page.goto("http://localhost:3000")

    note_cards = page.locator("[data-testid='note-card'], .note-card")

    if note_cards.count() > 0:
        # Click to edit
        note_cards.first.click()

        page.wait_for_selector("[data-testid='edit-panel'], .fixed.inset-0")

        # Find color selection buttons
        color_buttons = page.locator("button[aria-label*='color'], button[title*='color']")

        if color_buttons.count() > 0:
            # Click a different color
            first_color_button = color_buttons.first
            first_color_button.click()

            # Panel background should change (if implemented)
            # This is a basic check - more detailed color testing would require visual comparison

            # Save the change
            save_button = page.locator("button:has-text('Update'), button:has-text('更新')").first
            save_button.click()

            page.wait_for_selector("[data-testid='edit-panel'], .fixed.inset-0", state="hidden")

            # Note should still be visible
            expect(note_cards.first).to_be_visible()
