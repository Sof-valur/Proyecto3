# Import modules #
import tkinter
import os


# Delete login success window function #
def del_pass_not_recognized():
    screen_4.destroy()


# Delete login success window function #
def del_user_not_found():
    screen_5.destroy()


# Login success function #
def login_success():
    screen_8 = tkinter.Toplevel(screen)
    screen_8.title("Dashboard")
    screen_8.geometry("700x500")
    tkinter.Label(screen_8, text="Welcome to the dashboard").pack()
    tkinter.Button(screen_8, text="Create notes").pack()
    tkinter.Button(screen_8, text="View notes").pack()
    tkinter.Button(screen_8, text="Delete notes").pack()


# password not recognized function #
def password_not_recognized():
    global screen_4
    screen_4 = tkinter.Toplevel(screen)
    screen_4.title("Success")
    screen_4.geometry("700x500")
    tkinter.Label(screen_4, text="Password Error").pack()
    tkinter.Button(screen_4, text="OK", command=del_pass_not_recognized()).pack()


# username not found function #
def username_not_found():
    global screen_5
    screen_5 = tkinter.Toplevel(screen)
    screen_5.title("Success")
    screen_5.geometry("700x500")
    tkinter.Label(screen_5, text="Username not found").pack()
    tkinter.Button(screen_5, text="OK", command=del_user_not_found()).pack()


# Register use function #
def register_user():
    username_info = username.get()
    password_info = password.get()
    email_info = email.get()
    cellphone_info = cellphone.get()

    file = open(username_info, "w")
    file.write(username_info + "\n")
    file.write(password_info + "\n")
    file.write(email_info + "\n")
    file.write(cellphone_info)
    file.close()

    username_entry.delete(0, tkinter.END)
    password_entry.delete(0, tkinter.END)
    email_entry.delete(0, tkinter.END)
    cellphone_entry.delete(0, tkinter.END)

    tkinter.Label(screen_1, text="Registration Success", fg="green", font=("Times New Roman", 11)).pack()


# Login verify function #
def login_verify():
    username_1 = username_verify.get()
    password_1 = password_verify.get()
    username_entry_1.delete(0, tkinter.END)
    password_entry_1.delete(0, tkinter.END)

    list_of_files = os.listdir()
    if username_1 in list_of_files:
        file_1 = open(username_1, "r")
        verify = file_1.read().splitlines()
        if password_1 in verify:
            login_success()
        else:
            password_not_recognized()
    else:
        username_not_found()


# Register function #
def register():
    # Register screen variable #
    global screen_1
    screen_1 = tkinter.Toplevel(screen)
    screen_1.title("Register")
    screen_1.geometry("700x500")

    # Username and password requirements #
    global username
    global password
    global email
    global cellphone
    global username_entry
    global password_entry
    global email_entry
    global cellphone_entry

    username = tkinter.StringVar()
    password = tkinter.StringVar()
    email = tkinter.StringVar()
    cellphone = tkinter.StringVar()
    # Displaying username and password on screen #
    tkinter.Label(screen_1, text="Please enter details below").pack()
    tkinter.Entry(screen_1, text="")
    tkinter.Label(screen_1, text="Username *").pack()
    username_entry = tkinter.Entry(screen_1, textvariable=username)
    username_entry.pack()
    tkinter.Label(screen_1, text="Password *").pack()
    password_entry = tkinter.Entry(screen_1, textvariable=password)
    password_entry.pack()
    tkinter.Label(screen_1, text="email *").pack()
    email_entry = tkinter.Entry(screen_1, textvariable=email)
    email_entry.pack()
    tkinter.Label(screen_1, text="Cellphone *").pack()
    cellphone_entry = tkinter.Entry(screen_1, textvariable=cellphone)
    cellphone_entry.pack()

    # Register button #
    tkinter.Label(screen_1, text="").pack()
    tkinter.Button(screen_1, text="Register", width=10, height=1, command=register_user).pack()


# Login function #
def login():
    global screen_2
    screen_2 = tkinter.Toplevel(screen)
    screen_2.title("Login")
    screen_2.geometry("700x500")
    tkinter.Label(screen_2, text="Please enter details below to login").pack()
    tkinter.Entry(screen_2, text="")

    global username_verify
    global password_verify

    username_verify = tkinter.StringVar()
    password_verify = tkinter.StringVar()

    global username_entry_1
    global password_entry_1

    tkinter.Label(screen_2, text="Username *").pack()
    username_entry_1 = tkinter.Entry(screen_2, textvariable=username_verify)
    username_entry_1.pack()
    tkinter.Label(screen_2, text="").pack()
    tkinter.Label(screen_2, text="Password *").pack()
    password_entry_1 = tkinter.Entry(screen_2, textvariable=password_verify)
    password_entry_1.pack()
    tkinter.Label(screen_2, text="").pack()
    tkinter.Button(screen_2, text="Login", width=10, height=1, command=login_verify).pack()


# Function for main screen #
def main_screen():
    # screen variables and buttons #
    global screen
    screen = tkinter.Tk()
    screen.geometry("700x500")
    screen.title("Registration")
    tkinter.Label(text="REGISTRATION", bg="grey", width="500", height="2", font=("Times New Roman", 13)).pack()
    tkinter.Label(text="").pack()
    tkinter.Button(text="Login", height="2", width="30", command=login).pack()
    tkinter.Label(text="").pack()
    tkinter.Button(text="Register", height="2", width="30", command=register).pack()

    # main screen gameloop #
    screen.mainloop()


# call main screen #
main_screen()
