from src.model.ble_service import BLEService
from src.model.imu import IMUData
from src.model.timestamp import TimestampData

class ESP32BLEService(BLEService):
    """ESP32-specific BLE service implementation"""
    
    # UUIDs
    IMU1_CHAR_UUID = "55A58E5B-9F51-47DC-B6C7-EE929BA79664"
    IMU2_CHAR_UUID = "84b70b01-8869-4a23-ab4f-fbfd1a25a925"
    TIMESTAMP_CHAR_UUID = "7AE63A01-7AD5-464B-803D-8A392D242CC7"
    
    def __init__(self):
        super().__init__()
        self._imu1_notify_callback = None
        self._imu2_notify_callback = None
    
    async def read_imu(self, char_uuid):
        """Read IMU data from a characteristic"""
        if not self.is_connected():
            return None
            
        try:
            data = await self.client.read_gatt_char(char_uuid)
            imu_data = IMUData.from_bytes(data)
            return imu_data
        except Exception as e:
            print(f"Error reading IMU data: {e}")
            return None
    
    async def read_imu1(self):
        """Read IMU1 data"""
        return await self.read_imu(self.IMU1_CHAR_UUID)
    
    async def read_imu2(self):
        """Read IMU2 data"""
        return await self.read_imu(self.IMU2_CHAR_UUID)
    
    async def read_timestamp(self):
        """Read timestamp data"""
        if not self.is_connected():
            return None
            
        try:
            data = await self.client.read_gatt_char(self.TIMESTAMP_CHAR_UUID)
            return TimestampData.from_bytes(data)
        except Exception as e:
            print(f"Error reading timestamp: {e}")
            return None
    
    async def write_timestamp(self, timestamp_data):
        """Write timestamp data"""
        if not self.is_connected():
            return False
            
        try:
            await self.client.write_gatt_char(self.TIMESTAMP_CHAR_UUID, timestamp_data.raw_data)
            return True
        except Exception as e:
            print(f"Error writing timestamp: {e}")
            return False
    
    async def _notification_handler(self, sender, data, callback):
        """Handle notification data"""
        try:
            imu_data = IMUData.from_bytes(data)
            if imu_data and callback:
                await callback(sender, imu_data)
        except Exception as e:
            print(f"Error in notification handler: {e}")
    
    async def start_imu_notify(self, uuid, callback):
        """Start IMU notifications for a characteristic"""
        if not self.is_connected():
            return False
            
        try:
            async def handler(sender, data):
                await self._notification_handler(sender, data, callback)
                
            await self.client.start_notify(uuid, handler)
            return True
        except Exception as e:
            print(f"Error starting notifications: {e}")
            return False
    
    async def start_imu1_notify(self, callback):
        """Start IMU1 notifications"""
        self._imu1_notify_callback = callback
        return await self.start_imu_notify(self.IMU1_CHAR_UUID, callback)
    
    async def start_imu2_notify(self, callback):
        """Start IMU2 notifications"""
        self._imu2_notify_callback = callback
        return await self.start_imu_notify(self.IMU2_CHAR_UUID, callback)
    
    async def stop_imu1_notify(self):
        """Stop IMU1 notifications"""
        if not self.is_connected():
            return False
            
        try:
            await self.client.stop_notify(self.IMU1_CHAR_UUID)
            return True
        except Exception as e:
            print(f"Error stopping IMU1 notifications: {e}")
            return False
    
    async def stop_imu2_notify(self):
        """Stop IMU2 notifications"""
        if not self.is_connected():
            return False
            
        try:
            await self.client.stop_notify(self.IMU2_CHAR_UUID)
            return True
        except Exception as e:
            print(f"Error stopping IMU2 notifications: {e}")
            return False
