# Cấu trúc BLE Service

## 1. Định nghĩa UUID

### Service UUID
```
"4fafc201-1fb5-459e-8fcc-c5c9c331914b"
```

### Characteristics UUIDs
```
Timestamp: "7AE63A01-7AD5-464B-803D-8A392D242CC7"
IMU1: "55A58E5B-9F51-47DC-B6C7-EE929BA79664"  
IMU2: "84b70b01-8869-4a23-ab4f-fbfd1a25a925"
```

## 2. Các Characteristics

### Timestamp
- Quyền: Read, Write
- Độ dài: 8 bytes
- Định dạng: uint64 (Little-endian)
- Mục đích: Đọc/ghi thời gian hệ thống

### IMU1
- Quyền: Read, Notify
- Độ dài: 18 bytes
- Chu kỳ notify: 3 giây
- Mục đích: Đọc dữ liệu cảm biến 1

### IMU2
- Quyền: Read, Notify
- Độ dài: 18 bytes
- Chu kỳ notify: 5 giây
- Mục đích: Đọc dữ liệu cảm biến 2

## 3. Kiến trúc phần mềm

### ESP32 (Server)
```cpp
class ServerCallbacks: public NimBLEServerCallbacks {
    void onConnect();
    void onDisconnect();
}

class TimestampCallbacks: public NimBLECharacteristicCallbacks {
    void onWrite();
}
```

### Python (Client)
```python
class ESP32BLEService:
    async def connect_to_device()
    async def read_characteristic()
    async def write_characteristic()
    async def start_notify()
    async def stop_notify()
```

## 4. Quy trình kết nối

1. Server (ESP32):
   - Khởi tạo BLE device
   - Tạo service và characteristics
   - Bắt đầu quảng bá

2. Client (Python):
   - Quét tìm thiết bị
   - Kết nối tới địa chỉ MAC
   - Đọc/ghi characteristics
   - Đăng ký notify (nếu cần)

## 5. Quản lý kết nối

### Server side:
- Tự động bắt đầu quảng bá khi khởi động
- Dừng quảng bá khi có kết nối
- Tự động quảng bá lại khi mất kết nối

### Client side:
- Hiển thị danh sách thiết bị tìm thấy
- Quản lý trạng thái kết nối
- Xử lý mất kết nối tự động

## 6. Xử lý dữ liệu

### Timestamp:
- Gửi/nhận: 8 bytes
- Định dạng: Little-endian uint64
- Chuyển đổi thành datetime

### IMU data:
- Gửi/nhận: 18 bytes array
- Chuyển đổi thành list int
- Lấy giá trị đầu tiên để hiển thị

## 7. Giao diện người dùng
- Nút Connect/Disconnect
- Nút Read/Write timestamp
- Nút Start/Stop notify cho IMU
- Hiển thị giá trị timestamp và IMU
- Hiển thị trạng thái kết nối

## 8. Chú ý bảo mật
- Không yêu cầu xác thực
- Không mã hóa dữ liệu
- Chỉ nên sử dụng trong môi trường phát triển
