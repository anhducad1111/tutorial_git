# Hướng Dẫn Lập Trình với Bleak

## Giới Thiệu về Bleak

### Tổng Quan
- **Bleak** (Bluetooth Low Energy platform Agnostic Klient) là thư viện Python
- Hỗ trợ đa nền tảng: Windows, Linux, MacOS
- Sử dụng async/await cho lập trình bất đồng bộ
- Giao diện đơn giản và dễ sử dụng

### Cài Đặt và Thiết Lập
```bash
# Cài đặt qua pip
pip install bleak

# Yêu cầu Python >= 3.7
```

## Các Tính Năng Cơ Bản

### 1. Quét Thiết Bị BLE
```python
import asyncio
from bleak import BleakScanner

async def scan_devices():
    devices = await BleakScanner.discover()
    for d in devices:
        print(f"Tìm thấy thiết bị: {d.name} ({d.address})")

# Chạy scanner
asyncio.run(scan_devices())
```

### 2. Kết Nối Thiết Bị
```python
from bleak import BleakClient

async def connect_device(address):
    async with BleakClient(address) as client:
        # Kiểm tra kết nối
        if client.is_connected:
            print(f"Đã kết nối với {address}")
            
            # Thực hiện các thao tác với thiết bị
            services = await client.get_services()
            for service in services:
                print(f"Service: {service.uuid}")
```

### 3. Đọc và Ghi Characteristic
```python
async def read_write_example(address, char_uuid):
    async with BleakClient(address) as client:
        # Đọc giá trị
        value = await client.read_gatt_char(char_uuid)
        print(f"Giá trị đọc được: {value}")
        
        # Ghi giá trị
        await client.write_gatt_char(
            char_uuid,
            b"Hello BLE",  # Dữ liệu dạng bytes
            response=True  # Chờ phản hồi
        )
```

### 4. Đăng Ký Nhận Thông Báo
```python
def notification_handler(sender: int, data: bytearray):
    print(f"Nhận thông báo từ {sender}: {data}")

async def enable_notifications(address, char_uuid):
    async with BleakClient(address) as client:
        await client.start_notify(
            char_uuid,
            notification_handler
        )
        
        # Chờ nhận thông báo trong 60 giây
        await asyncio.sleep(60)
        
        await client.stop_notify(char_uuid)
```

## Ví Dụ Thực Tế

### 1. Ứng Dụng Đọc Cảm Biến Nhiệt Độ
```python
import asyncio
from bleak import BleakClient

TEMPERATURE_SERVICE_UUID = "0000181A-0000-1000-8000-00805F9B34FB"
TEMPERATURE_CHAR_UUID = "00002A1C-0000-1000-8000-00805F9B34FB"

class TemperatureSensor:
    def __init__(self, address):
        self.address = address
        self.client = None
        
    async def connect(self):
        self.client = BleakClient(self.address)
        await self.client.connect()
        
    async def read_temperature(self):
        if not self.client.is_connected:
            await self.connect()
            
        temp_bytes = await self.client.read_gatt_char(
            TEMPERATURE_CHAR_UUID
        )
        return float(int.from_bytes(temp_bytes, 'little')) / 100

    async def monitor_temperature(self, callback):
        def temperature_handler(_, data):
            temp = float(int.from_bytes(data, 'little')) / 100
            callback(temp)
            
        await self.client.start_notify(
            TEMPERATURE_CHAR_UUID,
            temperature_handler
        )

# Sử dụng
async def main():
    sensor = TemperatureSensor("XX:XX:XX:XX:XX:XX")
    
    # Đọc một lần
    temp = await sensor.read_temperature()
    print(f"Nhiệt độ hiện tại: {temp}°C")
    
    # Giám sát liên tục
    def on_temperature(temp):
        print(f"Nhiệt độ mới: {temp}°C")
    
    await sensor.monitor_temperature(on_temperature)
    await asyncio.sleep(300)  # Giám sát trong 5 phút
```

