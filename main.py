import tkinter as tk

def main():
    print("Hello, World!")

if __name__ == "__main__":
    def on_button_click():
        main()

    root = tk.Tk()
    root.title("Tkinter Example")

    button = tk.Button(root, text="Run Main", command=on_button_click)
    button.pack(pady=20)

    root.mainloop()