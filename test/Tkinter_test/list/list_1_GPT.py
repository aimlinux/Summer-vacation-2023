import tkinter as tk
from tkinter import ttk

def update_buttons(event):
    selected_item = listbox.get(listbox.curselection())
    update_button_visibility(selected_item)

def update_button_visibility(selected_item):
    for button in button_list:
        button.grid_forget()
    if selected_item in button_dict:
        for row, button_row in enumerate(button_dict[selected_item]):
            for col, button in enumerate(button_row):
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

root = tk.Tk()
root.title("Stylish List and Buttons")

style = ttk.Style()
style.configure("Listbox", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 10))

listbox = tk.Listbox(root, selectbackground="lightblue")
listbox.grid(row=0, column=0, padx=10, pady=10, rowspan=3, sticky="ns")

listbox.insert(tk.END, "Item 1")
listbox.insert(tk.END, "Item 2")
listbox.insert(tk.END, "Item 3")

button_frame = tk.Frame(root)
button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

button_dict = {
    "Item 1": [
        [ttk.Button(button_frame, text=f"Button {row*5+col+1}") for col in range(5)] for row in range(2)
    ],
    "Item 2": [
        [ttk.Button(button_frame, text=f"Button {row*5+col+1}") for col in range(5)] for row in range(2)
    ],
    "Item 3": [
        [ttk.Button(button_frame, text=f"Button {row*5+col+1}") for col in range(5)] for row in range(2)
    ]
}
button_list = [button for button_row in button_dict.values() for row in button_row for button in row]

update_button_visibility("")

listbox.bind("<<ListboxSelect>>", update_buttons)

for row in range(2):
    button_frame.grid_rowconfigure(row, weight=1)
for col in range(5):
    button_frame.grid_columnconfigure(col, weight=1)

root.mainloop()