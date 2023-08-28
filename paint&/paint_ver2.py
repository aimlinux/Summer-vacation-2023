import tkinter as tk
from tkinter import PhotoImage
from tkinter import ttk
import PySimpleGUI as sg
import atexit
import sys 
import os

forced_exit = True


main_font = "Arial"

main_fm_bg = "#ffffff"
main_pw_bg = "#ffe4e1"

title_btn_bg = "#00ced1"
introduction_btn_bg = "#ffffff"

button1_text = "タイトルへ"
button2_text = "オプション"
button3_text = "aimlinux"
button4_text = "aimlinux"

TOOLBAR_OPTIONS = { 
    "font" : "main_font, 15",
    "bg" : "#00ced1",
    "fg" : "#00334d"
}


#各ウィンドウのカウント
count_title = False


# BackgroundFrameを作成
class BackgroundFrame(tk.Frame):
    def __init__(self, master=None, bg_image=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        bg_image_path = "paint&/image/aimlinux.png"
        
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
        
        global count_title
        count_title = True
        
        global pw_main, fm_main
        
        # メインウィンドウ作成
        pw_main = tk.PanedWindow(self.master, bg=main_pw_bg, orient="vertical")
        pw_main.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        # メインフレーム作成
        fm_main = tk.Frame(pw_main, bd=5, bg=main_pw_bg, relief="ridge", borderwidth=10)
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
                                width=30, relief="raised", borderwidth=5) # reliefによって影を表現
        start_button.pack(side=tk.TOP, pady=(450, 50), padx=(750, 150)) # 「fill="x"」：水平方向に埋める
        exit_button = tk.Button(bg_frame, text="終了する", font=(main_font, 20), bg=title_btn_bg, 
                                width=30, relief="raised", borderwidth=5, command=self.exit_App)
        exit_button.pack(side=tk.TOP, padx=(750, 150))
        
        introduction_button = tk.Button(bg_frame, text="このゲームについて", font=(main_font, 18), bg=introduction_btn_bg, width=30, relief="raised", borderwidth=3)
        introduction_button.pack(side=tk.TOP, padx=(30, 800), pady=(40, 0))



    #アプリケーションが終了されたとき
    def exit_App(self):
        global forced_exit
        forced_exit = False
        
        if count_title == True:
            self.master.quit()


#アプリケーションが強制的に終了されたとき
def goodbye():
    if forced_exit == True:
        popup = sg.popup_ok_cancel('アプリケーションを終了しますか？', font=(main_font, 16), text_color='#000000', background_color=main_fm_bg)
        print(popup)
        
        if popup == "OK":
            exit_message = "App Exit"
            #messagebox.showinfo("App Exit", "アプリケーションを終了しました。")
            print(exit_message)
            pass
        elif popup == "Cancel":
            restart_message = "continue" 
            # 「continue」を引数と捨て再起動関数を実行
            restart(restart_message)

#再起動
def restart(restart_message):
    if restart_message == "continue":
        print("continue... ")
    #Restart python script itself
    os.execv(sys.executable, ['python'] + sys.argv)
    

#pythonプログラムが終了したことを取得してgoodbye関数を実行
atexit.register(goodbye)



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
