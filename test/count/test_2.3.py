import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import random as rand

main_pw_bg = "#ffe4e1"

# カウントダウンのアニメーション
class AnimationCountdownWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("")
        # 画面の幅と高さを取得
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        window_width = 1280
        window_height = 800
        x = (screen_width // 2) - (window_width // 2) 
        y = (screen_height // 3) - (window_height // 3)
        self.master.geometry(f"{window_width}x{window_height-10}+{x}+{y}")

        # ペインウィンドウの作成
        pw_window = tk.PanedWindow(self.master, bg="#ffe4e1", orient="vertical", 
                                   bd=5, relief="ridge", borderwidth=10)
        pw_window.pack(expand=True, fill=tk.BOTH)

        # MatplotlibのFigureを作成
        self.fig = Figure(figsize=(12, 8), dpi=100, facecolor=main_pw_bg)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_aspect('equal')
        self.ax.axis('off')

        # 初期フォントサイズ
        self.initial_font_size = 400

        # アニメーションの初期化
        self.font_size = self.initial_font_size
        self.font_name = "Yu Gothic"
        self.font_weight = "bold"
        self.font = (self.font_name, self.font_size, self.font_weight)
        self.num_text = 5

        self.t1 = self.ax.text(0.5, 0.5, str(self.num_text), ha='center', va='center',
                               fontdict={'fontname': self.font_name, 'fontsize': self.font_size, 'fontweight': self.font_weight})

        def init():
            return self.t1,

        def update(num):
            if self.num_text == 5:
                if self.font_size == 20:
                    self.num_text = 4
                    self.font_size = self.initial_font_size
                    r = rand.random()
                    g = rand.random()
                    b = rand.random()
                    new_color = (r, g, b)
                    self.t1.set_color(new_color)
                else:
                    if self.font_size == self.initial_font_size:
                        r = rand.random()
                        g = rand.random()
                        b = rand.random()
                        new_color = (r, g, b)
                        self.t1.set_color(new_color)
                    self.font_size = self.font_size - 5
                    self.t1.set_fontsize(self.font_size)
                    self.t1.set_text(str(self.num_text))

            elif self.num_text == 4:
                if self.font_size == 20:
                    self.num_text = 3
                    self.font_size = self.initial_font_size
                    r = rand.random()
                    g = rand.random()
                    b = rand.random()
                    new_color = (r, g, b)
                    self.t1.set_color(new_color)
                else:
                    if self.font_size == self.initial_font_size:
                        r = rand.random()
                        g = rand.random()
                        b = rand.random()
                        new_color = (r, g, b)
                        self.t1.set_color(new_color)
                    self.font_size = self.font_size - 5
                    self.t1.set_fontsize(self.font_size)
                    self.t1.set_text(str(self.num_text))

            elif self.num_text == 3:
                if self.font_size == 20:
                    self.num_text = 2
                    self.font_size = self.initial_font_size
                    r = rand.random()
                    g = rand.random()
                    b = rand.random()
                    new_color = (r, g, b)
                    self.t1.set_color(new_color)
                else:
                    if self.font_size == self.initial_font_size:
                        r = rand.random()
                        g = rand.random()
                        b = rand.random()
                        new_color = (r, g, b)
                        self.t1.set_color(new_color)
                    self.font_size = self.font_size - 5
                    self.t1.set_fontsize(self.font_size)
                    self.t1.set_text(str(self.num_text))

            elif self.num_text == 2:
                if self.font_size == 20:
                    self.num_text = 1
                    self.font_size = self.initial_font_size
                    r = rand.random()
                    g = rand.random()
                    b = rand.random()
                    new_color = (r, g, b)
                    self.t1.set_color(new_color)
                else:
                    if self.font_size == self.initial_font_size:
                        r = rand.random()
                        g = rand.random()
                        b = rand.random()
                        new_color = (r, g, b)
                        self.t1.set_color(new_color)
                    self.font_size = self.font_size - 5
                    self.t1.set_fontsize(self.font_size)
                    self.t1.set_text(str(self.num_text))

            elif self.num_text == 1:
                if self.font_size == 20:
                    self.num_text = "スタート"
                    self.font_size = self.initial_font_size
                    r = rand.random()
                    g = rand.random()
                    b = rand.random()
                    new_color = (r, g, b)
                    self.t1.set_color(new_color)
                else:
                    if self.font_size == self.initial_font_size:
                        r = rand.random()
                        g = rand.random()
                        b = rand.random()
                        new_color = (r, g, b)
                        self.t1.set_color(new_color)
                    self.font_size = self.font_size - 5
                    self.t1.set_fontsize(self.font_size)
                    self.t1.set_text(str(self.num_text))

            elif self.num_text == "スタート":
                if self.font_size == 0:
                    # カウント終了
                    self.master.after(200, self.master.destroy)  # 400ミリ秒後にウィンドウを閉じる
                else:
                    if self.font_size == self.initial_font_size:
                        r = rand.random()
                        g = rand.random()
                        b = rand.random()
                        new_color = (r, g, b)
                        self.t1.set_color(new_color)
                    self.font_size = self.font_size - 4
                    self.t1.set_fontsize(self.font_size)
                    self.t1.set_text(str(self.num_text))

            return self.t1,

        # MatplotlibのFigureをTkinterウィンドウに埋め込む
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas_widget = self.canvas.get_tk_widget()
        #self.canvas_widget.pack()
        pw_window.add(self.canvas_widget)

        self.ani = animation.FuncAnimation(self.fig, update, init_func=init, interval=7, frames=10)

if __name__ == "__main__":
    root = tk.Tk()
    animation_window = AnimationCountdownWindow(root)
    root.mainloop()