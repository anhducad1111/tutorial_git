from src.model.person import Student, Teacher, Class
from src.model.teacher_manager import TeacherManager
from src.model.student_manager import StudentManager
from src.model.class_manager import ClassManager

def main():
    teacher_manager = TeacherManager()
    student_manager = StudentManager()
    class_manager = ClassManager()

    while True:
        print("\n--- Menu ---")
        print("1. Quản lý giáo viên")
        print("2. Quản lý sinh viên")
        print("3. Quản lý lớp học")
        print("4. Thoát")
        choice = input("Chọn chức năng: ")

        if choice == "1":
            print("\n--- Quản lý giáo viên ---")
            print("1. Thêm giáo viên")
            print("2. Xóa giáo viên")
            print("3. Cập nhật thông tin giáo viên")
            print("4. Danh sách giáo viên")
            sub_choice = input("Chọn chức năng: ")

            if sub_choice == "1":
                name = input("Nhập tên giáo viên: ")
                age = int(input("Nhập tuổi giáo viên: "))
                subject = input("Nhập môn giảng dạy: ")
                teacher = Teacher(name, age, subject)
                teacher_manager.add_teacher(teacher)
                print("Đã thêm giáo viên.")
            elif sub_choice == "2":
                name = input("Nhập tên giáo viên cần xóa: ")
                teacher_manager.remove_teacher(name)
                print("Đã xóa giáo viên.")
            elif sub_choice == "3":
                name = input("Nhập tên giáo viên cần cập nhật: ")
                subject = input("Nhập môn giảng dạy mới: ")
                teacher_manager.update_teacher(name, subject)
                print("Đã cập nhật thông tin giáo viên.")
            elif sub_choice == "4":
                print("\nDanh sách giáo viên:")
                print(teacher_manager.list_teachers())
            else:
                print("Lựa chọn không hợp lệ!")

        elif choice == "2":
            print("\n--- Quản lý sinh viên ---")
            print("1. Thêm sinh viên")
            print("2. Xóa sinh viên")
            print("3. Cập nhật thông tin sinh viên")
            print("4. Danh sách sinh viên")
            sub_choice = input("Chọn chức năng: ")

            if sub_choice == "1":
                name = input("Nhập tên sinh viên: ")
                age = int(input("Nhập tuổi sinh viên: "))
                student_id = input("Nhập mã sinh viên: ")
                student = Student(name, age, student_id)
                student_manager.add_student(student)
                print("Đã thêm sinh viên.")
            elif sub_choice == "2":
                student_id = input("Nhập mã sinh viên cần xóa: ")
                student_manager.remove_student(student_id)
                print("Đã xóa sinh viên.")
            elif sub_choice == "3":
                student_id = input("Nhập mã sinh viên cần cập nhật: ")
                new_name = input("Nhập tên mới (bỏ trống nếu không thay đổi): ")
                new_age = input("Nhập tuổi mới (bỏ trống nếu không thay đổi): ")
                new_age = int(new_age) if new_age else None
                student_manager.update_student(student_id, new_name, new_age)
                print("Đã cập nhật thông tin sinh viên.")
            elif sub_choice == "4":
                print("\nDanh sách sinh viên:")
                print(student_manager.list_students())
            else:
                print("Lựa chọn không hợp lệ!")

        elif choice == "3":
            print("\n--- Quản lý lớp học ---")
            print("1. Thêm lớp học")
            print("2. Phân công giáo viên cho lớp")
            print("3. Thêm sinh viên vào lớp")
            print("4. Danh sách lớp học")
            sub_choice = input("Chọn chức năng: ")

            if sub_choice == "1":
                class_name = input("Nhập tên lớp học: ")
                teacher_name = input("Nhập tên giáo viên phụ trách: ")
                teacher = next((t for t in teacher_manager.teachers if t.name == teacher_name), None)
                if teacher:
                    class_obj = Class(class_name, teacher)
                    class_manager.add_class(class_obj)
                    print("Đã thêm lớp học.")
                else:
                    print("Không tìm thấy giáo viên.")
            elif sub_choice == "2":
                class_name = input("Nhập tên lớp học: ")
                teacher_name = input("Nhập tên giáo viên mới: ")
                teacher = next((t for t in teacher_manager.teachers if t.name == teacher_name), None)
                if teacher:
                    class_manager.assign_teacher(class_name, teacher)
                    print("Đã phân công giáo viên.")
                else:
                    print("Không tìm thấy giáo viên.")
            elif sub_choice == "3":
                class_name = input("Nhập tên lớp học: ")
                student_id = input("Nhập mã sinh viên: ")
                student = next((s for s in student_manager.students if s.student_id == student_id), None)
                if student:
                    class_obj = next((c for c in class_manager.classes if c.class_name == class_name), None)
                    if class_obj:
                        class_obj.add_student(student)
                        print("Đã thêm sinh viên vào lớp.")
                    else:
                        print("Không tìm thấy lớp học.")
                else:
                    print("Không tìm thấy sinh viên.")
            elif sub_choice == "4":
                print("\nDanh sách lớp học:")
                print(class_manager.list_classes())
            else:
                print("Lựa chọn không hợp lệ!")

        elif choice == "4":
            print("Thoát chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()