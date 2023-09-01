import tkinter as tk
from tkinter import ttk
import time

# ウィンドウを作成
root = tk.Tk()
root.title("採点中....")
root.geometry("400x150")
root.configure(bg='#FF69B4')  # バックグラウンドカラーをピンクに設定

# フォントのカスタマイズ
font_style = ("Comic Sans MS", 36)  # かわいいフォントを指定
text_color = "white"
bg_color = "#FF69B4"  # 同じピンク色を背景に設定

# メッセージを表示
loading_label = ttk.Label(root, text="採点中....", font=font_style, foreground=text_color, background=bg_color)
loading_label.pack(pady=20)

# 点滅テキストを表示するラベル
blinking_label = ttk.Label(root, text="", font=font_style, foreground=text_color, background=bg_color)
blinking_label.pack(pady=10)

# 点滅テキストを更新する関数
def update_blinking_text():
    blinking_label.config(text="Please Wait...")
    root.update_idletasks()
    time.sleep(1)  # 1秒間表示
    blinking_label.config(text="")
    root.update_idletasks()
    time.sleep(1)  # 1秒間非表示
    update_blinking_text()

# ラベルの点滅を開始
update_blinking_text()

# ウィンドウを表示
root.mainloop()
