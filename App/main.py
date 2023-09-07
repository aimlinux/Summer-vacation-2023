import tkinter as tk
from tkinter import filedialog 
from tkinter import messagebox
from tkinter import scrolledtext 
from tkinter import PhotoImage
from tkinter import ttk
import PySimpleGUI as sg
#import pyautogui as pg # スクショ撮影用
# 併用するとtkinterのウィンドウが小さくなる（pgモジュールのコードが原因らしい）
import cv2
import PIL
from PIL import Image, ImageTk
from PIL import ImageGrab # pgが使えないため
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import random as rand
import atexit
import time
from time import sleep
import sys  
import os 


# ペイントされた回数をカウントするためのファイル
count_filename = './count.txt'


forced_exit = True # 強制終了されたかどうか

last_photo = None # お手本のイラストが選択されているかどうか


main_font = "Helvetica"

main_pw_bg = "#ffe4e1"
title_fm_bg = "#ffffff"
choice_pw_bg = "#ffe4e1"
choice_fm_bg = "#ffe4e1"
see_model_pw_bg = "#ffe4e1"
see_model_fm_bg = "#ffe4e1"
illustration_pw_bg = "#ffe4e1"
illustration_fm_bg = "#ffe4e1"
scoring_pw_bg = "#ffe4e1"
scoring_fm_bg = "#ffe4e1"

title_btn_bg = "#00ced1"
choice_btn_bg = "#00ced1"
see_model_btn_bg = "#00ced1"
introduction_btn_bg = "#ffffff"
illustration_btn_bg = "#00ced1"
scoring_btn_bg = "#00ced1"

button1_text = "タイトルへ"
button2_text = "オプション"
button3_text = "ランキング"
button4_text = "aimlinux"

TOOLBAR_OPTIONS = { 
    "font" : "main_font, 15",
    "bg" : "#00ced1",
    "fg" : "#00334d"
}

# 各ウィンドウのサイズ
difficulty_window_size = "500x600+500+100"
warning_window_size = "600x140+500+400"
game_start_window_size = "800x200+300+200"
scoring_sub_window_size = "600x200+500+320"

# 各ウィンドウのカウント
count_title = False
count_choice = False
count_see_model = False
count_illustration = False


# カウントダウンアニメーションウィンドウのカウント
# animation_finished_judge_1 = True

#一度きりのイベント
the_only_1 = True
the_only_2 = True


