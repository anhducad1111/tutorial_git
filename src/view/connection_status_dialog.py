import customtkinter as ctk
from src.config.app_config import AppConfig
from src.view.button_component import ButtonComponent

from src.view.view_interfaces import ConnectionStatusViewInterface

class ConnectionStatusDialog(ctk.CTkToplevel, ConnectionStatusViewInterface):
    """Dialog to show connection status"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.parent = parent
        self._destroyed = False
        self.config = AppConfig()  # Get singleton instance
        
        self._setup_window()
        self._create_layout()
        
    def _setup_window(self):
        """Configure dialog window"""
        self.title("Connecting")
        self.overrideredirect(False)  # Keep window decorations
        self.configure(fg_color="#1F1F1F")  # Dark background
        self.geometry("400x200")  # Adjust size as needed
        self.resizable(False, False)  # Fix window size
        self.protocol("WM_DELETE_WINDOW", self.destroy)  # Handle window close button
        self._center_window()
        self._make_modal()
        
        
    def _center_window(self):
        """Center dialog on parent window"""
        x = self.parent.winfo_x() + (self.parent.winfo_width() - 450) // 2
        y = self.parent.winfo_y() + (self.parent.winfo_height() - 350) // 2
        self.geometry(f"+{max(0, x)}+{max(0, y)}")
        
    def _make_modal(self):
        """Make dialog modal"""
        self.transient(self.parent)
        self.grab_set()
        
    def _create_layout(self):
        """Create dialog layout"""
        # Border frame
        border_frame = ctk.CTkFrame(
            self,
            fg_color=("#2B2D30", "#2B2D30"),
            border_color=("#777777", "#777777"),
            border_width=1,
            corner_radius=8
        )
        border_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Main frame with padding
        main_frame = ctk.CTkFrame(border_frame, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="Connecting...",
            font=self.config.TEXT_FONT
        )
        self.status_label.pack(pady=20)
        
        # OK button (initially hidden)
        self.ok_button = ButtonComponent(
            main_frame,
            button_text="OK",
            command=self._on_ok_clicked,
            width=100
        )
        self.ok_button.pack(pady=20)
        self.ok_button.pack_forget()
        
    def show_connecting(self):
        """Show connecting state"""
        self.status_label.configure(text="Connecting...")
        self.ok_button.configure(state="disabled")
        self.ok_button.pack()
        
    def on_ok_clicked(self, callback):
        """Set callback for when OK button is clicked"""
        self._ok_callback = callback

    def _on_ok_clicked(self):
        """Internal handler for OK button click"""
        if hasattr(self, '_ok_callback'):
            self._ok_callback()
        self.destroy()
        
    def show_connected(self, device_info):
        """Show connected state with device info"""
        info_text = f"Connected to:\n{device_info.name}\nRSSI: {device_info.rssi} dBm"
        self.status_label.configure(text=info_text)
        self.ok_button.configure(state="normal")
        
    def show_failed(self):
        """Show connection failed state"""
        self.status_label.configure(text="Connection failed")
        self.ok_button.pack(pady=20)
        
    def destroy(self):
        """Override destroy to handle cleanup"""
        self._destroyed = True
        super().destroy()
