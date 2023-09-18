import tkinter as tk
from tkinter import ttk

def create_frame(parent_frame, text):
    frame = tk.Frame(parent_frame, relief="ridge", borderwidth=2)
    label = tk.Label(frame, text=text, padx=10, pady=5)
    label.pack(fill="both", expand=True)
    return frame

def on_select(event):
    global last_selected_index
    selected_item = listbox.curselection()
    if selected_item:
        index = selected_item[0]
        selected_text = listbox.get(index)
        
        # 前回の選択状態に関連するフレームを非表示にする
        if last_selected_index is not None:
            last_selected_text = listbox.get(last_selected_index)
            last_selected_frame = frame_dict.get(last_selected_text)
            if last_selected_frame:
                last_selected_frame.pack_forget()
        
        # 新しいリストに対応するフレームを表示
        frame = frame_dict.get(selected_text)
        if frame:
            frame.pack(fill="both", expand=True)
            label.config(text=f"Selected Item: {selected_text}")
        
        last_selected_index = index


root = tk.Tk()
root.title("List of Frames")

main_frame = ttk.Frame(root)
main_frame.pack(fill="both", expand=True)

listbox_frame = ttk.Frame(main_frame)
listbox_frame.pack(side="left", fill="y")

scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical")
listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)
listbox.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

frame_dict = {}  # リスト項目と対応するフレームの辞書
last_selected_index = None  # 前回選択されたリストのインデックス

for i in range(1, 21):
    item_text = f"Item {i}"
    listbox.insert(tk.END, item_text)
    frame = create_frame(main_frame, f"Frame for {item_text}")
    frame_dict[item_text] = frame  # 辞書に登録して対応付け
    frame.pack_forget()  # フレームを初めは非表示

listbox.bind("<<ListboxSelect>>", on_select)
label = ttk.Label(main_frame, text="Selected Item:")
label.pack()

root.mainloop()
