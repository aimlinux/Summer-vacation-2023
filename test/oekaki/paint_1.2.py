import tkinter
from tkinter.colorchooser import askcolor
from tkinter import filedialog
from tkinter import messagebox

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
        window = tkinter.Tk()
        window.title("Fancy Scribble")

        self.canvas = tkinter.Canvas(window, bg=self.background_color, width=800, height=600)
        self.canvas.pack(fill=tkinter.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_pressed)
        self.canvas.bind("<B1-Motion>", self.on_dragged)
        self.canvas.bind("<ButtonRelease-1>", self.on_released)

        controls_frame = tkinter.Frame(window)
        controls_frame.pack(side=tkinter.BOTTOM, fill=tkinter.X)

        color_button = tkinter.Button(controls_frame, text="ペンの色を変更", command=self.change_pen_color)
        color_button.pack(side=tkinter.LEFT)

        background_button = tkinter.Button(controls_frame, text="背景色を変更", command=self.change_background_color)
        background_button.pack(side=tkinter.LEFT)

        pen_width_scale = tkinter.Scale(controls_frame, from_=1, to=10, label="ペンの太さ", orient=tkinter.HORIZONTAL,
                                       command=self.change_pen_width)
        pen_width_scale.set(self.pen_width)
        pen_width_scale.pack(side=tkinter.LEFT)

        pen_shape_label = tkinter.Label(controls_frame, text="ペンの形状")
        pen_shape_label.pack(side=tkinter.LEFT)
        pen_shape_options = ["circle", "rectangle", "line"]
        pen_shape_menu = tkinter.OptionMenu(controls_frame, tkinter.StringVar(), *pen_shape_options,
                                            command=self.change_pen_shape)
        pen_shape_menu.pack(side=tkinter.LEFT)

        clear_button = tkinter.Button(controls_frame, text="クリア", command=self.clear_canvas)
        clear_button.pack(side=tkinter.LEFT)

        save_button = tkinter.Button(controls_frame, text="保存", command=self.save_canvas)
        save_button.pack(side=tkinter.LEFT)

        return window

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = FancyScribble()
    app.run()
