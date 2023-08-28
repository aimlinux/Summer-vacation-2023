import tkinter as tk
root = tk.Tk()
root.geometry("500x300")
root.title('グラデーション')

x_place=0
color_changer=40

for i in range(25):
    c=str(224499+color_changer)
    tk.Frame(root,width=100,height=300,bg="#"+c).place(x=x_place,y=0)
    x_place=x_place+20
    color_changer=color_changer+200
label = tk.Label(root, text="テキストを置いてみる",bg="#226499",fg="white")
label.place(x=200, y=130)
root.mainloop()