# Lộ Trình Học Bluetooth Low Energy (BLE) và Bleak

## 1. Kiến Thức Cơ Bản về BLE

- Tổng quan về BLE
  - So sánh BLE với Bluetooth cổ điển
  - Ưu điểm và nhược điểm của BLE
  - Các ứng dụng phổ biến của BLE
- Kiến trúc giao thức BLE
  - Tầng vật lý (Physical Layer)
  - Tầng liên kết (Link Layer)
  - Giao diện điều khiển máy chủ (Host Controller Interface - HCI)
  - Giao thức điều khiển và thích ứng liên kết logic (L2CAP)
  - Quản lý bảo mật (Security Manager Protocol - SMP)
  - Giao thức thuộc tính (Attribute Protocol - ATT)

## 2. Vai Trò và Mô Hình Kết Nối BLE

- Các vai trò trong BLE
  - Central (Thiết bị trung tâm)
    - Vai trò quét và kết nối
    - Quản lý kết nối
  - Peripheral (Thiết bị ngoại vi)
    - Quảng bá dữ liệu
    - Phản hồi yêu cầu kết nối
- Quy trình kết nối
  - Quảng bá (Advertising)
  - Quét (Scanning)
  - Thiết lập kết nối
  - Trao đổi dữ liệu

## 3. GATT Services và Characteristics

- Cấu trúc GATT
  - Services (Dịch vụ)
    - Định nghĩa và mục đích
    - UUID của service
  - Characteristics (Đặc tính)
    - Cấu trúc dữ liệu
    - Quyền truy cập
  - Descriptors (Bộ mô tả)
- Các thuộc tính của Characteristic
  - Read (Đọc)
  - Write (Ghi)
  - Notify (Thông báo)
  - Indicate (Chỉ báo)
- Services tiêu chuẩn phổ biến
  - Device Information Service
  - Battery Service
  - Heart Rate Service
  - Environmental Sensing Service

## 4. Làm Quen với Bleak

- Giới thiệu về Bleak
  - Tổng quan và ưu điểm
  - Cài đặt và thiết lập môi trường
  - Yêu cầu hệ thống
- Các tính năng cơ bản
  - Quét thiết bị
  - Kết nối thiết bị
  - Đọc/ghi characteristics
  - Đăng ký thông báo

## 5. Lập Trình với Bleak

- Thiết lập môi trường
  ```python
  pip install bleak
  ```
- Các thao tác cơ bản

  - Quét thiết bị

  ```python
  from bleak import BleakScanner
  devices = await BleakScanner.discover()
  ```

  - Kết nối tới thiết bị

  ```python
  from bleak import BleakClient
  async with BleakClient(address) as client:
      # Thực hiện các thao tác
  ```

  - Đọc characteristic

  ```python
  value = await client.read_gatt_char(characteristic_uuid)
  ```

  - Ghi characteristic

  ```python
  await client.write_gatt_char(characteristic_uuid, data)
  ```

  - Đăng ký nhận thông báo

  ```python
  def notification_handler(sender, data):
      print(f"Received: {data}")

  await client.start_notify(characteristic_uuid, notification_handler)
  ```

## 6. Thực Hành và Ứng Dụng

- Xây dựng ứng dụng đơn giản
  - Quét và hiển thị danh sách thiết bị
  - Kết nối với thiết bị BLE
  - Đọc/ghi dữ liệu
  - Xử lý thông báo
- Các kịch bản thực tế
  - Thu thập dữ liệu cảm biến
  - Điều khiển thiết bị
  - Giám sát trạng thái thiết bị

## 7. Bảo Mật và Tối Ưu

- Bảo mật trong BLE
  - Mã hóa và xác thực
  - Ghép nối thiết bị
  - Các mô hình bảo mật
- Tối ưu hiệu năng
  - Quản lý năng lượng
  - Tối ưu kết nối
  - Xử lý lỗi và khôi phục

## Tài Nguyên Học Tập

- Tài liệu chính thức
  - [Bleak Documentation](https://bleak.readthedocs.io/)
  - [Bluetooth SIG](https://www.bluetooth.com/specifications/specs/)
- Nguồn học trực tuyến
  - Tutorial và hướng dẫn
  - Ví dụ mã nguồn
  - Cộng đồng và diễn đàn

## Lưu Ý Quan Trọng

1. Học theo thứ tự từ cơ bản đến nâng cao
2. Thực hành nhiều với các ví dụ thực tế
3. Tham khảo tài liệu chính thức khi cần thiết
4. Tham gia cộng đồng để học hỏi và chia sẻ kinh nghiệm
