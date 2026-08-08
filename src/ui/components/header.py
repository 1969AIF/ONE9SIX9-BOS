"""Top header bar with application title and current date."""

from datetime import date

import customtkinter as ctk

from src.config.theme import Theme


class Header(ctk.CTkFrame):
    """Displays the application name and today's date."""

    def __init__(self, master: ctk.CTkBaseClass, **kwargs) -> None:
        super().__init__(
            master,
            height=Theme.HEADER_HEIGHT,
            fg_color=Theme.BG_HEADER,
            corner_radius=0,
            **kwargs,
        )
        self.grid_propagate(False)
        self._build()

    def _build(self) -> None:
        self.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            self,
            text="ONE9SIX9 BOS",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_XL, "bold"),
            text_color=Theme.TEXT_PRIMARY,
            anchor="w",
        )
        title_label.grid(row=0, column=0, padx=24, pady=16, sticky="w")

        date_label = ctk.CTkLabel(
            self,
            text=date.today().strftime("%A, %d %B %Y"),
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MD),
            text_color=Theme.TEXT_SECONDARY,
            anchor="e",
        )
        date_label.grid(row=0, column=1, padx=24, pady=16, sticky="e")
