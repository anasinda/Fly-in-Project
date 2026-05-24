import matplotlib.pyplot as plt

# matplotlib is a huge library with many modules. pyplot is the specific module
# inside it that provides a simple interface for creating and managing figures and plots.

fig, ax = plt.subplots() # fig == figure == canvas we draw on --- ax == plot == visual representation of data on a graph

ax.plot([0, 1], [0, 1]) #draws a line from one zone to the next
ax.scatter([0, 5], [0, 5]) # draws a dot on the connected line from one zone to the other
ax.text(x, y, name, ha='', va='') # create text, put it in cordinates x & y, ha and va change it's position around that cordinate
plt.show() # show the visual representation of what you made

def on_key(event):
    if event.key == 'right':
        pass

fig.canvas.mpl_connect('key_press_event', on_key) # listen to event, when event happens, pass the event object to the function obj as argument and call it
ax.cla() # clear drawing area
fig.canvas.draw() #redraw everything

fig.canvas.mpl_connect('key_press_event', on_key) # ok so when we do plt.show(), the system creates a window using it's gui with whatever we drawn, and the
                                                 # gui's backend service starts a while loop that ends whenever we close the window, in the while loop we
                                                 # listen for events, if an event happens it capture its, and see which method is called the moment that
                                                 # specific event happens so it can send it, and then depending on the method, we do whatever we want with the object data
