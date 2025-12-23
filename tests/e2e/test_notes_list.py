import pytest
from playwright.sync_api import Page, expect

def test_notes_list_loads(page: Page):
    """Test that the notes list loads correctly"""
    page.goto("http://localhost:3000")

    # Wait for the app to load (should not show loading forever)
    page.wait_for_selector("#app")

    # Should either show notes or empty state
    expect(page.locator("text=No notes yet").or_(page.locator("[data-testid='note-card']"))).to_be_visible()

def test_empty_state_display(page: Page):
    """Test empty state when no notes exist"""
    page.goto("http://localhost:3000")

    # Wait for app to load
    page.wait_for_selector("#app")

    # Look for empty state elements
    empty_state = page.locator("text=No notes yet, text=暂无笔记")
    if empty_state.count() > 0:
        expect(empty_state.first).to_be_visible()

def test_note_card_structure(page: Page):
    """Test that note cards have the correct structure"""
    page.goto("http://localhost:3000")

    # Wait for app to load
    page.wait_for_selector("#app")

    # Find note cards
    note_cards = page.locator("[data-testid='note-card'], .note-card")

    if note_cards.count() > 0:
        first_card = note_cards.first

        # Should have title
        title = first_card.locator("h3, [data-testid='note-title']")
        expect(title).to_be_visible()

        # Should have content preview
        content = first_card.locator("p, [data-testid='note-content']")
        expect(content).to_be_visible()

        # Should be clickable
        expect(first_card).to_have_attribute("cursor", "pointer")

def test_note_click_opens_edit(page: Page):
    """Test that clicking a note opens the edit panel"""
    page.goto("http://localhost:3000")

    # Wait for app to load
    page.wait_for_selector("#app")

    note_cards = page.locator("[data-testid='note-card'], .note-card")

    if note_cards.count() > 0:
        # Click the first note
        note_cards.first.click()

        # Should open edit panel
        page.wait_for_selector("[data-testid='edit-panel'], .fixed.inset-0")

        # Panel should contain form elements
        title_input = page.locator("input[placeholder*='Title'], input[placeholder*='标题']")
        expect(title_input).to_be_visible()

        content_input = page.locator("textarea[placeholder*='content'], textarea[placeholder*='写下你的想法']")
        expect(content_input).to_be_visible()

def test_responsive_design(page: Page):
    """Test that the layout is responsive"""
    page.goto("http://localhost:3000")

    # Test on mobile viewport
    page.set_viewport_size({"width": 375, "height": 667})

    # App should still be usable
    expect(page.locator("#app")).to_be_visible()

    # Floating action button should be visible
    fab = page.locator("button[aria-label*='create'], button:has-text('+')")
    expect(fab).to_be_visible()

def test_scroll_behavior(page: Page):
    """Test scrolling behavior with many notes"""
    page.goto("http://localhost:3000")

    # Wait for app to load
    page.wait_for_selector("#app")

    # Check if there's a scrollable container
    scrollable_container = page.locator("[data-testid='notes-container'], .overflow-y-auto, .max-h-\\[\\d+\\]")

    # If there are many notes, there should be a scrollable area
    note_cards = page.locator("[data-testid='note-card'], .note-card")
    if note_cards.count() > 5:
        # Should be able to scroll
        expect(scrollable_container).to_be_visible()
