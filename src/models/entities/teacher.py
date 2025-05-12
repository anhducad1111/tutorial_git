from src.models.entities.person import Person

class Teacher(Person):
    def __init__(self, name, age, subject):
        super().__init__(name, age)
        self.subject = subject

    def get_details(self):
        return f"Subject: {self.subject}"

    def print_info(self):
        super().print_info()
        print(self.get_details())
