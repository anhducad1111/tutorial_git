from src.models.managers.student_manager import StudentManager
from src.models.entities.student import Student

class StudentPresenter:
    def __init__(self, view):
        self.view = view
        self.student_manager = StudentManager()

    def add_student(self, name: str, age: int, student_id: str):
        try:
            student = Student(name, age, student_id)
            self.student_manager.add_student(student)
            self.load_students()
        except Exception as e:
            self.view._show_error(str(e))

    def remove_student(self, student_id: str):
        try:
            self.student_manager.remove_student(student_id)
            self.load_students()
        except Exception as e:
            self.view._show_error(str(e))

    def update_student(self, student_id: str, name: str = None, age: int = None):
        try:
            self.student_manager.update_student(student_id, name, age)
            self.load_students()
        except Exception as e:
            self.view._show_error(str(e))

    def load_students(self):
        try:
            students = self.student_manager.list_students()
            self.view.update_student_list(students)
        except Exception as e:
            self.view._show_error(str(e))
