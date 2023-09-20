import tkinter as tk

def on_mousewheel(event):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")

root = tk.Tk()
root.title("Vertical Scrolling Frame Example")

# 垂直スクロールバーを作成
scrollbar = tk.Scrollbar(root, orient="vertical")
scrollbar.pack(side="right", fill="y")

# スクロール可能なキャンバスを作成
canvas = tk.Canvas(root, yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)

# スクロールバーとキャンバスを連動
scrollbar.config(command=canvas.yview)

# フレームをキャンバス上に配置
frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

# フレームにウィジェットを追加
for i in range(50):
    label = tk.Label(frame, text=f"Label {i+1}", padx=20, pady=10)
    label.pack()

# マウスホイールでスクロールできるように設定
canvas.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.bind_all("<MouseWheel>", on_mousewheel)

root.mainloop()
