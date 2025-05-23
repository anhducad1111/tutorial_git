import customtkinter as ctk
from src.config.app_config import AppConfig

class CoordinateEntry(ctk.CTkFrame):
    def __init__(self, parent, label=""):
        super().__init__(parent)
        
        self.configure(fg_color="transparent")
        
        # Add label
        prefix = ctk.CTkLabel(
            self,
            text=label + ":",
            font=AppConfig.LABEL_FONT,
            text_color=AppConfig.LABEL_COLOR
        )
        prefix.pack(side="left")

        # Value display
        self.value_display = ctk.CTkTextbox(
            self,
            width=AppConfig.VALUE_DISPLAY_WIDTH,
            height=AppConfig.VALUE_DISPLAY_HEIGHT,
            font=AppConfig.VALUE_FONT,
            text_color=AppConfig.TEXT_COLOR,
            fg_color=AppConfig.TEXTBOX_COLOR,
            border_width=AppConfig.BORDER_WIDTH,
            border_color=AppConfig.BORDER_COLOR,
            corner_radius=AppConfig.CORNER_RADIUS,
            state="disabled"
        )
        self.value_display.pack(side="left", padx=5)

        # Unit label
        self.unit_label = ctk.CTkLabel(
            self,
            text="",
            font=AppConfig.LABEL_FONT,
            text_color=AppConfig.LABEL_COLOR
        )
        self.unit_label.pack(side="left")

    def set_unit(self, unit):
        """Set the unit label"""
        self.unit_label.configure(text=unit)

    def set_value(self, value):
        """Set the displayed value"""
        # Format floating point value
        if isinstance(value, float):
            text = f"{value:.3f}"
        else:
            text = str(value)

        # Update display
        self.value_display.configure(state="normal")
        self.value_display.delete("1.0", "end")
        self.value_display.insert("1.0", text)
        self.value_display.configure(state="disabled")
