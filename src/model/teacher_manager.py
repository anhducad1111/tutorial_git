class TeacherManager:
    def __init__(self):
        self.teachers = []

    def add_teacher(self, teacher):
        self.teachers.append(teacher)

    def remove_teacher(self, teacher_name):
        self.teachers = [t for t in self.teachers if t.name != teacher_name]

    def update_teacher(self, teacher_name, new_subject):
        for teacher in self.teachers:
            if teacher.name == teacher_name:
                teacher.subject = new_subject
                break

    def list_teachers(self):
        return "\n".join([f"Name: {teacher.name}, Age: {teacher.age}, Subject: {teacher.subject}" for teacher in self.teachers])