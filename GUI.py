from tkinter import *
from PIL import ImageTk, Image
import os
import numpy as np
from resizeimage import resizeimage
import MatrixMult
import AiFitEvo

def addLine(entryTextBox):
    entryTextBox.delete(0, END)
    entryTextBox.insert(0, "This is a test.")
    #entryTextBox.get <-- get current text

def getPicture(textBox, entryTextBox):
    global img
    print(entryTextBox.get())
    if os.path.isfile(entryTextBox.get()):
        img = Image.open(entryTextBox.get())
        DisplayImage(img)

def makeRandomImage():
    global img
    print("makeRandomImage starting...")
    img = Image.new("RGB", (canvasImage.width(), canvasImage.height()), "white")
    vals = list(img.getdata())
    newVals = []
    for pixel in vals:
        newVals.append( (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256)) )
    img.putdata(newVals)
    #DisplayImage(img)
    print("makeRandomImage Done!")
    return img


def resizeImage(event):
    global img
    w,h = event.width-50, event.height-50
    if (img.size[0] < w):
        w = img.size[0]
    if (img.size[1] < h):
       h = img.size[1]
    print("w:",w,"/",img.size[0],"\th:",h,"/",img.size[1])
    DisplayImage(resizeimage.resize_cover(img, [w,h], validate=True))

def DisplayImage(NewImage):
    #print("DisplayImage starting...")
    global canvasImage
    if NewImage is not NONE:
        canvasImage = ImageTk.PhotoImage(NewImage)
        panel.create_image(20, 20, anchor=NW, image=canvasImage)
        panel.update()
        #textBox.configure(image=canvasImage)
        #textBox.image = NewImage
    else:
        panel.update()
    #print("DisplayImage Done!!!")

def CompareImages(A, B):
    temp = MatrixMult.MatrixDifferenceNumpy(A, B)
    print(temp)

global canvasImage
global img
global panel
global root
root = Tk()
#title = Label(root, text="Hello World!")
#title.pack()
topFrame = Frame(root)
botFrame = Frame(root)

#CTRL+/ to block comment
#CTRL+SHIFT+/ To un-block-comment
#canvasImage = ImageTk.PhotoImage(Image.new("RGB", (100, 100), "white"))
img = Image.open("D:\Adam\Pictures\kity.jpg")
canvasImage = ImageTk.PhotoImage(img)
var = IntVar()
c = Checkbutton(root, text="Check me out!", variable=var)
filePathTextLine = Entry(root)
panel = Canvas(root, width=canvasImage.width(), height=canvasImage.height(), relief="ridge")
panel.create_image(20, 20, anchor=NW, image=canvasImage)
panel.bind('<Configure>', resizeImage)
Button1 = Button(root, text='Get Picture', fg='red', command= lambda: getPicture(panel, filePathTextLine))
Button2 = Button(root, text='Compare Images', fg='green', command= lambda: CompareImages(img,makeRandomImage()))
Button3 = Button(root, text='AiFitEvo', fg='blue', command= lambda: AiFitEvo.GetFitPic(img, img.size[0], img.size[1], DisplayImage))

panel.pack(fill=BOTH, expand=TRUE)
Button1.pack(side=LEFT)
Button2.pack(side=LEFT)
Button3.pack(side=LEFT)
c.pack(side=BOTTOM)
filePathTextLine.pack(side=BOTTOM, fill=BOTH)
root.mainloop()