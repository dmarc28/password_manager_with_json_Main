from tkinter import *
import random
import string
from ttkthemes import ThemedTk
app = ThemedTk(theme="clearlooks")
app.title("Password Manager")
app.config(bg="#BEF0CB", padx=40, pady=40)



app = ThemedTk(theme="clearlooks")
app.title("Password Manager")
app.config(bg="#BEF0CB", padx=40, pady=40)


def add_new_letter(start_x, y):
    width = app.winfo_screenwidth()
    height = app.winfo_screenheight()
    x = start_x
    letters = random.choice(string.ascii_letters + string.digits)
    label = Label(app, text=letters, font=("Arial", 20), bg="white", fg="black")
    label.grid(row=0, column=x)
    if y < height:
        y += 5
        label.grid(row=y, column=x)
        app.after(50, add_new_letter, start_x, y)


app.configure(bg="black")
app.after(50, add_new_letter, 0, 0)
app.after(50, add_new_letter, 1, 0)
app.after(50, add_new_letter, 2, 0)

add_new_letter(0, 0)
add_new_letter(1, 0)
add_new_letter(2, 0)

canvas = Canvas(app, bg="white")
canvas.grid(row=0, column=0, columnspan=3, rowspan=3, sticky="nsew")

button = Button(app, text="Button")
button.grid(row=3, column=0, columnspan=3, sticky="ew")

label = Label(app, text="Label")
label.grid(row=4, column=0, columnspan=3, sticky="ew")


app.mainloop()