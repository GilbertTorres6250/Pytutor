from tkinter import *
from tkinter import ttk
import sqlite3

current_page = 0
courses_per_page = 12
lessons_per_page= 12
displayWindow = None
quizWindow = None
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
                    type TEXT DEFAULT 'lesson',
                    FOREIGN KEY(course_id) REFERENCES Lesson_plans(id)
                )''')
cursor.execute('''CREATE TABLE IF NOT EXISTS Quizes (
                    id INTEGER PRIMARY KEY,
                    lesson_id INTEGER,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    correct INTEGER NOT NULL,
                    FOREIGN KEY(lesson_id) REFERENCES Courses(id)
                )''')
connection.commit()

win = Tk()
win.state("zoomed")
win.geometry("630x400")
win.title("PyTutor")
win.configure(background="black")
screen_wide= win.winfo_screenwidth()
screen_tall= win.winfo_screenheight()

def on_closing_display_window():
    global displayWindow
    if displayWindow is not None:
        displayWindow.destroy()
        displayWindow = None

def on_closing_quiz_window():
    global quizWindow
    if quizWindow is not None:
        quizWindow.destroy()
        quizWindow = None
# CLOSING WINDOW STUFF CLOSING WINDOW STUFF CLOSING WINDOW STUFF CLOSING WINDOW STUFF CLOSING WINDOW STUFF CLOSING WINDOW STUFF

def add_courses():
    courses_name = "New Lesson"
    lesson_amount = 1
    cursor.execute("INSERT INTO Lesson_plans (name, lessons) VALUES (?, ?)", (courses_name, lesson_amount))
    update_courses_list()

def add_lesson(course_id):
    newLesson = "New"
    material = ""
    cursor.execute("INSERT INTO Courses (course_id, lesson_name, material, type) VALUES (?, ?, ?, ?)",(course_id, newLesson, material, 'lesson'))
    connection.commit()
    update_lesson_list(course_id)

def add_quiz(course_id):
    newLesson = "Quiz"
    material = ""
    question=""
    answer=""
    correct= True
    cursor.execute("INSERT INTO Courses (course_id, lesson_name, material, type) VALUES (?, ?, ?, ?)",(course_id, newLesson, material, 'quiz'))
    last=cursor.lastrowid
    cursor.execute("INSERT INTO Quizes(lesson_id,question, answer, correct) VALUES (?,?,?,?)", (last,question, answer, correct) )
    connection.commit()
    update_lesson_list(course_id)

def display_lessons(course_id, course_name, courses, ):#xfcgvcftgvhvugytcryvbhuvgycftfvbuyvtcrvybunbvytcrvybbuytcrvybyuvtcr
    global current_page, lesson_frame, btB, btLA, btQA
    current_page = 0
    btN.place_forget()
    frame.pack_forget()
    lesson_frame = Frame(win, background="black")
    lesson_frame.pack(pady=100)
    update_lesson_list(course_id)
    btLA = Button(win, text="ADD LESSON", command=lambda c=course_id: add_lesson(c), width=10, padx=20,pady=10, font="Impact", relief=RAISED, bd=5)
    btLA.place(x=screen_wide*.845,y=screen_tall*.02)
    btQA = Button(win, text="ADD QUIZ", command=lambda c=course_id: add_quiz(c), width=10, padx=20,pady=10, font="Impact", relief=RAISED, bd=5)
    btQA.place(x=screen_wide*.7,y=screen_tall*.02)
    btB = Button(win, text="BACK", command= back, width=10, padx=20, pady=10,font="Impact", relief=RAISED, bd=5)
    btB.place(x=screen_wide * .035, y=screen_tall * .02)

def back():
    lesson_frame.pack_forget()
    frame.pack(framePack)
    btB.place_forget()
    btLA.place_forget()
    btQA.place_forget()
    btN.place(NPlacement)
#LESSON LESSON LESSON LESSON LESSON LESSON LESSON LESSON LESSON LESSON LESSON LESSON LESSON LESSON LESSON LESSON
def open_lesson(lesson):
    global displayWindow, btSave, btEdit, lessonLabel
    lesson_id, course_id, lesson_name, material, type = lesson
    if displayWindow is not None:
        displayWindow.focus()
        return
    displayWindow = Toplevel(win)
    displayWindow.title(lesson_name)
    displayWindow.geometry("600x600")
    displayWindow.configure(background="black")
    lessonLabel= Label(displayWindow, text=f"{lesson_name}", font="impact", background="black", foreground="white")
    lessonLabel.pack(side=TOP)

    ent_Material = Text(displayWindow, width=30, height=5, relief=RIDGE, bd=10, )
    ent_Material.insert(END, material)
    ent_Material.config(state='disabled')
    ent_Material.pack(pady=5, padx=10, fill=BOTH, expand=True)

    def edit_lesson():
        global btSave, entName

        lessonLabel.pack_forget()
        entName = Entry(displayWindow, font="impact",justify=CENTER)
        entName.insert(END, lesson_name)
        entName.pack(side= TOP, pady=1)

        matfo=ent_Material.pack_info()
        ent_Material.pack(matfo)

        ent_Material.config(state="normal")
        btnfo=btEdit.pack_info()
        btEdit.pack_forget()
        btSave = Button(displayWindow, text="Save",command=save_lesson, width=10, relief=RAISED, bd=5)
        btSave.pack(btnfo)

    def save_lesson():
        global btEdit

        new_Material = ent_Material.get("1.0", END).strip()
        new_Name = entName.get().strip()
        lesson_id, course_id, lesson_name, material, type = lesson
        cursor.execute("UPDATE Courses SET material =? WHERE id=?",(new_Material, lesson_id))
        cursor.execute("UPDATE Courses SET lesson_name =? WHERE id=?",(new_Name, lesson_id))
        connection.commit()

        entName.pack_forget()
        lessonLabel.configure(text=new_Name)
        lessonLabel.pack(side= TOP)

        matfo = ent_Material.pack_info()
        ent_Material.pack(matfo)

        ent_Material.config(state="disabled")
        btnfo= btSave.pack_info()
        btSave.pack_forget()
        btEdit = Button(displayWindow, text="Edit", command=edit_lesson, width=10, relief=RAISED, bd=5)
        btEdit.pack(btnfo)
        update_lesson_list(course_id)

    def delete_lesson():
        cursor.execute("DELETE FROM Courses WHERE id=?", (lesson_id,))
        connection.commit()
        on_closing_display_window()
        update_lesson_list(course_id)

    btEdit = Button(displayWindow, text="Edit",command=edit_lesson, width=10, relief=RAISED, bd=5)
    btEdit.pack(pady=5,side=TOP)

    btDelete = Button(displayWindow, text="Delete", command= delete_lesson, width=10, relief=RAISED, bd=5)
    btDelete.pack(pady=5,side=BOTTOM)

    displayWindow.protocol("WM_DELETE_WINDOW", on_closing_display_window)
    displayWindow.minsize(width=400, height=400)
#QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ
def open_quiz(lesson):
    global quizWindow, btSave, btEdit, lessonLabel, current_question
    lesson_id, course_id, lesson_name, material, type = lesson
    current_question=0
    cursor.execute("SELECT * FROM Quizes WHERE lesson_id = ?", (lesson_id,))
    quizzes = cursor.fetchall()
    if quizWindow is not None:
        quizWindow.focus()
        return

    quizWindow = Toplevel(win)
    quizWindow.title("Quiz Maker")
    quizWindow.geometry("600x600")
    quizWindow.configure(background="black")

    lessonLabel = Label(quizWindow, text=f"{lesson_name}", font=("impact", 25), background="black", foreground="white")
    lessonLabel.pack(side=TOP)

    questionlabel = Label(quizWindow, font=("Arial", 18), bg="black", fg="white", wraplength=600)
    questionlabel.pack(pady=10)

    answerslabel = Label(quizWindow, font=("Arial", 16), bg="black", fg="lightgray", justify=LEFT)
    answerslabel.pack(pady=5)

    correctlabel = Label(quizWindow, font=("Arial", 16), bg="black", fg="lightgreen")
    correctlabel.pack(pady=5)

    def edit_quiz():
        global entName, entQuestion, entAnswers, entCorrect, btAddAns, btRemoveAns
        quiz = quizzes[current_question]
        quiz_id, _, question, answer, correct = quiz

        entName= Entry(quizWindow, font="impact",justify=CENTER)
        entName.insert(END, lesson_name)
        entName.pack(lessonLabel.pack_info())

        entQuestion= Entry(quizWindow, font=("Arial", 16), width=80)
        entQuestion.insert(0, question.strip())
        entQuestion.pack(pady=5)
        
        entAnswers= Entry(quizWindow, font=("Arial", 16), width=80)
        entAnswers.insert(0, answer.strip())
        entAnswers.pack(pady=5)

        entCorrect = Entry(quizWindow, font=("Arial", 16), width=10)
        entCorrect.insert(0, str(correct))
        entCorrect.pack(pady=5)

        lessonLabel.pack_forget()
        questionlabel.pack_forget()
        answerslabel.pack_forget()
        correctlabel.pack_forget()
        btEdit.pack_forget()

        btAddAns = Button(quizWindow, text="+ Answer")
        btAddAns.pack( padx=20, pady=5)

        btRemoveAns = Button(quizWindow, text="- Answer")
        btRemoveAns.pack(padx=20, pady=5)

        btSave.pack(pady=10)
        btDelete.pack(btDelete.pack_info())

    def save_quiz():
        new_name=entName.get().strip()
        new_question = entQuestion.get().strip()
        new_answers = entAnswers.get().strip()
        new_correct = entCorrect.get().strip()

        quiz = quizzes[current_question]
        quiz_id = quiz[0]

        cursor.execute("UPDATE Courses SET lesson_name=? WHERE id=?", (new_name,lesson_id))

        cursor.execute("UPDATE Quizes SET question=?, answer=?, correct=? WHERE id=?",(new_question, new_answers, int(new_correct), quiz_id))
        connection.commit()

        cursor.execute("SELECT * FROM Quizes WHERE lesson_id = ?", (lesson_id,))
        quizzes.clear()
        quizzes.extend(cursor.fetchall())

        entName.pack_forget()
        entQuestion.pack_forget()
        entAnswers.pack_forget()
        entCorrect.pack_forget()
        btAddAns.pack_forget()
        btRemoveAns.pack_forget()
        btSave.pack_forget()

        lessonLabel.configure(text=new_name)
        lessonLabel.pack()
        questionlabel.pack(pady=10)
        answerslabel.pack(pady=5)
        correctlabel.pack(pady=5)
        btEdit.pack(pady=10)
        btDelete.pack(btDelete.pack_info())
        update_lesson_list(course_id)
        change_quiz_page(current_question)

    def delete_lesson():
        cursor.execute("DELETE FROM Courses WHERE id=?", (lesson_id,))
        connection.commit()
        on_closing_quiz_window()
        update_lesson_list(course_id)

    def change_quiz_page(index):
        if 0 <= index < len(quizzes):
            quiz_id, lesson_id_fk, question, answer, correct = quizzes[index]
            questionlabel.config(text=f"Q{index + 1}: {question.strip()}")

            options = answer.strip().split("|")
            answers_text = "\n".join([f"{i + 1}) {opt.strip()}" for i, opt in enumerate(options)])
            answerslabel.config(text=answers_text)

            correctlabel.config(text=f"Correct Answer: {correct}) {options[int(correct) - 1].strip() if correct <= len(options) else 'N/A'}")

    def previous_question():
        global current_question
        if current_question > 0:
            current_question -= 1
            change_quiz_page(current_question)

    def next_question():
        global current_question
        if current_question < len(quizzes) - 1:
            current_question += 1
            change_quiz_page(current_question)

    change_quiz_page(current_question)

    btEdit = Button(quizWindow, text="Edit", command=edit_quiz, width=10, relief=RAISED, bd=5)
    btEdit.pack(pady=5, side=TOP)

    btDelete = Button(quizWindow, text="Delete", command=delete_lesson, width=10, relief=RAISED, bd=5)
    btDelete.pack(pady=5, side=TOP)

    btSave = Button(quizWindow, text="Save", command=save_quiz, width=10, relief=RAISED, bd=5)
    btSave.pack_forget()

    btQP = Button(quizWindow, text="←", font=("Impact", 18), width=4, padx=30, pady=2, relief=RAISED, bd=5,command=previous_question)
    btQP.place(x=quizWindow.winfo_screenheight()*.1,y=quizWindow.winfo_screenheight()*.8)

    btQN = Button(quizWindow, text="→", font=("Impact", 18), width=4, padx=30, pady=2, relief=RAISED, bd=5,command=next_question)
    btQN.place(x=quizWindow.winfo_screenheight()*.9,y=quizWindow.winfo_screenheight()*.8)
    quizWindow.protocol("WM_DELETE_WINDOW", on_closing_quiz_window)
    quizWindow.resizable(0, 0)

def update_lesson_list(course_id):
    for widget in lesson_frame.winfo_children():
        widget.destroy()

    cursor.execute("SELECT * FROM Courses WHERE course_id = ?", (course_id,))
    lessons = cursor.fetchall()
    row_count = 0
    column_count = 0

    for lesson in lessons:
        lesson_id, course_id, lesson_name, material, type = lesson
        is_quiz = (type == 'quiz')

        if is_quiz == True:
            button_text = f"★{lesson_name}"
            button_color = "grey"
            button_command = lambda q=lesson: open_quiz(q)
        else:
            button_text= f"☆{lesson_name}"
            button_color="SystemButtonFace"
            button_command = lambda l=lesson: open_lesson(l)

        lesson_button = Button(lesson_frame,text=button_text,command=button_command,width=30,padx=20,pady=20,font="Arial",relief=RAISED,bd=5,bg=button_color)
        lesson_button.grid(row=row_count, column=column_count, padx=10, pady=10)

        column_count += 1
        if column_count == 3:
            column_count = 0
            row_count += 1

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
framePack=frame.pack_info()

update_courses_list()
labelMain = Label(win, text="PYTUTOR", foreground="white", background="Black", font=("impact", 40))
labelMain.place(x=screen_wide*.42, y=10)
btN = Button(win, text="NEW", width=10, padx=20, pady=10, command=add_courses, relief=RAISED, bd=5, font="impact")
btN.place(x=screen_wide * .035, y=screen_tall * .02)
NPlacement=btN.place_info()

win.mainloop()
connection.close()
