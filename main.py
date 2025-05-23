import asyncio
import time
import customtkinter as ctk
from bleak import BleakScanner
from src.config.app_config import AppConfig
from src.views.connection_dialog import ConnectionDialog
from src.utils.esp32_ble import ESP32BLEService
from datetime import datetime

class BLEMonitor(ctk.CTk):
    def __init__(self):
        super().__init__()

        self._destroyed = False
        self.title(AppConfig.WINDOW_TITLE)
        self.geometry("800x600")

        self.connected_device = None
        self.device_rssi = None
        self.imu1_notifying = False
        self.imu2_notifying = False

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        self.ble_service = ESP32BLEService()

        self._create_gui()
        self._setup_asyncio_integration()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _setup_asyncio_integration(self):
        def handle_asyncio():
            self.loop.stop()
            self.loop.run_forever()
            self.after(10, handle_asyncio)
        self.after(10, handle_asyncio)

    def _format_timestamp(self, timestamp):
        """Format timestamp value for display"""
        try:
            dt = datetime.fromtimestamp(timestamp)
            return (
                f"UNIX Timestamp: {timestamp}\n"
                f"Date/Time: {dt.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Raw bytes: {' '.join(f'{b:02x}' for b in timestamp.to_bytes(8, 'little'))}"
            )
        except Exception as e:
            return f"Error: {e}"

    def _format_imu_value(self, value, hex_str):
        """Format IMU value for display"""
        return (
            f"Value: {value}\n"
            f"Raw bytes: {hex_str}"
        )

    async def _on_imu1_notify(self, sender, result):
        if result:
            value, hex_str = result
            self._update_display(self.imu1_display, self._format_imu_value(value, hex_str))

    async def _on_imu2_notify(self, sender, result):
        if result:
            value, hex_str = result
            self._update_display(self.imu2_display, self._format_imu_value(value, hex_str))

    def _read_imu1(self):
        self.loop.create_task(self._read_imu1_value())

    def _read_imu2(self):
        self.loop.create_task(self._read_imu2_value())

    async def _read_imu1_value(self):
        result = await self.ble_service.read_imu1()
        if result:
            value, hex_str = result
            self._update_display(self.imu1_display, self._format_imu_value(value, hex_str))

    async def _read_imu2_value(self):
        result = await self.ble_service.read_imu2()
        if result:
            value, hex_str = result
            self._update_display(self.imu2_display, self._format_imu_value(value, hex_str))

    def _create_gui(self):
        # Control frame
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.pack(fill="x", padx=10, pady=5)

        self.connect_button = ctk.CTkButton(
            self.control_frame,
            text="Connect Device",
            command=self._show_connection_dialog
        )
        self.connect_button.pack(side="left", padx=5)

        self.disconnect_button = ctk.CTkButton(
            self.control_frame,
            text="Disconnect",
            command=self._disconnect_device,
            state="disabled"
        )
        self.disconnect_button.pack(side="left", padx=5)

        # Timestamp frame
        self.timestamp_frame = ctk.CTkFrame(self)
        self.timestamp_frame.pack(fill="x", padx=10, pady=5)

        timestamp_label = ctk.CTkLabel(self.timestamp_frame, text="Timestamp:", anchor="w")
        timestamp_label.pack(side="left", padx=5)

        self.read_timestamp_btn = ctk.CTkButton(
            self.timestamp_frame,
            text="Read",
            command=self._read_timestamp,
            state="disabled",
            width=60
        )
        self.read_timestamp_btn.pack(side="left", padx=5)

        self.write_timestamp_btn = ctk.CTkButton(
            self.timestamp_frame,
            text="Write Current Time",
            command=self._write_current_time,
            state="disabled"
        )
        self.write_timestamp_btn.pack(side="left", padx=5)

        self.timestamp_display = ctk.CTkTextbox(
            self.timestamp_frame,
            height=60,
            width=300,
            state="disabled"
        )
        self.timestamp_display.pack(side="left", fill="x", expand=True, padx=5)

        # IMU1 frame 
        self.imu1_frame = ctk.CTkFrame(self)
        self.imu1_frame.pack(fill="x", padx=10, pady=5)

        imu1_label = ctk.CTkLabel(self.imu1_frame, text="IMU1:", anchor="w")
        imu1_label.pack(side="left", padx=5)

        self.read_imu1_btn = ctk.CTkButton(
            self.imu1_frame,
            text="Read",
            command=self._read_imu1,
            state="disabled",
            width=60
        )
        self.read_imu1_btn.pack(side="left", padx=5)

        self.imu1_notify_btn = ctk.CTkButton(
            self.imu1_frame,
            text="Start Notify",
            command=lambda: self.loop.create_task(self._toggle_imu1_notify()),
            state="disabled"
        )
        self.imu1_notify_btn.pack(side="left", padx=5)

        self.imu1_display = ctk.CTkTextbox(
            self.imu1_frame,
            height=150,  # Higher to show all sensor values
            width=400,  # Wider for raw bytes
            state="disabled"
        )
        self.imu1_display.pack(side="left", fill="x", expand=True, padx=5)

        # IMU2 frame
        self.imu2_frame = ctk.CTkFrame(self)
        self.imu2_frame.pack(fill="x", padx=10, pady=5)

        imu2_label = ctk.CTkLabel(self.imu2_frame, text="IMU2:", anchor="w")
        imu2_label.pack(side="left", padx=5)

        self.read_imu2_btn = ctk.CTkButton(
            self.imu2_frame,
            text="Read",
            command=self._read_imu2,
            state="disabled",
            width=60
        )
        self.read_imu2_btn.pack(side="left", padx=5)

        self.imu2_notify_btn = ctk.CTkButton(
            self.imu2_frame,
            text="Start Notify", 
            command=lambda: self.loop.create_task(self._toggle_imu2_notify()),
            state="disabled"
        )
        self.imu2_notify_btn.pack(side="left", padx=5)

        self.imu2_display = ctk.CTkTextbox(
            self.imu2_frame,
            height=150,  # Higher to show all sensor values
            width=400,  # Wider for raw bytes
            state="disabled"
        )
        self.imu2_display.pack(side="left", fill="x", expand=True, padx=5)

        # Info frame
        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.pack(fill="x", padx=10, pady=5)

        self.info_label = ctk.CTkLabel(
            self.info_frame,
            text="No device connected",
            wraplength=550
        )
        self.info_label.pack(padx=10, pady=10)

    def _show_connection_dialog(self):
        ConnectionDialog(self, self.loop, BleakScanner, self._handle_connection)

    def _handle_connection(self, device_info):
        self.connected_device = device_info
        self.device_rssi = device_info['rssi']
        self.loop.create_task(self._connect_to_device())

    async def _connect_to_device(self):
        if not self.connected_device:
            return

        success, message = await self.ble_service.connect_to_device(self.connected_device['address'])
        self.after(0, self._update_connection_status, success, message)

    def _update_connection_status(self, connected: bool, message: str):
        if connected:
            self.info_label.configure(
                text=f"Connected to: {self.connected_device['name']}\nRSSI: {self.device_rssi} dBm"
            )
            self.connect_button.configure(state="disabled")
            self.disconnect_button.configure(state="normal")
            self._enable_controls(True)
        else:
            self.info_label.configure(text=f"Connection status: {message}")
            self.connect_button.configure(state="normal")
            self.disconnect_button.configure(state="disabled")
            self._enable_controls(False)
            self._clear_displays()
            self.loop.create_task(self._stop_all_notifications())

    def _enable_controls(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        self.read_timestamp_btn.configure(state=state)
        self.write_timestamp_btn.configure(state=state)
        self.read_imu1_btn.configure(state=state)
        self.read_imu2_btn.configure(state=state)
        self.imu1_notify_btn.configure(state=state)
        self.imu2_notify_btn.configure(state=state)

    async def _stop_all_notifications(self):
        if self.imu1_notifying:
            await self.ble_service.stop_imu1_notify()
            self.imu1_notify_btn.configure(text="Start Notify")
            self.imu1_notifying = False
        if self.imu2_notifying:
            await self.ble_service.stop_imu2_notify()
            self.imu2_notify_btn.configure(text="Start Notify")
            self.imu2_notifying = False

    def _clear_displays(self):
        for display in [self.timestamp_display, self.imu1_display, self.imu2_display]:
            display.configure(state="normal")
            display.delete("1.0", "end")
            display.configure(state="disabled")

    def _update_display(self, textbox, value, prefix=""):
        if not self._destroyed:
            textbox.configure(state="normal")
            textbox.delete("1.0", "end")
            textbox.insert("1.0", f"{prefix}{value}")
            textbox.configure(state="disabled")

    def _read_timestamp(self):
        self.loop.create_task(self._read_timestamp_value())

    def _write_current_time(self):
        current_time = int(time.time())
        self.loop.create_task(self._write_timestamp_value(current_time))

    async def _read_timestamp_value(self):
        value = await self.ble_service.read_timestamp()
        if value is not None:
            self._update_display(self.timestamp_display, self._format_timestamp(value))

    async def _write_timestamp_value(self, timestamp):
        if await self.ble_service.write_timestamp(timestamp):
            await self._read_timestamp_value()

    async def _toggle_imu1_notify(self):
        if not self.imu1_notifying:
            success = await self.ble_service.start_imu1_notify(self._on_imu1_notify)
            if success:
                self.imu1_notify_btn.configure(text="Stop Notify")
                self.imu1_notifying = True
        else:
            await self.ble_service.stop_imu1_notify()
            self.imu1_notify_btn.configure(text="Start Notify")
            self.imu1_notifying = False

    async def _toggle_imu2_notify(self):
        if not self.imu2_notifying:
            success = await self.ble_service.start_imu2_notify(self._on_imu2_notify)
            if success:
                self.imu2_notify_btn.configure(text="Stop Notify")
                self.imu2_notifying = True
        else:
            await self.ble_service.stop_imu2_notify()
            self.imu2_notify_btn.configure(text="Start Notify")
            self.imu2_notifying = False

    def _disconnect_device(self):
        self.loop.create_task(self._disconnect_from_device())

    async def _disconnect_from_device(self):
        if await self.ble_service.disconnect():
            self.after(0, self._update_connection_status, False, "Disconnected")

    def on_closing(self):
        self._destroyed = True
        self.loop.create_task(self.ble_service.disconnect())
        self.loop.run_until_complete(asyncio.sleep(0.1))
        self.loop.stop()
        self.quit()

if __name__ == "__main__":
    ctk.set_appearance_mode(AppConfig.APPEARANCE_MODE)
    app = BLEMonitor()
    app.mainloop()
