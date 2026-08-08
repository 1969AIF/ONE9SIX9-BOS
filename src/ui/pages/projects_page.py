"""Project management page."""

import customtkinter as ctk

from src.config.theme import Theme
from src.services.excel_service import ExcelService, Project
from src.ui.components.new_project_dialog import NewProjectDialog
from src.ui.pages.base_page import BasePage

LIST_COLUMNS = ("Project Code", "Project Name", "Status")


class ProjectsPage(BasePage):
    """Displays and manages projects from the Excel workbook."""

    PAGE_TITLE = "Project Management"

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
            text="New Project",
            width=140,
            fg_color=Theme.BG_ACTIVE,
            hover_color="#2ea043",
            command=self._open_new_project_dialog,
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
        """Reload projects from Excel and redraw the list."""
        if self._rows_frame is None:
            return

        for widget in self._rows_frame.winfo_children():
            widget.destroy()

        projects = ExcelService.get_projects()

        if not projects:
            empty_label = ctk.CTkLabel(
                self._rows_frame,
                text="No projects yet. Click New Project to add one.",
                font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MD),
                text_color=Theme.TEXT_MUTED,
                anchor="w",
            )
            empty_label.grid(row=0, column=0, columnspan=3, padx=16, pady=24, sticky="w")
            return

        for row_index, project in enumerate(projects):
            self._add_row(row_index, project)

    def _add_row(self, row_index: int, project: Project) -> None:
        assert self._rows_frame is not None

        values = (project.project_code, project.project_name, project.status)
        for column_index, value in enumerate(values):
            label = ctk.CTkLabel(
                self._rows_frame,
                text=value,
                font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MD),
                text_color=Theme.TEXT_PRIMARY,
                anchor="w",
            )
            label.grid(row=row_index, column=column_index, padx=16, pady=10, sticky="w")

    def _open_new_project_dialog(self) -> None:
        NewProjectDialog(self, on_save=self._save_project)

    def _save_project(
        self,
        project_code: str,
        project_name: str,
        status: str,
    ) -> None:
        ExcelService.add_project(project_code, project_name, status)
        self.refresh()
