import tkinter as tk
from tkinter import filedialog
from tkinter import StringVar
import glob
import pyautogui
import pytesseract
from pytesseract import Output
import cv2
import tesserocr
from PIL import Image
from tesserocr import PyTessBaseAPI, RIL
import cv2
import pytesseract
from pytesseract import Output
import numpy as np 

pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'

def open_file():
    """Открываем файл для редактирования"""
    filepath = askopenfilename(
        filetypes=[("Python file", "*.py")]
    )
    if not filepath:
        return
   # with open(filepath, "r") as input_file:
 #       text = input_file.read()
#        txt_edit.insert(tk.END, text)

def browse_button():
    global folder_path
    global filesList
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    browseButton.configure(text = folder_path.get())
    print(folder_path.get())
    filesList.set(glob.glob(folder_path.get() + "/*.py"))
    print(glob.glob(folder_path.get() + "/*.py"))

def moveToWord():
    img = pyautogui.screenshot()
    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    n_boxes = len(d['level'])
    imgW, imgH = img.size
    screenW, screenH = pyautogui.size()
    widthCoef = screenW / imgW
    heightCoef = screenH / imgH
    for i in range(n_boxes):
        if int(d['conf'][i]) > 60:
#            print(d['text'][i])
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            img = cv2.rectangle(np.array(img), (x, y), (x + w, y + h), (0, 255, 0), 2)
            if d['text'][i] == "Stop":
                print(x * widthCoef, y * heightCoef)
                moveMouse(x * widthCoef, y * heightCoef)

    #cv2.imshow('img', img)
    #cv2.waitKey(0)

def moveMouse(x, y):
    """
    Move mouse to coordinates
    """
    print(x, y)
    pyautogui.moveTo(x, y)

def start():
    """
    start
    """
    for path in glob.glob(folder_path.get() + "/*.py"):
        #print(path)
        file1 = open(path, 'r') 
        lines = file1.readlines() 
        count = 0
        for line in lines: 
            print("Line{}: {}".format(count, line.strip())) 

window = tk.Tk()
filesList = StringVar()
filesList.set("No files")
folder_path = StringVar()
folder_path.set("Choose the folder with tests")

browseButton = tk.Button(text=folder_path.get(), width=55, height=5, bg="blue", fg="green", command=browse_button)
startButton = tk.Button(text="Start", width=5, height=2, bg="blue", fg="red", command=start)
stopButton = tk.Button(text="Stop",width=5,height=2,bg="blue",fg="red", command=browse_button)

myframe = tk.Frame(window)
myentry = tk.Entry(myframe, textvariable = filesList, state='readonly')
myscroll = tk.Scrollbar(myframe, orient = 'horizontal', command=myentry.xview)
myentry.config(xscrollcommand=myscroll.set)
myframe.grid()
myentry.grid(row=1, sticky='ew')
myscroll.grid(row=2, sticky='ew')

browseButton.grid(row=3, sticky='ew')
startButton.grid(row=4, sticky='ew')
stopButton.grid(row=5, sticky='ew')
window.mainloop()
