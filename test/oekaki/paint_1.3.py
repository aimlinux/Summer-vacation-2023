import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import math

class FancyScribble:

    def __init__(self):
        self.background_color = "#fff"  # デフォルトの背景色を設定
        self.pen_color = "black"
        self.pen_width = 2
        self.pen_shape = "circle"
        self.drawing = False
        self.sx, self.sy = None, None
        self.window = self.create_window()

    def on_pressed(self, event):
        self.drawing = True
        self.sx = event.x
        self.sy = event.y
        self.draw(event)

    def on_dragged(self, event):
        if self.drawing:
            self.draw(event)

    def on_released(self, event):
        self.drawing = False

    def draw(self, event):
        x, y = event.x, event.y
        
        self.pen_width = int(self.pen_width)
        
        if self.drawing:
            if self.pen_shape == "circle":
                self.canvas.create_oval(x, y, x + self.pen_width, y + self.pen_width,
                                        outline=self.pen_color, width=self.pen_width)
            elif self.pen_shape == "rectangle":
                self.canvas.create_rectangle(x, y, x + self.pen_width, y + self.pen_width,
                                            outline=self.pen_color, width=self.pen_width)
            else:
                self.canvas.create_line(self.sx, self.sy, x, y,
                                        fill=self.pen_color, width=self.pen_width)
            self.sx, self.sy = x, y

    def change_pen_color(self):
        color = askcolor()[1]
        if color:
            self.pen_color = color

    def change_background_color(self):
        color = askcolor()[1]
        if color:
            self.background_color = color
            self.canvas.config(bg=self.background_color)

    def change_pen_width(self, value):
        self.pen_width = value

    def change_pen_shape(self, shape):
        self.pen_shape = shape

    def clear_canvas(self):
        self.canvas.delete("all")

    def save_canvas(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            try:
                self.canvas.postscript(file=file_path, colormode='color')
                messagebox.showinfo("保存成功", "キャンバスを保存しました。")
            except Exception as e:
                messagebox.showerror("保存エラー", str(e))

    def create_window(self):
        window = tk.Tk()
        window.title("Fancy Scribble")

        self.canvas = tk.Canvas(window, bg=self.background_color, width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_pressed)
        self.canvas.bind("<B1-Motion>", self.on_dragged)
        self.canvas.bind("<ButtonRelease-1>", self.on_released)

        controls_frame = tk.Frame(window)
        controls_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # 丸いボタンを描画
        radius = 20
        button_x = 40
        button_y = 30
        self.canvas.create_oval(button_x - radius, button_y - radius, button_x + radius, button_y + radius,
                                fill="lightblue", outline=self.pen_color, width=2)
        circle_button = tk.Button(window, text="丸", command=lambda: self.change_pen_shape("circle"))
        circle_button.place(x=10, y=10)

        # ボタンのスタイルを設定
        style = ttk.Style()
        style.configure("TButton", padding=10, relief="flat", background="lightblue", font=("Helvetica", 12))
        ttk.Button(controls_frame, text="背景色を変更", command=self.change_background_color).pack(side=tk.LEFT)

        return window

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = FancyScribble()
    app.run()
