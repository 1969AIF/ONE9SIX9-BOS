"""Tests for startup page selection and project save flow."""

from __future__ import annotations

import customtkinter as ctk
from pathlib import Path

from src.app import MainWindow
from src.services.excel_service import ExcelService
from src.ui.components.new_project_dialog import NewProjectDialog


def test_startup_opens_dashboard() -> None:
    ctk.set_appearance_mode("dark")

    root = MainWindow()
    root.update()

    dashboard = root._pages["Dashboard"]
    projects = root._pages["Projects"]

    assert root._current_page is dashboard
    assert dashboard.winfo_ismapped()
    assert not projects.winfo_ismapped()
    assert root._sidebar._active_item == "Dashboard"

    root.destroy()
    print("PASS: startup opens Dashboard")


def test_save_project_persists() -> None:
    project_root = Path(__file__).resolve().parent.parent
    ExcelService.initialize(project_root)

    code = "TEST-BUGFIX-001"
    name = "Bugfix Verification Project"

    ExcelService.add_project(code, name, "Active")
    ExcelService._workbook = None
    ExcelService.initialize(project_root)

    projects = ExcelService.get_projects()
    assert any(p.project_code == code and p.project_name == name for p in projects)

    print("PASS: project save persists across reload")


def test_dialog_validation_and_cancel() -> None:
    ctk.set_appearance_mode("dark")

    saved: list[tuple[str, str, str]] = []

    root = ctk.CTk()
    root.withdraw()

    dialog = NewProjectDialog(root, on_save=lambda c, n, s: saved.append((c, n, s)))
    root.update()

    assert dialog.winfo_exists()
    save_buttons = [
        child
        for child in dialog.winfo_children()[0].winfo_children()
        if getattr(child, "_text", None) == "Save"
    ]
    footer = [child for child in dialog.winfo_children() if isinstance(child, ctk.CTkFrame)][-1]
    button_texts = []
    for child in footer.winfo_children():
        if isinstance(child, ctk.CTkButton):
            button_texts.append(child.cget("text"))

    assert "Save" in button_texts
    assert "Cancel" in button_texts

    dialog._handle_save()
    root.update()
    assert not saved
    assert dialog.winfo_exists()

    dialog._code_entry.insert(0, "VAL-001")
    dialog._name_entry.insert(0, "Validated Project")
    dialog._handle_save()
    root.update()

    assert not dialog.winfo_exists()
    assert saved == [("VAL-001", "Validated Project", "Active")]

    saved.clear()
    dialog2 = NewProjectDialog(root, on_save=lambda c, n, s: saved.append((c, n, s)))
    root.update()
    dialog2._code_entry.insert(0, "SHOULD-NOT-SAVE")
    dialog2._name_entry.insert(0, "Cancelled")
    dialog2._handle_cancel()
    root.update()

    assert not dialog2.winfo_exists()
    assert saved == []

    root.destroy()
    print("PASS: dialog validation, save, and cancel")


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    ExcelService.initialize(project_root)

    test_startup_opens_dashboard()
    test_save_project_persists()
    test_dialog_validation_and_cancel()
    print("All tests passed.")
