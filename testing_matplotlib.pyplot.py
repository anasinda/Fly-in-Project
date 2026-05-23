import matplotlib.pyplot as plt

# matplotlib is a huge library with many modules. pyplot is the specific module
# inside it that provides a simple interface for creating and managing figures and plots.

fig, ax = plt.subplots()

ax.plot([0, 1], [0, 1]) #draws a line from one zone to the next
ax.scatter([0, 5], [0, 5]) # draws a dot on the connected line from one zone to the other

plt.show() # show the visual representation of what you made

def on_key(event):
    if event.key == 'right':
        pass

fig.canvas.mpl_connect('key_press_event', on_key) # listen to event, when event happens, pass the event object to the function obj as argument and call it
ax.cla() # clear drawing area
fig.canvas.draw() #redraw everything
