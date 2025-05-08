from abc import ABC, abstractmethod

class Person(ABC):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @abstractmethod
    def get_details(self):
        pass

    def print_info(self):
        print(f"Name: {self.name}, Age: {self.age}")


class Student(Person):
    def __init__(self, name, age, student_id):
        super().__init__(name, age)
        self.student_id = student_id

    def get_details(self):
        return f"Student ID: {self.student_id}"

    def print_info(self):
        super().print_info()
        print(self.get_details())


class Teacher(Person):
    def __init__(self, name, age, subject):
        super().__init__(name, age)
        self.subject = subject

    def get_details(self):
        return f"Subject: {self.subject}"

    def print_info(self):
        super().print_info()
        print(self.get_details())


class Class:
    def __init__(self, class_name, teacher):
        self.class_name = class_name
        self.teacher = teacher
        self.students = []

    def add_student(self, student):
        if isinstance(student, Student):
            self.students.append(student)
        else:
            raise TypeError("Only Student objects can be added to the class.")

    def print_info(self):
        print(f"Class Name: {self.class_name}")
        print("Teacher:")
        self.teacher.print_info()
        print("Students:")
        for student in self.students:
            student.print_info()