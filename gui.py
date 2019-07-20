import tkinter as tk

master = tk.Tk()

screen_width  = master.winfo_screenwidth()
screen_height = master.winfo_screenheight()

screen_ratio = 0.4

gui_width = int(screen_ratio*screen_width)
gui_height= int(screen_ratio*screen_height)
print(gui_width)
print(gui_height)

test_text_number = 0

master.title("Test GUI")
master.resizable(width= False, height=False)
master.geometry('{}x{}'.format(gui_width, gui_height))


left_frame = tk.Frame( master, background='white', height=gui_height, width=int(0.8*gui_width))
left_frame.pack(side='left')

right_frame = tk.Frame(master, background='gray', height=gui_height, width=int(0.2*gui_width))
right_frame.pack(side='right')

master.update()

canvas = tk.Canvas(left_frame, background='white', height=left_frame.winfo_height(), width=left_frame.winfo_width())
import numpy as np
for x in np.arange(0, 500, 150):
    for y in np.arange(0, 500, 150):
        canvas.create_text(x, y, text="({}, {}): number is {}".format(x,y, test_text_number))

canvas.pack()

def raise_number():
    global test_text_number
    test_text_number+=1

button = tk.Button( right_frame, text="Quit", command=master.destroy )
button.pack(side='top')
button2 = tk.Button( right_frame, text="Laugh", command=raise_number() )
button2.pack(side='top')

#canvas.pack()
master.mainloop()
