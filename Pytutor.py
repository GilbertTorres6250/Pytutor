from tkinter import *
from tkinter import ttk
import sqlite3

current_page = 0
courses_per_page = 12
lessons_per_page = 12
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
win.geometry("900x600")
win.title("PyTutor")
win.configure(background="black")
screen_wide = win.winfo_screenwidth()
screen_tall = win.winfo_screenheight()


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
    cursor.execute("INSERT INTO Courses (course_id, lesson_name, material, type) VALUES (?, ?, ?, ?)",
                   (course_id, newLesson, material, 'lesson'))
    connection.commit()
    update_lesson_list(course_id)

def add_quiz(course_id):
    newLesson = "Quiz"
    material = ""
    question = ""
    answer = ""
    correct = True
    cursor.execute("INSERT INTO Courses (course_id, lesson_name, material, type) VALUES (?, ?, ?, ?)",(course_id, newLesson, material, 'quiz'))
    last = cursor.lastrowid
    cursor.execute("INSERT INTO Quizes(lesson_id,question, answer, correct) VALUES (?,?,?,?)",(last, question, answer, correct))
    connection.commit()
    update_lesson_list(course_id)

def display_lessons(course_id, course_name,courses):  # xfcgvcftgvhvugytcryvbhuvgycftfvbuyvtcrvybunbvytcrvybbuytcrvybyuvtcr
    global current_page, lesson_frame, btB, btLA, btQA
    current_page = 0
    frame.pack_forget()
    lesson_frame = Frame(win, background="black")
    lesson_frame.pack(pady=100)
    update_lesson_list(course_id)
    btLA = Button(win, text="ADD LESSON", command=lambda c=course_id: add_lesson(c), width=10, padx=20, pady=10,font="Impact", relief=RAISED, bd=5)
    btLA.place(anchor="n", relx =.9,rely=.02)
    btQA = Button(win, text="ADD QUIZ", command=lambda c=course_id: add_quiz(c), width=10, padx=20, pady=10,font="Impact", relief=RAISED, bd=5)
    btQA.place(anchor="n", relx =.8,rely=.02)
    btB = Button(win, text="BACK", command=back, width=10, padx=20, pady=10, font="Impact", relief=RAISED, bd=5)
    btB.place(btN.place_info())
    btN.place_forget()

def back():
    lesson_frame.pack_forget()
    frame.pack(framePack)
    btB.place_forget()
    btLA.place_forget()
    btQA.place_forget()
    btN.place(NPlacement)

# LESSON LESSON LESSON LESSON LESSON LESSON LESSON LESSON LESSON LESSON LESSON LESSON LESSON LESSON LESSON LESSON
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
    lessonLabel = Label(displayWindow, text=f"{lesson_name}", font="impact", background="black", foreground="white")
    lessonLabel.pack(side=TOP)

    ent_Material = Text(displayWindow, width=30, height=5, relief=RIDGE, bd=10, )
    ent_Material.insert(END, material)
    ent_Material.config(state='disabled')
    ent_Material.pack(pady=5, padx=10, fill=BOTH, expand=True)

    def edit_lesson():
        global btSave, entName

        lessonLabel.pack_forget()
        entName = Entry(displayWindow, font="impact", justify=CENTER)
        entName.insert(END, lesson_name)
        entName.pack(side=TOP, pady=1)

        matfo = ent_Material.pack_info()
        ent_Material.pack(matfo)

        ent_Material.config(state="normal")
        btnfo = btEdit.pack_info()
        btEdit.pack_forget()
        btSave = Button(displayWindow, text="Save", command=save_lesson, width=10, relief=RAISED, bd=5)
        btSave.pack(btnfo)

    def save_lesson():
        global btEdit

        new_Material = ent_Material.get("1.0", END).strip()
        new_Name = entName.get().strip()
        lesson_id, course_id, lesson_name, material, type = lesson
        cursor.execute("UPDATE Courses SET material =? WHERE id=?", (new_Material, lesson_id))
        cursor.execute("UPDATE Courses SET lesson_name =? WHERE id=?", (new_Name, lesson_id))
        connection.commit()

        entName.pack_forget()
        lessonLabel.configure(text=new_Name)
        lessonLabel.pack(side=TOP)

        matfo = ent_Material.pack_info()
        ent_Material.pack(matfo)

        ent_Material.config(state="disabled")
        btnfo = btSave.pack_info()
        btSave.pack_forget()
        btEdit = Button(displayWindow, text="Edit", command=edit_lesson, width=10, relief=RAISED, bd=5)
        btEdit.pack(btnfo)
        update_lesson_list(course_id)

    def delete_lesson():
        cursor.execute("DELETE FROM Courses WHERE id=?", (lesson_id,))
        connection.commit()
        on_closing_display_window()
        update_lesson_list(course_id)

    btEdit = Button(displayWindow, text="Edit", command=edit_lesson, width=10, relief=RAISED, bd=5)
    btEdit.pack(pady=5, side=TOP)

    btDelete = Button(displayWindow, text="Delete", command=delete_lesson, width=10, relief=RAISED, bd=5)
    btDelete.pack(pady=5, side=BOTTOM)

    displayWindow.protocol("WM_DELETE_WINDOW", on_closing_display_window)
    displayWindow.minsize(width=400, height=400)

# QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ QUIZ
def open_quiz(lesson):
    global quizWindow, btSaveQuiz, btEditQuiz, quizLabel, current_question,btAddQuestion
    lesson_id, course_id, lesson_name, material, type = lesson
    current_question = 0
    cursor.execute("SELECT * FROM Quizes WHERE lesson_id = ?", (lesson_id,))
    quizzes = cursor.fetchall()
    if quizWindow is not None:
        quizWindow.focus()
        return

    quizWindow = Toplevel(win)
    quizWindow.title("Quiz Maker")
    quizWindow.geometry("600x600")
    quizWindow.configure(background="black")

    quizLabel = Label(quizWindow, text=f"{lesson_name}", font=("impact", 25), background="black", foreground="white")
    quizLabel.pack(side=TOP)

    questionlabel = Label(quizWindow, font=("Arial", 18), bg="black", fg="white", wraplength=600)
    questionlabel.pack(pady=10)

    answerslabel = Label(quizWindow, font=("Arial", 16), bg="black", fg="lightgray", justify=LEFT)
    answerslabel.pack(pady=5)

    correctlabel = Label(quizWindow, font=("Arial", 16), bg="black", fg="lightgreen")
    correctlabel.pack(pady=5)

    def edit_quiz():
        global entName, entQuestion, entAnswerList, dropper, btAddAns, btRemoveAns,btn_frame
        quiz = quizzes[current_question]
        quiz_id, _, question, answer, correct = quiz

        entName = Entry(quizWindow, font=("impact", 25), justify=CENTER,relief=RIDGE, bd=5)
        entName.insert(END, lesson_name)
        entName.pack(quizLabel.pack_info(), pady=1)

        entQuestion = Entry(quizWindow, font=("Arial", 16),relief=RIDGE, bd=5)
        entQuestion.insert(0, question.strip())
        entQuestion.pack(pady=5)


        answers = answer.strip().split("|")
        entAnswerList = []

        def refresh_dropdown():
            values = [str(i + 1) for i in range(len(entAnswerList))]
            dropper['values'] = values
            if int(dropper_var.get()) > len(values):
                dropper_var.set("1")

        def add_answer():
            new_ent = Entry(quizWindow, font=("Arial", 14),relief=RIDGE, bd=5)
            new_ent.insert(END, f"Option {len(entAnswerList) + 1}")
            new_ent.pack(pady=2)
            entAnswerList.append(new_ent)
            refresh_dropdown()

        def remove_answer():
            if len(entAnswerList) > 1:
                last = entAnswerList.pop()
                last.destroy()
                refresh_dropdown()

        for answer in answers:
            ent = Entry(quizWindow, font=("Arial", 14),relief=RIDGE, bd=5)
            ent.insert(END, answer.strip())
            ent.pack(pady=2)
            entAnswerList.append(ent)

        dropper_var = StringVar(value=str(correct))
        dropper = ttk.Combobox(quizWindow, textvariable=dropper_var,values=[str(i + 1) for i in range(len(entAnswerList))],state="readonly", width=5, font=("Arial", 14))
        dropper.pack(pady=5)
        btQuizPrev.configure(state=DISABLED)
        btQuizNext.configure(state=DISABLED)
        btAddQuestion.configure(state=DISABLED)

        quizLabel.pack_forget()
        questionlabel.pack_forget()
        answerslabel.pack_forget()
        correctlabel.pack_forget()
        btEditQuiz.pack_forget()

        btn_frame = Frame(quizWindow,background="black")
        btn_frame.pack(pady=5)
        btAddAns = Button(btn_frame, text="+ Answer",command=add_answer)
        btAddAns.pack(side=LEFT, padx=10)

        btRemoveAns = Button(btn_frame, text="- Answer",command=remove_answer)
        btRemoveAns.pack(side=LEFT, padx=10)

        btSaveQuiz.pack(pady=10)
        btDeleteQuiz.pack(btDeleteQuiz.pack_info())

    def save_quiz():
        new_name = entName.get().strip()
        new_question = entQuestion.get().strip()
        new_correct = dropper.get().strip()
        new_answers_list = [entry.get().strip() for entry in entAnswerList]
        new_answers = "|".join(new_answers_list)
        quiz = quizzes[current_question]
        quiz_id = quiz[0]

        cursor.execute("UPDATE Courses SET lesson_name=? WHERE id=?", (new_name, lesson_id))

        cursor.execute("UPDATE Quizes SET question=?, answer=?, correct=? WHERE id=?",(new_question, new_answers, int(new_correct), quiz_id))
        connection.commit()

        cursor.execute("SELECT * FROM Quizes WHERE lesson_id = ?", (lesson_id,))
        quizzes.clear()
        quizzes.extend(cursor.fetchall())

        btn_frame.pack_forget()
        entName.pack_forget()
        entQuestion.pack_forget()
        dropper.pack_forget()
        btAddAns.pack_forget()
        btRemoveAns.pack_forget()
        btSaveQuiz.pack_forget()
        for answer in entAnswerList:
            answer.pack_forget()
        btQuizPrev.configure(state=NORMAL)
        btQuizNext.configure(state=NORMAL)
        btAddQuestion.configure(state=NORMAL)

        quizLabel.configure(text=new_name)
        quizLabel.pack()
        questionlabel.pack(pady=10)
        answerslabel.pack(pady=5)
        correctlabel.pack(pady=5)
        btEditQuiz.pack(pady=5)
        btDeleteQuiz.pack(btDeleteQuiz.pack_info())
        update_lesson_list(course_id)
        change_quiz_page(current_question)

    def delete_quiz():
        cursor.execute("DELETE FROM Courses WHERE id=?", (lesson_id,))
        connection.commit()
        on_closing_quiz_window()
        update_lesson_list(course_id)

    def change_quiz_page(index):
        nonlocal btQuizNext
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

    def add_question():
        question=""
        answer=""
        correct=1
        cursor.execute("INSERT INTO Quizes(lesson_id,question, answer, correct) VALUES (?,?,?,?)",(lesson_id, "", "", 1)
        )
        connection.commit()

        # Reload quizzes from database
        cursor.execute("SELECT * FROM Quizes WHERE lesson_id = ?", (lesson_id,))
        quizzes.clear()
        quizzes.extend(cursor.fetchall())

        current_question = len(quizzes) - 1
        change_quiz_page(current_question)

    change_quiz_page(current_question)
    
    btAddQuestion = Button(quizWindow, text="Add", command=add_question, font="Impact", width=8, relief=RAISED, bd=5)
    btAddQuestion.place(anchor=N, relx=.08, rely=.01)

    btEditQuiz = Button(quizWindow, text="Edit", command=edit_quiz, width=10, relief=RAISED, bd=5)
    btEditQuiz.pack(pady=5, side=TOP)

    btDeleteQuiz = Button(quizWindow, text="Delete", command=delete_quiz, width=10, relief=RAISED, bd=5)
    btDeleteQuiz.pack(pady=5, side=TOP)

    btSaveQuiz = Button(quizWindow, text="Save", command=save_quiz, width=10, relief=RAISED, bd=5)
    btSaveQuiz.pack_forget()

    btQuizPrev = Button(quizWindow, text="⮜--", font=("Impact", 18), padx=20, relief=RAISED, bd=5,command=previous_question)
    btQuizPrev.place(anchor=S, relx =.1,rely=.9)

    btQuizNext = Button(quizWindow, text="--⮞", font=("Impact", 18), padx=20, relief=RAISED, bd=5,command=next_question)
    btQuizNext.place(anchor=S, relx =.9,rely=.9)

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
            button_text = f"☆{lesson_name}"
            button_color = "SystemButtonFace"
            button_command = lambda l=lesson: open_lesson(l)

        lesson_button = Button(lesson_frame, text=button_text, command=button_command, width=30, padx=20, pady=20,font="Arial", relief=RAISED, bd=5, bg=button_color)
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
        course_button = Button(frame, text=lessons_name, command=lambda l=lessons: display_lessons(*l), width=30,padx=20, pady=20, font=20, relief=RAISED, bd=5)
        course_button.grid(row=row_count, column=column_count, padx=10, pady=10)
        column_count += 1
        if column_count == 3:
            column_count = 0
            row_count += 1

frame = Frame(win, background="black")
frame.pack(pady=100)
framePack = frame.pack_info()

update_courses_list()
labelMain = Label(win, text="PYTUTOR", foreground="white", background="black", font=("impact", 40))
labelMain.place(anchor=N, relx =.5,rely=.01)
btN = Button(win, text="NEW", width=10, padx=20, pady=10, command=add_courses, relief=RAISED, bd=5, font="impact")
btN.place(anchor=N, relx =.05,rely=.02)
NPlacement = btN.place_info()

win.mainloop()
connection.close()
