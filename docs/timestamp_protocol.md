# Giao thức truyền dữ liệu Timestamp

## 1. Cấu trúc dữ liệu

### ESP32 (Phía gửi)

```cpp
uint64_t currentTime = time(nullptr);  // Unix timestamp dạng uint64
```

Dữ liệu được gửi dưới dạng 8 byte (64-bit), trong đó:

- Dạng số: Unix timestamp (số giây từ 1/1/1970)
- Kiểu: uint64_t
- Thứ tự byte: Little-endian

### Python (Phía nhận)

```python
struct.unpack('<Q', value)[0]  # Giải mã 8 byte thành uint64
```

## 2. Quy trình đọc/ghi

### Đọc timestamp:

1. ESP32:

```cpp
uint64_t currentTime = time(nullptr);  // Lấy thời gian hiện tại
pTimestampChar->setValue((uint8_t*)&currentTime, 8);  // Gửi 8 byte
```

2. Python:

```python
# Đọc và giải mã
timestamp = struct.unpack('<Q', value)[0]
# Hiển thị
dt = datetime.fromtimestamp(timestamp)
print(f"Unix: {timestamp}, Date: {dt}")
```

### Ghi timestamp:

1. Python:

```python
# Đóng gói timestamp thành 8 byte
value = struct.pack('<Q', timestamp)
await characteristic.write(value)
```

2. ESP32:

```cpp
// Nhận và cập nhật thời gian hệ thống
uint64_t timestamp;
memcpy(&timestamp, value.data(), 8);
timeval tv = { (time_t)timestamp, 0 };
settimeofday(&tv, NULL);
```

## 3. Định dạng dữ liệu

### Ví dụ giá trị

```
Unix timestamp: 1684813200
Date/Time: 2023-05-23 00:00:00
```

### Dạng bytes (Little-endian)

```
[00 95 15 64 00 00 00 00]
```

## 4. Các tính năng

### Read Timestamp

- Đọc thời gian hiện tại từ ESP32
- Hiển thị cả timestamp và datetime

### Write Current Time

- Gửi thời gian hiện tại của máy tính đến ESP32
- ESP32 cập nhật thời gian hệ thống

## 5. Xử lý lỗi

### ESP32:

- Kiểm tra độ dài dữ liệu (phải là 8 byte)
- Kiểm tra kết nối trước khi gửi

### Python:

- Xử lý ngoại lệ khi giải mã bytes
- Xử lý timestamp không hợp lệ
- Hiển thị thông báo lỗi khi cần

## 6. Chú ý

- ESP32 sẽ giữ thời gian kể cả khi mất kết nối BLE
- Mỗi lần kết nối mới nên đồng bộ lại thời gian
- Sử dụng uint64_t để tránh vấn đề năm 2038
