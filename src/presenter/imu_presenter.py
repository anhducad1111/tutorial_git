import asyncio
from src.model.imu import IMUData

class IMUPresenter:
    """Presenter for IMU data operations"""
    
    def __init__(self, view, ble_service, characteristic_uuid, loop):
        self.view = view
        self.service = ble_service
        self.char_uuid = characteristic_uuid
        self.loop = loop
        self.notifying = False
        
    async def read_data(self):
        """Read IMU data once"""
        if not self.service.is_connected():
            return False
            
        data = await self.service.read_characteristic(self.char_uuid)
        if data:
            imu_data = IMUData.from_bytes(data)
            if imu_data:
                self._update_view(imu_data)
                return True
        return False
        
    async def toggle_notifications(self):
        """Toggle notifications on/off"""
        if not self.service.is_connected():
            return False
            
        if self.notifying:
            result = await self.service.stop_notify(self.char_uuid)
            if result:
                self.notifying = False
                self.view.toggle_notify(False)
            return result
        else:
            result = await self.service.start_notify(
                self.char_uuid, 
                self._notification_handler
            )
            if result:
                self.notifying = True
                self.view.toggle_notify(True)
            return result
            
    async def _notification_handler(self, sender, data):
        """Handle incoming notifications"""
        imu_data = IMUData.from_bytes(data)
        if imu_data:
            # Use event loop to update UI from notification callback
            self.loop.create_task(self._update_view_async(imu_data))
            
    async def _update_view_async(self, imu_data):
        """Update view asynchronously (safe for callbacks)"""
        self._update_view(imu_data)
        
    def _update_view(self, imu_data):
        """Update view with IMU data"""
        self.view.update_accel(
            imu_data.accel['x'], 
            imu_data.accel['y'], 
            imu_data.accel['z']
        )
        self.view.update_gyro(
            imu_data.gyro['x'], 
            imu_data.gyro['y'], 
            imu_data.gyro['z']
        )
        self.view.update_magn(
            imu_data.mag['x'], 
            imu_data.mag['y'], 
            imu_data.mag['z']
        )
        self.view.update_debug_text(imu_data.to_hex_string())
        
    def is_notifying(self):
        """Check if notifications are active"""
        return self.notifying
