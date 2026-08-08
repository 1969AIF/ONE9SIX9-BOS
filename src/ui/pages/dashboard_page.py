"""Dashboard page with placeholder metric cards."""

import customtkinter as ctk

from src.config.theme import Theme
from src.ui.components.dashboard_card import DashboardCard
from src.ui.pages.base_page import BasePage


class DashboardPage(BasePage):
    """Main dashboard view with summary metric cards."""

    PAGE_TITLE = "Dashboard"

    def __init__(self, master: ctk.CTkBaseClass, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._build_cards()

    def _build_cards(self) -> None:
        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.pack(fill="both", expand=True, padx=32, pady=(0, 32))

        for column in range(4):
            cards_frame.grid_columnconfigure(column, weight=1, uniform="card")

        card_definitions = (
            ("Income This Month", Theme.ACCENT_INCOME),
            ("Expenses This Month", Theme.ACCENT_EXPENSE),
            ("Net Profit", Theme.ACCENT_PROFIT),
            ("Pending Approvals", Theme.ACCENT_PENDING),
        )

        for index, (title, accent) in enumerate(card_definitions):
            card = DashboardCard(cards_frame, title=title, accent_color=accent)
            card.grid(row=0, column=index, padx=8, pady=8, sticky="nsew")
