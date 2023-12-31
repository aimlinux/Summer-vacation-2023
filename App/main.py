import tkinter as tk
from tkinter import filedialog 
from tkinter import messagebox 
from tkinter import PhotoImage
from tkinter import scrolledtext
from tkinter import ttk
import PySimpleGUI as sg
#import pyautogui as pg # スクショ撮影用 併用するとtkinterのウィンドウが小さくなる（pgモジュールのコードが原因らしい）
import cv2
import PIL
from PIL import Image, ImageTk
from PIL import ImageGrab # pgが使えないため
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import skimage
from skimage.metrics import structural_similarity as compare_ssim
import pygame as pe
from pydub import AudioSegment
from pydub.playback import play
import threading
import random as rand
import atexit
import webbrowser
import logging
import time
import sys  
import os 


# 開発者名前とパスワード
debugger_name = "a"
debugger_pas = "a"

# logを保存するためのファイル
log_file_path = './log/test.log'

# -------- Logの各設定 --------
#logの出力名を設定
logger = logging.getLogger('Log')
#logLevelを設定
global log_lebel
log_lebel = 10
logger.setLevel(log_lebel)
#logをコンソール出力するための設定
sh = logging.StreamHandler()
logger.addHandler(sh)
#logのファイル出力先設定
fh = logging.FileHandler(log_file_path)
logger.addHandler(fh)
#全てのフォーマットオプションとその役割
# %(asctime)s	実行時刻
# %(filename)s	ファイル名
# %(funcName)s	行番号
# %(levelname)s	ログの定義
# %(lineno)d	ログレベル名
# %(message)s	ログメッセージ
# %(module)s	モジュール名
# %(name)s	関数名
# %(process)d	プロセスID
# %(thread)d	スレッドID
formatter = logging.Formatter('%(asctime)s --- process : %(process)d --- message : %(message)s')
fh.setFormatter(formatter)
sh.setFormatter(formatter)


# ペイントされた回数をカウントするためのテキストファイル
count_filename = './count.txt'
with open(count_filename, encoding="UTF-8") as f:
    f_text = f.read()
with open(count_filename, mode='w') as f: # 書き込みで開いて、初期からスタート
    if not f_text:
        f.write("0")
    else:
        f.write(f_text)
        
        
# 各情報を保存する為のテキストファイル
info_filename = './info.txt'
with open(info_filename, encoding="UTF-8") as f:
    info_text = f.read()    
    #print(info_text)
    
    
forced_exit = True # 強制終了されたかどうか
last_photo = None # お手本のイラストが選択されているかどうか

main_font = "Helvetica"

main_pw_bg = "#ffe4e1"
title_fm_bg = "#ffe4e1"
choice_pw_bg = "#ffe4e1"
choice_fm_bg = "#ffe4e1"
see_model_pw_bg = "#ffe4e1"
see_model_fm_bg = "#ffe4e1"
illustration_pw_bg = "#ffe4e1"
illustration_fm_bg = "#ffe4e1"
scoring_pw_bg = "#ffe4e1"
scoring_fm_bg = "#ffe4e1"
ranking_pw_bg = "#ffe4e1"
ranking_fm_bg = "#ffe4e1"

credit_bg = "#1AE0A3"
link_bg = "#1AE0A3"
link_fg = "#191970"
log_bg = "#1AE0A3"
about_this_app_bg = "#1AE0A3"

title_btn_bg = "#7FDBF0"
choice_btn_bg = "#7CF3CE"
see_model_btn_bg = "#00ced1"
introduction_btn_bg = "#fff0f5"
illustration_btn_bg = "#00ced1"
scoring_btn_bg = "#00ced1"
ranking_btn_bg = "#00ced1"
log_btn_bg = "#00ced1"
about_this_app_bg = "#c0c0c0"

button1_text = "タイトルへ"
button2_text = "オプション"
button3_text = "ランキング"
button4_text = "クレジット"
button5_text = "開発者ログ"

TOOLBAR_OPTIONS = { 
    "font" : "main_font, 15",
    "bg" : "#00ced1",
    "fg" : "#00334d"
}

# 各ウィンドウのサイズ
difficulty_window_size = "500x600+500+100"
warning_window_size = "600x140+500+400"
game_start_window_size = "800x200+300+300"
scoring_sub_window_size = "600x200+500+320"
credit_window_size = "600x650+500+100"
no_ranking_window_size = "850x180+360+360"
enter_name_window_size = "830x350+360+240"
log_window_size = "800x650+400+100"
about_this_app_window_size = "600x650+500+100"


#一度きりのイベント
the_only_1 = True
the_only_2 = True
the_only_debugger_login = False

