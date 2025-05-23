# Kiến Thức Cơ Bản về Bluetooth Low Energy (BLE)

## Giới Thiệu về BLE

### So Sánh BLE với Bluetooth Cổ Điển

| Đặc điểm              | BLE                                      | Bluetooth Cổ Điển  |
| --------------------- | ---------------------------------------- | ------------------ |
| Tiêu thụ năng lượng   | Rất thấp (0.01x đến 0.5x)                | Cao                |
| Tốc độ truyền dữ liệu | 1 Mbps (BLE 4.0/4.1)<br>2 Mbps (BLE 5.0) | 1-3 Mbps           |
| Độ trễ                | 3ms                                      | 100ms              |
| Khoảng cách           | 10-50m (BLE 4.0/4.1)<br>200m (BLE 5.0)   | 10-100m            |
| Ứng dụng phổ biến     | IoT, thiết bị y tế, cảm biến             | Audio, truyền file |

### Ưu Điểm của BLE

1. **Tiết kiệm năng lượng**

   - Chu kỳ hoạt động ngắn
   - Chế độ ngủ khi không hoạt động
   - Tối ưu cho pin cúc áo (coin cell)

2. **Đơn giản hóa**

   - Giao thức đơn giản
   - Dễ triển khai
   - Chi phí thấp

3. **Tương thích**
   - Hỗ trợ đa nền tảng
   - Tích hợp sẵn trên nhiều thiết bị
   - Khả năng mở rộng tốt

### Nhược Điểm của BLE

1. **Giới hạn băng thông**

   - Tốc độ truyền thấp hơn Bluetooth cổ điển
   - Không phù hợp truyền file lớn
   - Độ trễ có thể thay đổi

2. **Khoảng cách**
   - Phụ thuộc môi trường
   - Bị ảnh hưởng bởi vật cản
   - Giảm hiệu suất ở khoảng cách xa

## Kiến Trúc Giao Thức BLE

### 1. Tầng Vật Lý (Physical Layer)

- **Tần số hoạt động**: 2.4GHz ISM band
- **Kênh truyền**: 40 kênh (37 kênh dữ liệu, 3 kênh quảng bá)
- **Điều chế**: GFSK (Gaussian Frequency Shift Keying)
- **Công suất phát**: -20dBm đến +10dBm

### 2. Tầng Liên Kết (Link Layer)

- **Vai trò**:

  - Quản lý trạng thái kết nối
  - Định dạng gói tin
  - Điều khiển luồng
  - Xử lý lỗi

- **Trạng thái hoạt động**:
  ```
  Standby → Advertising → Scanning → Initiating → Connected
  ```

### 3. Giao Diện Điều Khiển (HCI - Host Controller Interface)

- **Chức năng**:

  - Giao tiếp giữa host và controller
  - Truyền lệnh và sự kiện
  - Quản lý bộ đệm

- **Các loại gói tin HCI**:
  - Command packets
  - Event packets
  - Data packets
  - Synchronous packets

### 4. Giao Thức L2CAP (Logical Link Control and Adaptation Protocol)

- **Vai trò**:

  - Phân mảnh và tái tạo gói tin
  - Đa kênh logic trên một kênh vật lý
  - Quản lý QoS

- **Đặc điểm**:
  - MTU cố định: 23 bytes
  - Không hỗ trợ retransmission
  - Kênh tĩnh cho ATT và SMP

### 5. Giao Thức ATT (Attribute Protocol)

- **Cấu trúc dữ liệu**:

  - Attributes (UUID, Handle, Value)
  - Client/Server model
  - Operations (Read, Write, Notify, Indicate)

- **Ví dụ Attribute**:
  ```
  Handle: 0x0001
  Type: 0x2800 (Primary Service)
  Value: 0x180F (Battery Service)
  ```

### 6. Quản Lý Bảo Mật (SMP - Security Manager Protocol)

- **Chức năng**:

  - Ghép nối (Pairing)
  - Liên kết (Bonding)
  - Mã hóa (Encryption)

- **Cấp độ bảo mật**:
  1. Just Works
  2. Passkey Entry
  3. Out of Band
  4. Numeric Comparison (LE Secure)

## Ứng Dụng Thực Tế của BLE

### 1. Thiết Bị Y Tế

- Máy đo nhịp tim
- Máy đo đường huyết
- Thiết bị theo dõi sức khỏe

### 2. Internet of Things (IoT)

- Cảm biến môi trường
- Điều khiển thiết bị thông minh
- Hệ thống tự động hóa nhà thông minh

### 3. Định Vị và Theo Dõi

- Beacon
- Theo dõi tài sản
- Định vị trong nhà

## Tổng Kết

- BLE là công nghệ tối ưu cho các ứng dụng IoT và thiết bị di động
- Ưu điểm nổi bật về tiết kiệm năng lượng
- Kiến trúc giao thức phức tạp nhưng linh hoạt
- Phù hợp cho các ứng dụng cần truyền dữ liệu nhỏ, thời gian thực

## Tài Liệu Tham Khảo

1. [Bluetooth SIG - Core Specification](https://www.bluetooth.com/specifications/specs/)
2. [Introduction to Bluetooth Low Energy](https://learn.adafruit.com/introduction-to-bluetooth-low-energy)
3. [BLE Technical Overview](https://developer.android.com/guide/topics/connectivity/bluetooth-le)
