"""Dialog for creating a new project."""

from collections.abc import Callable

import customtkinter as ctk

from src.config.theme import Theme

STATUS_OPTIONS = ("Active", "Completed", "On Hold")


class NewProjectDialog(ctk.CTkToplevel):
    """Modal dialog for entering new project details."""

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        on_save: Callable[[str, str, str], None],
    ) -> None:
        super().__init__(master)

        self._on_save = on_save
        self.title("New Project")
        self.geometry("440x380")
        self.resizable(False, False)
        self.configure(fg_color=Theme.BG_CARD)
        self.transient(master.winfo_toplevel())
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self._handle_cancel)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build()
        self._center_on_parent(master)
        self._code_entry.focus_set()

    def _build(self) -> None:
        form = ctk.CTkFrame(self, fg_color="transparent")
        form.grid(row=0, column=0, sticky="nsew", padx=24, pady=(24, 0))

        title_label = ctk.CTkLabel(
            form,
            text="New Project",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_LG, "bold"),
            text_color=Theme.TEXT_PRIMARY,
            anchor="w",
        )
        title_label.pack(anchor="w", pady=(0, 20))

        self._code_entry = self._add_field(form, "Project Code")
        self._name_entry = self._add_field(form, "Project Name")

        status_label = ctk.CTkLabel(
            form,
            text="Status",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SM),
            text_color=Theme.TEXT_SECONDARY,
            anchor="w",
        )
        status_label.pack(anchor="w", pady=(12, 4))

        self._status_menu = ctk.CTkOptionMenu(
            form,
            values=list(STATUS_OPTIONS),
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MD),
            fg_color=Theme.BG_DARK,
            button_color=Theme.BG_CARD_HOVER,
            button_hover_color=Theme.BORDER,
            dropdown_fg_color=Theme.BG_CARD,
            anchor="w",
        )
        self._status_menu.set(STATUS_OPTIONS[0])
        self._status_menu.pack(fill="x")

        self._error_label = ctk.CTkLabel(
            form,
            text="",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SM),
            text_color=Theme.ACCENT_EXPENSE,
            anchor="w",
        )
        self._error_label.pack(anchor="w", pady=(12, 0))

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
        entry.pack(fill="x")
        return entry

    def _handle_save(self) -> None:
        project_code = self._code_entry.get().strip()
        project_name = self._name_entry.get().strip()
        status = self._status_menu.get()

        if not project_code or not project_name:
            self._error_label.configure(
                text="Project Code and Project Name are required."
            )
            return

        self._on_save(project_code, project_name, status)
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
