import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def update_buttons(event):
    selected_item = listbox.get(listbox.curselection())
    update_button_visibility(selected_item)

def update_button_visibility(selected_item):
    # ボタンフレーム内のウィジェットを全て削除
    for widget in button_frame.winfo_children():
        widget.destroy()
    
    if selected_item in button_dict:
        for row, button_row in enumerate(button_dict[selected_item]):
            for col, button in enumerate(button_row):
                button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

def button_click(button_number):
    print(f"Button {button_number} clicked!")

root = tk.Tk()
root.title("Stylish List and Buttons")
root.geometry("1280x800")  # ウィンドウサイズを設定

pw_main = tk.Frame(root, bg="#197190", bd=5, relief="ridge", borderwidth=10)
pw_main.pack(side="left", fill="both", expand=True)

style = ttk.Style()
style.configure("Listbox", font=("Helvetica", 16))  # リストのフォントサイズを大きく
style.configure("TButton", font=("Helvetica", 16))  # ボタンのフォントサイズを大きく

# ラベルを追加
label = tk.Label(pw_main, text="お手本にするイラストを選択してください", font=("Helvetica", 30), padx=70, pady=55)
label.pack(fill="both")

listbox = tk.Listbox(pw_main, selectbackground="lightblue", font=("Helvetica", 25), height=5)  # リストの高さを調整
listbox.pack(fill="both", expand=True)

item_1 = "動物"
item_2 = "植物"
item_3 = "その他"


button_list_1 = ["馬", "牛", "サル", "a", "3", "s", "e", "as", "ds", "sdgds", "馬", "牛", "サ", "a", "3", "s", "e", "as", "ds", "sdgds", "馬", "牛", "ル", "a", "3", "s", "e", "as", "ds", "sdgds"]


listbox.insert(tk.END, item_1)
listbox.insert(tk.END, item_2)
listbox.insert(tk.END, item_3)

listbox.select_set(0)  # 最初のアイテムを選択状態にする

button_frame = tk.Frame(root, bg="white")  # ボタンフレームを作成
button_frame.pack(side="left", fill="both", expand=True)

button_dict = {
    item_1: [
        [ttk.Button(button_frame, text=f"{button_list_1[row*5+col+1-1]}", command=lambda num=row*5+col+1: button_click(num)) for col in range(5)] for row in range(2)
    ],
    item_2: [
        [ttk.Button(button_frame, text=f"{button_list_1[row*5+col+1-1]}", command=lambda num=row*5+col+1: button_click(num)) for col in range(10, 15)] for row in range(2)
    ],
    item_3: [
        [ttk.Button(button_frame, text=f"{button_list_1[row*5+col+1-1]}", command=lambda num=row*5+col+1: button_click(num)) for col in range(20, 25)] for row in range(2)
    ]
}

update_button_visibility("")

listbox.bind("<<ListboxSelect>>", update_buttons)

root.mainloop()
