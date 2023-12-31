import tkinter as tk
from tkinter import messagebox
import math

class CountdownWindow:
    def __init__(self, master, seconds):
        self.master = master
        self.seconds = seconds
        self.remaining = tk.IntVar()
        self.remaining.set(self.seconds)

        self.canvas = tk.Canvas(master, width=200, height=200, bg="white")
        self.canvas.pack()

        self.label = tk.Label(self.canvas, text="", font=("Helvetica", 48))
        self.label.pack()

        self.marker_angle = 0  # マークの初期角度
        self.update_label()
        self.update_marker()
        self.update()  # アニメーションを開始

    def update_label(self):
        self.label.configure(text=f"Time left: {self.remaining.get()} seconds")

    def update_marker(self):
        self.canvas.delete("marker")  # 以前のマークを削除
        cx, cy = 100, 100  # キャンバスの中央座標
        radius = 70  # マークの半径
        marker_x = cx + radius * math.cos(math.radians(self.marker_angle))
        marker_y = cy + radius * math.sin(math.radians(self.marker_angle))
        self.canvas.create_oval(marker_x - 5, marker_y - 5, marker_x + 5, marker_y + 5, fill="red", tags="marker")

    def update(self):
        if self.remaining.get() > 0:
            self.remaining.set(self.remaining.get() - 1)
            self.update_label()
            self.update_marker()
            self.marker_angle += 6  # 6度ずつ回転
            self.canvas.after(1000, self.update)  # 1秒後に再度更新
        else:
            self.master.destroy()
            # ここにカウントダウン終了後のアクションを追加します
            messagebox.showinfo("カウントダウン終了", "カウントダウンが終了しました。")

# カウントダウンウィンドウを作成し、秒数を指定します（ここでは10秒）
root = tk.Tk()
countdown_window = CountdownWindow(root, seconds=10)

root.mainloop()
