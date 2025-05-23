import customtkinter as ctk
from src.config.app_config import AppConfig

class ButtonComponent(ctk.CTkButton):
    """Custom button component with consistent styling"""
    
    def __init__(
        self, 
        master, 
        text,
        command=None,
        width=AppConfig.BUTTON_WIDTH,
        height=AppConfig.BUTTON_HEIGHT,
        fg_color=AppConfig.BUTTON_COLOR,
        hover_color=AppConfig.BUTTON_HOVER_COLOR,
        font=AppConfig.BUTTON_FONT,
        corner_radius=AppConfig.BUTTON_CORNER_RADIUS,
        state="normal",
        **kwargs
    ):
        super().__init__(
            master=master,
            text=text,
            command=command,
            width=width,
            height=height,
            fg_color=fg_color,
            hover_color=hover_color,
            font=font,
            corner_radius=corner_radius,
            state=state,
            **kwargs
        )
