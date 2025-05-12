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
