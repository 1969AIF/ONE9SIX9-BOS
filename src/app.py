"""Main application window."""

import customtkinter as ctk

from src.config.theme import Theme
from src.ui.components.header import Header
from src.ui.components.sidebar import Sidebar
from src.ui.pages.base_page import BasePage
from src.ui.pages.dashboard_page import DashboardPage
from src.ui.pages.projects_page import ProjectsPage
from src.ui.pages.suppliers_page import SuppliersPage
from src.ui.pages.categories_page import CategoriesPage
from src.ui.pages.expenses_page import ExpensesPage


class MainWindow(ctk.CTk):
    """Root window containing sidebar, header, and page content."""

    def __init__(self) -> None:
        super().__init__()

        self.title(Theme.WINDOW_TITLE)
        self.geometry(f"{Theme.WINDOW_WIDTH}x{Theme.WINDOW_HEIGHT}")
        self.minsize(Theme.WINDOW_WIDTH, Theme.WINDOW_HEIGHT)
        self.configure(fg_color=Theme.BG_DARK)

        self._pages: dict[str, BasePage] = {}
        self._current_page: BasePage | None = None

        self._build_layout()
        self._register_pages()
        self._show_page("Dashboard")

    def _build_layout(self) -> None:
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._sidebar = Sidebar(self, on_navigate=self._show_page)
        self._sidebar.grid(row=0, column=0, sticky="ns")

        content = ctk.CTkFrame(self, fg_color=Theme.BG_DARK, corner_radius=0)
        content.grid(row=0, column=1, sticky="nsew")
        content.grid_rowconfigure(1, weight=1)
        content.grid_columnconfigure(0, weight=1)

        self._header = Header(content)
        self._header.grid(row=0, column=0, sticky="ew")

        self._page_container = ctk.CTkFrame(
            content,
            fg_color=Theme.BG_DARK,
            corner_radius=0,
        )
        self._page_container.grid(row=1, column=0, sticky="nsew")
        self._page_container.grid_rowconfigure(0, weight=1)
        self._page_container.grid_columnconfigure(0, weight=1)

    def _register_pages(self) -> None:
        self._pages["Dashboard"] = DashboardPage(self._page_container)
        self._pages["Projects"] = ProjectsPage(self._page_container)
        self._pages["Suppliers"] = SuppliersPage(self._page_container)
        self._pages["Categories"] = CategoriesPage(self._page_container)
        self._pages["Expenses"] = ExpensesPage(self._page_container)

    def _show_page(self, page_name: str) -> None:
        if page_name not in self._pages:
            return

        for page in self._pages.values():
            page.grid_remove()

        self._current_page = self._pages[page_name]
        self._current_page.grid(row=0, column=0, sticky="nsew")

        if hasattr(self._current_page, "refresh"):
            self._current_page.refresh()

        self._sidebar.set_active(page_name)
