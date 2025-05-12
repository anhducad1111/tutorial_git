from src.models.managers.class_manager import ClassManager
from src.models.managers.teacher_manager import TeacherManager
from src.models.managers.student_manager import StudentManager
from src.models.entities.class_ import Class

class ClassPresenter:
    def __init__(self, view):
        self.view = view
        self.class_manager = ClassManager()
        self.teacher_manager = TeacherManager()
        self.student_manager = StudentManager()

    def add_class(self, class_name: str, teacher_name: str):
        try:
            teacher = self.teacher_manager.get_teacher(teacher_name)
            if not teacher:
                raise ValueError(f"Không tìm thấy giáo viên: {teacher_name}")
            
            class_obj = Class(class_name, teacher)
            self.class_manager.add_class(class_obj)
            self.load_classes()
        except Exception as e:
            self.view._show_error(str(e))

    def assign_teacher(self, class_name: str, teacher_name: str):
        try:
            teacher = self.teacher_manager.get_teacher(teacher_name)
            if not teacher:
                raise ValueError(f"Không tìm thấy giáo viên: {teacher_name}")
            
            self.class_manager.assign_teacher(class_name, teacher)
            self.load_classes()
        except Exception as e:
            self.view._show_error(str(e))

    def add_student_to_class(self, class_name: str, student_id: str):
        try:
            student = self.student_manager.get_student(student_id)
            if not student:
                raise ValueError(f"Không tìm thấy sinh viên: {student_id}")
            
            class_obj = self.class_manager.get_class(class_name)
            if not class_obj:
                raise ValueError(f"Không tìm thấy lớp: {class_name}")
                
            class_obj.add_student(student)
            self.load_classes()
        except Exception as e:
            self.view._show_error(str(e))

    def load_classes(self):
        try:
            classes = self.class_manager.list_classes()
            self.view.update_class_list(classes)
        except Exception as e:
            self.view._show_error(str(e))
