class StudentManager:
    def __init__(self):
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def remove_student(self, student_id):
        self.students = [s for s in self.students if s.student_id != student_id]

    def update_student(self, student_id, new_name=None, new_age=None):
        for student in self.students:
            if student.student_id == student_id:
                if new_name:
                    student.name = new_name
                if new_age:
                    student.age = new_age
                break

    def list_students(self):
        return "\n".join([f"Name: {student.name}, Age: {student.age}, ID: {student.student_id}" for student in self.students])