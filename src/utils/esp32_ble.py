from .ble_service import BLEService
import struct
import asyncio

class ESP32BLEService(BLEService):
    """ESP32-specific BLE service implementation"""
    
    def __init__(self):
        super().__init__()
        self.timestamp_uuid = "7AE63A01-7AD5-464B-803D-8A392D242CC7"
        self.imu1_uuid = "55A58E5B-9F51-47DC-B6C7-EE929BA79664"
        self.imu2_uuid = "84b70b01-8869-4a23-ab4f-fbfd1a25a925"

    def _process_timestamp(self, value):
        """Process timestamp value from bytes to uint64"""
        if len(value) != 8:
            return None
        try:
            timestamp = struct.unpack('<Q', value)[0]
            return timestamp
        except Exception as e:
            print(f"Error processing timestamp: {e}")
            return None

    def _process_imu_data(self, value):
        """Process IMU data from bytes to structured data"""
        try:
            if not value or len(value) != 18:
                return None
                
            # Parse 9 int16 values (little-endian)
            values = struct.unpack('<9h', value)
            
            # Format data structure
            data = {
                'accel': {'x': values[0], 'y': values[1], 'z': values[2]},
                'gyro': {'x': values[3], 'y': values[4], 'z': values[5]},
                'mag': {'x': values[6], 'y': values[7], 'z': values[8]}
            }
            
            # Format hex string
            hex_str = ' '.join(f'{b:02x}' for b in value)
            
            return data, hex_str
            
        except Exception as e:
            print(f"Error processing IMU data: {e}")
            return None

    def _format_imu_data(self, data):
        """Format IMU data for display"""
        return (
            f"Accelerometer (mg):\n"
            f"  X: {data['accel']['x']}\n"
            f"  Y: {data['accel']['y']}\n"
            f"  Z: {data['accel']['z']}\n"
            f"Gyroscope (0.01 rad/s):\n"
            f"  X: {data['gyro']['x']}\n"
            f"  Y: {data['gyro']['y']}\n"
            f"  Z: {data['gyro']['z']}\n"
            f"Magnetometer (uT):\n"
            f"  X: {data['mag']['x']}\n"
            f"  Y: {data['mag']['y']}\n"
            f"  Z: {data['mag']['z']}"
        )

    async def read_timestamp(self):
        """Read timestamp value"""
        return await self.read_characteristic(
            self.timestamp_uuid, 
            self._process_timestamp
        )

    async def write_timestamp(self, timestamp):
        """Write timestamp value"""
        try:
            value = struct.pack('<Q', int(timestamp))
            print(f"Writing timestamp bytes: {' '.join(f'{b:02x}' for b in value)}")
            return await self.write_characteristic(self.timestamp_uuid, value)
        except Exception as e:
            print(f"Error writing timestamp: {e}")
            return False

    async def read_imu1(self):
        """Read IMU1 value"""
        result = await self.read_characteristic(
            self.imu1_uuid,
            self._process_imu_data
        )
        if result:
            data, hex_str = result
            return self._format_imu_data(data), hex_str
        return None

    async def read_imu2(self):
        """Read IMU2 value"""
        result = await self.read_characteristic(
            self.imu2_uuid,
            self._process_imu_data
        )
        if result:
            data, hex_str = result
            return self._format_imu_data(data), hex_str
        return None

    async def start_imu1_notify(self, callback):
        """Start IMU1 notifications"""
        async def notification_handler(sender, data):
            result = self._process_imu_data(data)
            if result:
                data, hex_str = result
                await callback(sender, (self._format_imu_data(data), hex_str))
        return await self.start_notify(self.imu1_uuid, notification_handler)

    async def start_imu2_notify(self, callback):
        """Start IMU2 notifications"""
        async def notification_handler(sender, data):
            result = self._process_imu_data(data)
            if result:
                data, hex_str = result
                await callback(sender, (self._format_imu_data(data), hex_str))
        return await self.start_notify(self.imu2_uuid, notification_handler)

    async def stop_imu1_notify(self):
        """Stop IMU1 notifications"""
        return await self.stop_notify(self.imu1_uuid)

    async def stop_imu2_notify(self):
        """Stop IMU2 notifications"""
        return await self.stop_notify(self.imu2_uuid)
