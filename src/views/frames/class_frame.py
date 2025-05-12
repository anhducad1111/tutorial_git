import customtkinter as ctk

class ClassFrame(ctk.CTkFrame):

    def __init__(self, master, presenter):
        super().__init__(master)
        self.presenter = presenter
        self._init_ui()

    def _init_ui(self):

        # Title
        title = ctk.CTkLabel(self, text="Quản lý Lớp học", font=("Arial", 20, "bold"))
        title.pack(pady=20)

        # Form Frame
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(pady=20, padx=20, fill="x")
        
        # Class Name
        ctk.CTkLabel(form_frame, text="Tên lớp:").pack(side="left", padx=5)
        self.class_name_entry = ctk.CTkEntry(form_frame)
        self.class_name_entry.pack(side="left", padx=5)
        
        # Teacher Name
        ctk.CTkLabel(form_frame, text="Giáo viên:").pack(side="left", padx=5)
        self.teacher_name_entry = ctk.CTkEntry(form_frame)
        self.teacher_name_entry.pack(side="left", padx=5)

        # Student Management Frame
        student_frame = ctk.CTkFrame(self)
        student_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(student_frame, text="Thêm sinh viên:").pack(side="left", padx=5)
        self.student_id_entry = ctk.CTkEntry(student_frame)
        self.student_id_entry.pack(side="left", padx=5)

        # Buttons Frame
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        # Class Management Buttons
        add_class_btn = ctk.CTkButton(button_frame, text="Thêm lớp", 
                                     command=self._on_add_class)
        add_class_btn.pack(side="left", padx=5)

        update_teacher_btn = ctk.CTkButton(button_frame, text="Đổi giáo viên",
                                         command=self._on_update_teacher)
        update_teacher_btn.pack(side="left", padx=5)

        # Student Management Button
        add_student_btn = ctk.CTkButton(button_frame, text="Thêm sinh viên vào lớp",
                                      command=self._on_add_student)
        add_student_btn.pack(side="left", padx=5)

        # List Frame
        list_frame = ctk.CTkFrame(self)
        list_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Class List
        self.class_list = ctk.CTkTextbox(list_frame, height=200)
        self.class_list.pack(fill="both", expand=True, padx=10, pady=10)

    def _on_add_class(self):
        class_name = self.class_name_entry.get()
        teacher_name = self.teacher_name_entry.get()
        if class_name and teacher_name:
            self.presenter.add_class(class_name, teacher_name)
            self._clear_class_form()

    def _on_update_teacher(self):
        class_name = self.class_name_entry.get()
        teacher_name = self.teacher_name_entry.get()
        if class_name and teacher_name:
            self.presenter.assign_teacher(class_name, teacher_name)
            self._clear_class_form()

    def _on_add_student(self):
        class_name = self.class_name_entry.get()
        student_id = self.student_id_entry.get()
        if class_name and student_id:
            self.presenter.add_student_to_class(class_name, student_id)
            self.student_id_entry.delete(0, "end")

    def _clear_class_form(self):
        self.class_name_entry.delete(0, "end")
        self.teacher_name_entry.delete(0, "end")
        self.student_id_entry.delete(0, "end")

    def update_class_list(self, classes):
        self.class_list.delete("0.0", "end")
        for class_obj in classes:
            info = f"Class Name: {class_obj.class_name}\n"
            info += f"Teacher: {class_obj.teacher.name}\n"
            info += f"Students ({len(class_obj.students)}):\n"
            for student in class_obj.students:
                info += f"  - {student.name} (ID: {student.student_id})\n"
            info += "-" * 30 + "\n"
            self.class_list.insert("end", info)

    def _show_error(self, message):
        # You could create a more sophisticated error dialog here
        print(f"Error: {message}")
