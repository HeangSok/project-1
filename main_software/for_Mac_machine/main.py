import tkinter.messagebox
from tkinter import *
from PIL import ImageTk, Image # to install: pip3 install pillow
from time import *
from dataset_window import dataset
import json
import os

# todo:-----------define_function------------

def date_time(run = True):
    """Real-time clock"""
    # global time_label, day_label, date_label
    if run:
        time_string = strftime("%I:%M:%S %p")
        time_label.config(text=time_string)

        day_string = strftime("%A")
        day_label.config(text=day_string)

        date_string = strftime("%B %d, %Y")
        date_label.config(text=date_string)
        home_frame.after(1000, date_time)  # use recursive technique; this function allows the frame1 to update in every 1000ms


def about_info():
    """About this software"""
    tkinter.messagebox.showinfo("Information", "This software is built by student: Heang Sok.")
    print("Note: If you run this software on MAC, the OS shows unexpected warning sometimes.",
          "\n\t  Some widgets, especially messagebox, in tkinter are not compatible with MAC OS.")


def back_to_home_window(screen):
    """Back to login window"""
    screen.destroy()
    home_window()


def go_to_dataset_window():
    """Go to dataset window"""
    if check_credential():
        date_time(run=False)
        root.destroy()
        dataset()


def check_credential():
    """Check credential when login """
    count = 0
    input_username = home_username_entry.get()
    input_password = home_password_entry.get()
    default_value = {
        "admin": {
            "contact": "admin",
            "password": "admin",
        }
    }
    # Acknowledgement: this technique is learnt from Udemy.com => Dr Angela Yu
    if len(input_username) == 0 or len(input_password) == 0:
        tkinter.messagebox.showinfo("Empty Fields", "Please! Fill in all required entry fields.")
        print("Note: If you run this software on MAC, the OS shows unexpected warning sometimes.",
              "\n\t  Some widgets, especially messagebox, in tkinter are not compatible with MAC OS.")
    else:
        try:
            with open("profile.json", "r") as json_file:  # todo: consider using sqlite instead of json
                # Reading old data
                old_data = json.load(json_file)
        except:
            with open("profile.json", "w") as json_file:
                # convert python object, in this case new_profile(type: dictionary) to json object
                json.dump(default_value, json_file, indent=4)
                tkinter.messagebox.showinfo("Content Not Found", f"Content not found. Please! Try again.")
                print("Note: If you run this software on MAC, the OS shows unexpected warning sometimes.",
                      "\n\t  Some widgets, especially messagebox, in tkinter are not compatible with MAC OS.")
        else:
            # these codes execute only if no exceptions were raised in the try block

            if input_username in old_data:
                for key in list(old_data):  # turn it to a list first, don't use .keys() or .items() function because it will show RuntimeError
                    if old_data[key]["password"] == input_password and key == input_username:
                        return True
                        break
                    else:
                        count += 1

                if count == len(list(old_data)):
                    tkinter.messagebox.showinfo("Invalid Information", f"Invalid username or password. Please! Try again.")
                    print("Note: If you run this software on MAC, the OS shows unexpected warning sometimes.",
                          "\n\t  Some widgets, especially messagebox, in tkinter are not compatible with MAC OS.")
            else:
                tkinter.messagebox.showinfo("Invalid Information", f"Please! Check your username again.")
                print("Note: If you run this software on MAC, the OS shows unexpected warning sometimes.",
                      "\n\t  Some widgets, especially messagebox, in tkinter are not compatible with MAC OS.")
        finally:
            home_username_entry.delete(0, END)
            home_password_entry.delete(0, END)

    return False


