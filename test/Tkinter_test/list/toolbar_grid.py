import tkinter as tk
from tkinter import PhotoImage
from tkinter import ttk
import PySimpleGUI as sg
import atexit
import sys 
import os


#強制終了されたかどうか
forced_exit = True


main_font = "Arial"

title_fm_bg = "#ffffff"
choice_fm_bg = "#214090"
choice_pw_bg = "#214090"
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




# アプリケーション（GUI）クラス
class Application(tk.Frame):
    # ... (前のコードと同じ)

    def create_widgets(self):

        toolbar_button1 = tk.Button(self.master, text=button1_text, **TOOLBAR_OPTIONS)
        toolbar_button1.grid(row=0, column=0, padx=4, pady=4)
        toolbar_button2 = tk.Button(self.master, text=button2_text, **TOOLBAR_OPTIONS)
        toolbar_button2.grid(row=0, column=1, padx=2, pady=4)
        toolbar_button3 = tk.Button(self.master, text=button3_text, **TOOLBAR_OPTIONS)
        toolbar_button3.grid(row=0, column=2, padx=2, pady=4)
        toolbar_button4 = tk.Button(self.master, text=button4_text, **TOOLBAR_OPTIONS)
        toolbar_button4.grid(row=0, column=3, padx=2, pady=4)


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
