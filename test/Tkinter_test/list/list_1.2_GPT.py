import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk



def update_buttons(event):
    selected_item = listbox.get(listbox.curselection())
    update_button_visibility(selected_item)

def update_button_visibility(selected_item):
    for button in button_list:
        button.grid_forget()
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
pw_main.grid(row=0, column=0, sticky="nsew")


style = ttk.Style()
style.configure("Listbox", font=("Helvetica", 16))  # リストのフォントサイズを大きく
style.configure("TButton", font=("Helvetica", 16))  # ボタンのフォントサイズを大きく

# ラベルを追加
label = tk.Label(pw_main, text="お手本にするイラストを選択してください", font=("Helvetica", 30), padx=70, pady=55)
label.grid(row=1, column=0, columnspan=2, sticky="nsew")

listbox = tk.Listbox(pw_main, selectbackground="lightblue", font=("Helvetica", 25), height=5)  # リストの高さを調整
listbox.grid(row=2, column=0, padx=20, pady=20, rowspan=3, sticky="ns")

item_1 = "動物"
item_2 = "植物"
item_3 = "その他"

button_list_1 = ["馬", "牛", "サル", "a", "3", "s", "e", "as", "ds", "sdgds", "馬", "牛", "サ", "a", "3", "s", "e", "as", "ds", "sdgds", "馬", "牛", "ル", "a", "3", "s", "e", "as", "ds", "sdgds"]


listbox.insert(tk.END, item_1)
listbox.insert(tk.END, item_2)
listbox.insert(tk.END, item_3)

listbox.select_set(0)  # 最初のアイテムを選択状態にする
#listbox.event_generate("<<ListboxSelect>>")  # 選択イベントを発生させて更新


button_frame = tk.Frame(pw_main, width=100)
button_frame.grid(row=2, column=1, padx=20, pady=20, sticky="nsew")

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
button_list = [button for button_row in button_dict.values() for row in button_row for button in row]

update_button_visibility("")

listbox.bind("<<ListboxSelect>>", update_buttons)

for row in range(2):
    button_frame.grid_rowconfigure(row, weight=1)
for col in range(5):
    button_frame.grid_columnconfigure(col, weight=1)





root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

update_buttons(None)  # 初期選択アイテムに対するボタンを表示

root.mainloop()