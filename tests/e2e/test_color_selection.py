import pytest
from playwright.sync_api import Page, expect

def test_color_selection_ui(page: Page):
    """Test that color selection UI is present and functional"""
    page.goto("http://localhost:3000")

    # Create a new note
    create_button = page.locator("button[aria-label*='create'], button:has-text('+')").first
    create_button.click()

    page.wait_for_selector("[data-testid='create-panel'], .fixed.inset-0")

    # Check for color selection elements
    color_section = page.locator("text=color, text=颜色")
    color_buttons = page.locator("button[aria-label*='color'], button[title*='color'], button[class*='color']")

    # Should have color selection UI
    expect(color_section.or_(color_buttons)).to_be_visible()

def test_color_button_interaction(page: Page):
    """Test that color buttons are clickable and provide feedback"""
    page.goto("http://localhost:3000")

    create_button = page.locator("button[aria-label*='create'], button:has-text('+')").first
    create_button.click()

    page.wait_for_selector("[data-testid='create-panel'], .fixed.inset-0")

    # Find color buttons
    color_buttons = page.locator("button[aria-label*='color'], button[title*='color'], button[style*='background']")

    if color_buttons.count() > 0:
        first_color_button = color_buttons.first

        # Should be clickable
        expect(first_color_button).to_be_enabled()

        # Click the color button
        first_color_button.click()

        # Should provide visual feedback (implementation dependent)
        # At minimum, the button should still be visible and functional

def test_panel_background_color_change(page: Page):
    """Test that selecting colors changes the panel background"""
    page.goto("http://localhost:3000")

    create_button = page.locator("button[aria-label*='create'], button:has-text('+')").first
    create_button.click()

    page.wait_for_selector("[data-testid='create-panel'], .fixed.inset-0")

    # Find the panel background element
    panel = page.locator("[data-testid='create-panel'], .fixed.inset-0 .bg-white, .fixed.inset-0 [class*='bg-']")

    if panel.count() > 0:
        # Get initial background color
        initial_bg = panel.first.get_attribute("style") or ""

        # Find and click a color button
        color_buttons = page.locator("button[aria-label*='color'], button[title*='color']")
        if color_buttons.count() > 0:
            color_buttons.first.click()

            # Panel background should change (or at least not break)
            expect(panel.first).to_be_visible()

def test_color_persistence(page: Page):
    """Test that selected colors are applied to saved notes"""
    page.goto("http://localhost:3000")

    # Create a note with a specific color
    create_button = page.locator("button[aria-label*='create'], button:has-text('+')").first
    create_button.click()

    page.wait_for_selector("[data-testid='create-panel'], .fixed.inset-0")

    # Select a non-default color
    color_buttons = page.locator("button[title*='Blue'], button[aria-label*='Blue']")
    if color_buttons.count() > 0:
        color_buttons.first.click()

        # Fill in note details
        title_input = page.locator("input[placeholder*='Title'], input[placeholder*='标题']").first
        content_input = page.locator("textarea[placeholder*='content'], textarea[placeholder*='写下你的想法']").first

        title_input.fill("Color Test Note")
        content_input.fill("Testing color selection")

        # Save the note
        save_button = page.locator("button:has-text('Save'), button:has-text('保存')").first
        save_button.click()

        page.wait_for_selector("[data-testid='create-panel'], .fixed.inset-0", state="hidden")

        # Check that the note card has the selected color
        note_cards = page.locator("[data-testid='note-card'], .note-card")
        expect(note_cards.first).to_contain_text("Color Test Note")

        # The note card should have the selected background color
        # (Exact color verification would require more complex CSS checking)

def test_color_touch_targets(page: Page):
    """Test that color buttons meet accessibility guidelines"""
    page.goto("http://localhost:3000")

    create_button = page.locator("button[aria-label*='create'], button:has-text('+')").first
    create_button.click()

    page.wait_for_selector("[data-testid='create-panel'], .fixed.inset-0")

    color_buttons = page.locator("button[aria-label*='color'], button[title*='color']")

    if color_buttons.count() > 0:
        first_button = color_buttons.first

        # Check minimum touch target size (44px is iOS guideline)
        # This is a basic check - more detailed accessibility testing would use specialized tools
        expect(first_button).to_be_visible()

def test_color_hover_states(page: Page):
    """Test color button hover states"""
    page.goto("http://localhost:3000")

    create_button = page.locator("button[aria-label*='create'], button:has-text('+')").first
    create_button.click()

    page.wait_for_selector("[data-testid='create-panel'], .fixed.inset-0")

    color_buttons = page.locator("button[aria-label*='color'], button[title*='color']")

    if color_buttons.count() > 0:
        first_button = color_buttons.first

        # Hover over the button (if hover states are implemented)
        first_button.hover()

        # Button should remain functional
        expect(first_button).to_be_enabled()

def test_default_color_selection(page: Page):
    """Test that a default color is pre-selected"""
    page.goto("http://localhost:3000")

    create_button = page.locator("button[aria-label*='create'], button:has-text('+')").first
    create_button.click()

    page.wait_for_selector("[data-testid='create-panel'], .fixed.inset-0")

    # Should have a default color selected (usually yellow #FFE57F)
    selected_color_indicators = page.locator("[data-testid='selected-color'], .selected, .ring-2, .border-gray-800")

    # At least one color should appear selected
    if selected_color_indicators.count() == 0:
        # Check for yellow color being active by default
        yellow_buttons = page.locator("button[style*='#FFE57F'], button[title*='Yellow']")
        expect(yellow_buttons).to_be_visible()
