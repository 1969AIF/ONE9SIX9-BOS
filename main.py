"""Application entry point for ONE9SIX9 Business Operating System."""

from pathlib import Path

import customtkinter as ctk

from src.app import MainWindow
from src.services.excel_service import ExcelService


def main() -> None:
    """Initialize and run the application."""
    project_root = Path(__file__).resolve().parent
    ExcelService.initialize(project_root)

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
