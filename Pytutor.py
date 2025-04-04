from tkinter import filedialog
from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox
import os

current_page = 0
courses_per_page = 12
lessons_per_page= 12
newWindow = None
displayWindow = None

# WINDOW NONE WINDOW NONE WINDOW NONE WINDOW NONE WINDOW NONE WINDOW NONE WINDOW NONE WINDOW NONE WINDOW NONE WINDOW NONE
connection = sqlite3.connect('Lesson_plans.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS Lesson_plans (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    lessons INTEGER NOT NULL
                )''')
cursor.execute('''CREATE TABLE IF NOT EXISTS Courses (
                    id INTEGER PRIMARY KEY,
                    course_id INTEGER,
                    lesson_name TEXT NOT NULL,
                    material TEXT NOT NULL,
                    FOREIGN KEY(course_id) REFERENCES Lesson_plans(id)
                )''')
connection.commit()

win = Tk()
win.geometry("630x400")
win.state("zoomed")
win.title("PyTutor")
win.configure(background="black")


def on_closing_new_window():
    global newWindow
    if newWindow is not None:
        newWindow.destroy()
        newWindow = None

def on_closing_display_window():
    global displayWindow
    if displayWindow is not None:
        displayWindow.destroy()
        displayWindow = None

# CLOSING WINDOW STUFF CLOSING WINDOW STUFF CLOSING WINDOW STUFF CLOSING WINDOW STUFF CLOSING WINDOW STUFF CLOSING WINDOW STUFF

def open_new_window():
    global newWindow

    if newWindow is not None:
        newWindow.focus()
        return
    newWindow = Toplevel(win)
    newWindow.title("New course")
    newWindow.geometry("400x400")
    newWindow.configure(background="black")

    text = StringVar()
    text.set("Name of courses Plan")
    entNewName = Entry(newWindow, relief=RIDGE, bd=5, textvariable=text)
    entNewName.pack(pady=5)

    text = StringVar()
    text.set("Number of lessons")
    entNumLessons = Entry(newWindow, relief=RIDGE, bd=5, textvariable=text)
    entNumLessons.pack(pady=5)

    def add_courses():
        courses_name = entNewName.get()
        lesson_amount = int(entNumLessons.get())
        cursor.execute("INSERT INTO Lesson_plans (name, lessons) VALUES (?, ?)", (courses_name, lesson_amount))
        course_id = cursor.lastrowid
        material=""

        for lesson in range(lesson_amount):
            lesson_name = f"Lesson {lesson+1}"
            cursor.execute("INSERT INTO Courses (course_id, lesson_name, material) VALUES (?, ?, ?)", (course_id, lesson_name, material))
        connection.commit()

        update_courses_list()
        on_closing_new_window()

    btA = Button(newWindow, text="Add", command=add_courses, width=10, relief=RAISED, bd=5)
    btA.pack(pady=5)

def add_lesson(course_id):
    update_lesson_list(course_id)
    print(course_id)

def display_lessons(course_id, course_name, courses):#xfcgvcftgvhvugytcryvbhuvgycftfvbuyvtcrvybunbvytcrvybbuytcrvybyuvtcr
    global current_page, lesson_frame
    current_page = 0
    frame.destroy()
    lesson_frame = Frame(win, background="red")
    lesson_frame.pack(pady=100)
    update_lesson_list(course_id)


def open_lesson(lesson):
    global displayWindow, btSave, btEdit
    lesson_id, course_id, lesson_name, material = lesson
    if displayWindow is not None:
        displayWindow.focus()
        return
    displayWindow = Toplevel(win)
    displayWindow.title(lesson_name)
    displayWindow.geometry("400x400")
    Label(displayWindow, text=f"{lesson_name}", font="impact").pack()

    Label(displayWindow, text="Material:", font="bold").pack()

    ent_Material = Text(displayWindow, width=30, height=5, relief=RIDGE, bd=10, )
    ent_Material.insert(END, material)
    ent_Material.config(state='disabled')
    ent_Material.pack(pady=5, padx=10, fill=BOTH, expand=True)

    def edit_lesson():
        global btSave
        ent_Material.config(state="normal")
        btEdit.destroy()
        btSave = Button(displayWindow, text="Save",command=save_lesson, width=10, relief=RAISED, bd=5)
        btSave.pack(pady=5,side=TOP)

    def save_lesson():
        global btEdit

        new_Material = ent_Material.get("1.0", END).strip()
        lesson_id, course_id, lesson_name, material = lesson
        cursor.execute("UPDATE Courses SET material =? WHERE id=?",(new_Material, lesson_id))
        connection.commit()

        ent_Material.config(state="disabled")
        btSave.destroy()
        btEdit = Button(displayWindow, text="Edit", command=edit_lesson, width=10, relief=RAISED, bd=5)
        btEdit.pack(pady=5, side=TOP)
        update_lesson_list(course_id)


    btEdit = Button(displayWindow, text="Edit",command=edit_lesson, width=10, relief=RAISED, bd=5)
    btEdit.pack(pady=5,side=TOP)

    btDelete = Button(displayWindow, text="Delete", width=10, relief=RAISED, bd=5)
    btDelete.pack(pady=5,side=BOTTOM)

    displayWindow.protocol()
    displayWindow.protocol("WM_DELETE_WINDOW", on_closing_display_window)
    displayWindow.minsize(width=400, height=400)

def update_lesson_list(course_id):
    global lesson_frame
    for widget in lesson_frame.winfo_children():
        widget.destroy()

    cursor.execute("SELECT * FROM Courses WHERE course_id = ?", (course_id,))
    lessons = cursor.fetchall()
    row_count = 0
    column_count = 0

    for lesson in lessons:
        lesson_id, course_id, lesson_name, material = lesson
        lesson_button = Button(lesson_frame, text=lesson_name, command=lambda l=lesson: open_lesson(l),width=30, padx=20, pady=20, font="Arial", relief=RAISED, bd=5)
        lesson_button.grid(row=row_count, column=column_count, padx=10, pady=10)
        column_count += 1
        if column_count == 3:
            column_count = 0
            row_count += 1
    btLA= Button(lesson_frame, text="Add Lesson", command=lambda c=course_id: add_lesson(c), width=30, padx=20, pady=20, font="Arial", relief=RAISED, bd=5)
    btLA.grid(row=row_count, column=column_count, padx=10, pady=10)

def update_courses_list(Lesson_plans=None):
    if Lesson_plans is None:
        cursor.execute("SELECT * FROM Lesson_plans LIMIT ? OFFSET ?",(courses_per_page, current_page * courses_per_page))
        Lesson_plans = cursor.fetchall()

    for widget in frame.winfo_children():
        widget.destroy()

    row_count = 0
    column_count = 0

    for lessons in Lesson_plans:
        lessons_id, lessons_name, _ = lessons
        course_button = Button(frame, text=lessons_name,command=lambda l=lessons: display_lessons(*l), width=30,padx=20, pady=20, font=20, relief=RAISED, bd=5)
        course_button.grid(row=row_count, column=column_count, padx=10, pady=10)
        column_count += 1
        if column_count == 3:
            column_count = 0
            row_count += 1

frame = Frame(win, background="black")
frame.pack(pady=100)

update_courses_list()
labelMain = Label(win, text="PYTUTOR", foreground="white", background="Black", font=("impact", 40))
labelMain.place(x=425, y=10)
btN = Button(win, text="NEW", height=2, width=6, command=open_new_window, relief=RAISED, bd=5, font="impact")
btN.place(x=0, y=1)

win.mainloop()
connection.close()
