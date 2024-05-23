import tkinter as tk
from tkinter import ttk


class RungeKuttaApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Runge-Kutta Method ODE")


        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Runge-Kutta Method ODE").grid(column=0, row=0, padx=10, pady=10)

    def on_close(self):
        self.destroy()


if __name__ == "__main__":
    app = RungeKuttaApp()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
