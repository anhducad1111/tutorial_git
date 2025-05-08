class ClassManager:
    def __init__(self):
        self.classes = []

    def add_class(self, class_obj):
        self.classes.append(class_obj)

    def assign_teacher(self, class_name, teacher):
        for class_obj in self.classes:
            if class_obj.class_name == class_name:
                class_obj.teacher = teacher
                break

    def list_classes(self):
        return "\n".join(str(class_obj) for class_obj in self.classes)