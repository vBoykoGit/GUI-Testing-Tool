import tkinter as tk
from tkinter import filedialog
from tkinter import StringVar
import glob

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
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    broseButton.configure(text = folder_path.get())
    print(folder_path.get())
    print(glob.glob(folder_path.get() + "/*.py"))

window = tk.Tk()
folder_path = StringVar()
folder_path.set("Choose the folder with tests")

broseButton = tk.Button(
    text=folder_path.get(),
    width=55,
    height=5,
    bg="blue",
    fg="green",
    command=browse_button
)
startButton = tk.Button(
    text="Start",
    width=5,
    height=2,
    bg="blue",
    fg="red",
    command=browse_button
)

stopButton = tk.Button(
    text="Stop",
    width=5,
    height=2,
    bg="blue",
    fg="red",
    command=browse_button
)

broseButton.pack()
startButton.pack()
stopButton.pack()
window.mainloop()