# *-----------------------------------------------------------------------------------------*
# |--------------------------change_password_function_block---------------------------------|
# |_________________________________________________________________________________________|
def save_new_password():
    """Save new password"""
    count = 0
    old_username = old_user_entry.get()
    old_password = old_password_entry.get()
    new_password = new_password_entry.get()
    default_value = {
        "default_name": {
            "contact": "defaul_value",
            "password": "defaul_value",
        }
    }
    # Acknowledgement: this technique is learnt from Udemy.com => Dr Angela Yu
    if len(old_username) == 0 or len(old_password) == 0 or len(new_password) == 0:
        tkinter.messagebox.showinfo("Empty Fields", "Please! Fill in all required entry fields.")
        print("Note: If you run this software on MAC, the OS shows unexpected warning sometimes.",
              "\n\t  Some widgets, especially messagebox, in tkinter are not compatible with MAC OS.")
    else:
        try:
            with open("profile.json", "r") as json_file:
                # Reading old data
                old_data = json.load(json_file)
        except:
            with open("profile.json", "w") as json_file:
                # convert python object, in this case new_profile(type: dictionary) to json object
                json.dump(default_value, json_file, indent=4)
                tkinter.messagebox.showinfo("Content Not Found", f"Content not found. Please! Try again.")
                print("Note: If you run this software on MAC, the OS shows unexpected warning sometimes.",
                      "\n\t  Some widgets, especially messagebox, in tkinter are not compatible with MAC OS.")
        else:
            # these codes execute only if no exceptions were raised in the try block

            if old_username in old_data:
                for key in list(old_data):  # turn it to a list first, don't use .keys() or .items() function because it will show RuntimeError
                    if old_data[key]["password"] == old_password and key == old_username:
                        old_data[key]["password"] = new_password
                        new_data = old_data
                        with open("profile.json", "w") as json_file:
                            json.dump(new_data, json_file, indent=4)
                        break
                    else:
                        count += 1

                if count == len(list(old_data)):
                    tkinter.messagebox.showinfo("Invalid Information", f"Invalid username or password. Please! Try again.")
                    print("Note: If you run this software on MAC, the OS shows unexpected warning sometimes.",
                          "\n\t  Some widgets, especially messagebox, in tkinter are not compatible with MAC OS.")
            else:
                tkinter.messagebox.showinfo("Invalid Information", f"Please! Check your username again.")
                print("Note: If you run this software on MAC, the OS shows unexpected warning sometimes.",
                      "\n\t  Some widgets, especially messagebox, in tkinter are not compatible with MAC OS.")
        finally:
            old_user_entry.delete(0, END)
            old_password_entry.delete(0, END)
            new_password_entry.delete(0, END)

def change_password_window():
    """Change Password window."""
    global edit_profile_screen, edit_profile_frame_1, old_user_entry, old_password_entry, new_password_entry

    edit_profile_screen = Toplevel() # todo: find a way to make it popup in the middle of the screen
    edit_profile_screen.config(padx=50, pady=50, bg="light yellow")
    edit_profile_screen.title("Change Password Window")

    edit_profile_frame_1 = Frame(edit_profile_screen, bg="light yellow")
    edit_profile_frame_1.grid(row=0, column=0)

    # set up a page logo
    logo_label = Label(edit_profile_frame_1, image=logo_img, bg="light yellow")
    logo_label.grid(row=0, column=1, columnspan=2, pady=(0,20))

    # setup labels and put it into edit_profile_screen
    old_user_label = Label(edit_profile_frame_1, text="Username:", bg="light yellow")
    old_user_label.grid(row=1, column=0, sticky=E)
    old_password_label = Label(edit_profile_frame_1, text="Old Password:", bg="light yellow")
    old_password_label.grid(row=2, column=0, sticky=E)
    new_password_label = Label(edit_profile_frame_1, text="New Password:", bg="light yellow")
    new_password_label.grid(row=3, column=0, sticky=E)

    # setup entries and put it into edit_profile_screen
    old_user_entry = Entry(edit_profile_frame_1, width=35)
    old_user_entry.grid(row=1, column=1, columnspan=2)
    old_user_entry.focus()
    old_password_entry = Entry(edit_profile_frame_1, width=35)
    old_password_entry.grid(row=2, column=1, sticky=W + E)
    new_password_entry = Entry(edit_profile_frame_1, width=35)
    new_password_entry.grid(row=3, column=1, sticky=W + E)

    # set button
    login_button = Button(edit_profile_frame_1, text="SAVE PASSWORD", width=16, command=lambda: save_new_password())
    login_button.grid(row=4, column=1, columnspan=2, sticky=W + E)
    back_button = Button(edit_profile_frame_1, text="BACK TO HOME", width=16, command=lambda: back_to_home_window(edit_profile_screen))
    back_button.grid(row=5, column=1, columnspan=2, sticky=W + E)
    exit_button = Button(edit_profile_frame_1, text="EXIT PROGRAM", width=16, command=lambda: quit())
    exit_button.grid(row=6, column=1, columnspan=2, sticky=W + E)


# *-----------------------------------------------------------------------------------------*
# |--------------------------------profile_function_block-----------------------------------|
# |_________________________________________________________________________________________|