# BackgroundFrameを作成
class BackgroundFrame(tk.Frame):
    def __init__(self, master=None, bg_image=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        bg_image_path = "./image/fd.png"
        
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
        # self.animation_window = None
    
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
        global button_list_thing
        button_list_thing = ["馬", "牛", "サル", "a", "3", "s", "e", "as", "ds", "sdgds", "馬", "牛", "サ", "a", "3", "s", "e", "as", "ds", "sdgds", "馬", "牛", "ル", "a", "3", "s", "e", "as", "ds", "sdgds"]
        
        self.listbox.insert(tk.END, item_1)
        self.listbox.insert(tk.END, item_2)
        self.listbox.insert(tk.END, item_3)
        
        self.listbox.select_set(0)  # 最初のアイテムを選択状態にする
        #listbox.event_generate("<<ListboxSelect>>")  # 選択イベントを発生させて更新

        self.button_frame = tk.Frame(fm_choice, width=100, bg="#ffff8e", relief="ridge", borderwidth=2)
        self.button_frame.grid(row=2, column=1, padx=20, pady=20, sticky="nsew")

        self.button_dict = {
            item_1: [
                [ttk.Button(self.button_frame, text=f"{button_list_thing[row*5+col+1-1]}", command=lambda num=row*5+col+1: self.button_click(num)) for col in range(5)] for row in range(2)
            ],
            item_2: [
                [ttk.Button(self.button_frame, text=f"{button_list_thing[row*5+col+1-1]}", command=lambda num=row*5+col+1: self.button_click(num)) for col in range(10, 15)] for row in range(2)
            ],
            item_3: [
                [ttk.Button(self.button_frame, text=f"{button_list_thing[row*5+col+1-1]}", command=lambda num=row*5+col+1: self.button_click(num)) for col in range(20, 25)] for row in range(2)
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
        self.image = Image.open("./image/image_1.jpg")  # 画像のパスを指定
        image_width = 500
        self.image = self.image.resize((image_width, int(image_width/1280*800)))
        # モザイク処理
        original = self.image # 元の画像のサイズを記憶
        intensity = 30 # 大きいほどモザイクが荒く
        self.image = self.image.resize((round(self.image.width / intensity), round(self.image.height / intensity)))
        # self.image = self.image.resize((original.width,original.height),resample=Image.NEAREST) # 最近傍補間
        #上が非推奨らしいので、、
        self.image = self.image.resize((original.width, original.height), resample=Image.Resampling.NEAREST)  # または Image.Dither.NONE
        # self.image = self.image.resize((original.width, original.height), resample=Image.BILINEAR) #双線形補間
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
        image_path = f"./image/image_{button_number}.jpg"  # 各ボタンに対応する画像ファイル名を指定
        self.image = Image.open(image_path)
        image_width = 500  # マージンを考慮して調整
        self.image = self.image.resize((image_width, int(image_width*800/1280)))
        # モザイク処理
        original = self.image # 元の画像のサイズを記憶
        intensity = 30 # 大きいほどモザイクが荒く
        self.image = self.image.resize((round(self.image.width / intensity), round(self.image.height / intensity)))
        # self.image = self.image.resize((original.width,original.height),resample=Image.NEAREST) # 最近傍補間
        #上が非推奨らしいので、、
        self.image = self.image.resize((original.width, original.height), resample=Image.Resampling.NEAREST)  # または Image.Dither.NONE
        # self.image = self.image.resize((original.width, original.height), resample=Image.BILINEAR) #双線形補間
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
            
        
    # 難易度を決定
    def difficulty_decision(self, difficulty):
        
        global last_difficulty
        last_difficulty = difficulty
        if last_photo and last_difficulty:
            print(f"{last_photo} : {last_difficulty}")
            
            global difficulty_window
            difficulty_window.destroy()
            time.sleep(0.2)
            
            global game_start_window
            game_start_window = tk.Toplevel(bg=choice_fm_bg, bd=5)
            game_start_window.geometry(game_start_window_size)
            game_start_window.title("これで決定？")
            game_start_window.lift() # 他のウィンドウより前面に固定
            
            painting_model = button_list_thing[last_photo-1]
            print(painting_model)
            if last_difficulty == "button_1":
                painting_difficulty = "初級"
            elif last_difficulty == "button_2":
                painting_difficulty = "中級"
            elif last_difficulty == "button_3":
                painting_difficulty = "上級"
            
            label = tk.Label(game_start_window, text=f"お手本のイラストは\"{painting_model}\"で難易度\"{painting_difficulty}\"でゲームをスタートしますか？",
                            bg=choice_fm_bg, font=(main_font, 17))
            label.pack(side=tk.TOP, padx=(0, 0), pady=(20, 10))
            label = tk.Label(game_start_window, text="「スタート」ボタンを押すとゲームがスタートし、\nお手本のイラストが見れるようになります。",
                            bg=choice_fm_bg, font=(main_font, 14))
            label.pack(side=tk.TOP, padx=(0, 0), pady=(0, 20))
            
            return_title_button = tk.Button(game_start_window, text="戻る", bg=choice_btn_bg, font=(main_font, 14), width=10,
                                        relief="raised", borderwidth=5, command=self.return_choice)
            return_title_button.pack(side=tk.LEFT, padx=(250, 10))
            decided_button = tk.Button(game_start_window, text="スタート", bg=choice_btn_bg, font=(main_font, 14), width=10,
                                        relief="raised", borderwidth=5, command=lambda: self.countdown_animation_1())
            decided_button.pack(side=tk.LEFT, padx=(100, 10))
            
        else:
            pass
        
        
    # イラスト選択へ戻る
    def return_choice(self):
        game_start_window.destroy()
        return 0


# -------- カウントダウンアニメーション１ --------
    def countdown_animation_1(self):

        game_start_window.destroy()

        fm_choice.destroy()
        self.master.after(500)
        
        global pw_window
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
        self.num_text = 3

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
                    self.master.after(400, self.To_see_model_1)  # 400ミリ秒後にウィンドウを閉じる
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


    # see_modelの為に
    def To_see_model_1(self):
        global the_only_1
        if the_only_1 == True:
            the_only_1 = False
            pw_window.destroy()
            self.see_model()
            
        
    # イラストのお手本を表示
    def see_model(self):
        
        # game_start_window.destroy()
        # fm_choice.destroy()
        # self.master.after(500)
        
        # pw_window.destroy()
        
        global count_choice
        count_choice = False
        global count_see_model
        count_see_model = True
        
        global skip_on
        skip_on = "NULL"
        
        global pw_see_model
        pw_see_model = tk.PanedWindow(self.master, bg=see_model_pw_bg, orient="vertical")
        pw_see_model.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        fm_see_model = tk.Frame(pw_see_model, bd=5, bg=see_model_pw_bg, relief="ridge", borderwidth=10)
        pw_see_model.add(fm_see_model)
        
        # ツールバー作成
        fm_toolbar = tk.Frame(fm_see_model, bg=see_model_fm_bg)
        fm_toolbar.pack(anchor="nw")

        toolbar_button1 = tk.Button(fm_toolbar, text=button1_text, **TOOLBAR_OPTIONS)
        toolbar_button1.pack(side=tk.LEFT, padx=4, pady=4)
        toolbar_button2 = tk.Button(fm_toolbar, text=button2_text, **TOOLBAR_OPTIONS)
        toolbar_button2.pack(side=tk.LEFT, padx=2, pady=4)
        toolbar_button3 = tk.Button(fm_toolbar, text=button3_text, **TOOLBAR_OPTIONS)
        toolbar_button3.pack(side=tk.LEFT, padx=2, pady=4)
        toolbar_button4 = tk.Button(fm_toolbar, text=button4_text, **TOOLBAR_OPTIONS)
        toolbar_button4.pack(side=tk.LEFT, padx=2, pady=4)
        
        label = tk.Label(fm_see_model, text="制限時間内にイラストを覚えよう", bg=see_model_fm_bg, font=(main_font, 25))
        label.pack(side=tk.TOP, padx=(0, 0), pady=(20, 0))
        
        # お手本の画像の表示
        self.image = Image.open(f"./image/image_{last_photo}.jpg")  # 画像のパスを指定
        image_width = 820
        self.image = self.image.resize((image_width, int(image_width/1280*800)))

        photo = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(fm_see_model, image=photo, bg="#000000")
        self.image_label.pack(side=tk.TOP, padx=(0, 0), pady=(20, 0))
        self.image_label.image = photo

        # 難易度によって制限時間を決定
        if last_difficulty == "button_1":
            self.count_time = 30 + 1
        elif last_difficulty == "button_2":
            self.count_time = 20 + 1
        elif last_difficulty == "button_3":
            self.count_time = 10 + 1

        self.timer_bg = "#191970"
        self.count_label = tk.Label(fm_see_model, text=f"残り {self.count_time} 秒", fg=self.timer_bg, bg=see_model_fm_bg, font=(main_font, 30))
        self.count_label.pack(side=tk.LEFT, padx=(520, 0), pady=(20, 20))
        
        skip_button = tk.Button(fm_see_model, text="スキップする", bg=see_model_btn_bg, font=(main_font, 18), width=16,
                                        relief="raised", borderwidth=5, command=lambda: self.countdown_animation_2(skip_button = 1))
        skip_button.pack(side=tk.LEFT, padx=(100, 0), pady=(20, 20))
            
        self.update_timer()
        
    # 制限時間をカウントして表示する
    def update_timer(self):
        if skip_on == "NULL":
            if self.count_time >= 0:
                self.count_time = self.count_time - 1
                if self.count_time <= 10:
                    self.timer_bg = "red"
                self.count_label.config(text=f"残り {self.count_time} 秒", fg=self.timer_bg)
            
            if self.count_time == -1:
                skip_button = 0
                self.countdown_animation_2(skip_button)
            else:
                # Update every 1000ms (1 second)
                self.master.after(1000, self.update_timer)



# -------- カウントダウンアニメーション２ --------
    def countdown_animation_2(self, skip_button):

        pw_see_model.destroy()
        self.master.after(600)
        
        global pw_window
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
        self.num_text = 3

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
                    self.master.after(50, self.To_see_model_2(skip_button))  # 400ミリ秒後にウィンドウを閉じる
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

    # see_modelの為に
    def To_see_model_2(self, skip_button):
        global the_only_2
        if the_only_2 == True:
            the_only_2 = False
            pw_window.destroy()
            self.drawing_illustration(skip_button)
            
        


    #イラストをペイント
    def drawing_illustration(self, skip_button):
        
        global skip_on
        if skip_button == 1:
            skip_on = "Yes"
        elif skip_button == 0:
            skip_on = "No"
        print(f"skip_button : " + str(skip_on))
        
        global skip_on_draw
        skip_on_draw = "NULL"
        
        global count_see_model
        count_see_model = False
        global count_illustration
        count_illustration = True
        
        global pw_illustration
        pw_illustration = tk.PanedWindow(self.master, bg=illustration_pw_bg, orient="vertical")
        pw_illustration.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        fm_illustration = tk.Frame(pw_illustration, bd=5, bg=illustration_pw_bg, relief="ridge", borderwidth=10)
        pw_illustration.add(fm_illustration)
        
        # ツールバー作成
        fm_toolbar = tk.Frame(fm_illustration, bg=illustration_fm_bg)
        fm_toolbar.pack(anchor="nw")

        toolbar_button1 = tk.Button(fm_toolbar, text=button1_text, **TOOLBAR_OPTIONS)
        toolbar_button1.pack(side=tk.LEFT, padx=4, pady=4)
        toolbar_button2 = tk.Button(fm_toolbar, text=button2_text, **TOOLBAR_OPTIONS)
        toolbar_button2.pack(side=tk.LEFT, padx=2, pady=4)
        toolbar_button3 = tk.Button(fm_toolbar, text=button3_text, **TOOLBAR_OPTIONS)
        toolbar_button3.pack(side=tk.LEFT, padx=2, pady=4)
        toolbar_button4 = tk.Button(fm_toolbar, text=button4_text, **TOOLBAR_OPTIONS)
        toolbar_button4.pack(side=tk.LEFT, padx=2, pady=4)
        
        label = tk.Label(fm_illustration, text="制限時間内にイラストを描こう", bg=illustration_fm_bg, font=(main_font, 25))
        label.pack(side=tk.TOP, padx=(0, 0), pady=(20, 0))
        
        # x = window_width - 50
        # y = window_height - 120
        x = 820 # お手本の写真と合わせる
        y = x / 1280 * 820
        self.canvas = tk.Canvas(fm_illustration, bg="#fff", width=x, height=y)
        self.canvas.pack(side=tk.TOP, padx=(20, 20), pady=(20, 20))
        
        # 難易度によって制限時間を決定
        if last_difficulty == "button_1":
            self.count_draw_time = 60 + 1
        elif last_difficulty == "button_2":
            self.count_draw_time = 40 + 1
        elif last_difficulty == "button_3":
            self.count_draw_time = 20 + 1
        
        self.timer_draw_bg = "#191970"
        self.count_draw_label = tk.Label(fm_illustration, text=f"残り {self.count_draw_time} 秒", fg=self.timer_draw_bg, bg=illustration_fm_bg, font=(main_font, 30))
        self.count_draw_label.pack(side=tk.LEFT, padx=(520, 0), pady=(20, 20))
        skip_draw_button = tk.Button(fm_illustration, text="これで完成！！", bg=illustration_btn_bg, font=(main_font, 18), width=16,
                                        relief="raised", borderwidth=5, command=lambda: self.scoring(skip_button_draw = 1))
        skip_draw_button.pack(side=tk.LEFT, padx=(100, 0), pady=(20, 20))
        
        self.update_draw_timer()
        
    # 制限時間をカウントして表示する
    def update_draw_timer(self):
        if skip_on_draw == "NULL":
            if self.count_draw_time >= 0:
                self.count_draw_time = self.count_draw_time - 1
                if self.count_draw_time <= 10:
                    self.timer_draw_bg = "red"
                self.count_draw_label.config(text=f"残り {self.count_draw_time} 秒", fg=self.timer_draw_bg)

            if self.count_draw_time == -1:
                skip_button_draw = 0
                self.scoring(skip_button_draw)
            else:
                # Update every 1000ms (1 second)
                self.master.after(1000, self.update_draw_timer)


    # scoring
    def scoring(self, skip_button_draw):
        
        global count_change_scoring_sub
        count_change_scoring_sub = 12
        
        global skip_on_draw
        if skip_button_draw == 1:
            skip_on_draw = "Yes"
        elif skip_button_draw == 0:
            skip_on_draw = "No"
        print(f"skip_button_draw : " + str(skip_on_draw))
        
        # canvasの縦横座標を取得
        # canvas_width = self.canvas.winfo_width()
        # canvas_height = self.canvas.winfo_height()
        # canvas_x = self.canvas.winfo_x()
        # canvas_y = self.canvas.winfo_y()
        # print(f"{canvas_width} x {canvas_height} + {canvas_x} + {canvas_y}")      
        #スクショ撮影
        global illustration_number
        illustration_number = 12
        # top = 260
        # left = 552
        # width = 835
        # height = 540
        # pg.screenshot(f'./illustration_image/illustration_{str(illustration_number)}.png', region=(left, top, width, height)) # pgを使ってのスクショは？
        screen_shot = ImageGrab.grab()
        screen_shot.save(f'./illustration_image/illustration_{str(illustration_number)}.png')
        # トリミング
        image = Image.open(f'./illustration_image/illustration_{str(illustration_number)}.png')
        left = 452
        upper = 238
        right = 1487
        lower = 906
        im_crop = image.crop((left, upper, right, lower))
        im_crop.save(f'./illustration_image/illustration_{str(illustration_number)}.png')
        
        
        
        pw_illustration.destroy()
        
        global count_illustration
        count_illustration = False
        global count_scoring
        count_scoring = True
        
        global pw_scoring
        pw_scoring = tk.PanedWindow(self.master, bg=scoring_pw_bg, orient="vertical")
        pw_scoring.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        fm_scoring = tk.Frame(pw_scoring, bd=5, bg=scoring_pw_bg, relief="ridge", borderwidth=10)
        pw_scoring.add(fm_scoring)
        
        self.master.after(500)
        
        global scoring_sub_window
        #採点中ウィンドウの表示
        if skip_on != "NULL" and skip_on_draw != "NULL":
            scoring_sub_window = tk.Toplevel(bg=scoring_fm_bg, bd=5)
            scoring_sub_window.geometry(scoring_sub_window_size)
            scoring_sub_window.title("scoring")
            scoring_sub_window.lift() # 他のウィンドウより前面に固定
            
            initial_scoring_sub_text = "採点中"
            self.scoring_sub_text = initial_scoring_sub_text
            # ランダムにRGBを作成
            red = rand.randint(0, 255)
            green = rand.randint(0, 255)
            blue = rand.randint(0, 255)
            color_code = "#{:02X}{:02X}{:02X}".format(red, green, blue)
            initial_scoring_sub_fg = color_code
            self.scoring_sub_fg = initial_scoring_sub_fg
            self.scoring_sub_label = tk.Label(scoring_sub_window, text=self.scoring_sub_text, bg=scoring_fm_bg, fg=self.scoring_sub_fg, font=(main_font, 48))
            self.scoring_sub_label.pack(side=tk.TOP, padx=(0, 0), pady=(35, 10))
            
            self.change_scoring_sub_text()
            
        
        # ツールバー作成
        fm_toolbar = tk.Frame(fm_scoring, bg=scoring_fm_bg)
        fm_toolbar.pack(anchor="nw")

        toolbar_button1 = tk.Button(fm_toolbar, text=button1_text, **TOOLBAR_OPTIONS)
        toolbar_button1.pack(side=tk.LEFT, padx=4, pady=4)
        toolbar_button2 = tk.Button(fm_toolbar, text=button2_text, **TOOLBAR_OPTIONS)
        toolbar_button2.pack(side=tk.LEFT, padx=2, pady=4)
        toolbar_button3 = tk.Button(fm_toolbar, text=button3_text, **TOOLBAR_OPTIONS)
        toolbar_button3.pack(side=tk.LEFT, padx=2, pady=4)
        toolbar_button4 = tk.Button(fm_toolbar, text=button4_text, **TOOLBAR_OPTIONS)
        toolbar_button4.pack(side=tk.LEFT, padx=2, pady=4)
        

        
                
    # 採点中のウィンドウのアニメーション
    def change_scoring_sub_text(self):
        global count_change_scoring_sub
        if count_change_scoring_sub % 4 == 0:
            self.scoring_sub_text = "採点中"
        elif count_change_scoring_sub % 4 == 3:
            self.scoring_sub_text = "採点中."
        elif count_change_scoring_sub % 4 == 2:
            self.scoring_sub_text = "採点中.."
        elif count_change_scoring_sub % 4 == 1:
            self.scoring_sub_text = "採点中..."
        self.scoring_sub_text
        # ランダムにRGBを作成
        red = rand.randint(0, 255)
        green = rand.randint(0, 255)
        blue = rand.randint(0, 255)
        color_code = "#{:02X}{:02X}{:02X}".format(red, green, blue)
        self.scoring_sub_fg = color_code
        self.scoring_sub_label.config(text=self.scoring_sub_text, fg=self.scoring_sub_fg)
        
        count_change_scoring_sub = count_change_scoring_sub - 1
        if count_change_scoring_sub > 0:
            self.master.after(800, self.change_scoring_sub_text)
        else:
            print("rei")
            global scoring_sub_window
            scoring_sub_window.destroy()
            return 0
        
        


    # 注意ウィンドウを消す
    def exit_warning(self):
        difficulty_window.destroy()
        return 0
    
    
    # タイトルへ戻る
    def return_title(self):
        if count_choice == True:
            fm_choice.destroy()
        elif count_see_model == True:
            pw_see_model.destroy
        else: 
            pass
        
        self.create_widgets()
        


    # アプリケーションが終了されたとき
    def exit_App(self):
        global forced_exit
        forced_exit = False
        
        if count_title == True:
            self.master.quit()
        else: 
            pass


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
y = (screen_height // 3) - (window_height // 3)
#y = 2

myapp = Application(master=main_window)
myapp.master.title("paintApp")
myapp.master.geometry(f"{window_width}x{window_height-10}+{x}+{y}")
myapp.mainloop()
