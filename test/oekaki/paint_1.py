import tkinter as tk


# アプリケーション（GUI）クラス
class Application(tk.Frame):
    DEBUG_LOG = True
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

        self.create_widgets()
    
    
    def on_pressed(self, event):
        self.sx = event.x
        self.sy = event.y
        self.canvas.create_oval(self.sx, self.sy, self.event.x, self.event.y,
                                outline = self.color.get(),
                                width = self.width.get())
    
    

    def on_dragged(self, event):
        self.canvas.create_line(self.sx, self.sy, event.x, event.y,
                            fill = self.color.get(),
                            width = self.width.get())
        self.sx = event.x
        self.sy = event.y
        
        
    def click1(self,event):
        self.canvas.create_oval(self.sx-20,self.sy-20,self.sx+20,self.sy+20,
                            fill = self.color.get(),
                            width = self.width.get())

    def click2(self,event):
        self.canvas.create_oval(self.sx-40,self.sy-30,self.sx+40,self.sy+30,
                            fill = self.color.get(),
                            width = self.width.get())
        
    
    
    def create_widgets(self):
        # メインウィンドウ作成
        pw_main = tk.PanedWindow(self.master, bg="red", orient="vertical")
        pw_main.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        
        # メインフレーム作成
        fm_main = tk.Frame(pw_main, bd=5, bg="blue", relief="ridge", borderwidth=10)
        pw_main.add(fm_main)
        x = window_width - 30
        y = window_height - 20
        self.canvas = tk.Canvas(fm_main, bg="#fff", width=x, height=y)
        self.canvas.pack()
        
        COLORS = ["red", "white", "blue", "pink", "green","black"]
        self.color = tk.StringVar()                    
        self.color.set(COLORS[1])                             
        b = tk.OptionMenu(fm_main, self.color, *COLORS) 
        b.pack(side = tk.LEFT)
        
        self.width = tk.Scale(fm_main, from_ = 1, to = 10,
                            orient = tk.HORIZONTAL) 
        self.width.set(5)                                       
        self.width.pack(side = tk.LEFT)
        
        quit_button = tk.Button(fm_main, text = "終了",
                                command = self.master.quit)
        quit_button.pack(side = tk.RIGHT)
        
        self.canvas.bind("<ButtonPress-1>", self.on_pressed)
        self.canvas.bind("<B1-Motion>", self.on_dragged)
        self.canvas.bind("<ButtonPress-2>",self.click1)
        self.canvas.bind("<ButtonPress-3>",self.click2)



main_window = tk.Tk()        

# 画面の幅と高さを取得
screen_width = main_window.winfo_screenwidth()
screen_height = main_window.winfo_screenheight()

window_width = 1280
window_height = 800
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 3) - (window_height // 3)


myapp = Application(master=main_window)
myapp.master.title("paintApp")
myapp.master.geometry(f"{window_width}x{window_height}+{x}+{y}")
myapp.mainloop()
