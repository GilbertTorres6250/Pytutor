from tkinter import filedialog
from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox
import os

newWindow = None

connection = sqlite3.connect('Lesson_plans.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS Lesson_plans (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    ingredients TEXT NOT NULL,
                    directions TEXT NOT NULL
                )''')
connection.commit()

win = Tk()
win.geometry("630x400")
win.state("zoomed")
win.title("TASTY & TIMELESS")
win.configure(background="black")

def on_closing_new_window():
    global newWindow
    if newWindow is not None:
        newWindow.destroy()
        newWindow = None

def openNewWindow():
    global newWindow

    def temp_text(e):
        entNewName.delete(0, "end")

    if newWindow is not None:
        newWindow.focus()
        return
    newWindow = Toplevel(win)
    newWindow.title("New Recipe")
    newWindow.geometry("400x400")
    newWindow.configure(background="black")

    text = StringVar()
    text.set("Name of Lesson Plan")
    entNewName = Entry(newWindow, relief=RIDGE, bd=5, textvariable=text)
    entNewName.pack(pady=5)
    entNewName.exclude_change = True
    entNewName.bind("<FocusIn>", temp_text)



btN = Button(win, text="NEW", height=2, width=6, command=openNewWindow,relief=RAISED, bd=5,font="impact")
btN.place(x=0, y=1)

win.resizable(0, 0)
win.mainloop()
connection.close()