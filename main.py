import asyncio
import customtkinter as ctk
from bleak import BleakScanner
from src.config.app_config import AppConfig
from src.views.main_view import MainView
from src.views.imu_views import IMU1View, IMU2View
from src.views.timestamp_view import TimestampView 
from src.model.esp32_service import ESP32BLEService
from src.presenter.connection_presenter import ConnectionPresenter
from src.presenter.imu_presenter import IMUPresenter
from src.presenter.timestamp_presenter import TimestampPresenter
from src.views.connection_dialog import ConnectionDialog

class BLEMonitorApp:
    """Main application class using MVP pattern"""
    
    def __init__(self):
        # Set appearance mode
        ctk.set_appearance_mode(AppConfig.APPEARANCE_MODE)
        
        # Create event loop
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        # Initialize BLE service
        self.ble_service = ESP32BLEService()
        
        # Create main view
        self.main_view = MainView()
        self.content_area = self.main_view.create_content_area()
        
        # Create IMU views
        imu_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        imu_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        imu_frame.grid_columnconfigure(0, weight=1)
        imu_frame.grid_columnconfigure(1, weight=1)
        
        self.imu1_view = IMU1View(imu_frame)
        self.imu1_view.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        self.imu2_view = IMU2View(imu_frame)
        self.imu2_view.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        # Create timestamp view
        self.timestamp_view = TimestampView(self.content_area)
        self.timestamp_view.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        
        # Override clear_displays
        def clear_displays():
            self.timestamp_view.clear()
            self.imu1_view.update_accel(0, 0, 0)
            self.imu1_view.update_gyro(0, 0, 0)
            self.imu1_view.update_magn(0, 0, 0)
            self.imu1_view.update_debug_text("")
            self.imu2_view.update_accel(0, 0, 0)
            self.imu2_view.update_gyro(0, 0, 0)
            self.imu2_view.update_magn(0, 0, 0)
            self.imu2_view.update_debug_text("")
            
        self.main_view.clear_displays = clear_displays
        
        # Create presenters
        self.connection_presenter = ConnectionPresenter(
            self.main_view,
            self.ble_service,
            self.loop
        )
        
        self.imu1_presenter = IMUPresenter(
            self.imu1_view,
            self.ble_service,
            self.ble_service.IMU1_CHAR_UUID,
            self.loop
        )
        
        self.imu2_presenter = IMUPresenter(
            self.imu2_view,
            self.ble_service,
            self.ble_service.IMU2_CHAR_UUID,
            self.loop
        )
        
        self.timestamp_presenter = TimestampPresenter(
            self.timestamp_view,
            self.ble_service,
            self.ble_service.TIMESTAMP_CHAR_UUID
        )
        
        # Setup event handlers
        self._setup_event_handlers()
        
        # Setup asyncio integration
        self._setup_asyncio_integration()
        
        # Setup window close handler
        self.main_view.protocol("WM_DELETE_WINDOW", self._on_closing)
        
    def _setup_event_handlers(self):
        """Setup event handlers for UI controls"""
        # Connection handlers
        self.main_view.set_handlers(
            connect_command=self._show_connection_dialog,
            disconnect_command=self._disconnect_device
        )
        
        # IMU1 handlers
        self.imu1_view.button_read.configure(
            command=lambda: self.loop.create_task(self.imu1_presenter.read_data())
        )
        self.imu1_view.button_notify.configure(
            command=lambda: self.loop.create_task(self.imu1_presenter.toggle_notifications())
        )
        
        # IMU2 handlers
        self.imu2_view.button_read.configure(
            command=lambda: self.loop.create_task(self.imu2_presenter.read_data())
        )
        self.imu2_view.button_notify.configure(
            command=lambda: self.loop.create_task(self.imu2_presenter.toggle_notifications())
        )
        
        # Timestamp handlers
        self.timestamp_view.read_button.configure(
            command=lambda: self.loop.create_task(self.timestamp_presenter.read_timestamp())
        )
        self.timestamp_view.write_button.configure(
            command=lambda: self.loop.create_task(self.timestamp_presenter.write_current_time())
        )
        
    def _setup_asyncio_integration(self):
        """Setup asyncio integration with Tkinter"""
        def handle_asyncio():
            self.loop.stop()
            self.loop.run_forever()
            self.main_view.after(10, handle_asyncio)
        self.main_view.after(10, handle_asyncio)
        
    def _show_connection_dialog(self):
        """Show connection dialog"""
        self.connection_dialog = ConnectionDialog(self.main_view, self.loop, BleakScanner, self._handle_connection)
        
    def _handle_connection(self, device_info):
        """Handle device selection from connection dialog"""
        self.loop.create_task(self._connect_to_device(device_info))
        
    async def _connect_to_device(self, device_info):
        """Connect to the selected device"""
        # Convert device_info dict to BLEDeviceInfo
        from src.model.ble_service import BLEDeviceInfo
        ble_device = BLEDeviceInfo(
            address=device_info['address'],
            name=device_info['name'],
            rssi=device_info['rssi']
        )
        
        # Attempt connection
        success = await self.connection_presenter.connect_to_device(ble_device)
        if success:
            # Show success in dialog and set flag
            self.connection_dialog.connection_success = True
            self.connection_dialog.status_dialog.show_connected(ble_device)
            # Enable IMU and timestamp controls
            self.imu1_view.set_button_states(True)
            self.imu2_view.set_button_states(True)
            self.timestamp_view.set_button_states(True)
        else:
            # Show failure in dialog and set flag
            self.connection_dialog.connection_success = False
            self.connection_dialog.status_dialog.show_failed()
        
    def _disconnect_device(self):
        """Disconnect from current device"""
        self.loop.create_task(self._disconnect_and_disable())
        
    async def _disconnect_and_disable(self):
        """Disconnect and disable controls"""
        # Stop notifications first if they are active
        if self.imu1_presenter.is_notifying():
            await self.imu1_presenter.toggle_notifications()
        if self.imu2_presenter.is_notifying():
            await self.imu2_presenter.toggle_notifications()
            
        # Then disconnect
        await self.connection_presenter.disconnect()
        
        # Reset all displays and controls
        self.main_view.clear_displays()
        
        # Reset IMU notification states
        self.imu1_view.toggle_notify(False)
        self.imu2_view.toggle_notify(False)
        
        # Disable all controls
        self.imu1_view.set_button_states(False)
        self.imu2_view.set_button_states(False)
        self.timestamp_view.set_button_states(False)
        
    def _on_closing(self):
        """Handle window closing"""
        # Stop all notifications and disconnect
        async def cleanup():
            if self.imu1_presenter.is_notifying():
                await self.imu1_presenter.toggle_notifications()
            if self.imu2_presenter.is_notifying():
                await self.imu2_presenter.toggle_notifications()
            await self.ble_service.disconnect()
            
        self.loop.run_until_complete(cleanup())
        self.loop.stop()
        self.main_view.quit()
        
    def run(self):
        """Start the application"""
        self.main_view.mainloop()

if __name__ == "__main__":
    app = BLEMonitorApp()
    app.run()
