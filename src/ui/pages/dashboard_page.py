"""Dashboard page with live metric cards."""

import customtkinter as ctk

from src.config.theme import Theme
from src.services.excel_service import ExcelService
from src.ui.components.dashboard_card import DashboardCard
from src.ui.pages.base_page import BasePage


class DashboardPage(BasePage):
    """Main dashboard view with summary metric cards."""

    PAGE_TITLE = "Dashboard"

    def __init__(self, master: ctk.CTkBaseClass, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._cards: dict[str, DashboardCard] = {}
        self._build_cards()
        self.refresh()

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
            self._cards[title] = card

    def refresh(self) -> None:
        """Reload the latest figures from Excel and update the cards."""
        summary = ExcelService.get_dashboard_summary()
        net_profit = summary.income_total - summary.expenses_total

        self._cards["Income This Month"].set_value(
            "R0",
            subtitle="Income module coming soon",
        )
        self._cards["Expenses This Month"].set_value(
            self._format_rand(summary.expenses_total),
            subtitle=(
                f"{summary.expenses_count} expense"
                f"{'s' if summary.expenses_count != 1 else ''} this month"
                if summary.expenses_count > 0
                else "No expenses this month"
            ),
        )
        self._cards["Net Profit"].set_value(
            self._format_rand(net_profit),
            subtitle="Income minus expenses",
        )
        self._cards["Pending Approvals"].set_value(
            "0",
            subtitle="No approvals pending",
        )

    @staticmethod
    def _format_rand(value: float) -> str:
        if value < 0:
            return f"-R{abs(value):,.2f}"
        return f"R{value:,.2f}"
