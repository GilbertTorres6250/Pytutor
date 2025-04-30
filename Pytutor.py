from tkinter import *
from tkinter import ttk
import sqlite3

current_page = 0
current_lesson_page=0
courses_per_page = 12
lessons_per_page = 12
displayWindow = None
quizWindow = None
menuWindow = None

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
                    FOREIGN KEY(course_id) REFERENCES Lesson_plans(id) ON DELETE CASCADE
                )''')
cursor.execute('''CREATE TABLE IF NOT EXISTS Quizes (
                    id INTEGER PRIMARY KEY,
                    lesson_id INTEGER,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    correct INTEGER NOT NULL,
                    FOREIGN KEY(lesson_id) REFERENCES Courses(id) ON DELETE CASCADE
                )''')
cursor.execute('''CREATE TABLE IF NOT EXISTS colors (
                    id INTEGER PRIMARY KEY,
                    background_color TEXT,
                    foreground_color TEXT
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

def on_closing_menu_window():
    global menuWindow
    if menuWindow is not None:
        menuWindow.destroy()
        menuWindow = None

def add_courses():
    cursor.execute("INSERT INTO Lesson_plans (name, lessons) VALUES (?, ?)", ("New Lesson", 1))
    connection.commit()
    update_courses_list()

def add_lesson(course_id):
    newLesson = "New"
    cursor.execute("INSERT INTO Courses (course_id, lesson_name, material, type) VALUES (?, ?, ?, ?)",(course_id, newLesson, "", 'lesson'))
    connection.commit()
    update_lesson_list(course_id)

def add_quiz(course_id):
    newLesson = "Quiz"
    cursor.execute("INSERT INTO Courses (course_id, lesson_name, material, type) VALUES (?, ?, ?, ?)",(course_id, newLesson, "", 'quiz'))
    last = cursor.lastrowid
    cursor.execute("INSERT INTO Quizes(lesson_id,question, answer, correct) VALUES (?,?,?,?)",(last, "", "", 1))
    connection.commit()
    update_lesson_list(course_id)

def display_lessons(course_id, course_name,courses):  # xfcgvcftgvhvugytcryvbhuvgycftfvbuyvtcrvybunbvytcrvybbuytcrvybyuvtcr
    global current_lesson_page,current_page, lesson_frame, btB, btLA, btQA,btDC,btEC,btSC
    current_lesson_page = 0
    frame.pack_forget()
    lesson_frame = Frame(win, background=b)
    lesson_frame.pack(pady=100)

    labelMain.configure(text=course_name)

    next_button.configure(command=lambda: next_lesson_page(course_id))
    prev_button.configure(command=lambda: previous_lesson_page(course_id))

    update_lesson_list(course_id)

    def edit_course():
        global entMain
        entMain = Entry(win, font=("impact", 40), justify=CENTER, relief=RIDGE, bd=5)
        entMain.insert(END, course_name)
        entMain.place(labelMain.place_info())
        labelMain.place_forget()
        btDC.place(btB.place_info())
        btSC.place(btEC.place_info())
        btEC.place_forget()
        btB.place_forget()

    def save_course():
        new_name = entMain.get().strip()
        labelMain.place(entMain.place_info())
        labelMain.configure(text=new_name)
        btB.place(btDC.place_info())
        btEC.place(btSC.place_info())
        btSC.place_forget()
        btDC.place_forget()
        entMain.place_forget()
        cursor.execute("UPDATE Lesson_plans SET name=? WHERE id=?", (new_name, course_id))
        connection.commit()

    def delete_course():
        cursor.execute("DELETE FROM Lesson_plans WHERE id=?", (course_id,))
        connection.commit()
        cursor.execute("SELECT id FROM Courses WHERE course_id=?", (course_id,))
        all_lessons = cursor.fetchall()

        labelMain.place(entMain.place_info())
        labelMain.configure(text="PyTutor")
        btB.place(btDC.place_info())
        btEC.place(btSC.place_info())
        btSC.place_forget()
        btDC.place_forget()
        entMain.place_forget()

        for lesson in all_lessons:
            lesson_id = lesson[0]
            cursor.execute("DELETE FROM Courses WHERE id = ?", (lesson_id,))
            cursor.execute("DELETE FROM Quizes WHERE lesson_id = ?", (lesson_id,))

        connection.commit()
        on_closing_display_window()
        back()
        update_courses_list()

    btDC = Button(win, text="DELETE COURSE",command=delete_course, width=10, padx=20, pady=10, font="Impact", relief=RAISED, bd=5, bg=f, fg=b, activebackground=b,activeforeground=f)
    btDC.place_forget()
    btEC = Button(win, text="EDIT COURSE", command=edit_course, width=10, padx=20, pady=10, font="Impact", relief=RAISED, bd=5, bg=f, fg=b, activebackground=b,activeforeground=f)
    btEC.place(anchor=N, relx=.2, rely=.02)
    btSC = Button(win, text="SAVE COURSE", command=save_course, width=10, padx=20, pady=10, font="Impact",relief=RAISED, bd=5, bg=f, fg=b, activebackground=b,activeforeground=f)
    btSC.place_forget()

    btLA = Button(win, text="ADD LESSON", command=lambda c=course_id: add_lesson(c), width=10, padx=20, pady=10,font="Impact", relief=RAISED, bd=5, bg=f, fg=b, activebackground=b,activeforeground=f)
    btLA.place(anchor=N, relx=.92, rely=.02)
    btQA = Button(win, text="ADD QUIZ", command=lambda c=course_id: add_quiz(c), width=10, padx=20, pady=10,font="Impact", relief=RAISED, bd=5, bg=f, fg=b, activebackground=b,activeforeground=f)
    btQA.place(anchor=N, relx=.8, rely=.02)
    btB = Button(win, text="BACK", command=back, width=10, padx=20, pady=10, font="Impact", relief=RAISED, bd=5, bg=f, fg=b, activebackground=b,activeforeground=f)
    btB.place(btN.place_info())
    btN.place_forget()

def back():
    global current_page,current_lesson_page
    current_page=0
    current_lesson_page=0
    labelMain.configure(text="PYTUTOR")
    lesson_frame.pack_forget()
    frame.pack(framePack)
    btN.place(btB.place_info())
    btB.place_forget()
    btLA.place_forget()
    btQA.place_forget()
    btDC.place_forget()
    btEC.place_forget()
    update_courses_list()
    next_button.configure(command=next_page)
    prev_button.configure(command=previous_page)

def open_lesson(lesson):
    global displayWindow, btSave, btEdit, lessonLabel
    lesson_id, course_id, lesson_name, material, type = lesson
    if displayWindow is not None:
        displayWindow.focus()
        return
    displayWindow = Toplevel(win)
    displayWindow.title(lesson_name)
    displayWindow.geometry("600x600")
    displayWindow.configure(background=b)
    lessonLabel = Label(displayWindow, text=f"{lesson_name}", font="impact", background=b, foreground=f)
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
        btSave = Button(displayWindow, text="Save", command=save_lesson, width=10, relief=RAISED, bd=5, bg=f, fg=b, activebackground=b,activeforeground=f)
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
        btEdit.pack(btnfo)
        update_lesson_list(course_id)

    def delete_lesson():
        cursor.execute("DELETE FROM Courses WHERE id=?", (lesson_id,))
        connection.commit()
        on_closing_display_window()
        update_lesson_list(course_id)

    btEdit = Button(displayWindow, text="Edit", command=edit_lesson, width=10, relief=RAISED, bd=5, bg=f, fg=b, activebackground=b,activeforeground=f)
    btEdit.pack(pady=5, side=TOP)

    btDelete = Button(displayWindow, text="Delete", command=delete_lesson, width=10, relief=RAISED, bd=5, bg=f, fg=b, activebackground=b,activeforeground=f)
    btDelete.pack(pady=5, side=BOTTOM)

    displayWindow.protocol("WM_DELETE_WINDOW", on_closing_display_window)
    displayWindow.minsize(width=400, height=400)

def open_quiz(lesson):
    global quizWindow, btSaveQuiz, btEditQuiz, quizLabel, current_question, btAddQuestion
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
    quizWindow.configure(background=b)

    quizLabel = Label(quizWindow, text=f"{lesson_name}", font=("impact", 25), background=b, foreground=f)
    quizLabel.pack(side=TOP)

    questionlabel = Label(quizWindow, font=("Arial", 18), bg=b, fg=f, wraplength=600)
    questionlabel.pack(pady=10)

    answerslabel = Label(quizWindow, font=("Arial", 16), bg=b, fg=f, justify=LEFT)
    answerslabel.pack(pady=5)

    correctlabel = Label(quizWindow, font=("Arial", 16), bg=b, fg=f)
    correctlabel.pack(pady=5)

    def edit_quiz():
        global entQuizName, entQuestion, entAnswerList, dropper, btAddAns, btRemoveAns, btn_frame
        quiz = quizzes[current_question]
        quiz_id, _, question, answer, correct = quiz

        entQuizName = Entry(quizWindow, font=("impact", 25), justify=CENTER, relief=RIDGE, bd=5)
        entQuizName.insert(END, lesson_name.strip())
        entQuizName.pack(quizLabel.pack_info(), pady=1)

        entQuestion = Entry(quizWindow, font=("Arial", 16), relief=RIDGE, bd=5)
        entQuestion.insert(0, question.strip())
        entQuestion.pack()

        answers = answer.strip().split("|")
        entAnswerList = []

        def refresh_dropdown():
            values = [str(i + 1) for i in range(len(entAnswerList))]
            dropper['values'] = values
            if int(dropper_var.get()) > len(values):
                dropper_var.set("1")

        def add_answer():
            new_ent = Entry(quizWindow, font=("Arial", 14), relief=RIDGE, bd=5)
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
            ent = Entry(quizWindow, font=("Arial", 14), relief=RIDGE, bd=5)
            ent.insert(END, answer.strip())
            ent.pack()
            entAnswerList.append(ent)

        dropper_var = StringVar(value=str(correct))
        dropper = ttk.Combobox(quizWindow, textvariable=dropper_var,values=[str(i + 1) for i in range(len(entAnswerList))], state="readonly", width=5,font=("Arial", 14))
        dropper.pack(pady=5)
        btQuizPrev.configure(state=DISABLED)
        btQuizNext.configure(state=DISABLED)
        btAddQuestion.configure(state=DISABLED)
        btRemoveQuestion.configure(state=DISABLED)

        quizLabel.pack_forget()
        questionlabel.pack_forget()
        answerslabel.pack_forget()
        correctlabel.pack_forget()
        btEditQuiz.pack_forget()
        btDeleteQuiz.pack_forget()

        btn_frame = Frame(quizWindow, background=b)
        btn_frame.pack(pady=5)
        btAddAns = Button(btn_frame, text="+ Answer", command=add_answer, bg=f, fg=b, activebackground=b,activeforeground=f)
        btAddAns.pack(side=LEFT, padx=10)

        btRemoveAns = Button(btn_frame, text="- Answer", command=remove_answer, bg=f, fg=b, activebackground=b,activeforeground=f)
        btRemoveAns.pack(side=LEFT, padx=10)

        btSaveQuiz.pack(pady=10)

    def save_quiz():
        nonlocal lesson_name
        new_name = entQuizName.get().strip()
        lesson_name = new_name
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
        entQuizName.pack_forget()
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
        btRemoveQuestion.configure(state=NORMAL)

        quizLabel.configure(text=new_name)
        quizLabel.pack()
        questionlabel.pack(pady=10)
        answerslabel.pack(pady=5)
        correctlabel.pack(pady=5)
        btEditQuiz.pack(pady=5)
        btDeleteQuiz.pack(pady=5)
        update_lesson_list(course_id)
        change_quiz_page(current_question)

    def delete_quiz():
        cursor.execute("DELETE FROM Quizes WHERE lesson_id = ?", (lesson_id,))
        cursor.execute("DELETE FROM Courses WHERE id = ?", (lesson_id,))
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
        global current_question
        cursor.execute("INSERT INTO Quizes(lesson_id,question, answer, correct) VALUES (?,?,?,?)",(lesson_id, "", "", 1))
        connection.commit()

        cursor.execute("SELECT * FROM Quizes WHERE lesson_id = ?", (lesson_id,))
        quizzes.clear()
        quizzes.extend(cursor.fetchall())

        current_question = len(quizzes) - 1
        change_quiz_page(current_question)

    def remove_question():
        global current_question

        cursor.execute("SELECT id FROM Quizes WHERE lesson_id = ? ORDER BY id DESC LIMIT 1", (lesson_id,))
        last_quiz = cursor.fetchone()

        if last_quiz:
            last_id = last_quiz[0]
            cursor.execute("DELETE FROM Quizes WHERE id = ?", (last_id,))
            connection.commit()

            cursor.execute("SELECT * FROM Quizes WHERE lesson_id = ?", (lesson_id,))
            quizzes.clear()
            quizzes.extend(cursor.fetchall())

            current_question = max(0, len(quizzes) - 1)
            change_quiz_page(current_question)

    change_quiz_page(current_question)

    btAddQuestion = Button(quizWindow, text="Add Q", command=add_question, font="Impact", width=8, relief=RAISED, bd=5, bg=f, fg=b, activebackground=b,activeforeground=f)
    btAddQuestion.place(anchor=N, relx=.08, rely=.01)
    btRemoveQuestion = Button(quizWindow, text="- Last Q", command=remove_question, font="Impact", width=8, relief=RAISED, bd=5, bg=f, fg=b, activebackground=b,activeforeground=f)
    btRemoveQuestion.place(anchor=N, relx=.9, rely=.01)

    btEditQuiz = Button(quizWindow, text="Edit", command=edit_quiz, width=10, relief=RAISED, bd=5, bg=f, fg=b, activebackground=b,activeforeground=f)
    btEditQuiz.pack(pady=5, side=TOP)

    btDeleteQuiz = Button(quizWindow, text="Delete", command=delete_quiz, width=10, relief=RAISED, bd=5, bg=f, fg=b, activebackground=b,activeforeground=f)
    btDeleteQuiz.pack(pady=5, side=TOP)

    btSaveQuiz = Button(quizWindow, text="Save", command=save_quiz, width=10, relief=RAISED, bd=5, bg=f, fg=b, activebackground=b,activeforeground=f)
    btSaveQuiz.pack_forget()

    btQuizPrev = Button(quizWindow, text="⮜—", font=("Impact", 18), padx=20, relief=RAISED, bd=5,command=previous_question, bg=f, fg=b, activebackground=b,activeforeground=f)
    btQuizPrev.place(anchor=S, relx=.1, rely=.9)

    btQuizNext = Button(quizWindow, text="—⮞", font=("Impact", 18), padx=20, relief=RAISED, bd=5,command=next_question, bg=f, fg=b, activebackground=b,activeforeground=f)
    btQuizNext.place(anchor=S, relx=.9, rely=.9)

    quizWindow.protocol("WM_DELETE_WINDOW", on_closing_quiz_window)

def update_lesson_list(course_id):
    for widget in lesson_frame.winfo_children():
        widget.destroy()

    cursor.execute("SELECT * FROM Courses WHERE course_id = ? LIMIT ? OFFSET ?",(course_id, lessons_per_page, current_lesson_page * lessons_per_page))
    lessons = cursor.fetchall()
    row_count = 0
    column_count = 0

    for lesson in lessons:
        global is_quiz
        lesson_id, course_id, lesson_name, material, type = lesson
        is_quiz = (type == 'quiz')

        if is_quiz == True:
            button_text = f"★{lesson_name}"
            button_color = b
            fore = f
            button_command = lambda q=lesson: open_quiz(q)
        else:
            button_text = f"☆{lesson_name}"
            button_color = f
            fore = b
            button_command = lambda l=lesson: open_lesson(l)

        lesson_button = Button(lesson_frame, text=button_text, command=button_command, width=30, padx=20, pady=20,font="Arial", relief=RIDGE, bd=5, bg=button_color, fg=fore, activebackground=fore, activeforeground=button_color)
        lesson_button.grid(row=row_count, column=column_count, padx=10, pady=10)

        if is_quiz == True:
            lesson_button.reverse = True

        column_count += 1
        if column_count == 3:
            column_count = 0
            row_count += 1

    cursor.execute("SELECT COUNT(*) FROM Courses WHERE course_id = ?", (course_id,))
    total_lessons = cursor.fetchone()[0]
    total_lesson_pages = (total_lessons + lessons_per_page - 1) // lessons_per_page
    if current_lesson_page < total_lesson_pages - 1:
        next_button.configure(state=NORMAL)
    else:
        next_button.configure(state=DISABLED)

    if current_lesson_page > 0:
        prev_button.configure(state=NORMAL)
    else:
        prev_button.configure(state=DISABLED)

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
        course_button = Button(frame, text=lessons_name, command=lambda l=lessons: display_lessons(*l), width=30,padx=20, pady=20, font=20, relief=RIDGE, bd=5, bg=f, fg=b, activebackground=b,activeforeground=f)
        course_button.grid(row=row_count, column=column_count, padx=10, pady=10)
        column_count += 1
        if column_count == 3:
            column_count = 0
            row_count += 1

    cursor.execute("SELECT COUNT(*) FROM Lesson_plans")
    total_courses = cursor.fetchone()[0]
    total_pages = (total_courses + courses_per_page - 1) // courses_per_page
    if current_page < total_pages - 1:
        next_button.configure(state=NORMAL)
    else:
        next_button.configure(state=DISABLED)

    if current_page > 0:
        prev_button.configure(state=NORMAL)
    else:
        prev_button.configure(state=DISABLED)

def previous_page(event=None):
    global current_page
    current_page -= 1
    update_courses_list()

def next_page(event=None):
    global current_page
    current_page += 1
    update_courses_list()

def previous_lesson_page(course_id):
    global current_lesson_page
    current_lesson_page -= 1
    update_lesson_list(course_id)

def next_lesson_page(course_id):
    global current_lesson_page
    current_lesson_page += 1
    update_lesson_list(course_id)

def openMenuWindow():
    global menuWindow
    global labelColor

    if menuWindow is not None:
        menuWindow.focus()
        return
    menuWindow = Toplevel(win)
    menuWindow.title("COLOR MENU")
    menuWindow.geometry("400x450")
    menuWindow.resizable(0, 0)
    menuWindow.configure(background=b)
    menuWindow.protocol("WM_DELETE_WINDOW", on_closing_menu_window)

    labelColor = Label(menuWindow, text="COLORWAYS", foreground=f, background=b, font="impact")
    labelColor.grid(row=0, column=1, padx=20, pady=5)

    for i, (name, color_pair) in enumerate(color_map.items()):
        row = 1 + (i // 3)
        col = i % 3
        button = create_button(name, color_pair)
        button.exclude_change = True
        button.grid(row=row, column=col, padx=6, pady=10)

def create_button(name, color_pair):
    background_color, text_color = color_pair
    return Button(menuWindow,bg=background_color,fg=text_color, text=name, command=lambda: setColor(*color_pair),width=15,relief=RAISED,bd=5)

def setColor(b_color, f_color):
    global b, f
    b = b_color
    f = f_color
    saveColor(b, f)
    change()

def update_widget_colors(widget):
    if hasattr(widget, 'exclude_change') and widget.exclude_change:
        return
    if 'background' in widget.keys():
        widget.configure(background=b)
    if 'foreground' in widget.keys():
        widget.configure(foreground=f)
    if isinstance(widget, (Text, Entry)):
        widget.configure(foreground="black", background="white")
    if isinstance(widget, Button):
        widget.configure(background=f, foreground=b, activebackground=b, activeforeground=f)
    if hasattr(widget, 'reverse') and widget.reverse:
        try:
            widget.configure(activebackground=f, activeforeground=b)
        finally:
            widget.configure(background=b, foreground=f)

    for child in widget.winfo_children():
        update_widget_colors(child)

def change():
    for window in [win, quizWindow, displayWindow, menuWindow]:
        if window:
            update_widget_colors(window)

def saveColor(background, foreground):
    cursor.execute("INSERT INTO colors (background_color, foreground_color) VALUES (?, ?)",(background, foreground))
    connection.commit()

def loadColor():
    cursor.execute("SELECT * FROM colors ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    if result:
        return result[1], result[2]
    else:
        return "black", "white"

color_map = {
    "COFFEE": ("#4d3626", "#f3e9dc"),  # Dark brown
    "HORCHATA": ("#f2e9d9", "#b8976a"),  # Tan
    "DR PEPPER": ("#711f25", "white"),  # Red
    "MATCHA": ("#8EB288", "#3a4a37"),  # Pastel green
    "CREAMSICLE": ("#fbbd60", "#f7e0b6"),  # Orange
    "TARO": ("#9C7F91", "#E3B8C3"),  # Pastel Purple
    "BLUE CHEESE": ("#6a7f8c", "#d1d9e6"),  # Pastel Blue
    "OREO": ("#4d4a4b", "#eceaea"),  # Grey
    "WATERMELON": ("#1c5c0e", "#ff6666"),  # Dark green
    "HONEYDEW": ("#E0E094", "#8AB532"),  # Tan green
    "COTTON CANDY": ("#ffccdb", "#24b9bc"),  # Pink
    "BANANA": ("#f2f1a9", "#bf8040"),  # Yellow
    "BLUEBERRY": ("#003d99", "#995c00"),  # Blue
    "PASSIONFRUIT": ("#7b1157", "#e2e046"),  # Purple
    "COCONUT": ("#965a3e", "#fff2e6"),  # Brown
    "MANGO": ("#f4bb44", "#f46344"),  # Orange
    "LIME": ("#009900", "#ffff66"),  # Lime
    "LEMON": ("#ffff66", "#009900"),  # Yellow
    "PUMPKIN PIE": ("#D97A3B", "#F0A03A"),  # Orange
    "GRAPE": ("#6f2da8", "#E3B8C3"),  # Purple
    "GUAVA": ("#b6c360", "#ec6a4b"),  # Yucky Green
    "TOMATO": ("#ff6347", "#6dc242"),  # Red
    "HONEY": ("#f9c901", "#985b10"),  # Yellow
    "STRAWBERRY MILK": ("#fc5c8c", "#fbd8d8"),  # Pink
}

b, f = loadColor()
win.configure(background=b)
change()

frame = Frame(win, background=b)
frame.pack(pady=100)
framePack = frame.pack_info()

labelMain = Label(win, text="PYTUTOR", foreground=f, background=b, font=("impact", 40))
labelMain.place(anchor=N, relx=.5, rely=.01)

btN = Button(win, text="NEW", width=10, padx=20, pady=10, command=add_courses, relief=RAISED, bd=5, font="impact", bg=f, fg=b, activebackground=b,activeforeground=f)
btN.place(anchor=N, relx=.08, rely=.02)
btM = Button(win, text="MENU", width=10, padx=20, pady=10, bg=f, fg=b, activebackground=b,activeforeground=f, command=openMenuWindow,relief=RAISED, bd=5, font="impact")
btM.place(anchor=N, relx=.2, rely=.02)

prev_button = Button(win, text="⮜—",font=("Impact", 20), height=2, width=15,relief=RAISED, bd=5,command=previous_page, bg=f, fg=b, activebackground=b,activeforeground=f)
prev_button.place(relx=.04, rely=.8)
next_button = Button(win, text="—⮞",font=("Impact", 20), height=2, width=15,relief=RAISED, bd=5, command=next_page, bg=f, fg=b, activebackground=b,activeforeground=f)
next_button.place(relx=.8, rely=.8)

update_courses_list()
win.mainloop()
connection.close()
