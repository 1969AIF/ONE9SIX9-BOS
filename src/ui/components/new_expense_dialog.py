"""Dialog for creating a new expense."""

from collections.abc import Callable

import customtkinter as ctk

from src.config.theme import Theme
from src.services.excel_service import ExcelService

PLACEHOLDER_SUPPLIER = "Select a supplier…"
PLACEHOLDER_PROJECT = "Select a project…"
PLACEHOLDER_CATEGORY = "Select a category…"


class NewExpenseDialog(ctk.CTkToplevel):
    """Modal dialog for entering new expense details."""

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        on_save: Callable[[str, str, str, str, str, str, float, float, float], None],
    ) -> None:
        super().__init__(master)

        self._on_save = on_save
        self.title("New Expense")
        self.geometry("460x700")
        self.resizable(False, False)
        self.configure(fg_color=Theme.BG_CARD)
        self.transient(master.winfo_toplevel())
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self._handle_cancel)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._projects = ExcelService.get_projects()
        self._build()
        self._center_on_parent(master)
        self._date_entry.focus_set()

    def _build(self) -> None:
        form = ctk.CTkFrame(self, fg_color="transparent")
        form.grid(row=0, column=0, sticky="nsew", padx=24, pady=(24, 0))

        title_label = ctk.CTkLabel(
            form,
            text="New Expense",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_LG, "bold"),
            text_color=Theme.TEXT_PRIMARY,
            anchor="w",
        )
        title_label.pack(anchor="w", pady=(0, 20))

        self._date_entry = self._add_field(form, "Date")
        self._supplier_menu = self._add_dropdown(
            form,
            "Supplier",
            PLACEHOLDER_SUPPLIER,
            [s.supplier_name for s in ExcelService.get_suppliers()],
        )
        self._project_menu = self._add_dropdown(
            form,
            "Project",
            PLACEHOLDER_PROJECT,
            [f"{p.project_code} — {p.project_name}" for p in self._projects],
        )
        self._category_menu = self._add_dropdown(
            form,
            "Category",
            PLACEHOLDER_CATEGORY,
            [c.category_name for c in ExcelService.get_categories()],
        )
        self._invoice_entry = self._add_field(form, "Invoice/Receipt Number")
        self._description_entry = self._add_field(form, "Description")

        self._amount_entry = self._add_field(form, "Amount Excl. VAT")
        self._amount_entry.bind("<KeyRelease>", lambda _event: self._update_total())
        self._vat_entry = self._add_field(form, "VAT")
        self._vat_entry.bind("<KeyRelease>", lambda _event: self._update_total())

        total_label = ctk.CTkLabel(
            form,
            text="Total Incl. VAT",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SM),
            text_color=Theme.TEXT_SECONDARY,
            anchor="w",
        )
        total_label.pack(anchor="w", pady=(12, 4))

        self._total_label = ctk.CTkLabel(
            form,
            text="0.00",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_LG, "bold"),
            text_color=Theme.TEXT_ACCENT,
            anchor="w",
        )
        self._total_label.pack(anchor="w")

        self._error_label = ctk.CTkLabel(
            form,
            text="",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SM),
            text_color=Theme.ACCENT_EXPENSE,
            anchor="w",
        )
        self._error_label.pack(anchor="w", pady=(8, 0))

        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=1, column=0, sticky="ew", padx=24, pady=24)

        cancel_button = ctk.CTkButton(
            footer,
            text="Cancel",
            width=100,
            fg_color=Theme.BG_CARD_HOVER,
            hover_color=Theme.BORDER,
            command=self._handle_cancel,
        )
        cancel_button.pack(side="right", padx=(8, 0))

        save_button = ctk.CTkButton(
            footer,
            text="Save",
            width=100,
            fg_color=Theme.BG_ACTIVE,
            hover_color="#2ea043",
            command=self._handle_save,
        )
        save_button.pack(side="right")

        self.bind("<Return>", lambda _event: self._handle_save())
        self.bind("<Escape>", lambda _event: self._handle_cancel())

    def _add_field(
        self,
        parent: ctk.CTkFrame,
        label: str,
    ) -> ctk.CTkEntry:
        field_label = ctk.CTkLabel(
            parent,
            text=label,
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SM),
            text_color=Theme.TEXT_SECONDARY,
            anchor="w",
        )
        field_label.pack(anchor="w", pady=(0, 4))

        entry = ctk.CTkEntry(
            parent,
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MD),
            fg_color=Theme.BG_DARK,
            border_color=Theme.BORDER,
        )
        entry.pack(fill="x", pady=(0, 8))
        return entry

    def _add_dropdown(
        self,
        parent: ctk.CTkFrame,
        label: str,
        placeholder: str,
        values: list[str],
    ) -> ctk.CTkOptionMenu:
        field_label = ctk.CTkLabel(
            parent,
            text=label,
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SM),
            text_color=Theme.TEXT_SECONDARY,
            anchor="w",
        )
        field_label.pack(anchor="w", pady=(0, 4))

        menu = ctk.CTkOptionMenu(
            parent,
            values=[placeholder, *values],
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MD),
            fg_color=Theme.BG_DARK,
            button_color=Theme.BG_CARD_HOVER,
            button_hover_color=Theme.BORDER,
            dropdown_fg_color=Theme.BG_CARD,
            anchor="w",
        )
        menu.set(placeholder)
        menu.pack(fill="x", pady=(0, 8))
        return menu

    def _update_total(self) -> None:
        total = self._parse_amount(self._amount_entry.get()) + self._parse_amount(
            self._vat_entry.get()
        )
        self._total_label.configure(text=f"{total:.2f}")

    @staticmethod
    def _parse_amount(text: str) -> float:
        try:
            return float(text.replace(",", ".").strip())
        except ValueError:
            return 0.0

    def _handle_save(self) -> None:
        date = self._date_entry.get().strip()
        supplier = self._supplier_menu.get()
        project = self._project_menu.get()

        if not date:
            self._error_label.configure(text="Date is required.")
            return

        if not self._projects:
            self._error_label.configure(text="Please add a project first.")
            return

        if project == PLACEHOLDER_PROJECT:
            self._error_label.configure(text="Please select a project.")
            return

        amount_text = self._amount_entry.get().strip()
        vat_text = self._vat_entry.get().strip()

        if not amount_text:
            self._error_label.configure(text="Amount is required.")
            return

        try:
            amount = float(amount_text.replace(",", "."))
        except ValueError:
            self._error_label.configure(text="Enter a valid amount.")
            return

        try:
            vat = float(vat_text.replace(",", ".")) if vat_text else 0.0
        except ValueError:
            self._error_label.configure(text="Enter a valid VAT amount.")
            return

        total = round(amount + vat, 2)

        self._on_save(
            date,
            "" if supplier == PLACEHOLDER_SUPPLIER else supplier,
            project,
            "" if self._category_menu.get() == PLACEHOLDER_CATEGORY else self._category_menu.get(),
            self._invoice_entry.get().strip(),
            self._description_entry.get().strip(),
            amount,
            vat,
            total,
        )
        self._close()

    def _handle_cancel(self) -> None:
        self._close()

    def _close(self) -> None:
        self.grab_release()
        self.destroy()

    def _center_on_parent(self, master: ctk.CTkBaseClass) -> None:
        self.update_idletasks()
        parent = master.winfo_toplevel()
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        dialog_width = self.winfo_width()
        dialog_height = self.winfo_height()

        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        self.geometry(f"+{x}+{y}")
