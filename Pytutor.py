from tkinter import filedialog
from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox
import os

current_page = 0
courses_per_page = 12
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

def openNewWindow():
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
        lesson_amount = int(entNumLessons.get())  # Convert to int for adding lessons
        cursor.execute("INSERT INTO Lesson_plans (name, lessons) VALUES (?, ?)", (courses_name, lesson_amount))
        course_id = cursor.lastrowid  # Get the ID of the newly inserted course

        # Add lessons based on the number entered
        for i in range(lesson_amount):
            lesson_name = f"Lesson {i+1}"  # Example lesson name (you can modify this logic)
            cursor.execute("INSERT INTO Courses (course_id, lesson_name) VALUES (?, ?)", (course_id, lesson_name))
        connection.commit()

        update_courses_list()
        on_closing_new_window()

    btA = Button(newWindow, text="Add", command=add_courses, width=10, relief=RAISED, bd=5)
    btA.pack(pady=5)


def display_lessons(course_id, course_name, courses):
    cursor.execute("SELECT * FROM Courses WHERE course_id = ?", (course_id,))
    lessons = cursor.fetchall()
    frame.destroy()
    lesson_frame = Frame(win, background="red")
    lesson_frame.pack(pady=100)

    row_count = 0
    column_count = 0

    for lesson in lessons:
        lesson_id, _, lesson_name = lesson
        lesson_button = Button(lesson_frame, text=lesson_name, command=lambda lesson=lesson: display_lesson_detail(lesson), width=30, padx=20, pady=20, font="Arial", relief=RAISED, bd=5)
        lesson_button.grid(row=row_count, column=column_count, padx=10, pady=10)
        column_count += 1
        if column_count == 3:
            column_count = 0
            row_count += 1


def display_lesson_detail(lesson):
    lesson_id, course_id, lesson_name = lesson
    # Here you can implement the functionality to display the details of the lesson
    print(f"Displaying details for {lesson_name} (Lesson ID: {lesson_id})")


def update_courses_list(Lesson_plans=None):
    if Lesson_plans is None:
        cursor.execute("SELECT * FROM Lesson_plans LIMIT ? OFFSET ?",
                       (courses_per_page, current_page * courses_per_page))
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
labelMain = Label(win, text="TIMELESS RECIPES", foreground="white", background="Black", font=("impact", 40))
labelMain.place(x=425, y=10)
btN = Button(win, text="NEW", height=2, width=6, command=openNewWindow, relief=RAISED, bd=5, font="impact")
btN.place(x=0, y=1)

win.mainloop()

connection.close()
