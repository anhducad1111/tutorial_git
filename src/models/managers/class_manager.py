from src.models.entities.class_ import Class
from src.models.entities.teacher import Teacher

class ClassManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ClassManager, cls).__new__(cls)
            cls._instance.classes = []
        return cls._instance

    def add_class(self, class_obj):
        if not isinstance(class_obj, Class):
            raise TypeError("Can only add Class objects")
        self.classes.append(class_obj)

    def remove_class(self, class_name: str):
        self.classes = [c for c in self.classes if c.class_name != class_name]

    def get_class(self, class_name: str) -> Class:
        for class_obj in self.classes:
            if class_obj.class_name == class_name:
                return class_obj
        return None

    def assign_teacher(self, class_name: str, teacher: Teacher):
        if not isinstance(teacher, Teacher):
            raise TypeError("Teacher must be a Teacher object")
        class_obj = self.get_class(class_name)
        if class_obj:
            class_obj.teacher = teacher

    def list_classes(self) -> list:
        return self.classes

    def __str__(self):
        return "\n".join(str(class_obj) for class_obj in self.classes)
