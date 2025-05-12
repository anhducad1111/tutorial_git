from src.models.entities.person import Person

class Student(Person):
    def __init__(self, name, age, student_id):
        super().__init__(name, age)
        self.student_id = student_id

    def get_details(self):
        return f"Student ID: {self.student_id}"

    def print_info(self):
        super().print_info()
        print(self.get_details())
