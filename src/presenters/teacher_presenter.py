from src.models.managers.teacher_manager import TeacherManager
from src.models.entities.teacher import Teacher

class TeacherPresenter:
    def __init__(self, view):
        self.view = view
        self.teacher_manager = TeacherManager()

    def add_teacher(self, name: str, age: int, subject: str):
        try:
            teacher = Teacher(name, age, subject)
            self.teacher_manager.add_teacher(teacher)
            self.load_teachers()
        except Exception as e:
            self.view._show_error(str(e))

    def remove_teacher(self, name: str):
        try:
            self.teacher_manager.remove_teacher(name)
            self.load_teachers()
        except Exception as e:
            self.view._show_error(str(e))

    def update_teacher(self, name: str, subject: str):
        try:
            self.teacher_manager.update_teacher(name, subject)
            self.load_teachers()
        except Exception as e:
            self.view._show_error(str(e))

    def get_teacher(self, name: str) -> Teacher:
        try:
            return self.teacher_manager.get_teacher(name)
        except Exception as e:
            self.view._show_error(str(e))
            return None

    def load_teachers(self):
        try:
            teachers = self.teacher_manager.list_teachers()
            self.view.update_teacher_list(teachers)
        except Exception as e:
            self.view._show_error(str(e))
