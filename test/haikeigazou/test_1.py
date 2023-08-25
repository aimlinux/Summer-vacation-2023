import tkinter as tk
from tkinter import PhotoImage

class BackgroundFrame(tk.Frame):
    def __init__(self, master=None, bg_image=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        bg_image = "C:/Users/1k8ai/Documents/GitHub/Typing-Game/test/haikeigazou/image_2.png"
        
        if bg_image:
            self.bg_image = PhotoImage(file=bg_image)
            self.bg_label = tk.Label(self, image=self.bg_image)
            self.bg_label.place(relwidth=1, relheight=1)

# アプリケーションの作成
root = tk.Tk()
root.title("Background Image Example")
root.geometry("1280x800")

# 画像ファイルのパスを指定して、BackgroundFrameを作成
background_image_path = ""
background_frame = BackgroundFrame(root, bg_image=background_image_path)
background_frame.pack(fill="both", expand=True)

# 他の要素を追加
label = tk.Label(background_frame, text="Hello, Background!", font=("Helvetica", 24))
label.pack(padx=20, pady=20)

# アプリケーションの開始
root.mainloop()