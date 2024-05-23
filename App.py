import math
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GraphParams:
    def __init__(self, x_start, x_end, step_size, y_start):
        self.x_start = x_start
        self.x_end = x_end
        self.step_size = step_size
        self.y_start = y_start


def runge_kutta_method(x_start, y_start, x_end, step_size, func):
    x = x_start
    y = y_start
    points = [(x, y)]

    while x < x_end:
        k1 = step_size * func(x, y)
        k2 = step_size * func(x + 0.5 * step_size, y + 0.5 * k1)
        k3 = step_size * func(x + 0.5 * step_size, y + 0.5 * k2)
        k4 = step_size * func(x + step_size, y + k3)

        y = y + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        x = x + step_size

        points.append((x, y))

    return points


def differential_eq(x, y):
    return (math.sin(x) * math.sqrt(1 + x ** 2) - x * y) / 1 + x ** 2


def plot_graph(params):
    points = runge_kutta_method(params.x_start, params.y_start, params.x_end, params.step_size, differential_eq)
    x_vals, y_vals = zip(*points)

    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, label='Runge-Kutta')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.legend()
    return fig


def update_graph():
    try:
        x_start = float(entry_x_start.get())
        x_end = float(entry_x_end.get())
        step_size = float(entry_step_size.get())
        y_start = float(entry_y_start.get())
        params = GraphParams(x_start, x_end, step_size, y_start)
        fig = plot_graph(params)

        canvas = FigureCanvasTkAgg(fig, master=frame_graph)
        canvas.draw()
        canvas.get_tk_widget().pack()
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid numbers.")


app = tk.Tk()
app.title("Graph Plotter")

frame_inputs = tk.Frame(app)
frame_inputs.pack(side=tk.LEFT, padx=10, pady=10)

frame_graph = tk.Frame(app)
frame_graph.pack(side=tk.RIGHT, padx=10, pady=10)

tk.Label(frame_inputs, text="Start X").pack()
entry_x_start = tk.Entry(frame_inputs)
entry_x_start.pack()
entry_x_start.insert(0, "0.25")

tk.Label(frame_inputs, text="End X").pack()
entry_x_end = tk.Entry(frame_inputs)
entry_x_end.pack()
entry_x_end.insert(0, "10.0")

tk.Label(frame_inputs, text="Step Size").pack()
entry_step_size = tk.Entry(frame_inputs)
entry_step_size.pack()
entry_step_size.insert(0, "0.1")

tk.Label(frame_inputs, text="Y Start").pack()
entry_y_start = tk.Entry(frame_inputs)
entry_y_start.pack()
entry_y_start.insert(0, "1.0")

tk.Button(frame_inputs, text="Recalculate", command=update_graph).pack()

app.mainloop()
