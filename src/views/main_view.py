import customtkinter as ctk
from src.config.app_config import AppConfig
from src.views.button_component import ButtonComponent
from src.views.view_interfaces import ConnectionViewInterface

class MainView(ctk.CTk, ConnectionViewInterface):
    """Main application view implementing ConnectionViewInterface"""
    
    def __init__(self):
        super().__init__()
        
        self.title(AppConfig.WINDOW_TITLE)
        self.geometry("1200x800")
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create sidebar
        self._create_sidebar()
        
    def _create_sidebar(self):
        """Create sidebar with connection controls"""
        self.left_sidebar = ctk.CTkFrame(
            self,
            fg_color=AppConfig.PANEL_COLOR,
            corner_radius=0
        )
        self.left_sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        # Connection controls
        self.connect_button = ButtonComponent(
            self.left_sidebar,
            text="Connect Device",
            width=140
        )
        self.connect_button.pack(padx=20, pady=(20,10))

        self.disconnect_button = ButtonComponent(
            self.left_sidebar,
            text="Disconnect",
            state="disabled",
            width=140
        )
        self.disconnect_button.pack(padx=20, pady=10)

        # Connection info
        self.info_label = ctk.CTkLabel(
            self.left_sidebar,
            text="No device connected",
            wraplength=200,
            font=AppConfig.TEXT_FONT
        )
        self.info_label.pack(padx=20, pady=10)
        
    def create_content_area(self):
        """Create content area to hold IMU views and timestamp"""
        # Right container for IMU views and Timestamp
        self.right_container = ctk.CTkFrame(self, fg_color="transparent")
        self.right_container.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.right_container.grid_columnconfigure(0, weight=1)
        self.right_container.grid_rowconfigure(0, weight=1)  # IMU frame
        self.right_container.grid_rowconfigure(1, weight=0)  # Timestamp frame
        
        return self.right_container
        
    def update_connection_status(self, connected, device_info=None, message=""):
        """Update connection status display"""
        if connected:
            self.connect_button.configure(state="disabled")
            self.disconnect_button.configure(state="normal")
            
            # Show device info
            if device_info:
                info_text = f"Connected to:\n{device_info.name}\nRSSI: {device_info.rssi} dBm"
                self.info_label.configure(text=info_text)
            else:
                self.info_label.configure(text="Connected")
        else:
            self.connect_button.configure(state="normal")
            self.disconnect_button.configure(state="disabled")
            self.info_label.configure(text=message or "No device connected")
            
    def show_connection_status(self, result, message):
        """Show connection status (required by ConnectionPresenter)"""
        self.update_connection_status(result, message=message)
    
    def clear_displays(self):
        """Delegate to child views"""
        # This method is expected to be overridden in the main application
        # since it needs to access the specific IMU and timestamp views
        pass
        
    def set_handlers(self, connect_command, disconnect_command):
        """Set command handlers for buttons"""
        self.connect_button.configure(command=connect_command)
        self.disconnect_button.configure(command=disconnect_command)
