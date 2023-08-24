import tkinter as tk
from tkinter import font, colorchooser

def create_widgets(self):
    
    self.canvas.bind("", self.paint)
    self.canvas.bind("", self.reset)
    
def paint(self, event):
    if self.old_x and self.old_y:
        # create_line(始点のx座標,始点のy座標,終点のx座標,終点のy座標,線の太さなどのオプションを指定)
        self.canvas.create_line(self.old_x, self.old_y, event.x, event.y, width=5.0, fill=self.paint_color, capstyle=tk.ROUND)
        self.old_x = event.x
        self.old_y = event.y
        

def reset(self, event):
    self.old_x, self.old_y = None, None
    
    
def change_mode(self):
    #「ペン」ボタンが押されたとき
    if self.write_button['state'] == tk.NORMAL:
        # 各ボタンの状態を変更
        self.write_button['state'] = tk.DISABLED
        self.color_button['state'] = tk.NORMAL
        self.erase_button['state'] = tk.NORMAL
        #初期値もしくは、ユーザーが選択した色にする
        self.paint_color = self.color[1] 
    #「消しゴム」ボタンが押されたとき
    else:
        # 各ボタンの状態を変更
        self.write_button['state'] = tk.NORMAL
        self.color_button['state'] = tk.DISABLED
        self.erase_button['state'] = tk.DISABLED
        #線の色を白色にする
        self.paint_color = '#FFFFFF'
        
def color_change(self):
    # colorchooserの返り値を変数に格納
    self.color = tk.colorchooser.askcolor() 

    # 返り値のカラーコードをペンの色に設定
    self.paint_color = self.color[1]