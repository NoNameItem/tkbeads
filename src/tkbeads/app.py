"""TkbeadsApp - main application class."""

from pathlib import Path
from typing import ClassVar

from textual.app import App
from textual.binding import Binding, BindingType


class TkbeadsApp(App):
    """TUI application for viewing Beads tasks."""

    TITLE = "tkbeads"
    CSS_PATH = Path(__file__).parent / "styles" / "app.tcss"

    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("q", "quit", "Quit"),
    ]
