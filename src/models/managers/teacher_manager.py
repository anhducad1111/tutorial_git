from src.models.entities.teacher import Teacher

class TeacherManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TeacherManager, cls).__new__(cls)
            cls._instance.teachers = []
        return cls._instance

    def add_teacher(self, teacher):
        if not isinstance(teacher, Teacher):
            raise TypeError("Can only add Teacher objects")
        self.teachers.append(teacher)

    def remove_teacher(self, teacher_name: str):
        self.teachers = [t for t in self.teachers if t.name != teacher_name]

    def update_teacher(self, teacher_name: str, new_subject: str):
        for teacher in self.teachers:
            if teacher.name == teacher_name:
                teacher.subject = new_subject
                break

    def get_teacher(self, teacher_name: str) -> Teacher:
        for teacher in self.teachers:
            if teacher.name == teacher_name:
                return teacher
        return None

    def list_teachers(self) -> list:
        return self.teachers

    def __str__(self):
        return "\n".join(str(teacher) for teacher in self.teachers)
