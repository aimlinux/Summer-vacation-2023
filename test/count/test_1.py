import tkinter as tk
from tkinter import messagebox

class CountdownWindow:
    def __init__(self, master, seconds):
        self.master = master
        self.seconds = seconds
        self.remaining = tk.IntVar()
        self.remaining.set(self.seconds)

        self.label = tk.Label(master, text="", font=("Helvetica", 48))
        self.label.pack()

        self.update_label()
        self.master.after(1000, self.update)

    def update_label(self):
        self.label.configure(text=f"Time left: {self.remaining.get()} seconds")

    def update(self):
        if self.remaining.get() > 0:
            self.remaining.set(self.remaining.get() - 1)
            self.update_label()
            self.master.after(1000, self.update)
        else:
            self.master.destroy()
            # ここにカウントダウン終了後のアクションを追加します
            messagebox.showinfo("カウントダウン終了", "カウントダウンが終了しました。")

# カウントダウンウィンドウを作成し、秒数を指定します（ここでは10秒）
root = tk.Tk()
countdown_window = CountdownWindow(root, seconds=10)

root.mainloop()





