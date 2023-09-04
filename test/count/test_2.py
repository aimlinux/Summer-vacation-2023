import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
import matplotlib.animation as animation
from IPython.display import HTML
plt.rcParams['font.family'] = 'sans-serif'

fig, ax = plt.subplots(figsize=(6,6))
ax.set_aspect('equal')
ax.axis('off')

tlist = np.linspace(10,0,11).repeat(10).astype(int).astype(str)
t1 = ax.text(0.5, 0.5, tlist[0], ha='center',va='center', transform=ax.transAxes,fontsize=120)

rot=np.linspace(0,360,10)
rot_tile = np.tile(rot, 11)

colors = np.random.rand(11,3)
c_rep = colors.repeat(10,axis=0)

def init():   
    return t1,

def update(num):
    t1.set_text(tlist[num])
    t1.set_color(c_rep[num,:]) 
    t1.set_rotation(rot_tile[num])
    return t1,

ani = animation.FuncAnimation(fig, update, init_func=init,interval = 100, frames = 110)
ani.save('cd_animation.mp4', writer="ffmpeg",dpi=100)
HTML(ani.to_html5_video())