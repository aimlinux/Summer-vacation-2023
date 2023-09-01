import tkinter as tk
from tkinter import ttk
import time

# メインウィンドウを作成
root = tk.Tk()
root.title("採点中....")
root.geometry("400x150")  # ウィンドウサイズを調整

# 背景色を設定
root.configure(bg='black')

# メッセージを表示
loading_label = ttk.Label(root, text="採点中....", font=("Helvetica", 24), foreground="white", background="black")
loading_label.pack(pady=20)

# プログレスバーを表示
style = ttk.Style()
style.configure("TProgressbar", thickness=20, troughcolor="lightgray", background="blue")
progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="indeterminate", style="TProgressbar")
progress.pack()

# プログレスバーをアニメーションさせる関数
def animate_progressbar():
    progress.start()
    root.after(100, animate_progressbar)

# アニメーションを開始
animate_progressbar()

# ウィンドウを表示
root.mainloop()
