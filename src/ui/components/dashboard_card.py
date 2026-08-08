"""Dashboard metric card component."""

import customtkinter as ctk

from src.config.theme import Theme


class DashboardCard(ctk.CTkFrame):
    """Placeholder card for a dashboard metric."""

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        title: str,
        accent_color: str,
        **kwargs,
    ) -> None:
        super().__init__(
            master,
            fg_color=Theme.BG_CARD,
            corner_radius=Theme.CARD_CORNER_RADIUS,
            border_width=1,
            border_color=Theme.BORDER,
            **kwargs,
        )
        self._build(title, accent_color)

    def _build(self, title: str, accent_color: str) -> None:
        accent_bar = ctk.CTkFrame(
            self,
            width=4,
            fg_color=accent_color,
            corner_radius=2,
        )
        accent_bar.place(x=0, y=20, relheight=0.5)

        title_label = ctk.CTkLabel(
            self,
            text=title,
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MD),
            text_color=Theme.TEXT_SECONDARY,
            anchor="w",
        )
        title_label.pack(anchor="w", padx=24, pady=(24, 8))

        value_label = ctk.CTkLabel(
            self,
            text="—",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_XXL, "bold"),
            text_color=Theme.TEXT_PRIMARY,
            anchor="w",
        )
        value_label.pack(anchor="w", padx=24, pady=(0, 24))

        subtitle_label = ctk.CTkLabel(
            self,
            text="No data yet",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SM),
            text_color=Theme.TEXT_MUTED,
            anchor="w",
        )
        subtitle_label.pack(anchor="w", padx=24, pady=(0, 24))
