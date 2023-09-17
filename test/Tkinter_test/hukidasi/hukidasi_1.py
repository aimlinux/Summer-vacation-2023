import tkinter as tk
from tkinter import ttk

def on_button_click():
    # ボタンがクリックされたときのアクションをここに追加
    pass

def animate_button(event):
    # ボタンにアニメーションを追加する関数
    def change_button_color(color):
        styled_button.configure(style=f'Animated.TButton.{color}Button.TButton')
    
    # アニメーションのフレーム間隔と回数
    frame_interval = 100  # ミリ秒
    animation_frames = 10
    
    # ボタンのアニメーション
    for i in range(animation_frames):
        color = 'active' if i % 2 == 0 else 'default'
        root.after(i * frame_interval, lambda c=color: change_button_color(c))
    root.after(animation_frames * frame_interval, lambda: change_button_color('default'))

# Tkinterウィンドウの設定
root = tk.Tk()
root.title("おしゃれなUIボタン")
root.geometry("400x400")

# ボタンのスタイルを設定
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 14))
style.configure("Animated.TButton.defaultButton.TButton", foreground="white", background="#4CAF50", padding=10)
style.configure("Animated.TButton.activeButton.TButton", foreground="white", background="#45a049", padding=10)

# ボタンの作成
styled_button = ttk.Button(root, text="クリックしてアニメーション", command=on_button_click, style="Animated.TButton.defaultButton.TButton")
styled_button.pack(pady=20)
styled_button.bind("<Enter>", animate_button)

# メインループの開始
root.mainloop()
