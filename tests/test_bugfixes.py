"""Tests for startup page selection and project save flow."""

from __future__ import annotations

import customtkinter as ctk
from pathlib import Path

from src.app import MainWindow
from src.services.excel_service import ExcelService
from src.ui.components.new_project_dialog import NewProjectDialog
from src.ui.components.new_expense_dialog import (
    NewExpenseDialog,
    PLACEHOLDER_PROJECT,
)


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


def test_save_category_persists() -> None:
    project_root = Path(__file__).resolve().parent.parent
    ExcelService.initialize(project_root)

    code = "TEST-CAT-001"
    name = "Bugfix Verification Category"

    ExcelService.add_category(code, name)
    ExcelService._workbook = None
    ExcelService.initialize(project_root)

    categories = ExcelService.get_categories()
    assert any(
        c.category_code == code and c.category_name == name for c in categories
    )

    print("PASS: category save persists across reload")


def test_save_expense_persists() -> None:
    project_root = Path(__file__).resolve().parent.parent
    ExcelService.initialize(project_root)

    code = "TEST-EXP-PROJ"
    if not any(p.project_code == code for p in ExcelService.get_projects()):
        ExcelService.add_project(code, "Expense Test Project", "Active")

    ExcelService.add_expense(
        date="01/08/2026",
        supplier="Test Supplier",
        project="TEST-EXP-PROJ",
        category="Test Category",
        invoice_number="INV-001",
        description="Test expense",
        amount_ex_vat=100.0,
        vat=20.0,
        total=120.0,
    )
    ExcelService._workbook = None
    ExcelService.initialize(project_root)

    expenses = ExcelService.get_expenses()
    assert any(
        e.project == "TEST-EXP-PROJ"
        and e.description == "Test expense"
        and float(e.total) == 120.0
        for e in expenses
    )

    print("PASS: expense save persists across reload")


def test_expense_requires_project() -> None:
    ctk.set_appearance_mode("dark")

    project_root = Path(__file__).resolve().parent.parent
    ExcelService.initialize(project_root)

    code = "TEST-EXP-PROJ"
    if not any(p.project_code == code for p in ExcelService.get_projects()):
        ExcelService.add_project(code, "Expense Test Project", "Active")

    saved: list[tuple[object, ...]] = []

    root = ctk.CTk()
    root.withdraw()

    dialog = NewExpenseDialog(
        root,
        on_save=lambda *args: saved.append(args),
    )
    root.update()

    dialog._date_entry.insert(0, "02/08/2026")
    dialog._amount_entry.insert(0, "100")
    assert dialog._project_menu.get() == PLACEHOLDER_PROJECT

    dialog._handle_save()
    root.update()

    assert not saved
    assert dialog.winfo_exists()
    assert "select a project" in dialog._error_label.cget("text").lower()

    dialog._project_menu.set(f"{code} — Expense Test Project")
    dialog._handle_save()
    root.update()

    assert not dialog.winfo_exists()
    assert len(saved) == 1

    root.destroy()
    print("PASS: expense cannot be saved without a project")


def test_dashboard_summary_counts_current_month() -> None:
    from datetime import date

    project_root = Path(__file__).resolve().parent.parent
    ExcelService.initialize(project_root)

    code = "TEST-EXP-PROJ"
    if not any(p.project_code == code for p in ExcelService.get_projects()):
        ExcelService.add_project(code, "Expense Test Project", "Active")

    baseline = ExcelService.get_dashboard_summary()

    today = date.today()
    if today.month == 1:
        last_month = date(today.year - 1, 12, min(today.day, 28))
    else:
        last_month = date(today.year, today.month - 1, min(today.day, 28))

    ExcelService.add_expense(
        date=today.strftime("%d/%m/%Y"),
        supplier="Test Supplier",
        project=code,
        category="",
        invoice_number="",
        description="current month",
        amount_ex_vat=100.0,
        vat=20.0,
        total=120.0,
    )
    ExcelService.add_expense(
        date=last_month.strftime("%d/%m/%Y"),
        supplier="Test Supplier",
        project=code,
        category="",
        invoice_number="",
        description="previous month",
        amount_ex_vat=50.0,
        vat=10.0,
        total=60.0,
    )

    summary = ExcelService.get_dashboard_summary()
    assert summary.expenses_count == baseline.expenses_count + 1
    assert summary.expenses_total == baseline.expenses_total + 120.0
    assert summary.income_total == 0.0
    assert summary.pending_approvals == 0

    print("PASS: dashboard summary counts only the current month")


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
    import shutil

    project_root = Path(__file__).resolve().parent.parent
    workbook_path = project_root / "ONE9SIX9.xlsx"
    backup_path = project_root / "ONE9SIX9.test-backup.xlsx"
    shutil.copy2(workbook_path, backup_path)

    try:
        ExcelService.initialize(project_root)

        test_startup_opens_dashboard()
        test_save_project_persists()
        test_save_category_persists()
        test_save_expense_persists()
        test_expense_requires_project()
        test_dashboard_summary_counts_current_month()
        test_dialog_validation_and_cancel()
        print("All tests passed.")
    finally:
        shutil.copy2(backup_path, workbook_path)
        backup_path.unlink()
        ExcelService._workbook = None
