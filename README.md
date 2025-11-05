# Pytutor
Code for my python tutor app
In this project i used tkinter, sqlite3, and OS. 
The function of the program is to create a tool for tutorers such as myself to build lessons plans filled with lessons and quizes. The envirmoent of it also makes it easy for teachers to use it in order to assign digital homework by requireing screenshots of passed quizes.

It is set up as a 3x4 grid of buttons for lesson plans, and uses pages with page buttons and arrow buttons for navigation. Each lesson plan button changes the page into the lesson plan contents.
Inside the lesson plan the lessons and quizes are once again in a 3x4 grid and once again useing page naviagation. The quiz button is inversered colored to distiguish from the lessons. and each lesson/quiz button opens its contents in a sepereate smaller window. The lesson is a text block that teachers can edit, the quiz is a text block and radio buttons that teachers can edit the text of and nuber of radio buttons.
Lesson plans can be shared via exporting and importing them as text files. 

There is some personilization features such as different themes, this feature is in both the tutor and student app.
The seperation of apps allows for certain functions to only be performed by teachers such as the creation of a lesson plan and edits to plans.

Code wise the information is stored in a nested databse where the lesson plan databse holds the lesson and quiz databse.
