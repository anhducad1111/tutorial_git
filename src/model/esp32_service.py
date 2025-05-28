from src.model.ble_service import BLEService
from src.model.imu import IMUData, IMUEulerData
from src.model.timestamp import TimestampData
from src.model.sensor import FlexSensorData, ForceSensorData
from src.model.gamepad import JoystickData, ButtonsData
from src.model.overall_status import OverallStatus
from src.model.battery import BatteryLevelData, BatteryStateData

class ESP32BLEService(BLEService):
    """ESP32-specific BLE service implementation"""

    # Config value to name mappings
    ACCEL_GYRO_FREQ_MAP = {
        0: "LSM6DS_RATE_SHUTDOWN",
        1: "LSM6DS_RATE_12_5_HZ",
        2: "LSM6DS_RATE_26_HZ",
        3: "LSM6DS_RATE_52_HZ",
        4: "LSM6DS_RATE_104_HZ",
        5: "LSM6DS_RATE_208_HZ",
        6: "LSM6DS_RATE_416_HZ"
    }

    MAG_FREQ_MAP = {
        0: "LIS3MDL_DATARATE_0_625_HZ",
        1: "LIS3MDL_DATARATE_1_25_HZ",
        2: "LIS3MDL_DATARATE_2_5_HZ",
        3: "LIS3MDL_DATARATE_5_HZ",
        4: "LIS3MDL_DATARATE_10_HZ",
        5: "LIS3MDL_DATARATE_20_HZ",
        6: "LIS3MDL_DATARATE_40_HZ",
        7: "LIS3MDL_DATARATE_80_HZ"
    }

    ACCEL_RANGE_MAP = {
        0: "LSM6DS_ACCEL_RANGE_2_G",
        1: "LSM6DS_ACCEL_RANGE_4_G",
        2: "LSM6DS_ACCEL_RANGE_8_G",
        3: "LSM6DS_ACCEL_RANGE_16_G"
    }

    GYRO_RANGE_MAP = {
        0: "LSM6DS_GYRO_RANGE_125_DPS",
        1: "LSM6DS_GYRO_RANGE_250_DPS",
        2: "LSM6DS_GYRO_RANGE_500_DPS",
        3: "LSM6DS_GYRO_RANGE_1000_DPS",
        4: "LSM6DS_GYRO_RANGE_2000_DPS"
    }

    MAG_RANGE_MAP = {
        0: "LIS3MDL_RANGE_4_GAUSS",
        1: "LIS3MDL_RANGE_8_GAUSS",
        2: "LIS3MDL_RANGE_12_GAUSS",
        3: "LIS3MDL_RANGE_16_GAUSS"
    }

    # Reverse maps for config writing
    ACCEL_GYRO_FREQ_REV_MAP = {v: k for k, v in ACCEL_GYRO_FREQ_MAP.items()}
    MAG_FREQ_REV_MAP = {v: k for k, v in MAG_FREQ_MAP.items()}
    ACCEL_RANGE_REV_MAP = {v: k for k, v in ACCEL_RANGE_MAP.items()}
    GYRO_RANGE_REV_MAP = {v: k for k, v in GYRO_RANGE_MAP.items()}
    MAG_RANGE_REV_MAP = {v: k for k, v in MAG_RANGE_MAP.items()}
    
    # Device UUIDs and their corresponding data classes
    CHARACTERISTICS = {
        # Standard UUIDs
        "FIRMWARE_UUID": ("2A26", str),
        "MODEL_NUMBER_UUID": ("2A24", str),
        "MANUFACTURER_UUID": ("2A29", str),
        "HARDWARE_UUID": ("2A27", str),

        # Battery UUIDs
        "BATTERY_LEVEL_UUID": ("2A19", BatteryLevelData),
        "BATTERY_CHARGING_UUID": ("2A1A", BatteryStateData),

        # Configuration UUID
        "CONFIG_UUID": ("289f76d8-2edb-455d-8c3c-aabb42ab5b5c", None),  # Raw config characteristic

        # Device UUIDs
        "IMU1_CHAR_UUID": ("55A58E5B-9F51-47DC-B6C7-EE929BA79664", IMUData),
        "IMU2_CHAR_UUID": ("84b70b01-8869-4a23-ab4f-fbfd1a25a925", IMUData),
        "IMU1_EULER_UUID": ("5ABB059E-C70F-4E49-9C9D-16D546404E36", IMUEulerData),
        "IMU2_EULER_UUID": ("83370305-9668-44d5-b14d-7f1f480d6f17", IMUEulerData),
        "TIMESTAMP_CHAR_UUID": ("7AE63A01-7AD5-464B-803D-8A392D242CC7", TimestampData),
        "OVERALL_STATUS_UUID": ("b840e25c-183a-4a7e-8ec6-9a29ecc7ffdb", OverallStatus),
        "FLEX_SENSOR_UUID": ("9FE3F26A-8A04-4DB5-A97F-B24DCED652F9", FlexSensorData),
        "FORCE_SENSOR_UUID": ("f1461563-772e-43d4-ab00-8d2ac54c94f9", ForceSensorData),
        "JOYSTICK_UUID": ("c91e9c03-b4be-4bb2-a2a2-21f52353265a", JoystickData),
        "BUTTONS_UUID": ("34afe3d1-643e-4fe7-abd2-7e7a0cfb1601", ButtonsData)
    }

    def __init__(self):
        super().__init__()
        # Create UUID class attributes and initialize callbacks dictionary
        self._callbacks = {}
        for name, (uuid, _) in self.CHARACTERISTICS.items():
            setattr(self, name, uuid)
            self._callbacks[uuid] = None

    # Implement required abstract methods
    async def check_firmware_revision(self):
        """Check firmware revision string"""
        return await self._read_characteristic_data(self.FIRMWARE_UUID)
            
    async def check_model_number(self):
        """Check model number string"""
        return await self._read_characteristic_data(self.MODEL_NUMBER_UUID)
            
    async def check_manufacturer(self):
        """Check manufacturer string"""
        return await self._read_characteristic_data(self.MANUFACTURER_UUID)
            
    async def check_hardware_revision(self):
        """Check hardware revision string"""
        return await self._read_characteristic_data(self.HARDWARE_UUID)

    async def read_config(self):
        """Read IMU and sensor configuration"""
        if not self.is_connected():
            return None
        try:
            data = await self.read_characteristic(self.CONFIG_UUID)
            if not data or len(data) < 15:  # Must have at least 15 bytes
                return None
            return data
        except Exception as e:
            print(f"Error reading config: {e}")
            return None
            
    async def write_config(self, data):
        """Write IMU and sensor configuration
        
        Args:
            data (bytes): 15 bytes configuration data
        Returns:
            bool: True if successful
        """
        if not self.is_connected() or not data or len(data) != 15:
            return False
        try:
            await self.write_characteristic(self.CONFIG_UUID, data)
            return True
        except Exception as e:
            print(f"Error writing config: {e}")
            return False

    async def connect(self, device_info):
        """Connect to a BLE device and check profiles"""
        result = await super().connect(device_info)
        if result:
            # Read device profiles and update device_info
            device_info.firmware = await self.check_firmware_revision()
            device_info.model = await self.check_model_number()
            device_info.manufacturer = await self.check_manufacturer()
            device_info.hardware = await self.check_hardware_revision()

            # Start battery notifications
            if hasattr(device_info, 'view'):
                await self._start_battery_notifications(device_info.view)
        return result

    async def _read_characteristic_data(self, uuid):
        """Generic method to read and parse characteristic data"""
        if not self.is_connected():
            return None

        try:
            data = await self.read_characteristic(uuid)
            if not data:
                return None

            # Get the data class for this UUID
            data_class = next((cls for _, (u, cls) in self.CHARACTERISTICS.items() if u == uuid), None)
            if not data_class:
                return None

            # Handle string data types
            if data_class == str:
                return data.decode('utf-8')
            
            # Handle data model classes
            return data_class.from_bytes(data)

        except Exception as e:
            print(f"Error reading characteristic {uuid}: {e}")
            return None

    async def _write_characteristic_data(self, uuid, data):
        """Generic method to write characteristic data"""
        if not self.is_connected() or not data:
            return False

        try:
            # Handle data objects with raw_data attribute
            raw_data = data.raw_data if hasattr(data, 'raw_data') else data
            await self.write_characteristic(uuid, raw_data)
            return True
        except Exception as e:
            print(f"Error writing characteristic {uuid}: {e}")
            return False

    async def _generic_notification_handler(self, sender, data, callback, data_class):
        """Generic handler for notifications"""
        try:
            if data_class == str:
                parsed_data = data.decode('utf-8')
            else:
                parsed_data = data_class.from_bytes(data)

            if parsed_data and callback:
                if isinstance(parsed_data, (BatteryLevelData, BatteryStateData)):
                    # Special handling for battery data
                    value = parsed_data.level if isinstance(parsed_data, BatteryLevelData) else parsed_data.state_text
                    await callback(value)
                else:
                    await callback(sender, parsed_data)

        except Exception as e:
            print(f"Error in {data_class.__name__} notification handler: {e}")

    async def _start_notify_generic(self, uuid, callback):
        """Generic method to start notifications"""
        if not self.is_connected():
            return False
            
        try:
            # Get the data class for this UUID
            data_class = next((cls for _, (u, cls) in self.CHARACTERISTICS.items() if u == uuid), None)
            if not data_class:
                return False

            self._callbacks[uuid] = callback
            async def handler(sender, data):
                await self._generic_notification_handler(sender, data, callback, data_class)
            await self.client.start_notify(uuid, handler)
            return True
        except Exception as e:
            print(f"Error starting notifications for {uuid}: {e}")
            return False

    async def _stop_notify_generic(self, uuid):
        """Generic method to stop notifications"""
        if not self.client:  # Already disconnected
            self._callbacks[uuid] = None
            return True
            
        try:
            await self.client.stop_notify(uuid)
            self._callbacks[uuid] = None
            return True
        except Exception as e:
            if hasattr(e, 'args') and len(e.args) > 0:
                err_code = str(e.args[0])
                if err_code == "61":  # Already stopped
                    self._callbacks[uuid] = None
                    return True
            print(f"Error stopping notifications for {uuid}: {e}")
            return False

    async def _start_battery_notifications(self, view):
        """Start battery and charging notifications"""
        await self._start_notify_generic(self.BATTERY_LEVEL_UUID, view.update_battery)
        await self._start_notify_generic(self.BATTERY_CHARGING_UUID, view.update_charging)

    # IMU Methods
    async def start_imu1_notify(self, callback):
        """Start IMU1 notifications"""
        return await self._start_notify_generic(self.IMU1_CHAR_UUID, callback)
    
    async def start_imu2_notify(self, callback):
        """Start IMU2 notifications"""
        return await self._start_notify_generic(self.IMU2_CHAR_UUID, callback)
    
    async def stop_imu1_notify(self):
        """Stop IMU1 notifications"""
        return await self._stop_notify_generic(self.IMU1_CHAR_UUID)
    
    async def stop_imu2_notify(self):
        """Stop IMU2 notifications"""
        return await self._stop_notify_generic(self.IMU2_CHAR_UUID)

    # IMU Euler Methods
    async def start_imu1_euler_notify(self, callback):
        """Start IMU1 Euler angles notifications"""
        return await self._start_notify_generic(self.IMU1_EULER_UUID, callback)

    async def start_imu2_euler_notify(self, callback):
        """Start IMU2 Euler angles notifications"""
        return await self._start_notify_generic(self.IMU2_EULER_UUID, callback)

    async def stop_imu1_euler_notify(self):
        """Stop IMU1 Euler angles notifications"""
        return await self._stop_notify_generic(self.IMU1_EULER_UUID)

    async def stop_imu2_euler_notify(self):
        """Stop IMU2 Euler angles notifications"""
        return await self._stop_notify_generic(self.IMU2_EULER_UUID)

    # Overall Status Methods
    async def start_overall_status_notify(self, callback):
        """Start overall status notifications"""
        return await self._start_notify_generic(self.OVERALL_STATUS_UUID, callback)
            
    async def stop_overall_status_notify(self):
        """Stop overall status notifications"""
        return await self._stop_notify_generic(self.OVERALL_STATUS_UUID)

    # Sensor Methods
    async def start_flex_sensor_notify(self, callback):
        """Start flex sensor notifications"""
        return await self._start_notify_generic(self.FLEX_SENSOR_UUID, callback)

    async def start_force_sensor_notify(self, callback):
        """Start force sensor notifications"""
        return await self._start_notify_generic(self.FORCE_SENSOR_UUID, callback)

    async def stop_flex_sensor_notify(self):
        """Stop flex sensor notifications"""
        return await self._stop_notify_generic(self.FLEX_SENSOR_UUID)

    async def stop_force_sensor_notify(self):
        """Stop force sensor notifications"""
        return await self._stop_notify_generic(self.FORCE_SENSOR_UUID)

    # Gamepad Methods
    async def start_joystick_notify(self, callback):
        """Start joystick notifications"""
        return await self._start_notify_generic(self.JOYSTICK_UUID, callback)

    async def start_buttons_notify(self, callback):
        """Start buttons notifications"""
        return await self._start_notify_generic(self.BUTTONS_UUID, callback)

    async def stop_joystick_notify(self):
        """Stop joystick notifications"""
        return await self._stop_notify_generic(self.JOYSTICK_UUID)

    async def stop_buttons_notify(self):
        """Stop buttons notifications"""
        return await self._stop_notify_generic(self.BUTTONS_UUID)

    # Battery Methods
    async def stop_battery_notify(self):
        """Stop battery notifications"""
        await self._stop_notify_generic(self.BATTERY_LEVEL_UUID)
        await self._stop_notify_generic(self.BATTERY_CHARGING_UUID)

    # Read/Write Methods
    async def read_imu1(self):
        """Read IMU1 data"""
        return await self._read_characteristic_data(self.IMU1_CHAR_UUID)
    
    async def read_imu2(self):
        """Read IMU2 data"""
        return await self._read_characteristic_data(self.IMU2_CHAR_UUID)
    
    async def read_timestamp(self):
        """Read timestamp data"""
        return await self._read_characteristic_data(self.TIMESTAMP_CHAR_UUID)

    async def write_timestamp(self, timestamp_data):
        """Write timestamp data"""
        return await self._write_characteristic_data(self.TIMESTAMP_CHAR_UUID, timestamp_data)
