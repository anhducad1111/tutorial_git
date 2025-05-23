import customtkinter as ctk
from src.config.app_config import AppConfig
from src.views.button_component import ButtonComponent
from src.views.coordinate_entry import CoordinateEntry
from src.views.view_interfaces import IMUViewInterface
import customtkinter as ctk

class BaseIMUView(ctk.CTkFrame, IMUViewInterface):
    def __init__(self, parent, title="IMU View"):
        super().__init__(parent)
        
        self.title = title
        self.notifying = False
        
        # Config frame
        self.configure(fg_color=AppConfig.PANEL_COLOR)
        
        # Create layout
        self._create_title()
        self._create_content()

    def _create_title(self):
        """Create title section"""
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(fill="x", padx=10, pady=5)

        title = ctk.CTkLabel(
            title_frame, 
            text=self.title,
            font=AppConfig.HEADER_FONT
        )
        title.pack(side="left")

    def _create_content(self):
        """Create main content"""
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=10, pady=5)

        # Sensor data section
        sensor_frame = ctk.CTkFrame(content, fg_color="transparent")
        sensor_frame.pack(fill="x", pady=5)

        # Accelerometer
        self._create_sensor_group(sensor_frame, "Accelerometer", "accel")

        # Gyroscope  
        self._create_sensor_group(sensor_frame, "Gyroscope", "gyro")

        # Magnetometer
        self._create_sensor_group(sensor_frame, "Magnetometer", "magn")

        # Controls
        controls = ctk.CTkFrame(content, fg_color="transparent") 
        controls.pack(fill="x", pady=5)
        
        # Left controls
        left_controls = ctk.CTkFrame(controls, fg_color="transparent")
        left_controls.pack(side="left")
        
        self.button_read = ButtonComponent(
            left_controls, "Read",
            width=90
        )
        self.button_read.pack(side="left", padx=5)

        self.button_notify = ButtonComponent(
            left_controls, "Notify",
            width=90
        )
        self.button_notify.pack(side="left", padx=5)

        # Right controls
        right_controls = ctk.CTkFrame(controls, fg_color="transparent")
        right_controls.pack(side="right")

        self.button_config = ButtonComponent(
            right_controls, "Configure",
            width=90
        )
        self.button_config.pack(side="left", padx=5)

        self.button_calibrate = ButtonComponent(  
            right_controls, "Calibrate",
            width=90
        )
        self.button_calibrate.pack(side="left", padx=5)

        # Debug section
        debug_frame = ctk.CTkFrame(content, fg_color="transparent")
        debug_frame.pack(fill="x", pady=5)
        
        debug_label = ctk.CTkLabel(
            debug_frame,
            text="Debug:",
            font=AppConfig.LABEL_FONT
        )
        debug_label.pack(anchor="w")

        self.debug_text = ctk.CTkTextbox(
            debug_frame,
            height=80,
            font=AppConfig.TEXT_FONT,
            state="disabled"
        )
        self.debug_text.pack(fill="x")

    def _create_sensor_group(self, parent, name, prefix):
        """Create a sensor reading group"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=2)

        label = ctk.CTkLabel(
            frame, 
            text=f"{name}:",
            font=AppConfig.LABEL_FONT,
            width=120,
            anchor="w"
        )
        label.pack(side="left")

        # Create coordinate entries
        coords_frame = ctk.CTkFrame(frame, fg_color="transparent")
        coords_frame.pack(side="left", fill="x", expand=True)

        setattr(self, f"{prefix}_x", CoordinateEntry(coords_frame, "X"))
        getattr(self, f"{prefix}_x").pack(side="left", padx=5)

        setattr(self, f"{prefix}_y", CoordinateEntry(coords_frame, "Y"))
        getattr(self, f"{prefix}_y").pack(side="left", padx=5)

        setattr(self, f"{prefix}_z", CoordinateEntry(coords_frame, "Z"))
        getattr(self, f"{prefix}_z").pack(side="left", padx=5)

    def update_accel(self, x, y, z):
        """Update accelerometer values"""
        self.accel_x.set_value(x)
        self.accel_y.set_value(y)
        self.accel_z.set_value(z)

    def update_gyro(self, x, y, z):
        """Update gyroscope values"""
        self.gyro_x.set_value(x)
        self.gyro_y.set_value(y)
        self.gyro_z.set_value(z)

    def update_magn(self, x, y, z):
        """Update magnetometer values"""
        self.magn_x.set_value(x)
        self.magn_y.set_value(y)
        self.magn_z.set_value(z)

    def toggle_notify(self, enabled):
        """Toggle notification state"""
        self.notifying = enabled
        text = "Stop Notify" if enabled else "Notify"
        bg_color = AppConfig.DISCONNECT_COLOR if enabled else AppConfig.BUTTON_COLOR
        self.button_notify.configure(
            text=text,
            fg_color=bg_color
        )
        
    def update_debug_text(self, text):
        """Update debug text display"""
        self.debug_text.configure(state="normal")
        self.debug_text.delete("1.0", "end")
        self.debug_text.insert("1.0", text)
        self.debug_text.configure(state="disabled")
        
    def set_button_states(self, enabled):
        """Enable/disable buttons"""
        state = "normal" if enabled else "disabled"
        self.button_read.configure(state=state)
        self.button_notify.configure(state=state)
        self.button_config.configure(state=state)
        self.button_calibrate.configure(state=state)
