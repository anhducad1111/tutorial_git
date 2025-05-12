import customtkinter as ctk
from src.views.frames.student_frame import StudentFrame
from src.views.frames.teacher_frame import TeacherFrame
from src.views.frames.class_frame import ClassFrame

class MainWindow:
    def __init__(self, student_presenter, teacher_presenter, class_presenter):
        # Create root window
        self.root = ctk.CTk()
        self.root.title("Quản lý sinh viên")
        self.root.geometry("1200x700")
        
        # Store presenters
        self.student_presenter = student_presenter
        self.teacher_presenter = teacher_presenter
        self.class_presenter = class_presenter

        # Create main frames
        self.sidebar = ctk.CTkFrame(self.root, width=200)
        self.sidebar.pack(side="left", fill="y", padx=5, pady=5)
        
        self.main_content = ctk.CTkFrame(self.root)
        self.main_content.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        # Initialize frames
        self.student_frame = StudentFrame(self.main_content, student_presenter)
        self.teacher_frame = TeacherFrame(self.main_content, teacher_presenter)
        self.class_frame = ClassFrame(self.main_content, class_presenter)

        # Create navigation buttons
        ctk.CTkButton(self.sidebar, text="Quản lý Lớp học", 
                     command=self.show_class_management).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="Quản lý Sinh viên",
                     command=self.show_student_management).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="Quản lý Giáo viên", 
                     command=self.show_teacher_management).pack(pady=10, padx=20)

        # Show default view
        self.current_frame = None

    def show_class_management(self):
        self._switch_frame(self.class_frame)
        self.class_presenter.load_classes()

    def show_student_management(self):
        self._switch_frame(self.student_frame)
        self.student_presenter.load_students()

    def show_teacher_management(self):
        self._switch_frame(self.teacher_frame)
        self.teacher_presenter.load_teachers()

    def _switch_frame(self, new_frame):
        if self.current_frame:
            self.current_frame.pack_forget()
        new_frame.pack(fill="both", expand=True)
        self.current_frame = new_frame

    def run(self):
        # Show initial view after presenters are properly injected
        self.show_class_management()
        self.root.mainloop()
