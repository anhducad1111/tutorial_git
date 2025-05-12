import customtkinter as ctk

class TeacherFrame(ctk.CTkFrame):
    def __init__(self, master, presenter):
        super().__init__(master)
        self.presenter = presenter
        self._init_ui()

    def _init_ui(self):
        # Title
        title = ctk.CTkLabel(self, text="Quản lý Giáo viên", font=("Arial", 20, "bold"))
        title.pack(pady=20)

        # Form Frame
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(pady=20, padx=20, fill="x")
        
        # Name
        ctk.CTkLabel(form_frame, text="Tên GV:").pack(side="left", padx=5)
        self.name_entry = ctk.CTkEntry(form_frame)
        self.name_entry.pack(side="left", padx=5)
        
        # Age
        ctk.CTkLabel(form_frame, text="Tuổi:").pack(side="left", padx=5)
        self.age_entry = ctk.CTkEntry(form_frame)
        self.age_entry.pack(side="left", padx=5)
        
        # Subject
        ctk.CTkLabel(form_frame, text="Môn dạy:").pack(side="left", padx=5)
        self.subject_entry = ctk.CTkEntry(form_frame)
        self.subject_entry.pack(side="left", padx=5)

        # Buttons Frame
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        # Add Button
        add_btn = ctk.CTkButton(button_frame, text="Thêm giáo viên", 
                               command=self._on_add_teacher)
        add_btn.pack(side="left", padx=5)

        # Remove Button
        remove_btn = ctk.CTkButton(button_frame, text="Xóa giáo viên",
                                 command=self._on_remove_teacher)
        remove_btn.pack(side="left", padx=5)

        # Update Button
        update_btn = ctk.CTkButton(button_frame, text="Cập nhật môn dạy",
                                 command=self._on_update_teacher)
        update_btn.pack(side="left", padx=5)

        # List Frame
        list_frame = ctk.CTkFrame(self)
        list_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Teacher List
        self.teacher_list = ctk.CTkTextbox(list_frame, height=200)
        self.teacher_list.pack(fill="both", expand=True, padx=10, pady=10)

    def _on_add_teacher(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        subject = self.subject_entry.get()
        
        try:
            age = int(age)
            self.presenter.add_teacher(name, age, subject)
            self._clear_form()
        except ValueError:
            self._show_error("Tuổi phải là số nguyên")

    def _on_remove_teacher(self):
        name = self.name_entry.get()
        if name:
            self.presenter.remove_teacher(name)
            self._clear_form()

    def _on_update_teacher(self):
        name = self.name_entry.get()
        subject = self.subject_entry.get()
        if name and subject:
            self.presenter.update_teacher(name, subject)
            self._clear_form()

    def _clear_form(self):
        self.name_entry.delete(0, "end")
        self.age_entry.delete(0, "end")
        self.subject_entry.delete(0, "end")

    def update_teacher_list(self, teachers):
        self.teacher_list.delete("0.0", "end")
        for teacher in teachers:
            info = f"Name: {teacher.name}\n"
            info += f"Age: {teacher.age}\n"
            info += f"Subject: {teacher.subject}\n"
            info += "-" * 30 + "\n"
            self.teacher_list.insert("end", info)

    def _show_error(self, message):
        # You could create a more sophisticated error dialog here
        print(f"Error: {message}")
