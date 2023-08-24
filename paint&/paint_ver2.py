import tkinter as tk




main_bg = "#021049"


# アプリケーション（GUI）クラス
class Application(tk.Frame):
    DEBUG_LOG = True
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

        self.create_widgets()
    
    
    def create_widgets(self):
        
        global pw_main, fm_main
        
        #メインウィンドウ作成
        pw_main = tk.PanedWindow(self.master, bg=main_bg, orient="vertical")
        pw_main.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        #メインフレーム作成
        fm_main = tk.Frame(pw_main, bd=15, bg=main_bg, relief="ridge")
        pw_main.add(fm_main)



main_window = tk.Tk()        

#画面の幅と高さを取得
screen_width = main_window.winfo_screenwidth()
screen_height = main_window.winfo_screenheight()

window_width = 1200
window_height = 720
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 3) - (window_height // 3)


myapp = Application(master=main_window)
myapp.master.title("paintApp")
myapp.master.geometry(f"{window_width}x{window_height}+{x}+{y}")
myapp.mainloop()