def save_profile():
    """Save new profile."""
    can_save = True
    username = user_entry.get()
    contact = contact_entry.get()
    password = password_entry.get()
    new_profile = {
        username: {
            "contact": contact,
            "password": password,
        }
    }
    # Acknowledgement: this technique is learnt from Udemy.com => Dr Angela Yu
    if len(username) == 0 or len(password) == 0 or contact == "@griffituni.edu.au":
        tkinter.messagebox.showinfo("Empty Fields", "Please! Fill in all required entry fields.")
        print("Note: If you run this software on MAC, the OS shows unexpected warning sometimes.",
              "\n\t  Some widgets, especially messagebox, in tkinter are not compatible with MAC OS.")
    else:
        try:
            with open("profile.json", "r") as json_file:
                # Reading old data
                old_data = json.load(json_file)

        except FileNotFoundError:
            with open("profile.json", "w") as json_file:
                # convert python object, in this case new_profile(type: dictionary) to json object
                json.dump(new_profile, json_file, indent=4)
        else:
            # these codes execute only if no exceptions were raised in the try block
            if username not in old_data:
                for key in list(old_data):  # turn it to a list first, don't use .keys() or .items() function because it will show RuntimeError
                    if old_data[key]["contact"] == contact:
                        tkinter.messagebox.showinfo("Invalid Information!",
                                                    f"Please choose another email! '{contact}' is already existed.")
                        print("Note: If you run this software on MAC, the OS shows unexpected warning sometimes.",
                              "\n\t  Some widgets, especially messagebox, in tkinter are not compatible with MAC OS.")
                        can_save = False
                        break

                if can_save:
                    # Updating old data with new data
                    old_data.update(new_profile)
                    with open("profile.json", "w") as json_file:
                        #Saving updated data
                        json.dump(old_data, json_file, indent=4)
            else:
                tkinter.messagebox.showinfo("Invalid Information!", f"Please choose another username! '{username}' is already existed.")
                print("Note: If you run this software on MAC, the OS shows unexpected warning sometimes.",
                      "\n\t  Some widgets, especially messagebox, in tkinter are not compatible with MAC OS.")
        finally:
            user_entry.delete(0, END)
            password_entry.delete(0, END)
            contact_entry.delete(0, END)
            contact_entry.insert(0, "@griffituni.edu.au")

def profile_window():
    """Set up a new profile."""
    global profile_screen, user_entry, contact_entry, password_entry, email_default_text
    profile_screen = Toplevel() # todo: find a way to make it popup in the middle of the screen
    profile_screen.config(padx=50, pady=50, bg="light yellow")
    profile_screen.title("Profile Window")

    # logo image
    logo_label = Label(profile_screen, image=logo_img, bg="light yellow")
    logo_label.grid(row=0, column=0, columnspan=3, pady=20)

    # Todo: setup labels and put it into profile_screen
    user_label = Label(profile_screen, text="Username:", bg="light yellow")
    user_label.grid(row=1, column=0, sticky=E)
    contact_label = Label(profile_screen, text="Contact:", bg="light yellow")
    contact_label.grid(row=2, column=0, sticky=E)
    password_label = Label(profile_screen, text="Password:", bg="light yellow")
    password_label.grid(row=3, column=0, sticky=E)

    # Todo: setup entries and put it into profile_screen
    user_entry = Entry(profile_screen, width=35)
    user_entry.grid(row=1, column=1, columnspan=2)
    user_entry.focus()
    # set default text using Stringvar; you can use insert function which is much simpler
    email_default_text = StringVar(profile_screen, value="@griffituni.edu.au")
    contact_entry = Entry(profile_screen, width=35, textvariable=email_default_text,fg="gray")
    contact_entry.grid(row=2, column=1, columnspan=2)
    password_entry = Entry(profile_screen, width=18)
    password_entry.grid(row=3, column=1, sticky=W + E)

    # Todo: setup buttons and put it into profile_screen
    save_button = Button(profile_screen, text="SAVE", command=lambda: save_profile())
    save_button.grid(row=3, column=2, sticky=W + E)
    back_button = Button(profile_screen, text="BACK", width=18, command=lambda: back_to_home_window(profile_screen))
    back_button.grid(row=4, column=1, sticky=W + E)
    exit_button = Button(profile_screen, text="EXIT PROGRAM", width=16, command=lambda: quit())
    exit_button.grid(row=4, column=2, sticky=W + E)


# *-----------------------------------------------------------------------------------------*
# |----------------------------------home_function_block------------------------------------|
# |_________________________________________________________________________________________|

