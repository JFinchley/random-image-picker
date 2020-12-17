# random-image-picker-v1.0

from tkinter import *
from PIL import ImageTk, Image

import os
import random


def next_image(event=None, jump=1):     # changes the image in imgPanel
    # check weather initiating by checking whether imgPanel.path exists
    if imgPanel.path:
        index = imgChoice.index(imgPanel.path) + jump
        if index >= len(imgChoice):     # to ensure that once the last image is reached it will start again
            index = index - len(imgChoice)
        elif index < 0:
            index = len(imgChoice) + index  # len() is last image
    else:
        index = 0
    path = imgChoice[index]
    # check image hasn't been deleted by user
    if imgChoice[index] in imgDel:
        jump = (abs(jump) + 1) / (abs(jump) / jump)  # ensures that jump stays positive/negative
        next_image(jump=int(jump))
    else:
        try:
            new = Image.open(path)
            new = resize_image(new)
            new = ImageTk.PhotoImage(new)
            imgPanel.config(image=new)
            imgPanel.image = new
            imgPanel.path = path
            print(str(index) + ".\t" + path)
            window.focus_force()
        except IOError:
            imgPanel.path = path    # else when skipping for first image subsequent next_image assumes index still zero
            imgDel.append(path)     # ensure the faulty image doesn't get displayed again
            print(str(index) + ".\t" + path + "\n\t is unavailable (IOError), skipping image.")
            next_image()


def close(event=None):
    window.destroy()


def open_image(event=None):   # using default image viewer
    close()
    opn = Image.open(imgPanel.path).show()


def last_image(event=None, index=None):
    next_image(jump=-1)


def delete_image(event=None):
    path = imgPanel.path
    os.remove(path)
    imgDel.append(path)
    print(str(imgChoice.index(path)) + ".\t" + path + " now deleted.")
    next_image()


def resize_image(imgname):  # scales image to be under the height of the window, assumes landscape display
    window.update()  # allows window.winfo_width/height to work
    widthratio = imgname.width / window.winfo_width()
    heightratio = imgname.height / window.winfo_height()
    if widthratio >= heightratio and widthratio > 1:
        size = (window.winfo_width(), int(imgname.height / widthratio))
    elif heightratio > widthratio and heightratio > 1:
        size = (int(imgname.width / heightratio), window.winfo_height())
    else:
        size = (imgname.width, imgname.height)
    return imgname.resize(size, resample=Image.ANTIALIAS)


# lists all jpg files from which a random choice can be made
imgDel = []
imgChoice = []
# r=root, d=directories, f = files
for r, d, f in os.walk(os.getcwd()):
    for file in f:    # ^ top level directory, will includes sub-folders, os.getcwd() for running in place
        if '.jpg' in file:
            imgChoice.append(os.path.join(r, file).replace("\\", "/"))
random.shuffle(imgChoice)

# main window of an application
window = Tk()
window.title("Image selector")
window.state('zoomed')  # for maximised window
window.configure(background='grey')

# pack or place panels and buttons
imgPanel = Label(window, image=None)
imgPanel.path = None    # path attribute doesn't like being added in the module
imgPanel.pack(side="bottom", fill="both", expand="yes")
next_image()  # for the first random image
opnButton = Button(window, text="Open image (Up/Enter)", width=20, command=open_image).place(x=5, y=5)
nxtButton = Button(window, text="Next image (Right)", width=20, command=next_image).place(x=5, y=32)
prvButton = Button(window, text="Last image (Left)", width=20, command=last_image).place(x=5, y=59)
delButton = Button(window, text="Delete image (Del)", width=20, command=delete_image).place(x=5, y=86)
window.bind("<Return>", open_image)
window.bind("<Up>", open_image)
window.bind("<Right>", next_image)
window.bind("<Left>", last_image)
window.bind("<Delete>", delete_image)
window.bind("<Escape>", close)

# starts the GUI
window.mainloop()
