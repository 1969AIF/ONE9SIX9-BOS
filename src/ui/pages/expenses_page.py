"""Expense management page."""

import customtkinter as ctk

from src.config.theme import Theme
from src.services.excel_service import ExcelService, Expense
from src.ui.components.new_expense_dialog import NewExpenseDialog
from src.ui.pages.base_page import BasePage

LIST_COLUMNS = (
    "Date",
    "Supplier",
    "Project",
    "Category",
    "Invoice/Receipt Number",
    "Description",
    "Amount Excl. VAT",
    "VAT",
    "Total Incl. VAT",
)


class ExpensesPage(BasePage):
    """Displays and manages expenses from the Excel workbook."""

    PAGE_TITLE = "Expense Management"

    def __init__(self, master: ctk.CTkBaseClass, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._rows_frame: ctk.CTkScrollableFrame | None = None
        self._build_toolbar()
        self._build_list()
        self.refresh()

    def _build_toolbar(self) -> None:
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", padx=32, pady=(0, 16))

        new_button = ctk.CTkButton(
            toolbar,
            text="New Expense",
            width=140,
            fg_color=Theme.BG_ACTIVE,
            hover_color="#2ea043",
            command=self._open_new_expense_dialog,
        )
        new_button.pack(side="right")

    def _build_list(self) -> None:
        list_container = ctk.CTkFrame(
            self,
            fg_color=Theme.BG_CARD,
            corner_radius=Theme.CARD_CORNER_RADIUS,
            border_width=1,
            border_color=Theme.BORDER,
        )
        list_container.pack(fill="both", expand=True, padx=32, pady=(0, 32))

        header_frame = ctk.CTkFrame(list_container, fg_color=Theme.BG_HEADER, corner_radius=0)
        header_frame.pack(fill="x", padx=1, pady=(1, 0))

        for column_index, column_name in enumerate(LIST_COLUMNS):
            header_frame.grid_columnconfigure(column_index, weight=1)
            label = ctk.CTkLabel(
                header_frame,
                text=column_name,
                font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SM, "bold"),
                text_color=Theme.TEXT_SECONDARY,
                anchor="w",
            )
            label.grid(row=0, column=column_index, padx=16, pady=12, sticky="w")

        self._rows_frame = ctk.CTkScrollableFrame(
            list_container,
            fg_color=Theme.BG_CARD,
            corner_radius=0,
        )
        self._rows_frame.pack(fill="both", expand=True, padx=1, pady=(0, 1))

        for column_index in range(len(LIST_COLUMNS)):
            self._rows_frame.grid_columnconfigure(column_index, weight=1)

    def refresh(self) -> None:
        """Reload expenses from Excel and redraw the list."""
        if self._rows_frame is None:
            return

        for widget in self._rows_frame.winfo_children():
            widget.destroy()

        expenses = ExcelService.get_expenses()

        if not expenses:
            empty_label = ctk.CTkLabel(
                self._rows_frame,
                text="No expenses yet. Click New Expense to add one.",
                font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MD),
                text_color=Theme.TEXT_MUTED,
                anchor="w",
            )
            empty_label.grid(
                row=0, column=0, columnspan=len(LIST_COLUMNS), padx=16, pady=24, sticky="w"
            )
            return

        for row_index, expense in enumerate(expenses):
            self._add_row(row_index, expense)

    def _add_row(self, row_index: int, expense: Expense) -> None:
        assert self._rows_frame is not None

        values = (
            expense.date,
            expense.supplier,
            expense.project,
            expense.category,
            expense.invoice_number,
            expense.description,
            self._format_amount(expense.amount_ex_vat),
            self._format_amount(expense.vat),
            self._format_amount(expense.total),
        )
        for column_index, value in enumerate(values):
            label = ctk.CTkLabel(
                self._rows_frame,
                text=value or "—",
                font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MD),
                text_color=Theme.TEXT_PRIMARY,
                anchor="w",
            )
            label.grid(row=row_index, column=column_index, padx=16, pady=10, sticky="w")

    @staticmethod
    def _format_amount(value: str) -> str:
        try:
            return f"{float(value):.2f}"
        except ValueError:
            return value

    def _open_new_expense_dialog(self) -> None:
        NewExpenseDialog(self, on_save=self._save_expense)

    def _save_expense(
        self,
        date: str,
        supplier: str,
        project: str,
        category: str,
        invoice_number: str,
        description: str,
        amount_ex_vat: float,
        vat: float,
        total: float,
    ) -> None:
        ExcelService.add_expense(
            date=date,
            supplier=supplier,
            project=project,
            category=category,
            invoice_number=invoice_number,
            description=description,
            amount_ex_vat=amount_ex_vat,
            vat=vat,
            total=total,
        )
        self.refresh()
