import tkinter as tk
from tkinter import filedialog
from tkinter import StringVar
import glob
import pyautogui
import pytesseract
from pytesseract import Output
import cv2
from PIL import Image
import cv2
import pytesseract
from pytesseract import Output
import numpy as np
import time

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
#pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'

# UI


def open_file():
    """Открываем файл для редактирования"""
    filepath = askopenfilename(filetypes=[("Python file", "*.py")])
    if not filepath:
        return


def browse_button():
    global folder_path
    global filesList
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    browseButton.configure(text=folder_path.get())
    print(folder_path.get())
    filesList.set(glob.glob(folder_path.get() + "/*.py"))
    print(glob.glob(folder_path.get() + "/*.py"))


def start():
    """
    start
    """
    for path in glob.glob(folder_path.get() + "/*.py"):
        # print(path)
        file1 = open(path, 'r')
        lines = file1.readlines()
        count = 0
        for line in lines:
            print("Line{}: {}".format(count, line.strip()))
            exec(line, {'moveToWord': moveToWord,
                        'clickAtWord': clickAtWord, 'typeString': typeString})


def stop():
    """
    stop
    """
    print("stopped")

# Recognition


def moveToWord(word):
    (x, y) = getScreenWordCoordinates(word)
    moveMouse(x, y)


def clickAtWord(word):
    (x, y) = getScreenWordCoordinates(word)
    mouseClick(x, y)


def getScreenWordCoordinates(word):
    img = pyautogui.screenshot()
    imageData = pytesseract.image_to_data(img, output_type=Output.DICT)
    print(imageData)
    imgW, imgH = img.size
    screenW, screenH = pyautogui.size()
    widthCoef = screenW / imgW
    heightCoef = screenH / imgH
    filteredWordNums = imageData['word_num']
    filteredWords = imageData['text']
    wordsArray = word.split(' ')
    wordsDict = dict((w, False) for w in wordsArray)
    for i in range(len(filteredWordNums)):
        if (filteredWordNums[i] - 1 < len(wordsArray)) and (wordsArray[filteredWordNums[i] - 1] == filteredWords[i]):
            wordsDict[filteredWords[i]] = True
        else:
            print(wordsDict)
            isAllTrue = all(k == True for k in wordsDict.values())
            print(isAllTrue)
            if isAllTrue:
                (x, y, w, h) = (imageData['left'][i-1], imageData['top']
                                [i-1], imageData['width'][i-1], imageData['height'][i-1])
                print(x * widthCoef, y * heightCoef)
                #img = cv2.rectangle(np.array(img), (x, y), (x + w, y + h), (0, 255, 0), 2)
                #cv2.imshow('img', img)
                # cv2.waitKey(0)
                mouseClick(x * widthCoef, y * heightCoef)
                break
            else:
                for key in wordsDict:
                    wordsDict[key] = False

# User actions


def moveMouse(x, y):
    """
    Move mouse to coordinates
    """
    print(x, y)
    pyautogui.moveTo(x, y, 0.3)


def mouseClick(x, y):
    """
    Click mouse to coordinates
    """
    print(x, y)
    pyautogui.moveTo(x, y, 0.3)
    pyautogui.click(x=x, y=y)


def typeString(string, interval=0.25):
    """
    typeString
    """
    pyautogui.write(string, interval=interval)


# Main
window = tk.Tk()
filesList = StringVar()
filesList.set("No files")
folder_path = StringVar()
folder_path.set("Choose the folder with tests")

browseButton = tk.Button(text=folder_path.get(), width=55,
                         height=5, bg="blue", fg="green", command=browse_button)
startButton = tk.Button(text="Start", width=5, height=2,
                        bg="blue", fg="red", command=start)
stopButton = tk.Button(text="Stop", width=5, height=2,
                       bg="blue", fg="red", command=stop)

myframe = tk.Frame(window)
myentry = tk.Entry(myframe, textvariable=filesList, state='readonly')
myscroll = tk.Scrollbar(myframe, orient='horizontal', command=myentry.xview)
myentry.config(xscrollcommand=myscroll.set)
myframe.grid()
myentry.grid(row=1, sticky='ew')
myscroll.grid(row=2, sticky='ew')

browseButton.grid(row=3, sticky='ew')
startButton.grid(row=4, sticky='ew')
stopButton.grid(row=5, sticky='ew')
window.mainloop()
