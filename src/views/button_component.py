import customtkinter as ctk
from src.config.app_config import AppConfig

class ButtonComponent(ctk.CTkButton):
    def __init__(self, parent, button_text: str, **kwargs):
        # Set default values
        default_settings = {
            "text": button_text,
            "font": AppConfig.BUTTON_FONT,
            "text_color": AppConfig.TEXT_COLOR,
            "fg_color": AppConfig.BUTTON_COLOR,
            "width": AppConfig.BUTTON_WIDTH,
            "height": AppConfig.BUTTON_HEIGHT,
            "corner_radius": AppConfig.BUTTON_CORNER_RADIUS,
        }
        
        # Update defaults with any provided kwargs
        default_settings.update(kwargs)
        
        # Initialize with combined settings
        super().__init__(parent, **default_settings)
