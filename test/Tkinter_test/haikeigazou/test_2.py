import tkinter as tk
from tkinter import PhotoImage

class BackgroundFrame(tk.Frame):
    def __init__(self, master=None, bg_image=None, **kwargs):
        super().__init__(master, **kwargs)

        bg_image_path = "C:/Users/1k8ai/Documents/GitHub/Typing-Game/test/haikeigazou/image_2.png"

        if bg_image:
            self.bg_image = PhotoImage(file=bg_image_path)
            self.canvas = tk.Canvas(self, width=self.bg_image.width(), height=self.bg_image.height())
            self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
            self.canvas.pack(fill="both", expand=True)

# メインウィンドウを作成
root = tk.Tk()
root.title("Background Image Example")

# 背景画像を指定してBackgroundFrameを作成
background_image_path = "path_to_your_image.png"
background_frame = BackgroundFrame(root, bg_image=background_image_path)
background_frame.pack(fill="both", expand=True)

# 他のウィジェットを追加
label = tk.Label(background_frame, text="This is a label")
label.pack()

root.mainloop()