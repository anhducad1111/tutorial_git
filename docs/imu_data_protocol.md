# Giao thức truyền dữ liệu IMU

## 1. Cấu trúc dữ liệu

### ESP32 (Phía gửi)
```cpp
struct ImuData {
    int16_t accel[3];  // X, Y, Z in mg
    int16_t gyro[3];   // X, Y, Z in 1/100th rad/s
    int16_t mag[3];    // X, Y, Z in uT
};
```

Dữ liệu được gửi dưới dạng 18 byte theo thứ tự:
1. Accelerometer (mỗi giá trị 2 byte, int16_t)
   - X: ±2000 mg
   - Y: ±2000 mg
   - Z: ±2000 mg

2. Gyroscope (mỗi giá trị 2 byte, int16_t)
   - X: ±200 (1/100th rad/s)
   - Y: ±200 (1/100th rad/s)
   - Z: ±200 (1/100th rad/s)

3. Magnetometer (mỗi giá trị 2 byte, int16_t)
   - X: ±50 uT
   - Y: ±50 uT
   - Z: ±50 uT

### Python (Phía nhận)
```python
# Parse 9 int16 values (little-endian)
values = struct.unpack('<9h', value)

# Format data structure
data = {
    'accel': {'x': values[0], 'y': values[1], 'z': values[2]},
    'gyro': {'x': values[3], 'y': values[4], 'z': values[5]},
    'mag': {'x': values[6], 'y': values[7], 'z': values[8]}
}
```

## 2. Quy trình truyền nhận

### Bên gửi (ESP32):
1. Tạo dữ liệu IMU (giả lập):
```cpp
ImuData generateRandomImuData() {
    ImuData data;
    // Accelerometer: ±2g (±2000mg)
    data.accel[i] = random(-2000, 2000);
    // Gyroscope: ±2 rad/s (±200)
    data.gyro[i] = random(-200, 200);
    // Magnetometer: ±50 uT
    data.mag[i] = random(-50, 50);
    return data;
}
```

2. Gửi dữ liệu:
```cpp
ImuData imuData = generateRandomImuData();
pImu1Char->setValue((uint8_t*)&imuData, sizeof(ImuData));
pImu1Char->notify();
```

### Bên nhận (Python):
1. Parse dữ liệu:
```python
values = struct.unpack('<9h', value)  # 9 int16 little-endian
```

2. Hiển thị:
```
Accelerometer (mg):
  X: -1234
  Y: 567
  Z: 890
Gyroscope (0.01 rad/s):
  X: -123
  Y: 45
  Z: -67
Magnetometer (uT):
  X: 12
  Y: -34
  Z: 45
Raw bytes: ff b2 37 04 7a 05 85 ff 2d 00 bd ff 0c 00 de ff 2d 00
```

## 3. Chu kỳ cập nhật
- IMU1: Mỗi 3 giây (3000ms)
- IMU2: Mỗi 5 giây (5000ms)

## 4. Định dạng dữ liệu

### Accelerometer
- Đơn vị: mg (milli-g)
- Phạm vi: ±2000 mg
- Độ phân giải: 1 mg

### Gyroscope
- Đơn vị: 0.01 rad/s
- Phạm vi: ±2.00 rad/s (±200)
- Độ phân giải: 0.01 rad/s

### Magnetometer
- Đơn vị: uT (micro Tesla)
- Phạm vi: ±50 uT
- Độ phân giải: 1 uT

## 5. Xử lý lỗi

### ESP32:
- Kiểm tra kết nối trước khi gửi
- Debug in giá trị để kiểm tra

### Python:
- Kiểm tra độ dài data (18 bytes)
- Xử lý ngoại lệ khi parse dữ liệu
- Hiển thị raw bytes để debug
