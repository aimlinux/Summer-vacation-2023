import tkinter as tk
from tkinter import filedialog 
from tkinter import messagebox
from tkinter import scrolledtext 
from tkinter import PhotoImage
from tkinter import ttk
import PySimpleGUI as sg
import PIL
from PIL import Image, ImageTk
import atexit
import time
from time import sleep
import sys 
import os



forced_exit = True # 強制終了されたかどうか

last_photo = None # お手本のイラストが選択されているかどうか


main_font = "Helvetica"

title_fm_bg = "#ffffff"
choice_fm_bg = "#ffe4e1"
choice_pw_bg = "#ffe4e1"
main_pw_bg = "#ffe4e1"

title_btn_bg = "#00ced1"
choice_btn_bg = "#00ced1"
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

# 各ウィンドウのサイズ
difficulty_window_size = "500x600+500+100"
warning_window_size = "600x140+500+400"

# 各ウィンドウのカウント
count_title = False
count_choice = False


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
        
        global last_photo
        last_photo = None # お手本のイラストの選択を初期化
        
        global count_title
        count_title = True
        
        global pw_title, fm_title, bg_frame
        
        # メインウィンドウ作成
        pw_title = tk.PanedWindow(self.master, bg=main_pw_bg, orient="vertical")
        pw_title.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        # メインフレーム作成
        fm_title = tk.Frame(pw_title, bd=5, bg=main_pw_bg, relief="ridge", borderwidth=10)
        pw_title.add(fm_title)
        
        # 画像ファイルのパスを指定して、BackgroundFrameを作成
        bg_image_path = "path_to_your_image.png"
        bg_frame = BackgroundFrame(fm_title, bg_image=bg_image_path, bg="#ffffff")
        bg_frame.pack(fill="both", expand=True)
        # bg_frame = fm_title
        
        # ツールバー作成
        fm_toolbar = tk.Frame(bg_frame, bg=title_fm_bg)
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
                                width=30, relief="raised", borderwidth=5, command=self.start_App) # reliefによって影を表現
        start_button.pack(side=tk.TOP, pady=(450, 50), padx=(750, 150)) # 「fill="x"」：水平方向に埋める
        exit_button = tk.Button(bg_frame, text="終了する", font=(main_font, 20), bg=title_btn_bg, 
                                width=30, relief="raised", borderwidth=5, command=self.exit_App)
        exit_button.pack(side=tk.TOP, padx=(750, 150))
        
        introduction_button = tk.Button(bg_frame, text="このゲームについて", font=(main_font, 18), bg=introduction_btn_bg, width=30, relief="raised", borderwidth=3)
        introduction_button.pack(side=tk.TOP, padx=(30, 800), pady=(40, 0))


    #アプリケーションが始まった時
    def start_App(self):
        
        pw_title.destroy()
        fm_title.destroy()
        time.sleep(0.1)
        
        global count_title
        count_title = False
        global count_choice
        count_choice = True
        
        global fm_choice
        
        fm_choice = tk.Frame(self.master, bg=choice_pw_bg, bd=5, relief="ridge", borderwidth=10)
        #fm_choice.grid(row=0, column=0, sticky="nsew")]
        fm_choice.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        
        # -------- gridによって配置する --------
        style = ttk.Style()
        style.configure("Listbox", font=("Helvetica", 16))  # リストのフォントサイズを大きく
        style.configure("TButton", font=("Helvetica", 16))  # ボタンのフォントサイズを大きく
        
        # ラベルを追加
        label = tk.Label(fm_choice, text="お手本にするイラストを選択してください", font=("Helvetica", 30), bg=choice_fm_bg, padx=70, pady=55)
        label.grid(row=1, column=0, columnspan=2, sticky="nsew")
        
        self.listbox = tk.Listbox(fm_choice, selectbackground="lightblue", font=("Helvetica", 25), height=5)  # リストの高さを調整
        self.listbox.grid(row=2, column=0, padx=20, pady=20, rowspan=3, sticky="ns")
        
        item_1 = "動物"
        item_2 = "植物"
        item_3 = "その他"
        button_list_1 = ["馬", "牛", "サル", "a", "3", "s", "e", "as", "ds", "sdgds", "馬", "牛", "サ", "a", "3", "s", "e", "as", "ds", "sdgds", "馬", "牛", "ル", "a", "3", "s", "e", "as", "ds", "sdgds"]
        
        self.listbox.insert(tk.END, item_1)
        self.listbox.insert(tk.END, item_2)
        self.listbox.insert(tk.END, item_3)
        
        self.listbox.select_set(0)  # 最初のアイテムを選択状態にする
        #listbox.event_generate("<<ListboxSelect>>")  # 選択イベントを発生させて更新

        self.button_frame = tk.Frame(fm_choice, width=100, bg="#ffff8e", relief="ridge", borderwidth=2)
        self.button_frame.grid(row=2, column=1, padx=20, pady=20, sticky="nsew")

        self.button_dict = {
            item_1: [
                [ttk.Button(self.button_frame, text=f"{button_list_1[row*5+col+1-1]}", command=lambda num=row*5+col+1: self.button_click(num)) for col in range(5)] for row in range(2)
            ],
            item_2: [
                [ttk.Button(self.button_frame, text=f"{button_list_1[row*5+col+1-1]}", command=lambda num=row*5+col+1: self.button_click(num)) for col in range(10, 15)] for row in range(2)
            ],
            item_3: [
                [ttk.Button(self.button_frame, text=f"{button_list_1[row*5+col+1-1]}", command=lambda num=row*5+col+1: self.button_click(num)) for col in range(20, 25)] for row in range(2)
            ]
        }
        self.button_list = [button for button_row in self.button_dict.values() for row in button_row for button in row]

        self.update_button_visibility("")

        self.listbox.bind("<<ListboxSelect>>", self.update_buttons)

        for row in range(2):
            self.button_frame.grid_rowconfigure(row, weight=1)
        for col in range(5):
            self.button_frame.grid_columnconfigure(col, weight=1)

        # 画像の表示
        self.image = Image.open("paint&/image/image_1.jpg")  # 画像のパスを指定
        image_width = 500
        self.image = self.image.resize((image_width, int(image_width/1280*800)))

        photo = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(fm_choice, image=photo, bg=choice_fm_bg)
        self.image_label.grid(row=4, column=1, columnspan=2, padx=20, pady=20, sticky="nsew")
        self.image_label.image = photo

        #決定・戻るボタンの配置
        return_title_button = tk.Button(fm_choice, text="戻る", bg=choice_btn_bg, font=(main_font, 15), height=2, width=2, 
                                        relief="raised", borderwidth=5, command=self.return_title)
        return_title_button.grid(row=6, column=0, columnspan=1, padx=(50, 200), pady=20, sticky="nsew")
        
        decided_button = tk.Button(fm_choice, text="決定", bg=choice_btn_bg, font=(main_font, 15), height=2, width=2, 
                                    relief="raised", borderwidth=5, command=self.difficulty)
        decided_button.grid(row=6, column=1, columnspan=1, padx=(550, 100), pady=20, sticky="nsew")

        self.update_buttons(None)  # 初期選択アイテムに対するボタンを表示


    def update_buttons(self, event):
        selected_item = self.listbox.get(self.listbox.curselection())
        self.update_button_visibility(selected_item)

    def update_button_visibility(self, selected_item):
        for button in self.button_list:
            button.grid_forget()
        if selected_item in self.button_dict:
            for row, button_row in enumerate(self.button_dict[selected_item]):
                for col, button in enumerate(button_row):
                    button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

    def button_click(self, button_number):
        print(f"Button {button_number} clicked!")
        # 画像の表示
        image_path = f"paint&/image/image_{button_number}.jpg"  # 各ボタンに対応する画像ファイル名を指定
        self.image = Image.open(image_path)
        image_width = 500  # マージンを考慮して調整
        self.image = self.image.resize((image_width, int(image_width*800/1280)))

        photo = ImageTk.PhotoImage(self.image)
        self.image_label.config(image=photo)
        self.image_label.image = photo
        
        #最終的な決定
        global last_photo
        last_photo = button_number



    # 難易度を選ぶ
    def difficulty(self):
        global difficulty_window
        
        if not last_photo:
            difficulty_window = tk.Toplevel(bg=choice_fm_bg, bd=5)
            difficulty_window.geometry(warning_window_size)
            difficulty_window.title("warning")
            difficulty_window.lift() # 他のウィンドウより前面に固定
            
            label = tk.Label(difficulty_window, text="お手本のイラストが選択されていません", bg=choice_fm_bg, font=(main_font, 20))
            label.pack(side=tk.TOP, padx=(0, 0), pady=(10, 10))
            button = tk.Button(difficulty_window, text="OK", bg=choice_btn_bg, font=(main_font, 14), width=10, 
                                            relief="raised", borderwidth=5, command=self.exit_warning)
            button.pack(side=tk.TOP, padx=(0, 0), pady=(10, 10))
            
        else:
            difficulty_window = tk.Toplevel(bg=choice_fm_bg, bd=5)
            difficulty_window.geometry(difficulty_window_size)
            difficulty_window.title("難易度選択")
            difficulty_window.lift() # 他のウィンドウより前面に固定

            label = tk.Label(difficulty_window, text="-- 難易度を選択してください --", bg=choice_fm_bg, font=(main_font, 20))
            label.pack(side=tk.TOP, padx=(0, 0), pady=(40, 20))
            
            button_1 = tk.Button(difficulty_window, text="初級", bg=choice_btn_bg, font=(main_font, 15), width=18, 
                                            relief="raised", borderwidth=5, command=lambda: self.difficulty_decision("button_1"))
            button_1.pack(side=tk.TOP, padx=(0, 0), pady=(30, 12))
            text_label_1 = tk.Label(difficulty_window, text="お手本を見る時間：30秒以内\nペイントする時間：60秒以内", bg=choice_fm_bg, font=(main_font, 12))
            text_label_1.pack(side=tk.TOP, padx=(0, 0))
            button_2 = tk.Button(difficulty_window, text="中級", bg=choice_btn_bg, font=(main_font, 15), width=18, 
                                            relief="raised", borderwidth=5, command=lambda: self.difficulty_decision("button_2"))
            button_2.pack(side=tk.TOP, padx=(0, 0), pady=(40, 20))
            text_label_2 = tk.Label(difficulty_window, text="お手本を見る時間：20秒以内\nペイントする時間：40秒以内", bg=choice_fm_bg, font=(main_font, 12))
            text_label_2.pack(side=tk.TOP, padx=(0, 0))
            button_3 = tk.Button(difficulty_window, text="上級", bg=choice_btn_bg, font=(main_font, 15), width=18, 
                                            relief="raised", borderwidth=5, command=lambda: self.difficulty_decision("button_3"))
            button_3.pack(side=tk.TOP, padx=(0, 0), pady=(40, 20))
            text_label_3 = tk.Label(difficulty_window, text="お手本を見る時間：10秒以内\nペイントする時間：20秒以内", bg=choice_fm_bg, font=(main_font, 12))
            text_label_3.pack(side=tk.TOP, padx=(0, 0))
            
        
    def difficulty_decision(self, difficulty):
        
        last_difficulty = difficulty
        if last_photo and last_difficulty:
            print(f"{last_photo} : {last_difficulty}")
            
            global difficulty_window
            difficulty_window.destroy()
            time.sleep(0.5)
            
            global game_start_window
            game_start_window = tk.Toplevel(bg=choice_fm_bg, bd=5)
            game_start_window.geometry(difficulty_window_size)
            game_start_window.title("これで決定？")
            game_start_window.lift() # 他のウィンドウより前面に固定
            
        else:
            pass
        


    # 注意ウィンドウを消す
    def exit_warning(self):
        
        difficulty_window.destroy()
        return 0
    
    

    # タイトルへ戻る
    def return_title(self):
        
        if count_choice == True:
            fm_choice.destroy()
        else: 
            pass
        
        self.create_widgets()
        



    #アプリケーションが終了されたとき
    def exit_App(self):
        global forced_exit
        forced_exit = False
        
        if count_title == True:
            self.master.quit()


#アプリケーションが強制的に終了されたとき
def goodbye():
    # if forced_exit == True:
    #     popup = sg.popup_ok_cancel('アプリケーションを終了しますか？', font=(main_font, 12), text_color='#000000', background_color=main_pw_bg)
    #     print(popup)
        
    #     if popup == "OK":
    #         exit_message = "App Exit"
    #         #messagebox.showinfo("App Exit", "アプリケーションを終了しました。")
    #         print(exit_message)
    #         pass
    #     elif popup == "Cancel":
    #         restart_message = "continue" 
    #         # 「continue」を引数と捨て再起動関数を実行
    #         restart(restart_message)
    # else: 
        pass

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
#y = (screen_height // 3) - (window_height // 3)
y = 2

myapp = Application(master=main_window)
myapp.master.title("paintApp")
myapp.master.geometry(f"{window_width}x{window_height-10}+{x}+{y}")
myapp.mainloop()
