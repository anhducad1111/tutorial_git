import customtkinter as ctk
from src.views.main_window import MainWindow
from src.presenters.student_presenter import StudentPresenter
from src.presenters.teacher_presenter import TeacherPresenter
from src.presenters.class_presenter import ClassPresenter

def main():
    """_summary_
    
    """
    # Set theme and color
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Create presenters (views will be injected later)
    student_presenter = StudentPresenter(None)
    teacher_presenter = TeacherPresenter(None)
    class_presenter = ClassPresenter(None)

    # Create main window and inject presenters
    window = MainWindow(student_presenter, teacher_presenter, class_presenter)
    
    # Inject views into presenters
    student_presenter.view = window.student_frame
    teacher_presenter.view = window.teacher_frame
    class_presenter.view = window.class_frame

    # Start application
    window.run()

if __name__ == "__main__":
    main()