def home_window():
    """Login window."""
    global logo_img, img_list  # you have to set the variable that store the image to global or the image won't show
    global home_frame, time_label, day_label, date_label, home_username_entry, home_password_entry
    logo_img = PhotoImage(file=os.path.join('images', 'griffthuni 128x128.png'))
    home_frame = Frame(root, bg="light yellow")
    home_frame.place(relx=0, rely=0, width=1350, height=750)
    # logo
    logo_lable = Label(home_frame, image=logo_img, bg="light yellow")
    logo_lable.place(x=660, y=35)
    # title
    title = Label(home_frame, font=("PT Mono", 35, "bold"), bg="light yellow", text="New York Restaurant Inspection")
    title.place(x=360, y=200)
    # username
    home_username = Label(home_frame, font=("PT Mono", 20, "bold"), bg="light yellow", text="Username: ")
    home_username.place(x=370+120, y=240+40)
    home_username_entry = Entry(home_frame, width=25)
    home_username_entry.place(x=500+120, y=237+40)
    home_username_entry.focus()  # automatically put the cursor inside your entry
    # password
    home_password = Label(home_frame, font=("PT Mono", 20, "bold"), bg="light yellow", text="Password: ")
    home_password.place(x=370+120, y=280+40)
    home_password_entry = Entry(home_frame, width=25)
    home_password_entry.place(x=500+120, y=277+40)
    # buttons
    login_button = Button(home_frame, text="LOGIN", width=26, command=lambda: go_to_dataset_window())
    login_button.place(x=500+120, y=320+40)
    profile_button = Button(home_frame, text="SET UP PROFILE", width=26, command=lambda: profile_window())
    profile_button.place(x=500+120, y=360+40)
    edit_button = Button(home_frame, text="CHANGE PASSWORD", width=26, command=lambda: change_password_window())
    edit_button.place(x=500+120, y=400+40)
    about_button = Button(home_frame, text="About", width=26, command=lambda: about_info())
    about_button.place(x=500+120, y=440+40)
    exit_button = Button(home_frame, text="EXIT", width=26, command=lambda: quit())
    exit_button.place(x=500+120, y=480+40)

    # footer decoration => time and date
    # TODO: set up labels for real-time clock
    time_label = Label(home_frame, font=("Arial", 16), bg="light yellow", width=22)
    time_label.place(x=400-105-33, y=520+15+40+30)  # don't use it on the same line with Label(); you wont be able to use .config function; and i may cause some errors.
    day_label = Label(home_frame, font=("PT Mono", 16), bg="light yellow", width=20)
    day_label.place(x=400-105-33, y=545+15+40+30)
    date_label = Label(home_frame, font=("PT Mono", 16), bg="light yellow", width=20)
    date_label.place(x=400-105-33, y=570+15+40+30)
    date_time()  # call the clock

    # footer decoration => button
    img_list = []
    # Acknowledgement: All the images below are taken from Dr. Angela Yu
    for img in os.listdir("./images/png wallpapers"):
        i = Image.open(f"./images/png wallpapers/{img}")
        img_list.append(i)

    Button(home_frame, text="G", fg="black", font=("Party LET", 25), width=5, height=3,
           command=lambda: img_list[0].show()).place(x=500-33, y=520+40+30)
    Button(home_frame, text="R", fg="black", font=("Party LET", 25), width=5, height=3,
           command=lambda: img_list[1].show()).place(x=570-33, y=520+40+30)
    Button(home_frame, text="I", fg="black", font=("Party LET", 25), width=5, height=3,
           command=lambda: img_list[2].show()).place(x=640-33, y=520+40+30)
    Button(home_frame, text="F", fg="black", font=("Party LET", 25), width=5, height=3,
           command=lambda: img_list[3].show()).place(x=710-33, y=520+40+30)
    Button(home_frame, text="F", fg="black", font=("Party LET", 25), width=5, height=3,
           command=lambda: img_list[4].show()).place(x=780-33, y=520+40+30)
    Button(home_frame, text="I", fg="black", font=("Party LET", 25), width=5, height=3,
           command=lambda: img_list[5].show()).place(x=850-33, y=520+40+30)
    Button(home_frame, text="T", fg="black", font=("Party LET", 25), width=5, height=3,
           command=lambda: img_list[6].show()).place(x=920-33, y=520+40+30)
    Button(home_frame, text="H", fg="black", font=("Party LET", 25), width=5, height=3,
           command=lambda: img_list[7].show()).place(x=990-33, y=520+40+30)
    Button(home_frame, text="!", fg="black", font=("Party LET", 25), width=5, height=3,
           command=lambda: quit()).place(x=1060-33, y=520+40+30)

# todo:-----------define_variable------------
WINDOW_SIZE = "1350x750"

# todo:-----------initial_configure------------
# window configuration
def window():
    global root
    root = Tk()
    root.title('New York Restaurant Inspection')
    icon = PhotoImage(file=os.path.join('images', 'griffthuni.png'))  # use os to make the path works for cross platform
    root.iconphoto(False, icon)  # note this window icon don't work on mac
    root.geometry(WINDOW_SIZE)  # set window size
    root.pack_propagate(False)  # tell the widow that don't resize yourself based on the content
    root.resizable(0,0)  # don't allow the user to resize the window


window()
home_window()
root.mainloop()