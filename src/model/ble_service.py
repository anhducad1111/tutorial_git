from bleak import BleakScanner, BleakClient
from src.model.imu import IMUData
from src.model.timestamp import TimestampData

class BLEDeviceInfo:
    """Model class for BLE device information"""
    
    def __init__(self, address, name="Unknown", rssi=0):
        self.address = address
        self.name = name
        self.rssi = rssi
        
    @classmethod
    def from_discovered_device(cls, device):
        """Create from discovered BLE device"""
        return cls(
            address=device.address,
            name=device.name or "Unknown Device",
            rssi=device.rssi or 0
        )

class BLEService:
    """Model for BLE service operations"""
    
    def __init__(self):
        self.client = None
        self._connected = False
        self.connected_device = None
        
    async def scan_devices(self):
        """Scan for available BLE devices"""
        try:
            devices = await BleakScanner.discover()
            return [BLEDeviceInfo.from_discovered_device(device) for device in devices]
        except Exception as e:
            print(f"Error scanning for devices: {e}")
            return []
        
    async def connect(self, device_info):
        """Connect to a BLE device"""
        try:
            self.client = BleakClient(device_info.address)
            await self.client.connect()
            self._connected = True
            self.connected_device = device_info
            return True
        except Exception as e:
            self._connected = False
            print(f"Connection error: {e}")
            return False
            
    async def disconnect(self):
        """Disconnect from the device"""
        if not self.is_connected():
            return True
            
        try:
            await self.client.disconnect()
            self._connected = False
            self.connected_device = None
            return True
        except Exception as e:
            print(f"Disconnection error: {e}")
            return False
            
    def is_connected(self):
        """Check if device is connected"""
        return self.client is not None and self._connected
    
    async def read_characteristic(self, uuid):
        """Read characteristic value"""
        if not self.is_connected():
            return None
            
        try:
            return await self.client.read_gatt_char(uuid)
        except Exception as e:
            print(f"Error reading characteristic {uuid}: {e}")
            return None
            
    async def write_characteristic(self, uuid, data):
        """Write characteristic value"""
        if not self.is_connected():
            return False
            
        try:
            await self.client.write_gatt_char(uuid, data)
            return True
        except Exception as e:
            print(f"Error writing characteristic {uuid}: {e}")
            return False
            
    async def start_notify(self, uuid, callback):
        """Start notifications for a characteristic"""
        if not self.is_connected():
            return False
            
        try:
            await self.client.start_notify(uuid, callback)
            return True
        except Exception as e:
            print(f"Error starting notifications for {uuid}: {e}")
            return False
            
    async def stop_notify(self, uuid):
        """Stop notifications for a characteristic"""
        if not self.is_connected():
            return True
            
        try:
            await self.client.stop_notify(uuid)
            return True
        except Exception as e:
            print(f"Error stopping notifications for {uuid}: {e}")
            return False