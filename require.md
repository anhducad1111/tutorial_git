# Yêu Cầu Dự Án: Hệ Thống Quản Lý Sinh Viên Dựa Trên OOP

## Mục Tiêu
Phát triển một ứng dụng Python để quản lý sinh viên, nơi giáo viên có thể giám sát thông tin và hoạt động của sinh viên. Dự án phải áp dụng bốn nguyên tắc chính của Lập Trình Hướng Đối Tượng (OOP): đóng gói, kế thừa, đa hình và trừu tượng.

## Yêu Cầu Chức Năng
1. **Quản Lý Giáo Viên**
   - Thêm, cập nhật và xóa thông tin giáo viên.
   - Phân công giáo viên 

2. **Quản Lý Sinh Viên**
   - Thêm, cập nhật và xóa thông tin sinh viên.
   - Lưu trữ hồ sơ về điểm số của sinh viên.

3. **Quản Lý Lớp Học**
   - Tổ chức sinh viên vào các lớp 
   - Phân công giáo viên cho các lớp học.


## Áp Dụng Nguyên Tắc OOP
1. **Đóng Gói**
   - Sử dụng các thuộc tính riêng tư và cung cấp các phương thức getter và setter để quản lý truy cập dữ liệu của sinh viên và giáo viên.

2. **Kế Thừa**
   - Tạo một lớp cơ sở `Person` với các thuộc tính chung (ví dụ: tên, tuổi, thông tin liên lạc).
   - Kế thừa lớp `Student` và `Teacher` từ lớp `Person`.

3. **Đa Hình**
   - Triển khai các phương thức như `getDetails()` trong cả lớp `Student` và `Teacher`, cho phép các hành vi khác nhau cho từng lớp.

4. **Trừu Tượng**
   - Sử dụng các lớp trừu tượng hoặc giao diện để định nghĩa các hành vi chung 

## Yêu Cầu Kỹ Thuật
- Sử dụng Python làm ngôn ngữ lập trình.
- Tuân thủ các thực hành tốt nhất cho thiết kế OOP.
- Đảm bảo mã nguồn có tính module và có thể tái sử dụng.
- Bao gồm tài liệu và chú thích đầy đủ.
