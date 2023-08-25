import tkinter as tk
from tkinter import PhotoImage




main_font = "Arial"

main_fm_bg = "#ffffff"
main_pw_bg = "#ffe4e1"

title_btn_bg = "#00ced1"

button1_text = "21"
button2_text = "21"
button3_text = "21"
button4_text = "21"

TOOLBAR_OPTIONS = { 
    "font" : "main_font, 15",
    "bg" : "#00ced1",
    "fg" : "#00334d"
}



# BackgroundFrameを作成
class BackgroundFrame(tk.Frame):
    def __init__(self, master=None, bg_image=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        bg_image_path = "C:/Users/1k8ai/Documents/GitHub/Typing-Game/paint&/image/aimlinux.png"
        
        if bg_image:
            self.bg_image = PhotoImage(file=bg_image_path)
            self.bg_label = tk.Label(self, image=self.bg_image)
            self.bg_label.place(relwidth=1, relheight=1)
            # self.bg_image = PhotoImage(file=bg_image_path)
            # self.canvas = tk.Canvas(self, width=self.bg_image.width(), height=self.bg_image.height())
            # self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
            # self.canvas.pack(fill="both", expand=True)



# アプリケーション（GUI）クラス
class Application(tk.Frame):
    DEBUG_LOG = True
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

        self.create_widgets()
    
    
    def create_widgets(self):
        
        global pw_main, fm_main
        
        # メインウィンドウ作成
        pw_main = tk.PanedWindow(self.master, bg=main_pw_bg, orient="vertical")
        pw_main.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        # メインフレーム作成
        fm_main = tk.Frame(pw_main, bd=10, bg=main_pw_bg, relief="ridge")
        pw_main.add(fm_main)
        
        # 画像ファイルのパスを指定して、BackgroundFrameを作成
        bg_image_path = "path_to_your_image.png"
        bg_frame = BackgroundFrame(fm_main, bg_image=bg_image_path, bg="#ffffff")
        bg_frame.pack(fill="both", expand=True)
        
        # ツールバー作成
        fm_toolbar = tk.Frame(bg_frame, bg=main_fm_bg)
        fm_toolbar.pack(anchor="nw")

        toolbar_button1 = tk.Button(fm_toolbar, text=button1_text, **TOOLBAR_OPTIONS)
        toolbar_button1.pack(side=tk.LEFT, padx=4, pady=4)
        toolbar_button2 = tk.Button(fm_toolbar, text=button2_text, **TOOLBAR_OPTIONS)
        toolbar_button2.pack(side=tk.LEFT, padx=2, pady=4)
        toolbar_button3 = tk.Button(fm_toolbar, text=button3_text, **TOOLBAR_OPTIONS)
        toolbar_button3.pack(side=tk.LEFT, padx=2, pady=4)
        toolbar_button4 = tk.Button(fm_toolbar, text=button4_text, **TOOLBAR_OPTIONS)
        toolbar_button4.pack(side=tk.LEFT, padx=2, pady=4)
        
        start_button = tk.Button(bg_frame, text="はじめる", font=(main_font, 20), bg=title_btn_bg, 
                                width=30, relief="raised", borderwidth=5)
        start_button.pack(side=tk.TOP, pady=(450, 50), padx=(750, 150)) # 「fill="x"」：水平方向に埋める
        exit_button = tk.Button(bg_frame, text="終了する", font=(main_font, 20), bg=title_btn_bg, 
                                width=30, relief="raised", borderwidth=5)
        exit_button.pack(side=tk.TOP, padx=(750, 150))




main_window = tk.Tk()        

# 画面の幅と高さを取得
screen_width = main_window.winfo_screenwidth()
screen_height = main_window.winfo_screenheight()

window_width = 1280
window_height = 800
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 3) - (window_height // 3)


myapp = Application(master=main_window)
myapp.master.title("paintApp")
myapp.master.geometry(f"{window_width}x{window_height}+{x}+{y}")
myapp.mainloop()
