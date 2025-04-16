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

def open_quiz(lesson):
    global quizWindow, lessonLabel
    lesson_id, course_id, lesson_name, material, type = lesson
    if quizWindow is not None:
        quizWindow.focus()
        return

    cursor.execute("SELECT id, question, answer, correct FROM Quizes WHERE lesson_id=?", (lesson_id,))
    quiz_data = cursor.fetchall()

    quizWindow = Toplevel(win)
    quizWindow.title("Quiz")
    quizWindow.state("zoomed")
    quizWindow.configure(background="black")

    lessonLabel = Label(quizWindow, text=f"{lesson_name}", font=("impact", 25), background="black", foreground="white")
    lessonLabel.pack(side=TOP)

    quiz_frames = []

    for quiz_id, question, answer, correct in quiz_data:
        question_frame = Frame(quizWindow, background="red", pady=10)
        question_frame.pack()

        question_label = Label(question_frame, text=f"Q: {question}", font=("Impact", 15), background="black",foreground="white", wraplength=800, justify=LEFT)
        question_label.pack()

        options = answer.split("|")
        selected = IntVar(value=int(correct))

        radio_buttons = []
        for i, opt in enumerate(options, 1):
            rb = Radiobutton(question_frame, text=opt.strip(), variable=selected, value=i,font=("Arial", 12), background="black", foreground="white", selectcolor="red",state="disabled")
            rb.pack(anchor="w", padx=20)
            radio_buttons.append(rb)

        # Store everything so we can edit/save later
        quiz_frames.append({
            "frame": question_frame,
            "quiz_id": quiz_id,
            "question_label": question_label,
            "radio_buttons": radio_buttons,
            "selected": selected,
            "options": options
        })

    def edit_quizzes():
        global dropper,btn_add_ans,btn_remove_ans
        for qf in quiz_frames:
            # Replace question label with an Entry
            q_text = qf["question_label"].cget("text")[3:].strip()  # remove "Q: "
            ent = Entry(qf["frame"], font=("Arial", 12), width=80)
            ent.insert(END, q_text)
            qf["question_label"].pack_forget()
            ent.pack()
            qf["ent_question"] = ent

            # Remove existing radio buttons
            for rb in qf["radio_buttons"]:
                rb.pack_forget()

            # Add editable Entries for each existing answer
            new_opts = []
            for opt_text in qf["options"]:
                opt_entry = Entry(qf["frame"], font=("Arial", 12), width=60)
                opt_entry.insert(END, opt_text.strip())
                opt_entry.pack(anchor="w", padx=20)
                new_opts.append(opt_entry)

            qf["ent_options"] = new_opts

            # Function to update correct dropdown list
            def refresh_correct_dropdown(q):
                q["correct_dropdown"].configure(values=[str(i + 1) for i in range(len(q["ent_options"]))])
                if int(q["ent_correct"].get()) > len(q["ent_options"]):
                    q["ent_correct"].set("1")

            # Function to add a new answer
            def add_answer_field(q=qf):
                new_opt_entry = Entry(q["frame"], font=("Arial", 12), width=60)
                new_opt_entry.insert(END, "New Option")
                new_opt_entry.pack(anchor="w", padx=20)
                q["ent_options"].append(new_opt_entry)
                refresh_correct_dropdown(q)

            # Function to remove the last answer
            def remove_last_answer(q=qf):
                if len(q["ent_options"]) > 1:  # optional safety: keep at least 1
                    last_entry = q["ent_options"].pop()
                    last_entry.destroy()
                    refresh_correct_dropdown(q)

            # Create the correct answer dropdown
            correct_var = StringVar(value=str(qf["selected"].get()))
            dropper = ttk.Combobox(qf["frame"], textvariable=correct_var,values=[str(i + 1) for i in range(len(new_opts))],state="readonly", width=5)
            dropper.pack(anchor="w", padx=20)
            qf["ent_correct"] = correct_var
            qf["correct_dropdown"] = dropper

            # Buttons to add and remove answers
            btn_add_ans = Button(qf["frame"], text="➕ Add Answer", command=lambda q=qf: add_answer_field(q))
            btn_add_ans.pack(anchor="w", padx=20, pady=5)

            btn_remove_ans = Button(qf["frame"], text="➖ Remove Last Answer",command=lambda q=qf: remove_last_answer(q))
            btn_remove_ans.pack(anchor="w", padx=20, pady=5)

        btEdit.pack_forget()
        btSave.pack(pady=5, side=TOP)
        btDelete.pack(btDelete.pack_info())

    def save_quizzes():
        for qf in quiz_frames:
            dropper.pack_forget()
            btn_add_ans.pack_forget()
            btn_remove_ans.pack_forget()
            quiz_id = qf["quiz_id"]
            new_question = qf["ent_question"].get().strip()
            new_options = [e.get().strip() for e in qf["ent_options"]]
            new_correct = int(qf["ent_correct"].get().strip())

            new_answer_str = "|".join(new_options)

            # Update DB
            cursor.execute(
                "UPDATE Quizes SET question=?, answer=?, correct=? WHERE id=?",
                (new_question, new_answer_str, new_correct, quiz_id)
            )

            # Clear old widgets (edit mode)
            qf["ent_question"].destroy()
            for e in qf["ent_options"]:
                e.destroy()
            # Remove dropper
            qf["ent_correct"].widget = None

            # Rebuild static view (label + radio buttons)
            question_label = Label(qf["frame"], text=f"Q: {new_question}", font=("Impact", 15),
                                   background="black", foreground="white", wraplength=800, justify=LEFT)
            question_label.pack()
            qf["question_label"] = question_label

            selected = IntVar(value=new_correct)
            qf["selected"] = selected
            radio_buttons = []
            for i, opt in enumerate(new_options, 1):
                rb = Radiobutton(qf["frame"], text=opt, variable=selected, value=i,font=("Arial", 12), background="black", foreground="white", selectcolor="red",state="disabled")
                rb.pack(anchor="w", padx=20)
                radio_buttons.append(rb)
            qf["radio_buttons"] = radio_buttons
            qf["options"] = new_options

        connection.commit()

        btSave.pack_forget()
        btn_add_ans.pack_forget()
        btEdit.pack(pady=5, side=TOP)
        btDelete.pack(btDelete.pack_info())

    def delete_lesson():
        cursor.execute("DELETE FROM Courses WHERE id=?", (lesson_id,))
        cursor.execute("DELETE FROM Quizes WHERE lesson_id=?", (lesson_id,))
        connection.commit()
        on_closing_quiz_window()
        update_lesson_list(course_id)

    btEdit = Button(quizWindow, text="Edit", command=edit_quizzes, width=10, relief=RAISED, bd=5)
    btEdit.pack(pady=5, side=TOP)

    btSave = Button(quizWindow, text="Save", command=save_quizzes, width=10, relief=RAISED, bd=5)
    btSave.pack_forget()

    btDelete = Button(quizWindow, text="Delete", command=delete_lesson, width=10, relief=RAISED, bd=5)
    btDelete.pack(pady=5, side=TOP)
    quizWindow.protocol("WM_DELETE_WINDOW", on_closing_quiz_window)

def back():
    lesson_frame.pack_forget()
    frame.pack(framePack)
    btB.place_forget()
    btLA.place_forget()
    btQA.place_forget()
    btN.place(NPlacement)

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
            button_text = f"📝 {lesson_name}"
            button_color = "grey"
            button_command = lambda q=lesson: open_quiz(q)
        else:
            button_text= lesson_name
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