### 2. Ứng Dụng Điều Khiển LED
```python
import asyncio
from bleak import BleakClient

LED_SERVICE_UUID = "YOUR_LED_SERVICE_UUID"
LED_CHAR_UUID = "YOUR_LED_CHAR_UUID"

class LEDController:
    def __init__(self, address):
        self.address = address
        self.client = None
        
    async def connect(self):
        self.client = BleakClient(self.address)
        await self.client.connect()
        
    async def turn_on(self):
        await self.client.write_gatt_char(
            LED_CHAR_UUID,
            b'\x01'
        )
        
    async def turn_off(self):
        await self.client.write_gatt_char(
            LED_CHAR_UUID,
            b'\x00'
        )
        
    async def set_brightness(self, level: int):
        # level: 0-100
        await self.client.write_gatt_char(
            LED_CHAR_UUID,
            bytes([level])
        )
```

## Xử Lý Lỗi và Debug

### 1. Xử Lý Lỗi Kết Nối
```python
from bleak.exc import BleakError

async def safe_connect(address):
    try:
        async with BleakClient(address) as client:
            print("Kết nối thành công")
    except BleakError as e:
        print(f"Lỗi kết nối: {e}")
    except Exception as e:
        print(f"Lỗi không xác định: {e}")
```

### 2. Retry Mechanism
```python
import asyncio
from bleak import BleakError

async def connect_with_retry(address, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            client = BleakClient(address)
            await client.connect()
            return client
        except BleakError:
            if attempt == max_attempts - 1:
                raise
            print(f"Kết nối thất bại, thử lại ({attempt + 1}/{max_attempts})")
            await asyncio.sleep(1)
```

### 3. Logging và Debug
```python
import logging

# Thiết lập logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Sử dụng trong code
logger = logging.getLogger(__name__)
logger.debug("Đang quét thiết bị...")
logger.info("Tìm thấy thiết bị mới")
logger.warning("Kết nối không ổn định")
logger.error("Không thể kết nối")
```

## Tối Ưu Hiệu Suất

### 1. Connection Parameters
```python
async def optimize_connection(client):
    # Điều chỉnh các tham số kết nối nếu được hỗ trợ
    await client.write_gatt_char(
        "CONNECTION_PARAMS_CHAR_UUID",
        bytes([
            0x20, 0x00,  # min_interval (32 units = 40ms)
            0x30, 0x00,  # max_interval (48 units = 60ms)
            0x00, 0x00,  # slave_latency
            0xE8, 0x03   # supervision_timeout (1000 units = 10s)
        ])
    )
```

### 2. Batch Operations
```python
async def batch_read_characteristics(client, char_uuids):
    results = {}
    # Đọc nhiều characteristics cùng lúc
    tasks = [
        client.read_gatt_char(uuid)
        for uuid in char_uuids
    ]
    values = await asyncio.gather(*tasks)
    
    for uuid, value in zip(char_uuids, values):
        results[uuid] = value
    
    return results
```

### 3. Quản Lý Tài Nguyên
```python
class BLEDevice:
    def __init__(self, address):
        self.address = address
        self.client = None
    
    async def __aenter__(self):
        self.client = BleakClient(self.address)
        await self.client.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.disconnect()
```

## Các Mẫu Thiết Kế Phổ Biến

### 1. Observer Pattern
```python
class BLEDeviceManager:
    def __init__(self):
        self.observers = []
    
    def add_observer(self, observer):
        self.observers.append(observer)
    
    def notify_observers(self, data):
        for observer in self.observers:
            observer.update(data)

class TemperatureObserver:
    def update(self, temperature):
        print(f"Nhiệt độ mới: {temperature}°C")
```

### 2. Async Iterator
```python
class BLEDataStream:
    def __init__(self, client, char_uuid):
        self.client = client
        self.char_uuid = char_uuid
        self.buffer = asyncio.Queue()
    
    def data_handler(self, _, data):
        self.buffer.put_nowait(data)
    
    async def __aiter__(self):
        await self.client.start_notify(
            self.char_uuid,
            self.data_handler
        )
        return self
    
    async def __anext__(self):
        return await self.buffer.get()
```

## Tổng Kết
- Bleak cung cấp API đơn giản cho BLE
- Hỗ trợ đa nền tảng
- Xử lý bất đồng bộ hiệu quả
- Dễ dàng mở rộng và tùy chỉnh

## Tài Liệu Tham Khảo
1. [Bleak Documentation](https://bleak.readthedocs.io/)
2. [Bleak GitHub Repository](https://github.com/hbldh/bleak)
3. [Async Python Guide](https://docs.python.org/3/library/asyncio.html)
