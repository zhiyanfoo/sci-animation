
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.image as mgimg

fig, ax = plt.subplots( figsize=(4,4))
plt.axis([0, 1000, 0, 1000])

fname='assets/balloon.png'
img = mgimg.imread(fname)
imobj = ax.imshow(img, zorder=100, extent=(0,200, 0, 200))

def animate(i):
    imobj.set_extent((i,200 +i , i, 200  +i))
    return imobj,
anim = animation.FuncAnimation(fig, animate, frames=100,  interval=40, repeat=False)
ax.set_aspect('equal')
plt.show()
