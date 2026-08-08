"""Left navigation sidebar."""

from collections.abc import Callable

import customtkinter as ctk

from src.config.theme import Theme

NAV_ITEMS: tuple[str, ...] = (
    "Dashboard",
    "Expenses",
    "Income",
    "Projects",
    "Suppliers",
    "Documents",
    "Reports",
    "Administration",
)


class Sidebar(ctk.CTkFrame):
    """Vertical navigation panel with page selection buttons."""

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        on_navigate: Callable[[str], None],
        **kwargs,
    ) -> None:
        super().__init__(
            master,
            width=Theme.SIDEBAR_WIDTH,
            fg_color=Theme.BG_SIDEBAR,
            corner_radius=0,
            **kwargs,
        )
        self.grid_propagate(False)
        self._on_navigate = on_navigate
        self._buttons: dict[str, ctk.CTkButton] = {}
        self._active_item = "Dashboard"
        self._build()

    def _build(self) -> None:
        brand_label = ctk.CTkLabel(
            self,
            text="Navigation",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SM, "bold"),
            text_color=Theme.TEXT_MUTED,
            anchor="w",
        )
        brand_label.pack(fill="x", padx=20, pady=(24, 8))

        for item in NAV_ITEMS:
            button = ctk.CTkButton(
                self,
                text=item,
                anchor="w",
                height=40,
                corner_radius=Theme.BUTTON_CORNER_RADIUS,
                font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MD),
                fg_color="transparent",
                text_color=Theme.TEXT_SECONDARY,
                hover_color=Theme.BG_CARD,
                command=lambda name=item: self._select(name),
            )
            button.pack(fill="x", padx=12, pady=2)
            self._buttons[item] = button

        self._highlight_active()

    def set_active(self, item: str) -> None:
        """Highlight a navigation item without triggering navigation."""
        if item in self._buttons:
            self._active_item = item
            self._highlight_active()

    def _select(self, item: str) -> None:
        self._active_item = item
        self._highlight_active()
        self._on_navigate(item)

    def _highlight_active(self) -> None:
        for name, button in self._buttons.items():
            if name == self._active_item:
                button.configure(
                    fg_color=Theme.BG_ACTIVE,
                    text_color=Theme.TEXT_PRIMARY,
                )
            else:
                button.configure(
                    fg_color="transparent",
                    text_color=Theme.TEXT_SECONDARY,
                )
