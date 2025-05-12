from src.models.entities.student import Student
from src.models.entities.teacher import Teacher

class Class:
    def __init__(self, class_name, teacher):
        if not isinstance(teacher, Teacher):
            raise TypeError("Teacher must be an instance of Teacher class")
        self.class_name = class_name
        self.teacher = teacher
        self.students = []

    def add_student(self, student):
        if not isinstance(student, Student):
            raise TypeError("Only Student objects can be added to the class")
        self.students.append(student)

    def print_info(self):
        print(f"Class Name: {self.class_name}")
        print("Teacher:")
        self.teacher.print_info()
        print("Students:")
        for student in self.students:
            student.print_info()
