"""Entry point for python -m tkbeads."""

from tkbeads.app import TkbeadsApp


def main() -> None:
    """Run the application."""
    app = TkbeadsApp()
    app.run()


if __name__ == "__main__":
    main()
