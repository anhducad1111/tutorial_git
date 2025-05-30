import asyncio
from bleak import BleakScanner
from src.model.ble_service import BLEDeviceInfo

class ConnectionPresenter:
    """Presenter for handling device connections"""
    
    def __init__(self, main_view, ble_service, loop):
        self.main_view = main_view  # The main view (DeviceMonitorView)
        self.service = ble_service
        self.loop = loop
        self.connection_dialog = None
        self.status_dialog = None
        
    def _create_device_info(self, device_dict):
        """Create BLEDeviceInfo from dictionary"""
        device_info = BLEDeviceInfo(
            name=device_dict['name'],
            address=device_dict['address'],
            rssi=device_dict['rssi']
        )
        device_info.view = self.main_view
        return device_info
        
    async def connect_to_device(self, device_dict=None):
        """Connect to a device. If device_dict is None, show connection dialog"""
        if device_dict is None:
            # Show connection dialog and handle device selection
            from src.view.connection_dialog import ConnectionDialog
            self.connection_dialog = ConnectionDialog(
                self.main_view,
                self.loop,
                BleakScanner
            )
            
            # Set up dialog callbacks
            self.connection_dialog.on_device_selected(self._on_device_selected)
            self.connection_dialog.on_connect_clicked(self._on_connect_clicked)
            
            # Start initial scan
            self.loop.create_task(self._scan_for_devices())
        else:
            # Direct connection to device (e.g. for reconnect)
            device_info = self._create_device_info(device_dict)
            
            # Try to connect silently
            result = await self.service.connect(device_info)
            if result:
                await self.service.start_services()
                self.main_view.update_connection_status(True, device_info)
            else:
                self.main_view.update_connection_status(False, None, "Connection failed")
        
    async def _scan_for_devices(self):
        """Handle device scanning"""
        if not self.connection_dialog:
            return
            
        self.connection_dialog.show_scanning()
        device_count = 0
        
        async def detection_callback(device, advertisement_data):
            nonlocal device_count
            if device.name:  # Only show devices with names
                self.connection_dialog.add_device(
                    device.name,
                    device.address,
                    advertisement_data.rssi
                )
                device_count += 1
        
        try:
            async with BleakScanner(detection_callback=detection_callback) as scanner:
                await asyncio.sleep(5)  # Scan for 5 seconds
        except Exception as e:
            print(f"Scan error: {e}")
            
        self.connection_dialog.show_scan_complete(device_count)
        
    def _on_device_selected(self, device_info):
        """Handle device selection"""
        # Update view with device info, nothing else needed
        pass
        
    async def _on_connect_clicked(self, device_dict):
        """Handle connect button click"""
        from src.view.connection_status_dialog import ConnectionStatusDialog
        
        # Create and show status dialog
        self.status_dialog = ConnectionStatusDialog(self.connection_dialog)
        self.status_dialog.show_connecting()
        
        # Set up callback for OK button that closes both dialogs first
        def close_dialogs_and_start_services():
            # Close both dialogs immediately
            if self.status_dialog:
                self.status_dialog.destroy()
            if self.connection_dialog:
                self.connection_dialog.destroy()
                
            # Then start services if connection was successful
            if self.connection_dialog.connection_success:
                async def start_services():
                    await self.service.start_services()
                    self.main_view.update_connection_status(True, self.current_device_info)
                self.loop.create_task(start_services())
            
        self.status_dialog.on_ok_clicked(close_dialogs_and_start_services)
        
        # Try to connect
        device_info = self._create_device_info(device_dict)
        result = await self.service.connect(device_info)
        
        if result:
            # Store device info for service start
            self.current_device_info = device_info
            self.status_dialog.show_connected(device_info)
            self.connection_dialog.connection_success = True
        else:
            self.current_device_info = None
            self.status_dialog.show_failed()
            self.connection_dialog.connection_success = False
            
    async def disconnect(self):
        """Disconnect from current device"""
        if hasattr(self.service, 'stop_battery_notify'):
            await self.service.stop_battery_notify()
        result = await self.service.disconnect()
        self.main_view.update_connection_status(False, None, "Disconnected")
        return result
        
    def is_connected(self):
        """Check if device is connected"""
        return self.service.is_connected()
        
    def get_connected_device(self):
        """Get currently connected device info"""
        return self.service.connected_device
