"""Tests for TkbeadsApp."""

import pytest

from tkbeads.app import TkbeadsApp


@pytest.mark.asyncio
async def test_app_starts_and_quits_on_q():
    """App should start, show title 'tkbeads', and quit when q is pressed."""
    app = TkbeadsApp()
    async with app.run_test() as pilot:
        assert app.is_running
        assert app.title == "tkbeads"
        await pilot.press("q")
    assert not app.is_running
