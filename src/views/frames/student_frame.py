import customtkinter as ctk

class StudentFrame(ctk.CTkFrame):
    def __init__(self, master, presenter):
        super().__init__(master)
        self.presenter = presenter
        self._init_ui()

    def _init_ui(self):
        # Title
        title = ctk.CTkLabel(self, text="Quản lý Sinh viên", font=("Arial", 20, "bold"))
        title.pack(pady=20)

        # Form Frame
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(pady=20, padx=20, fill="x")
        
        # Student ID
        ctk.CTkLabel(form_frame, text="Mã SV:").pack(side="left", padx=5)
        self.student_id_entry = ctk.CTkEntry(form_frame)
        self.student_id_entry.pack(side="left", padx=5)
        
        # Name
        ctk.CTkLabel(form_frame, text="Tên SV:").pack(side="left", padx=5)
        self.name_entry = ctk.CTkEntry(form_frame)
        self.name_entry.pack(side="left", padx=5)
        
        # Age
        ctk.CTkLabel(form_frame, text="Tuổi:").pack(side="left", padx=5)
        self.age_entry = ctk.CTkEntry(form_frame)
        self.age_entry.pack(side="left", padx=5)

        # Buttons Frame
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        # Add Button
        add_btn = ctk.CTkButton(button_frame, text="Thêm sinh viên", 
                               command=self._on_add_student)
        add_btn.pack(side="left", padx=5)

        # Remove Button
        remove_btn = ctk.CTkButton(button_frame, text="Xóa sinh viên",
                                 command=self._on_remove_student)
        remove_btn.pack(side="left", padx=5)

        # Update Button
        update_btn = ctk.CTkButton(button_frame, text="Cập nhật",
                                 command=self._on_update_student)
        update_btn.pack(side="left", padx=5)

        # List Frame
        list_frame = ctk.CTkFrame(self)
        list_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Student List
        self.student_list = ctk.CTkTextbox(list_frame, height=200)
        self.student_list.pack(fill="both", expand=True, padx=10, pady=10)

    def _on_add_student(self):
        student_id = self.student_id_entry.get()
        name = self.name_entry.get()
        age = self.age_entry.get()
        
        try:
            age = int(age)
            self.presenter.add_student(name, age, student_id)
            self._clear_form()
        except ValueError:
            self._show_error("Tuổi phải là số nguyên")

    def _on_remove_student(self):
        student_id = self.student_id_entry.get()
        if student_id:
            self.presenter.remove_student(student_id)
            self._clear_form()

    def _on_update_student(self):
        student_id = self.student_id_entry.get()
        name = self.name_entry.get()
        age = self.age_entry.get()
        
        try:
            age = int(age) if age else None
            self.presenter.update_student(student_id, name, age)
            self._clear_form()
        except ValueError:
            self._show_error("Tuổi phải là số nguyên")

    def _clear_form(self):
        self.student_id_entry.delete(0, "end")
        self.name_entry.delete(0, "end")
        self.age_entry.delete(0, "end")

    def update_student_list(self, students):
        self.student_list.delete("0.0", "end")
        for student in students:
            info = f"Name: {student.name}\n"
            info += f"Age: {student.age}\n"
            info += f"Student ID: {student.student_id}\n"
            info += "-" * 30 + "\n"
            self.student_list.insert("end", info)

    def _show_error(self, message):
        # You could create a more sophisticated error dialog here
        print(f"Error: {message}")
