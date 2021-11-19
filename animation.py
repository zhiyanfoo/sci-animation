from matplotlib import animation
import matplotlib.pyplot as plt

def animate(init_func, next_frame, fig):
    fps = 30
    interval = int(1/fps * 1000)
    anim = animation.FuncAnimation(fig, next_frame,
                                   init_func=init_func,
                                   frames=40 * 60,
                                   interval=interval,
                                   blit=True,
                                   save_count=400,
                                   )
    writervideo = animation.FFMpegWriter(fps=fps, bitrate=5000)
    anim.save("output4.mp4", writer=writervideo)
    # plt.show()
