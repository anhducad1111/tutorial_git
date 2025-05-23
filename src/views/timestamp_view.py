import customtkinter as ctk
from src.config.app_config import AppConfig
from src.views.button_component import ButtonComponent
from src.views.view_interfaces import TimestampViewInterface

class TimestampView(ctk.CTkFrame, TimestampViewInterface):
    """View for displaying and managing timestamp data"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        # Config frame
        self.configure(fg_color=AppConfig.PANEL_COLOR)
        
        # Setup layout
        self.grid_columnconfigure(3, weight=1)  # Make textbox expandable
        
        self._create_controls()
        
    def _create_controls(self):
        """Create UI controls"""
        timestamp_label = ctk.CTkLabel(
            self, 
            text="Timestamp:", 
            anchor="w",
            font=AppConfig.LABEL_FONT
        )
        timestamp_label.grid(row=0, column=0, padx=5, pady=5)

        self.read_button = ButtonComponent(
            self,
            text="Read",
            state="disabled",
            width=90
        )
        self.read_button.grid(row=0, column=1, padx=5, pady=5)

        self.write_button = ButtonComponent(
            self,
            text="Write Current Time",
            state="disabled",
            width=140
        )
        self.write_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Timestamp display
        self.timestamp_text = ctk.CTkTextbox(
            self,
            height=80,
            font=AppConfig.TEXT_FONT,
            state="disabled"
        )
        self.timestamp_text.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="ew")
        
    def update_timestamp_display(self, formatted_text):
        """Update timestamp display with formatted text"""
        self.timestamp_text.configure(state="normal")
        self.timestamp_text.delete("1.0", "end")
        self.timestamp_text.insert("1.0", formatted_text)
        self.timestamp_text.configure(state="disabled")
        
    def set_button_states(self, enabled):
        """Enable/disable timestamp buttons"""
        state = "normal" if enabled else "disabled"
        self.read_button.configure(state=state)
        self.write_button.configure(state=state)
        
    def clear(self):
        """Clear the timestamp display"""
        self.update_timestamp_display("No timestamp data available")
