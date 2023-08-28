import tkinter as tk

def update_list_selection(event):
    selected_index = listbox.curselection()
    if selected_index:
        selected_item = listbox.get(selected_index[0])
        selected_label.config(text=f"Selected: {selected_item}")

root = tk.Tk()
root.title("Interactive Listbox")

# 左側のリストボックス
listbox_frame = tk.Frame(root, bg="lightgray")
listbox_frame.pack(side=tk.LEFT, fill=tk.Y)

listbox_label = tk.Label(listbox_frame, text="Options", font=("Helvetica", 16), bg="lightgray")
listbox_label.pack(side=tk.TOP, anchor=tk.W)

listbox = tk.Listbox(listbox_frame, font=("Helvetica", 12), selectbackground="gray")
options = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5", "Option 6", "Option 7", "Option 8", "Option 9", "Option 10"]
for option in options:
    listbox.insert(tk.END, option)
listbox.pack(side=tk.TOP, fill=tk.BOTH)
listbox.bind("<<ListboxSelect>>", update_list_selection)

# 右側のボタン
button_frame = tk.Frame(root, bg="white")
button_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

selected_label = tk.Label(button_frame, text="Selected:", font=("Helvetica", 14), bg="white")
selected_label.pack(side=tk.TOP, anchor=tk.W, padx=20, pady=10)

button_row_count = 2
button_col_count = 5
buttons = []
for i in range(button_row_count):
    row = []
    for j in range(button_col_count):
        button = tk.Button(button_frame, text=f"Button {i * button_col_count + j + 1}", font=("Helvetica", 12))
        button.pack(side=tk.LEFT, padx=10, pady=10)
        row.append(button)
    buttons.append(row)

root.mainloop()