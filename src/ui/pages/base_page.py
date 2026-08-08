"""Base class for application pages."""

import customtkinter as ctk

from src.config.theme import Theme


class BasePage(ctk.CTkFrame):
    """Common frame for all content pages."""

    PAGE_TITLE = "Page"

    def __init__(self, master: ctk.CTkBaseClass, **kwargs) -> None:
        super().__init__(
            master,
            fg_color=Theme.BG_DARK,
            corner_radius=0,
            **kwargs,
        )
        self._build_header()

    def _build_header(self) -> None:
        title_label = ctk.CTkLabel(
            self,
            text=self.PAGE_TITLE,
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_LG, "bold"),
            text_color=Theme.TEXT_PRIMARY,
            anchor="w",
        )
        title_label.pack(anchor="w", padx=32, pady=(24, 16))
