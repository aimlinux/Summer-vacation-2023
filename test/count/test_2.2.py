import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from matplotlib.patches import Circle
import matplotlib.animation as animation

root = tk.Tk()
root.geometry("500x500")

# MatplotlibのFigureを作成
fig = Figure(figsize=(6, 6), dpi=100)
ax = fig.add_subplot(111)
ax.set_aspect('equal')
ax.axis('off')

# テキストとアニメーションの初期化
tlist = np.linspace(3, 0, 4).repeat(10).astype(int).astype(str)
t1 = ax.text(0.5, 0.5, tlist[0], ha='center', va='center', fontsize=120)

rot = np.linspace(0, 360, 10)
rot_tile = np.tile(rot, 11)

colors = np.random.rand(110, 3)
c_rep = colors.repeat(10, axis=0)

def init():
    return t1,

def update(num):
    t1.set_text(tlist[num])
    t1.set_color(c_rep[num, :])
    t1.set_rotation(rot_tile[num])
    return t1,

# MatplotlibのFigureをTkinterウィンドウに埋め込む
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

ani = animation.FuncAnimation(fig, update, init_func=init, interval=100, frames=110)

root.mainloop()