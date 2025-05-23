import asyncio
from bleak import BleakScanner, BleakClient

class BLEService:
    """Base BLE service handling device scanning and connections"""
    
    def __init__(self):
        self.client = None
        
    async def scan_devices(self):
        """Scan for available BLE devices"""
        devices = await BleakScanner.discover()
        return devices
        
    async def connect_to_device(self, device_address):
        """Connect to a BLE device by address"""
        try:
            self.client = BleakClient(device_address)
            await self.client.connect()
            
            # Get all services after connection
            services = self.client.services
            
            # Format service information
            services_info = ""
            for service in services:
                services_info += f"\nService: {service.uuid}"
                for char in service.characteristics:
                    props = ', '.join(char.properties)
                    services_info += f"\n   ↳ Characteristic: {char.uuid}  (Properties: {props})"
                    
            return True, services_info
        except Exception as e:
            return False, str(e)
            
    async def disconnect(self):
        """Disconnect from the device"""
        if self.client and self.client.is_connected:
            await self.client.disconnect()
            self.client = None
            return True
        return False

    async def read_characteristic(self, uuid, process_func=None):
        """Generic read characteristic function"""
        if not self.client or not self.client.is_connected:
            return None
        try:
            value = await self.client.read_gatt_char(uuid)
            return process_func(value) if process_func else value
        except Exception as e:
            print(f"Error reading characteristic {uuid}: {e}")
            return None

    async def write_characteristic(self, uuid, value):
        """Generic write characteristic function"""
        if not self.client or not self.client.is_connected:
            return False
        try:
            await self.client.write_gatt_char(uuid, value)
            return True
        except Exception as e:
            print(f"Error writing characteristic {uuid}: {e}")
            return False

    async def start_notify(self, uuid, callback):
        """Generic start notification function"""
        if not self.client or not self.client.is_connected:
            return False
        try:
            await self.client.start_notify(uuid, callback)
            return True
        except Exception as e:
            print(f"Error starting notifications for {uuid}: {e}")
            return False

    async def stop_notify(self, uuid):
        """Generic stop notification function"""
        if not self.client or not self.client.is_connected:
            return False
        try:
            await self.client.stop_notify(uuid)
            return True
        except Exception as e:
            print(f"Error stopping notifications for {uuid}: {e}")
            return False