# サウンド選択
sound_name = 0

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
        
    # サウンド再生
    def sound_start(self):
        
        if sound_name == 0: # スタート際のサウンド
            sound_file_path = "./sound/start.wav"
            adjusted_sound_file_path = "./sound/start_up.wav"
        else:
            return 1
        
        # 速度調節がされていなかった場合にする
        if not os.path.exists(adjusted_sound_file_path):
            # -------- pydubによる再生速度調節 --------
            audio = AudioSegment.from_file(sound_file_path)
            speed_adjustment = 1.3
            ajusted_audio = audio.speedup(playback_speed=speed_adjustment)
            ajusted_audio.export(adjusted_sound_file_path, format="wav")
        sound_file_path = adjusted_sound_file_path
        
        # -------- pygameによるサウンド再生 --------
        pe.init() # pygameを初期化
        sound_object = pe.mixer.Sound(sound_file_path) # サウンドオブジェクトを作成
        # playback_speed = 1.2 # 再生速度の倍率（1.0がデフォルト）
        # sound_object.set_playback_speed(playback_speed)
        sound_object.play() # サウンドを再生
        pe.time.wait(int(sound_object.get_length() * 1000)) # 音声再生終了まで待つ
        pe.quit() # pygameを終了

        
    # メインウィンドウ作成
    def create_widgets(self):
        
        # Logファイルに記録を残す
        logger.log(100, "App Start")
        
        global last_photo
        last_photo = None # お手本のイラストの選択を初期化
        
        global the_only_1, the_only_2
        the_only_1 = True
        the_only_2 = True
        
        
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

        toolbar_button1 = tk.Button(fm_toolbar, text=button1_text, **TOOLBAR_OPTIONS, command=lambda: self.return_title("pw_title"))
        toolbar_button1.pack(side=tk.LEFT, padx=4, pady=4)
        toolbar_button2 = tk.Button(fm_toolbar, text=button2_text, **TOOLBAR_OPTIONS)
        toolbar_button2.pack(side=tk.LEFT, padx=2, pady=4)
        toolbar_button3 = tk.Button(fm_toolbar, text=button3_text, **TOOLBAR_OPTIONS, command=lambda: self.ranking("pw_title"))
        toolbar_button3.pack(side=tk.LEFT, padx=2, pady=4)
        toolbar_button4 = tk.Button(fm_toolbar, text=button4_text, **TOOLBAR_OPTIONS, command=self.credit)
        toolbar_button4.pack(side=tk.LEFT, padx=2, pady=4)
        toolbar_button5 = tk.Button(fm_toolbar, text=button5_text, **TOOLBAR_OPTIONS, command=self.log_window)
        toolbar_button5.pack(side=tk.LEFT, padx=2, pady=4)
        
        start_button = tk.Button(bg_frame, text="はじめる", font=(main_font, 20), bg=title_btn_bg, 
                                width=30, relief="raised", borderwidth=5, command=self.start_App) # reliefによって影を表現
        start_button.pack(side=tk.TOP, pady=(450, 50), padx=(750, 150)) # 「fill="x"」：水平方向に埋める
        exit_button = tk.Button(bg_frame, text="終了する", font=(main_font, 20), bg=title_btn_bg, 
                                width=30, relief="raised", borderwidth=5, command=self.exit_App)
        exit_button.pack(side=tk.TOP, padx=(750, 150))
        
        introduction_button = tk.Button(bg_frame, text="このゲームのトリセツ", font=(main_font, 18), bg=introduction_btn_bg, 
                                        width=30, relief="raised", borderwidth=3, command=self.about_this_app)
        introduction_button.pack(side=tk.TOP, padx=(30, 800), pady=(40, 0))


    #アプリケーションが始まった時
    def start_App(self):
        
        pw_title.destroy()
        fm_title.destroy()
        time.sleep(0.1)

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
                                        relief="raised", borderwidth=5, command=lambda: self.return_title("fm_choice"))
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
        
        # お手本が選択されていなかった場合
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
            

    # 注意ウィンドウを消す
    def exit_warning(self):
        difficulty_window.destroy()
        return 0
        
        
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
            
            return_choice_button = tk.Button(game_start_window, text="戻る", bg=choice_btn_bg, font=(main_font, 14), width=10,
                                        relief="raised", borderwidth=5, command=self.return_choice)
            return_choice_button.pack(side=tk.LEFT, padx=(250, 10))
            decided_button = tk.Button(game_start_window, text="スタート", bg=choice_btn_bg, font=(main_font, 14), width=10,
                                        relief="raised", borderwidth=5, command=lambda: self.countdown_animation_1())
            decided_button.pack(side=tk.LEFT, padx=(100, 10))
            
        else:
            pass
        
        
    # イラスト選択へ戻る
    def return_choice(self):
        game_start_window.destroy()
        return 0

    # 並列処理を使ってみたかった
    def countdown_animation_1_reserve(self):
        # アニメーションスレッドを開始
        animation_thread = threading.Thread(target=self.countdown_animation_1)
        animation_thread.start()
        global sound_name
        sound_name = 0
        # バックグラウンドサウンドを開始
        sound_thread = threading.Thread(target=self.sound_start)
        sound_thread.start()
        

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
        self.initial_font_size = 300

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

        toolbar_button1 = tk.Button(fm_toolbar, text=button1_text, **TOOLBAR_OPTIONS, command=lambda: self.return_title("else"))
        toolbar_button1.pack(side=tk.LEFT, padx=4, pady=4)
        toolbar_button2 = tk.Button(fm_toolbar, text=button2_text, **TOOLBAR_OPTIONS)
        toolbar_button2.pack(side=tk.LEFT, padx=2, pady=4)
        toolbar_button3 = tk.Button(fm_toolbar, text=button3_text, **TOOLBAR_OPTIONS, command=lambda: self.ranking("else"))
        toolbar_button3.pack(side=tk.LEFT, padx=2, pady=4)
        toolbar_button4 = tk.Button(fm_toolbar, text=button4_text, **TOOLBAR_OPTIONS, command=self.credit)
        toolbar_button4.pack(side=tk.LEFT, padx=2, pady=4)
        toolbar_button5 = tk.Button(fm_toolbar, text=button5_text, **TOOLBAR_OPTIONS, command=self.log_window)
        toolbar_button5.pack(side=tk.LEFT, padx=2, pady=4)
        
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
        else:
            return 0


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
        self.initial_font_size = 300

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

    # drawing_illustrationの為に
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
        
        global pw_illustration
        pw_illustration = tk.PanedWindow(self.master, bg=illustration_pw_bg, orient="vertical")
        pw_illustration.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        fm_illustration = tk.Frame(pw_illustration, bd=5, bg=illustration_pw_bg, relief="ridge", borderwidth=10)
        pw_illustration.add(fm_illustration)
        
        # ツールバー作成
        fm_toolbar = tk.Frame(fm_illustration, bg=illustration_fm_bg)
        fm_toolbar.pack(anchor="nw")

        toolbar_button1 = tk.Button(fm_toolbar, text=button1_text, **TOOLBAR_OPTIONS, command=lambda: self.return_title("else"))
        toolbar_button1.pack(side=tk.LEFT, padx=4, pady=4)
        toolbar_button2 = tk.Button(fm_toolbar, text=button2_text, **TOOLBAR_OPTIONS)
        toolbar_button2.pack(side=tk.LEFT, padx=2, pady=4)
        toolbar_button3 = tk.Button(fm_toolbar, text=button3_text, **TOOLBAR_OPTIONS, command=lambda: self.ranking("else"))
        toolbar_button3.pack(side=tk.LEFT, padx=2, pady=4)
        toolbar_button4 = tk.Button(fm_toolbar, text=button4_text, **TOOLBAR_OPTIONS, command=self.credit)
        toolbar_button4.pack(side=tk.LEFT, padx=2, pady=4)
        toolbar_button5 = tk.Button(fm_toolbar, text=button5_text, **TOOLBAR_OPTIONS, command=self.log_window)
        toolbar_button5.pack(side=tk.LEFT, padx=2, pady=4)
        
        label = tk.Label(fm_illustration, text="制限時間内にイラストを描こう", bg=illustration_fm_bg, font=(main_font, 25))
        label.pack(side=tk.TOP, padx=(0, 0), pady=(10, 0))
        
        # x = window_width - 50
        # y = window_height - 120
        x = 820 # お手本の写真と合わせる
        y = x / 1280 * 820
        self.canvas = tk.Canvas(fm_illustration, bg="#fff", width=x, height=y)
        self.canvas.pack(side=tk.TOP, padx=(20, 20), pady=(10, 0))
        
        self.canvas.bind("<ButtonPress-1>", self.on_pressed)
        self.canvas.bind("<B1-Motion>", self.on_dragged)
        self.canvas.bind("<ButtonPress-2>",self.click1)
        self.canvas.bind("<ButtonPress-3>",self.click2)
        
        COLORS = ["black", "white", "blue", "pink", "green","red"]
        self.color = tk.StringVar()                    
        self.color.set(COLORS[0])                             
        b = tk.OptionMenu(fm_illustration, self.color, *COLORS) 
        b.pack(side = tk.LEFT, padx=(200, 10), pady=(0, 0))
        
        self.width = tk.Scale(fm_illustration, from_ = 1, to = 10,
                                orient = tk.HORIZONTAL) 
        self.width.set(3)                                       
        self.width.pack(side = tk.LEFT, padx=(0, 10), pady=(0, 0))
        
        # 難易度によって制限時間を決定
        if last_difficulty == "button_1":
            self.count_draw_time = 60 + 1
        elif last_difficulty == "button_2":
            self.count_draw_time = 40 + 1
        elif last_difficulty == "button_3":
            self.count_draw_time = 20 + 1
        
        self.timer_draw_bg = "#191970"
        self.count_draw_label = tk.Label(fm_illustration, text=f"残り {self.count_draw_time} 秒", fg=self.timer_draw_bg, bg=illustration_fm_bg, font=(main_font, 30))
        self.count_draw_label.pack(side=tk.LEFT, padx=(150, 0), pady=(0, 20))
        skip_draw_button = tk.Button(fm_illustration, text="これで完成！！", bg=illustration_btn_bg, font=(main_font, 18), width=16,
                                        relief="raised", borderwidth=5, command=lambda: self.scoring(skip_button_draw = 1))
        skip_draw_button.pack(side=tk.LEFT, padx=(100, 0), pady=(0, 20))
        
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
        else:
            return 0


    def on_pressed(self, event):
        self.sx = event.x
        self.sy = event.y
        self.canvas.create_oval(self.sx, self.sy, event.x, event.y,
                                outline = self.color.get(),
                                width = self.width.get())

    def on_dragged(self, event):
        self.canvas.create_line(self.sx, self.sy, event.x, event.y,
                            fill = self.color.get(),
                            width = self.width.get())
        self.sx = event.x
        self.sy = event.y

    def click1(self,event):
        self.canvas.create_oval(self.sx-20,self.sy-20,self.sx+20,self.sy+20,
                            fill = self.color.get(),
                            width = self.width.get())

    def click2(self,event):
            self.canvas.create_oval(self.sx-40,self.sy-30,self.sx+40,self.sy+30,
                            fill = self.color.get(),
                            width = self.width.get())
            
            
    # scoring
    def scoring(self, skip_button_draw):
        
        global count_change_scoring_sub
        count_change_scoring_sub = 8 # 「採点中」の文字のアニメーションの繰り返し回数
        
        global skip_on_draw
        if skip_button_draw == 1:
            skip_on_draw = "Yes"
        elif skip_button_draw == 0:
            skip_on_draw = "No"
        print(f"skip_button_draw : " + str(skip_on_draw))
        
        if skip_button_draw != "NULL":
            # --------- スクリーンショット -------
            # 保存先を決定
            with open(count_filename, encoding="UTF-8") as f:
                f_text = f.read()
            illustration_number = int(f_text) + 1
            illustration_filename = f'./illustration_image/illustration_{str(illustration_number)}.png'
            
            with open(count_filename, mode='w') as f: 
                    f.write(str(illustration_number))
                    
            logger.log(100, f'SaveFile : {illustration_filename}')
            # スクショ撮影
            # top = 260
            # left = 552
            # width = 835
            # height = 540
            # pg.screenshot(illustration_filename, region=(left, top, width, height)) # pgを使ってのスクショは？
            screen_shot = ImageGrab.grab()
            screen_shot.save(illustration_filename)
            # トリミング
            image = Image.open(illustration_filename)
            left = 452
            upper = 215
            right = 1487
            lower = 883
            im_crop = image.crop((left, upper, right, lower))
            im_crop.save(illustration_filename)
            
            self.master.after(500)
            
        global scoring_sub_window
        #採点中ウィンドウの表示
        if skip_on != "NULL" or skip_on_draw != "NULL":
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
        
        pw_illustration.destroy()
        
        global pw_scoring
        pw_scoring = tk.PanedWindow(self.master, bg=scoring_pw_bg, orient="vertical")
        pw_scoring.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        fm_scoring = tk.Frame(pw_scoring, bd=5, bg=scoring_pw_bg, relief="ridge", borderwidth=10)
        pw_scoring.add(fm_scoring)
        
        # ツールバー作成
        fm_toolbar = tk.Frame(fm_scoring, bg=scoring_fm_bg)
        fm_toolbar.pack(anchor="nw")

        toolbar_button1 = tk.Button(fm_toolbar, text=button1_text, **TOOLBAR_OPTIONS, command=lambda: self.return_title("else"))
        toolbar_button1.pack(side=tk.LEFT, padx=4, pady=4)
        toolbar_button2 = tk.Button(fm_toolbar, text=button2_text, **TOOLBAR_OPTIONS)
        toolbar_button2.pack(side=tk.LEFT, padx=2, pady=4)
        toolbar_button3 = tk.Button(fm_toolbar, text=button3_text, **TOOLBAR_OPTIONS, command=lambda: self.ranking("pw_scoring"))
        toolbar_button3.pack(side=tk.LEFT, padx=2, pady=4)
        toolbar_button4 = tk.Button(fm_toolbar, text=button4_text, **TOOLBAR_OPTIONS, command=self.credit)
        toolbar_button4.pack(side=tk.LEFT, padx=2, pady=4)
        toolbar_button5 = tk.Button(fm_toolbar, text=button5_text, **TOOLBAR_OPTIONS, command=self.log_window)
        toolbar_button5.pack(side=tk.LEFT, padx=2, pady=4)
        
        #画像の類似度を比較
        image1_path = f'./image/image_{last_photo}.jpg'
        image2_path = illustration_filename
        similar = self.calculate_similarity(image1_path, image2_path)
        if similar == 10:
            print("Error")
        else:
            print(f"画像の類似度 : {similar:.2%}")
            #print(similar)
        
        
        # 結果画面の表示
        fm_scoring_image = tk.Frame(fm_scoring, bg=scoring_fm_bg, bd=10, relief="ridge", borderwidth=10)
        fm_scoring_image.pack(side=tk.TOP, padx=(20, 20), pady=(20, 0))
        fm_scoring_image_upper = tk.Frame(fm_scoring_image, bg=scoring_fm_bg)
        fm_scoring_image_upper.pack(side=tk.TOP, pady=(0, 0))
        fm_scoring_image_lower = tk.Frame(fm_scoring_image, bg=scoring_fm_bg)
        fm_scoring_image_lower.pack(side=tk.TOP, pady=(0, 0))
        
        label = tk.Label(fm_scoring_image_upper, text="お手本のイラスト", fg="black", bg=scoring_fm_bg, font=(main_font, 26))
        label.pack(side=tk.LEFT, padx=(50, 60), pady=(20, 0))
        label = tk.Label(fm_scoring_image_upper, text="あなたのイラスト", fg="black", bg=scoring_fm_bg, font=(main_font, 26))
        label.pack(side=tk.LEFT, padx=(60, 50), pady=(20, 0))
        
        # お手本の画像の表示
        image = Image.open(f"./image/image_{last_photo}.jpg")  # 画像のパスを指定
        image_width = 400
        image = image.resize((image_width, int(image_width/1280*800)))
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(fm_scoring_image_lower, image=photo, bg="#000000")
        image_label.pack(side=tk.LEFT, padx=(50, 30), pady=(20, 20))
        image_label.image = photo
        
        # ペイントした画像の表示
        image = Image.open(illustration_filename)  # 画像のパスを指定
        image_width = 400
        image = image.resize((image_width, int(image_width/1280*800)))
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(fm_scoring_image_lower, image=photo, bg="#000000")
        image_label.pack(side=tk.LEFT, padx=(30, 50), pady=(20, 20))
        image_label.image = photo
        
        fm_scoring_text_left = tk.Frame(fm_scoring, bg=scoring_fm_bg)
        fm_scoring_text_left.pack(side=tk.LEFT, padx=(150, 100), pady=(10, 0))
        fm_scoring_text_right = tk.Frame(fm_scoring, bg=scoring_fm_bg)
        fm_scoring_text_right.pack(side=tk.RIGHT, padx=(100, 100),  pady=(10, 0))
        
        # 難易度によってテキストを決定
        if last_difficulty == "button_1":
            difficulty_text = "初級"
        elif last_difficulty == "button_2":
            difficulty_text = "中級"
        elif last_difficulty == "button_3":
            difficulty_text = "上級"
        # 現在のランクを決定
        rank = "1"
        # 類似度の感想を決定
        re = similar * 100
        if 0 <= re < 40:
            similar_comment = "いまいちだね、、"
            similar_comment_fg = "#4682d4"
            mark = "..."
        elif 40 <= re < 70:
            similar_comment = "可もなく不可もなく？"
            similar_comment_fg = "#2f2f4f"
            mark = "..."
        elif 70 <= re <= 100:
            similar_comment = "素晴らしい才能！！"
            similar_comment_fg = "#ff00ff"
            mark = " !!"
        score_label = tk.Label(fm_scoring_text_left, text=f"類似度 : {similar:.2%}{mark}", bg=scoring_fm_bg, fg="#493563", font=(main_font, 24))
        score_label.pack(side=tk.TOP, padx=(50, 50), pady=(20, 0))
        score_label = tk.Label(fm_scoring_text_left, text=f"{similar_comment}", bg=scoring_fm_bg, fg=similar_comment_fg, font=(main_font, 24))
        score_label.pack(side=tk.TOP, padx=(50, 50), pady=(20, 0))
        ranking_label = tk.Label(fm_scoring_text_left, text=f"ランキング({difficulty_text}) : {rank}位", bg=scoring_fm_bg, fg="#493563", font=(main_font, 23))
        ranking_label.pack(side=tk.TOP, padx=(50, 50), pady=(20, 0))
        name_ranking_button = tk.Button(fm_scoring_text_left, text="ランキングに名前を登録", bg=scoring_btn_bg, fg="black", font=(main_font, 18), width=22, 
                                        relief="raised", borderwidth=5, command=self.enter_name)
        name_ranking_button.pack(side=tk.TOP, padx=(50, 50), pady=(30, 0))
        
        
        name_ranking_button = tk.Button(fm_scoring_text_right, text="ランキングを見る", bg=scoring_btn_bg, fg="black", font=(main_font, 18), width=22, 
                                        relief="raised", borderwidth=5, command=lambda: self.ranking("pw_scoring"))
        name_ranking_button.pack(side=tk.TOP, padx=(50, 50), pady=(30, 0))
        button = tk.Button(fm_scoring_text_right, text="イラストダウンロード", bg=scoring_btn_bg, fg="black", font=(main_font, 18), width=22, 
                                        relief="raised", borderwidth=5)
        button.pack(side=tk.TOP, padx=(50, 50), pady=(30, 0))
        button = tk.Button(fm_scoring_text_right, text="タイトルへ戻る", bg=scoring_btn_bg, fg="black", font=(main_font, 18), width=22, 
                                        relief="raised", borderwidth=5, command=lambda: self.return_title("else"))
        button.pack(side=tk.TOP, padx=(50, 50), pady=(30, 0))
        
        # 「info.txt」に各情報を追記（mode="a"）
        # illustration_number, last_number, usr_name_value, similar*100, last_difficultly
        with open(info_filename, encoding='UTF-8', mode="a") as f:
            global info_1, info_2, info_3, info_4
            info_1 = f"{illustration_number}"
            if last_difficulty == "button_1":
                aa = "初級"
            elif last_difficulty == "button_2":
                aa = "中級"
            else: 
                aa = "上級"
            info_2 = aa
            bb = button_list_thing[last_photo - 1]
            info_3 = bb
            info_4 = f"{similar:.2%}"
            info_5 = "NoName"
            line_contents = f"{info_1}, {info_2}, {info_3}, {info_4}, {info_5}\n"
            f.write(line_contents)
            
            
        
    #画像の類似度を比較する関関数
    def calculate_similarity(self, image1_path, image2_path):
        # 画像読み込み
        image1 = cv2.imread(image1_path)
        image2 = cv2.imread(image2_path)
        # 画像を同じサイズにリサイズ
        new_size = (400, 400)  # 新しいサイズを設定
        image1 = cv2.resize(image1, new_size)
        image2 = cv2.resize(image2, new_size)

        # 画像をグレースケールに変換
        gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        
        #画像のサイズが一致するか確認
        if gray_image1.shape != gray_image2.shape:
            #raise ValueError("Input images must have the same dimensions.")
            return 10
        else: 
            # 画像の類似度を計算
            similarity = compare_ssim(gray_image1, gray_image2)
            return similarity
                
                
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
            end_scoring_sub_text = "rei"
            print(end_scoring_sub_text)
            global scoring_sub_window
            scoring_sub_window.destroy()
            return 0
        
    # 名前を入力するウィンドウ
    def enter_name(self):
        global enter_name_window
        enter_name_window = tk.Toplevel(bg=main_pw_bg, bd=5)
        enter_name_window.geometry(enter_name_window_size)
        enter_name_window.title("enter name")
        enter_name_window.lift() # 他のウィンドウより前面に固定
        
        label = tk.Label(enter_name_window, text="ランキングに登録するニックネームを入力してください。",
                                bg=main_pw_bg, font=(main_font, 22))
        label.pack(side=tk.TOP, padx=(0, 0), pady=(20, 10))
        label = tk.Label(enter_name_window, text="※ニックネームは他のユーザーからも見られます。\n 2~10文字で入力して下さい。  [例：ほのか]",
                                fg="#000080", bg=main_pw_bg, font=(main_font, 18))
        label.pack(side=tk.TOP, padx=(0, 0), pady=(10, 10))
        #テキストボックス
        usr_name = tk.StringVar()
        name_entry = ttk.Entry(
            enter_name_window,
            textvariable=usr_name,
            width=30,
            font=(main_font, 25)
        )
        name_entry.pack(side=tk.TOP, padx=(10, 10), pady=(10, 10))
        button = tk.Button(enter_name_window, text="確定する", bg=title_btn_bg, font=(main_font, 22), 
                            width=10, command=lambda:self.name_confirmed(usr_name))
        button.pack(side=tk.TOP, padx=(0, 0), pady=(10, 0))
        
        return 0
        
        
    # 入力された名前を確定
    def name_confirmed(self, usr_name):
        usr_name_value = usr_name.get() # 入力された文字を取得
        #print(len(usr_name_value))
        
        # 文字数が2~10文字に収まっていなかった場合
        if not 2 <= len(usr_name_value) <= 10:
            messagebox.showwarning('warning', 'ニックネームは２～１０文字で入力して下さい。')
            self.enter_name()
        # 「info.txt」に名前を含めた情報を上書きする
        else:
            # ---- 最後の行を消去 ----
            with open(info_filename, encoding='UTF-8', mode='r') as f:
                lines = f.readlines()
            if lines:
                lines.pop() # 最後の行を消去
            with open(info_filename, encoding='UTF-8', mode='w') as f:
                f.writelines(lines)
            # ---- 書き込み ----
            with open(info_filename, encoding='UTF-8', mode='a') as f:
                info_5 = usr_name_value # 名前のみ上書きする
                line_contents = f"{info_1}, {info_2}, {info_3}, {info_4}, {info_5}\n"
                f.write(line_contents)
                
            self.master.after(200, enter_name_window.destroy)
            return 0
    
    
    # タイトルへ戻る
    def return_title(self, lala):
        
        if lala == "fm_choice":
            fm_choice.destroy()
            self.create_widgets()
        elif lala == "pw_title":
            pw_title.destroy()
            self.create_widgets()
        elif lala == "else": # ややこしくなるので再起動
            self.master.destroy()
            #Restart python script itself
            os.execv(sys.executable, ['python'] + sys.argv)
        else:
            print("Error")
        
        

    # ランキングの表示
    def ranking(self, ere):
        
        # ランキングが開けなかった場合
        if ere == "else":
            logger.log(100, "ranking from else")
            
            global no_ranking_window
            no_ranking_window = tk.Toplevel(bg=main_pw_bg, bd=5)
            no_ranking_window.geometry(no_ranking_window_size)
            no_ranking_window.title("no_ranking")
            no_ranking_window.lift() # 他のウィンドウより前面に固定
            
            label = tk.Label(no_ranking_window, text="ここでランキングは開けないよ、、\n タイトルに戻るかゲームを終了するとランキングが見れるようになるよ！",
                                bg=main_pw_bg, font=(main_font, 18))
            label.pack(side=tk.TOP, padx=(0, 0), pady=(10, 10))
            button = tk.Button(no_ranking_window, text="OK", bg=ranking_btn_bg, font=(main_font, 16), width=15, 
                                relief="raised", borderwidth=5, command=self.exit_no_ranking)
            button.pack(side=tk.TOP, padx=(10, 10), pady=(10, 0))
            
            
        elif ere == "pw_title" or ere == "pw_scoring":
            if ere == "pw_title":
                ere_return = 0
                self.master.after(200, pw_title.destroy)
            elif ere == "pw_scoring":
                ere_return = 1
                self.master.after(200, pw_scoring.destroy)
                
            logger.log(100, "ranking from title")
            
            global fm_ranking
            fm_ranking = tk.Frame(self.master, bg=ranking_pw_bg, bd=5, relief="ridge", borderwidth=10)
            fm_ranking.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
            
            
            # リストボックスのスタイルをttkで変更
            style = ttk.Style()
            style.configure("Listbox", font=("Helvetica", 14))
            
            label = tk.Label(fm_ranking, text="**現在のランキング**", font=(main_font, 32), bg=ranking_fm_bg)
            label.pack(side=tk.TOP, padx=(0, 0), pady=(40, 40))
            main_frame = tk.Frame(fm_ranking, bg=ranking_pw_bg, bd=3, relief="ridge", borderwidth=3, highlightbackground="black", highlightthickness=2)
            main_frame.pack(side=tk.TOP, padx=(20, 20), pady=(0, 30))
            
            #左側のフレーム作成
            left_frame = tk.Frame(main_frame, bg=ranking_pw_bg)
            left_frame.pack(side=tk.LEFT)
            label = tk.Label(left_frame, text="~~難易度選択~~", font=(main_font, 20), bg=ranking_fm_bg)
            label.pack(side=tk.TOP, padx=(40, 10), pady=(20, 8))
            #リストボックスを格納するフレーム作成
            listbox_frame = tk.Frame(left_frame, bg="lightblue", bd=5, relief="ridge", borderwidth=5)
            listbox_frame.pack(side=tk.TOP, padx=(40, 10), pady=(0, 200))
            self.listbox_ranking = tk.Listbox(listbox_frame, selectbackground="lightblue", font=(main_font, 22), height=5, width=10)
            self.listbox_ranking.pack()
            # 戻るボタン
            return_button = tk.Button(left_frame, text="戻る", bg=ranking_btn_bg, font=(main_font, 20), command=lambda: self.exit_ranking(ere_return))
            return_button.pack(side=tk.BOTTOM, padx=(0, 20), pady=(0, 20), ipadx=10, ipady=0)
            
            self.item_1 = "     初級"
            self.item_2 = "     中級"
            self.item_3 = "     上級"
            self.listbox_ranking.select_set(0) # 最初のアイテムを選択状態にする
            self.listbox_ranking.insert(tk.END, self.item_1)
            self.listbox_ranking.insert(tk.END, self.item_2)
            self.listbox_ranking.insert(tk.END, self.item_3)
            self.listbox_ranking.bind("<Button-1>", self.on_ranking_difficulty_click)
            
            
            # 右上のフレーム作成
            right_upper_frame = tk.Frame(main_frame, bg="#fffff3", bd=5, relief="ridge", borderwidth=5)
            right_upper_frame.pack(side=tk.TOP, padx=(30, 50), pady=(20, 0))
            example_text_1 = "[ランク]"
            example_text_2 = "[得点]"
            example_text_3 = "[ニックネーム]"
            example_text_4 = "[お手本]"
            see_example_btn_text = "観覧"
            right_upper_frame_bg = "#fffff3"
            see_example_btn_bg = "#ffffe4"
            label = tk.Label(right_upper_frame, text=example_text_1, fg="black", bg=right_upper_frame_bg, font=(main_font, 17))
            label.pack(side=tk.LEFT, padx=(30, 0), pady=(5, 5))
            label = tk.Label(right_upper_frame, text=example_text_2, fg="black", bg=right_upper_frame_bg, font=(main_font, 17))
            label.pack(side=tk.LEFT, padx=(40, 0), pady=(5, 5))
            label = tk.Label(right_upper_frame, text=example_text_3, fg="black", bg=right_upper_frame_bg, font=(main_font, 17))
            label.pack(side=tk.LEFT, padx=(40, 0), pady=(5, 5))
            label = tk.Label(right_upper_frame, text=example_text_4, fg="black", bg=right_upper_frame_bg, font=(main_font, 17))
            label.pack(side=tk.LEFT, padx=(40, 0), pady=(5, 5))
            button = tk.Button(right_upper_frame, text=see_example_btn_text, fg="black", bg=see_example_btn_bg, font=(main_font, 15))
            button.pack(side=tk.LEFT, padx=(40, 30), pady=(5, 5), ipadx=5, ipady=1)
            
            # 右下のフレーム作成
            right_lower_frame_cover = tk.Frame(main_frame, bg="#fffff1", bd=5, relief="ridge", borderwidth=5, height=360, width=700)
            right_lower_frame_cover.pack(side=tk.TOP, padx=(30, 30), pady=(30, 0), ipadx=10, ipady=10)
            scrollbar = tk.Scrollbar(right_lower_frame_cover, orient="vertical")
            scrollbar.pack(side=tk.LEFT, fill="y")
            self.right_lower_canvas = tk.Canvas(right_lower_frame_cover, yscrollcommand=scrollbar.set)
            self.right_lower_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            scrollbar.config(command=self.right_lower_canvas.yview)
            self.right_lower_frame = tk.Frame(self.right_lower_canvas, bg=ranking_fm_bg)
            self.right_lower_canvas.create_window((0, 0), window=self.right_lower_frame, anchor="nw")
            
            # マウスホイールでスクロールできるように設定
            self.right_lower_canvas.bind("<Configure>", lambda event, canvas=self.right_lower_canvas: self.right_lower_canvas.configure(scrollregion=self.right_lower_canvas.bbox("all")))
            self.right_lower_canvas.bind_all("<MouseWheel>", self.on_mousewheel)
            
    def on_mousewheel(self, event):
        self.right_lower_canvas.yview_scroll(-1 * (event.delta // 120), "units")
        
        
    # ランキングに表示する難易度が選ばれたことを取得
    def on_ranking_difficulty_click(self, event):
        listbox_ranking_item_index = self.listbox_ranking.nearest(event.y) # クリックされたアイテムのインデックスを取得
        listbox_ranking_item = self.listbox_ranking.get(listbox_ranking_item_index) # インデックスからアイテムの内容を取得
        #print(listbox_ranking_item)
        if listbox_ranking_item:
            if listbox_ranking_item == self.item_1:
                self.frame_1_1 = tk.Frame(self.right_lower_frame, bg="#fffff3", bd=5, relief="ridge", borderwidth=5)
                self.frame_1_1.pack(side=tk.TOP, padx=(30, 50), pady=(20, 0))
                example_text_1 = "[ランク]"
                example_text_2 = "[得点]"
                example_text_3 = "[ニックネーム]"
                example_text_4 = "[お手本]"
                see_example_btn_text = "観覧"
                right_upper_frame_bg = "#fffff3"
                see_example_btn_bg = "#ffffe4"
                label = tk.Label(self.frame_1_1, text=example_text_1, fg="black", bg=right_upper_frame_bg, font=(main_font, 17))
                label.pack(side=tk.LEFT, padx=(30, 0), pady=(5, 5))
                label = tk.Label(self.frame_1_1, text=example_text_2, fg="black", bg=right_upper_frame_bg, font=(main_font, 17))
                label.pack(side=tk.LEFT, padx=(40, 0), pady=(5, 5))
                label = tk.Label(self.frame_1_1, text=example_text_3, fg="black", bg=right_upper_frame_bg, font=(main_font, 17))
                label.pack(side=tk.LEFT, padx=(40, 0), pady=(5, 5))
                label = tk.Label(self.frame_1_1, text=example_text_4, fg="black", bg=right_upper_frame_bg, font=(main_font, 17))
                label.pack(side=tk.LEFT, padx=(40, 0), pady=(5, 5))
                button = tk.Button(self.frame_1_1, text=see_example_btn_text, fg="black", bg=see_example_btn_bg, font=(main_font, 15))
                button.pack(side=tk.LEFT, padx=(40, 30), pady=(5, 5), ipadx=5, ipady=1)
            
            elif listbox_ranking_item == self.item_2:
                print(listbox_ranking_item)
            elif listbox_ranking_item == self.item_3:
                print(listbox_ranking_item)
            else:
                print("Error")
                return 10
            
            
    # ランキングを終了する
    def exit_ranking(self, h):
        if h == 0:
            self.master.after(100, fm_ranking.destroy)
            self.create_widgets()
    
        elif h == 1:
            self.master.after(100, fm_ranking.destroy)
            #self.scoring("NULL")
            #self.create_widgets()
            self.master.destroy()
            os.execv(sys.executable, ['python'] + sys.argv)
            
        else:
            print("Error")
            return 10
        
            
            
            
    # ランキングが開けない注意ウィンドウを閉じる
    def exit_no_ranking(self):
        self.master.after(200, no_ranking_window.destroy)
        
        
    # クレジット
    def credit(self):
        
        logger.log(100, "view credits")
        
        global credit_window
        credit_window = tk.Toplevel(bg=credit_bg, bd=5)
        credit_window.geometry(credit_window_size)
        credit_window.title("credit")
        credit_window.lift() # 他のウィンドウより前面に固定
        
        global github_link, kousen_link
        programmer_name = "aa"
        github_owner = "aimlinux"
        github_link = "https://github.com/aimlinux/Summer-vacation-2023/blob/main/App/main.py"
        kousen_link = "https://www.yonago-k.ac.jp/"
        used_library = ["tkinter", "PySimpleGUI", "pyautogui", "cv2", "PIL", "matplotlib", "skimage", "random", "atexit", "webbrowser", "logging", "time", "sys", "os"]
        used_library_text = ""
        for i in range(len(used_library)):
            used_library_text = (used_library_text + ", " + used_library[i])
            i += 1
        label = tk.Label(credit_window, text=f"作成者 : {programmer_name}", bg=credit_bg, font=(main_font, 24))
        label.pack(side=tk.TOP, pady=(50, 0))
        label = tk.Label(credit_window, text=f"Githubリンク : {github_owner}", bg=link_bg, fg=link_fg, 
                        font=(main_font, 22), cursor="hand2")
        label.pack(side=tk.TOP, pady=(30, 0))
        label.bind("<Button-1>", lambda e: self.open_github_link())
        label = tk.Label(credit_window, text=f"米子高専ホームページ", bg=link_bg, fg=link_fg, 
                        font=(main_font, 24), cursor="hand2")
        label.pack(side=tk.TOP, pady=(30, 0))
        label.bind("<Button-1>", lambda e: self.open_kousen_link())
        label = tk.Label(credit_window, text="python使用ライブラリ : ", bg=credit_bg, font=(main_font, 20))
        label.pack(side=tk.TOP, pady=(30, 10))
        #オブジェクト配置初期はstateの値を変更できるようにしなければならない
        self.text_new_question_sub1 = scrolledtext.ScrolledText(credit_window, width=40, height=6, font=(main_font, 20), bg="#fff", state="normal")
        self.text_new_question_sub1.pack(side=tk.TOP, padx=(20, 20))
        self.text_new_question_sub1.insert(tk.END, used_library_text)
        #stateの値を変更できないよう（normalからtk.DISABLED）に設定
        self.text_new_question_sub1.config(state=tk.DISABLED)
        start_button = tk.Button(credit_window, text="とじる", font=(main_font, 22), bg=title_btn_bg, command=self.exit_credit)
        start_button.pack(side=tk.TOP, padx=(20, 20), pady=(30, 0))
        
        return 0
    
    #webブラウザでgithubリンクを開く
    def open_github_link(self):
        logger.log(100, "view github from credits")
        webbrowser.open_new(github_link)
        return 0
    
    #webブラウザで米子高専ホームページを開く
    def open_kousen_link(self):
        logger.log(100, "view kosenHP from credits")
        webbrowser.open_new(kousen_link)
        return 0
        
    #credit_windowから戻る
    def exit_credit(self):
        global credit_window
        credit_window.destroy()
    
    
    # 開発者ログ
    def log_window(self):
        logger.log(100, "view log_window")
        
        global login_window
        login_window = tk.Toplevel(bg=log_bg, bd=5)
        login_window.geometry(log_window_size)
        login_window.title("login")
        login_window.lift() # 他のウィンドウより前面に固定
        
        if login_window:
            # 上のフレーム
            upper_frame = tk.Frame(login_window, bg=log_bg)
            upper_frame.pack(side=tk.TOP, padx=(0, 0), pady=(200, 0))
            # 開発者ネイむ要求
            name_label = tk.Label(upper_frame, text="開発者ネーム : ", font=(main_font, 20), bg=log_bg)
            name_label.pack(side=tk.LEFT, padx=(0, 20), pady=0)
            self.name_entry = tk.Entry(upper_frame, font=(main_font, 20))
            self.name_entry.pack(side=tk.LEFT, padx=(0, 0), pady=0)
            # 下のフレーム
            lower_frame = tk.Frame(login_window, bg=log_bg)
            lower_frame.pack(side=tk.TOP, padx=(0, 0), pady=(30, 0))
            # 開発者パスワード要求
            pas_label = tk.Label(lower_frame, text="開発者パスワード : ", font=(main_font, 20), bg=log_bg)
            pas_label.pack(side=tk.LEFT, padx=(0, 20), pady=0)
            self.pas_entry = tk.Entry(lower_frame, show="*", font=(main_font, 20))
            self.pas_entry.pack(side=tk.LEFT, padx=(0, 0), pady=0)
            
            login_button = tk.Button(login_window, text="ログイン", bg=log_btn_bg, font=(main_font, 20), command=self.login_log)
            login_button.pack(side=tk.TOP, padx=(0, 0), pady=(30, 0))
            
            global the_only_debugger_login
            if the_only_debugger_login == True:
                self.master.after(200, self.login_log())
            
            
    def login_log(self):
        global the_only_debugger_login
        name = None
        pas = None
        name = self.name_entry.get()
        pas = self.pas_entry.get()
        if the_only_debugger_login == True:
            name = debugger_name
            pas = debugger_pas
            
        # 名前かパスワードが入力されていなかった場合
        if not name or not pas:
            login_window.destroy()
            messagebox.showwarning("warning", "名前とパスワードを正しく入力して下さい")
            logger.log(100, f"loginError : {name} : {pas}")
            return 10
        elif name == debugger_name and pas == debugger_pas:
            login_window.destroy()
            the_only_debugger_login = True
            messagebox.showinfo("warning", "開発者としてログインしました。")
            logger.log(100, f"loginComplete : {name} : {pas}")
            if name and pas:
                # logウィンドウ
                log_window = tk.Toplevel(bg=log_bg, bd=5)
                log_window.geometry(log_window_size)
                log_window.title("log")
                log_window.lift() # 他のウィンドウより前面に固定
                # スライダーの値が変更されたとき
                def log_slider_changed(event):
                    global log_lebel
                    log_lebel = log_slider_value
                    return 0
                
                select_frame = tk.LabelFrame(log_window, text="log text disable", bg=log_bg, relief='groove', width=800, height=50)
                select_frame.pack(side=tk.TOP, fill="x", padx=(20, 20), pady=(30, 20))
                label = tk.Label(select_frame, text="ログレベルを設定：", bg=log_bg, font=(main_font, 14))
                label.pack(side=tk.LEFT, padx=(30, 10), pady=(10, 10))
                log_slider_value = tk.DoubleVar()
                global log_lebel
                log_slider_value.set(int(log_lebel)) # 初期値を設定
                log_slider = tk.Scale(select_frame, from_=0, to=100, bg=log_bg, variable=log_slider_value, font=("arial", 12), orient="horizontal")
                log_slider.pack(side=tk.LEFT, padx=(0, 0), pady=(10, 10)) 
                log_slider.bind("<Motion>", log_slider_changed)
                
                #LOGを閉じる
                def exit_log():
                    log_window.destroy()
                back_button = tk.Button(select_frame, text="LOGを閉じる", font=(main_font, 14), bg=log_btn_bg, command=exit_log)
                back_button.pack(side=tk.LEFT, padx=(50, 20), pady=(10, 10))
                
                log_frame = tk.Frame(log_window, bd=5, borderwidth=10, bg="#fffff3", relief="ridge")
                log_frame.pack(side=tk.TOP, padx=(20, 20), pady=(30, 20), fill="x", expand=True)
                # logテキストを表示するスクロールフレーム
                self.log_txt_fg = "#2f4f4f"
                self.log_txt_font = "overstrike"
                self.log_txt = scrolledtext.ScrolledText(
                    log_frame,
                    bg="#fff4ff", 
                    fg=self.log_txt_fg, 
                    font=(self.log_txt_font, 12, "underline"),
                    insertbackground="#191970", 
                    selectbackground="lightblue", 
                    selectforeground="red",
                    cursor='clock',
                    state="normal",
                    height=500, 
                    width=500)
                self.log_txt.pack(fill=tk.BOTH, expand=1)
                
                
                
                #logファイルから最新の文字列を取得する
                with open(log_file_path, "r") as log_f:
                    log_file_text:str = log_f.read()
                    
                self.log_txt.delete(1.0, tk.END) # 一度全ての文字を消去
                self.log_txt.insert(1.0, log_file_text)
                    
                
                
                
        elif name == debugger_name and pas != debugger_pas:
            login_window.destroy()
            messagebox.showerror("warning", "パスワードが正しくありません。")
            logger.log(100, f"loginError : {name} : {pas}")
            return 10
        else:
            login_window.destroy()
            messagebox.showerror("warning", "名前とパスワードが正しくありません。")
            logger.log(100, f"loginError : {name} : {pas}")
            return 10
            
            
    # このゲームについて説明
    def about_this_app(self):
        about_this_app_window = tk.Toplevel(bg=about_this_app_bg, bd=5)
        about_this_app_window.geometry(about_this_app_window_size)
        about_this_app_window.title("about this app")
        about_this_app_window.lift() # 他のウィンドウより前面に固定
        about_this_app_frame = tk.Frame(about_this_app_window, bg="#fffff3", bd=5, relief="ridge", borderwidth=5)
        about_this_app_frame.pack(side=tk.TOP, padx=(10, 10), pady=(40, 30), expand=True)
        
        text_1 = "己の短期記憶能力とイラストセンスを問う"
        text_2 = "全年齢対象ですよ～～"
        text_3 = "画面の動作が不安定になったり操作不能に\nなったときなどには右上の赤いXボタンを\n押して強制終了してください。"
        text_4 = "そんなもの存在しないですよ～～"
        text_color = "#800000"
        
        title_label = tk.Label(about_this_app_frame, text="     ~~~トリセツ~~~      ", bg="#fffff3", font=(main_font, 23));
        title_label.pack(side=tk.TOP, padx=(50, 50), pady=(20, 20))
        label = tk.Label(about_this_app_frame, text=" ・ゲームの目的", bg="#fffff3", font=(main_font, 18));
        label.pack(side=tk.TOP, padx=(50, 50), pady=(10, 5))
        text = tk.Label(about_this_app_frame, text=text_1, bg="#fffff3", fg=text_color, font=(main_font, 13))
        text.pack(side=tk.TOP, padx=(50, 50), pady=(0, 10))
        label = tk.Label(about_this_app_frame, text=" ・対象年齢", bg="#fffff3", font=(main_font, 18));
        label.pack(side=tk.TOP, padx=(50, 50), pady=(10, 5))
        text = tk.Label(about_this_app_frame, text=text_2, bg="#fffff3", fg=text_color, font=(main_font, 13))
        text.pack(side=tk.TOP, padx=(50, 50), pady=(0, 10))
        label = tk.Label(about_this_app_frame, text=" ・ゲームが不安定になったとき", bg="#fffff3", font=(main_font, 18));
        label.pack(side=tk.TOP, padx=(50, 50), pady=(10, 5))
        text = tk.Label(about_this_app_frame, text=text_3, bg="#fffff3", fg=text_color, font=(main_font, 13))
        text.pack(side=tk.TOP, padx=(50, 50), pady=(0, 10))
        label = tk.Label(about_this_app_frame, text=" ・ライセンス", bg="#fffff3", font=(main_font, 18));
        label.pack(side=tk.TOP, padx=(50, 50), pady=(10, 5))
        text = tk.Label(about_this_app_frame, text=text_4, bg="#fffff3", fg=text_color, font=(main_font, 13))
        text.pack(side=tk.TOP, padx=(50, 50), pady=(0, 10))

    # アプリケーション終了ボタンが日佐れたとき
    def exit_App(self):
        global forced_exit
        forced_exit = False
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


# tkinterメインウィンドウを作成
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
myapp.master.lift()
myapp.mainloop()
