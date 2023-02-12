import tkinter.messagebox
from random import shuffle
from tkinter import font
import pyperclip
import json
from ttkthemes import ThemedTk
from tkinter import *
import random
import string

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def create_pass():
    password1 = [random.choice(string.ascii_letters) for _ in range(random.randint(3, 5))]
    password2 = [str(random.randint(0, 9)) for _ in range(random.randint(3, 4))]
    password3 = [random.choice(symbols) for _ in range(random.randint(3, 5))]

    combined_password = password1 + password2 + password3
    shuffle(combined_password)
    password = "".join(combined_password)
    print(password)

    input_password.delete(0, END)
    input_password.insert(0, f"{password}")
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def entry_valid():
    website = input_website.get()
    email = input_username.get()
    password = input_password.get()
    if len(website) > 3:
        website = website.lower()
        if ".com" in email:
            email = email
            if len(password) > 4:
                password = password
                new_data = {website: {"email": email, "password": password}}
                try:
                    with open('data.json', 'r') as data_f:
                        data = json.load(data_f)
                except FileNotFoundError:
                    with open('data.json', 'w') as data_f:
                        json.dump(new_data, data_f, indent=4)
                else:
                    data.update(new_data)
                    with open("data.json", "w") as data_f:
                        json.dump(data, data_f, indent=4)
                finally:
                    with open('data.json', 'r') as data_f:
                        data = json.load(data_f)
                        keys = set(data.keys())
                        new_keys = set(new_data.keys())
                        if new_keys.intersection(keys):
                            ask = tkinter.messagebox.askyesno(title="Replace?",
                                                              message="Do you want to replace the current password")
                            if ask:
                                tkinter.messagebox.showinfo(title="Saved", message="Your password have been saved")
                                input_website.delete(0, END)
                                input_password.delete(0, END)
                        else:
                            tkinter.messagebox.showinfo(title="Saved", message="Your password have been saved")
                            input_website.delete(0, END)
                            input_password.delete(0, END)
            else:
                tkinter.messagebox.showerror(title="Unsafe Password", message="Try longer password ")
        else:
            tkinter.messagebox.showerror(title="Email", message="Invalid Email")
    else:
        tkinter.messagebox.showerror(title="Website", message="Invalid Website")


# ---------------------------- FETCH PASSWORD ------------------------------- #


def search_data():
    website = (input_website.get()).lower()
    try:
        with open('data.json', 'r') as data_f:
            data = json.load(data_f)
    except FileNotFoundError:
        tkinter.messagebox.showerror(title=website, message="No password found")
    except NameError:
        tkinter.messagebox.showerror(title=website, message="No password found")
    except json.decoder.JSONDecodeError:
        tkinter.messagebox.showerror(title=website, message="The file is not in a valid JSON format")
    else:
        keys = data.keys()
        found = False
        for i in keys:
            if i == website:
                found = True
                print(data[website]["password"])
                print(data[website]["email"])
                tkinter.messagebox.showinfo(title=website, message=f'user id: {(data[website]["email"])} and '
                                                                   f'password: {(data[website]["password"])}')
                break
        if not found:
            tkinter.messagebox.showerror(title=website, message="No password found")


# ---------------------------- EVENTS ------------------------------- #


def on_entry_focus_in(event):
    event.widget.config(bg='#C9F4AA')


def on_entry_focus_out(event):
    event.widget.config(bg='#B5F1CC')


# ---------------------------- UI SETUP ------------------------------- #


app = ThemedTk(theme="clear-looks")
app.title("Password Manager")
app.config(bg="#BEF0CB", padx=40, pady=40)


def add_new_letter():
    x, y = random.randint(-15, 430), 0
    letter_num_string = random.choice(string.ascii_letters + string.digits)
    # my_colors_extended = ["red", "blue", "green", "yellow", "orange", "purple", "pink", "brown", "gray", "white"]
    my_colors = ["white", "blue", "gray", "purple", "#16FF00"]
    colors = random.choice(my_colors)
    label = Label(app, text=letter_num_string, font=("Arial", 12), bg="black", fg=colors)
    label.grid(row=0, column=0, columnspan=3)
    label.config(padx=5, pady=10)
    label.place(x=x, y=y)

    if x < height:
        x += 10
        label.place(x=x, y=y)
        app.after(10, add_new_letter)


width = app.winfo_screenwidth()
height = app.winfo_screenheight()


app.configure(bg="black")
add_new_letter()


canvas = Canvas(width=200, bg='black', height=200, highlightthickness=0)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(row=1, column=1, sticky="nsew")


# labels

my_font = my_font_except_add_button = font.Font(family="Calibre", size=11, weight="normal")
my_font_for_add_button = font.Font(family="Calibre", size=12, weight="bold")

label_web = Label(text="Website", bg="black", justify="left", fg="#16FF00", font=my_font)
label_web.grid(row=3, column=0, sticky="ew")
label_web.config(pady=5)
label_web.rowconfigure(1, weight=1)

label_username = Label(text="Email/Username", bg="black", justify="left", fg="#16FF00", font=my_font)
label_username.columnconfigure(1, weight=1)
label_username.grid(row=4, column=0)
label_username.config(pady=5)

label_password = Label(text="Password", bg="black", justify="left", fg="#16FF00", font=my_font)
label_password.grid(row=5, column=0)
label_password.config(pady=5)
label_password.rowconfigure(1, weight=1)


# Button


button = tkinter.Button(fg="Black", bg="Black", highlightcolor="Black", highlightthickness=0)
button.config(state="disabled")
button.grid(row=0, column=0, columnspan=3)


button_pass_add = Button(bg="#0F6292", fg="white", command=entry_valid, font=my_font_for_add_button)
button_pass_add.grid(row=6, column=1, sticky="nsew")
button_pass_add.config(width=7)
button_pass_add.config(padx=-2, pady=-1)

button_search = Button(text="Search", bg="#0F6292", fg="#16FF00", command=search_data, font=my_font)
button_search.grid(row=3, column=2, sticky="ew")
button_search.config(width=14, height=1)
button_search.config(padx=-2, pady=-1)

button_pass_gen = Button(text="Generate Password", bg="#0F6292", fg="#16FF00", command=create_pass, font=my_font)
button_pass_gen.grid(row=5, column=2, sticky="ew")
button_pass_gen.config(padx=-2, pady=-1)

button_pass_add = Button(text="Add", bg="#0F6292", fg="white", command=entry_valid, font=my_font_for_add_button)
button_pass_add.grid(row=6, column=1, sticky="nsew")
button_pass_add.config(width=7)
button_pass_add.config(padx=-2, pady=-1)


# Entry

input_website = Entry(width=24, highlightthickness=2, highlightcolor="#FFE7CC")
input_website.grid(row=3, column=1, columnspan=1)
input_website.focus()
input_website.bind('<FocusIn>', on_entry_focus_in)
input_website.bind('<FocusOut>', on_entry_focus_out)
input_username = Entry(app, width=42, highlightcolor="#FFE7CC", highlightthickness=2)
input_username.bind('<FocusIn>', on_entry_focus_in)
input_username.bind('<FocusOut>', on_entry_focus_out)
input_username.grid(row=4, column=1, columnspan=2)
input_username.insert(END, "ar.chowdhury28@gmail.com")
input_password = Entry(width=24, highlightthickness=2, highlightcolor="#FFE7CC", show="#")
input_password.bind('<FocusIn>', on_entry_focus_in)
input_password.bind('<FocusOut>', on_entry_focus_out)
input_password.grid(row=5, column=1)

app.mainloop()
