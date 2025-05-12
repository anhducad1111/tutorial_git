from src.models.entities.student import Student

class StudentManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StudentManager, cls).__new__(cls)
            cls._instance.students = []
        return cls._instance

    def add_student(self, student):
        if not isinstance(student, Student):
            raise TypeError("Can only add Student objects")
        self.students.append(student)

    def remove_student(self, student_id: str):
        self.students = [s for s in self.students if s.student_id != student_id]

    def update_student(self, student_id: str, new_name: str = None, new_age: int = None):
        for student in self.students:
            if student.student_id == student_id:
                if new_name:
                    student.name = new_name
                if new_age:
                    student.age = new_age
                break

    def get_student(self, student_id: str) -> Student:
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    def list_students(self) -> list:
        return self.students

    def __str__(self):
        return "\n".join(str(student) for student in self.students)
