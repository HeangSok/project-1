""" This student has separated the software functions and made it to small chunks so that it can be tested using
unittest """

import tkinter.messagebox
from tkinter import *
from tkinter import filedialog, messagebox
from datetime import datetime
import pandas as pd
import sqlite3
from PIL import Image  # to install: pip3 install pillow
from time import *
import json
import os


# note: since the original code does not have the return value, this student decided to modify parts of the original-
# code and add the return value in order to do the unit testing


# function 1
def date_time():
    """Real-time clock"""
    time_string = strftime("%I:%M:%S %p")
    day_string = strftime("%A")
    date_string = strftime("%B %d, %Y")
    return [str(time_string) + str(day_string) + str(date_string)]


# function 2
def acknowlegement():
    """About this software"""
    # note: the tkinter.messagebox.showinfo will return ok after the message is shown on the screen
    return tkinter.messagebox.showinfo("Acknowledgement", "I would like to express my gratitude to Dr Gervase Tuxworth and Teacher James Baker who have helped me in carrying out this project.")


# function 3
def check_credential(username, password):
    """Check credential when login """
    count = 0
    input_username = username
    input_password = password
    default_value = {
        "admin": {
            "contact": "admin",
            "password": "admin",
        }
    }
    # Acknowledgement: this technique is learnt from Udemy.com => Dr Angela Yu
    if len(input_username) == 0 or len(input_password) == 0:
        tkinter.messagebox.showinfo("Empty Fields", "Please! Fill in all required entry fields.")

    else:
        try:
            with open("profile.json", "r") as json_file:  # todo: consider using sqlite instead of json
                # Reading old data
                old_data = json.load(json_file)
        except:
            with open("profile.json", "w") as json_file:
                # convert python object, in this case new_profile(type: dictionary) to json object
                json.dump(default_value, json_file, indent=4)


        else:
            # these codes execute only if no exceptions were raised in the try block
            if input_username in old_data:
                for key in list(
                        old_data):  # turn it to a list first, don't use .keys() or .items() function because it will show RuntimeError
                    if old_data[key]["password"] == input_password and key == input_username:
                        return True
                        break
                    else:
                        count += 1

    return False


# function 4
# note: this code is taken from check_credential function
def open_json_file(filename):
    try:
        with open(filename, "r") as json_file:  # todo: consider using sqlite instead of json
            # Reading old data
            return True
    except:
        return False


# function 5
def save_profile(username, contact, password, filename):
    """Save new profile."""
    can_save = True
    username = username
    contact = contact
    password = password

    # Acknowledgement: this technique is learnt from Udemy.com => Dr Angela Yu
    if len(username) == 0 or len(password) == 0 or len(contact) == 0:
        return False
    else:
        try:
            with open(filename, "r") as json_file:
                # Reading old data
                old_data = json.load(json_file)

        except FileNotFoundError:
            return False
        else:
            # these codes execute only if no exceptions were raised in the try block
            if username not in old_data:
                for key in list(
                        old_data):  # turn it to a list first, don't use .keys() or .items() function because it will show RuntimeError
                    if old_data[key]["contact"] == contact:
                        can_save = False
                        break
                if can_save:
                    return True


# function 6
def open_file_dialog():
    """Open a new dataset."""
    try:
        file = filedialog.askopenfile(initialdir=".",
                                      title="Select CSV File Only",
                                      filetypes=(("CSV files", "*.csv"), ("DB files", "*.db"),
                                                 ("All Files", "*.*")))  # this function doesn't work well on mac
        filename = file.name.split("/")
        if filename[-1] == "New York Restaurant.csv":
            return True
    except:
        return False


# function 7
def loadfile(filename):
    """Load datasets to the treeview."""
    file_name = filename
    try:
        df = pd.read_csv(file_name)
        return True
    except FileNotFoundError:
        return False


# function 8
# note: this code is taken from search_by_date function
def convert_date_format(date):
    """convert date format from mm/dd/yyyy to yyyy-mm-dd to work with database"""
    date = date
    date = date.replace("/", "")
    use_date = date[4:] + "-" + date[:2] + "-" + date[2:4]
    return use_date


# function 9
def make_a_list_of_img():
    img_list = []
    # Acknowledgement: All the images below are taken from Dr. Angela Yu
    for img in os.listdir("./images/png wallpapers"):
        i = Image.open(f"./images/png wallpapers/{img}")
        img_list.append(i)
    return img_list


# function 10
# note: this code is taken from load file function
# the purpose of this code is to convert csv file to sqlite automatically
def convert_csv_to_db(filename):
    if "csv" in filename:
        df = pd.read_csv(filename)
        raw_filename = filename.replace(".csv", "")
        # create a database and connect
        db = sqlite3.connect(f"{raw_filename}.db")
        # convert dataframe to sqlite and set the table name to mytable
        data_type = {"INSPECTION DATE": "TEXT"} if raw_filename == "New York Restaurant" else None
        # convert df to db file
        try:
            df.to_sql(name='mytable', con=db, if_exists='replace', index=False, dtype=data_type)
            return True
        except:
            return False
    else:
        return False


# function 11
def search_by_date(start_date, end_date):
    query = f"""SELECT * FROM mytable 
    WHERE (substr([INSPECTION DATE],7,4)
    ||'-'||substr([INSPECTION DATE],1,2)
    ||'-'||substr([INSPECTION DATE],4,2))
    BETWEEN ('{start_date}') AND ('{end_date}')
    ORDER BY [INSPECTION DATE] ASC
    ;"""
    db = sqlite3.connect("New York Restaurant.db")
    cursor = db.cursor()
    record = cursor.execute(query)
    data = record.fetchall()

    if data:
        return True
    else:
        return False


# function 12
def search_by_date_keyword(start_date, end_date, keywords):
    query = f"""SELECT * FROM mytable 
            WHERE ((substr([INSPECTION DATE],7,4)
            ||'-'||substr([INSPECTION DATE],1,2)
            ||'-'||substr([INSPECTION DATE],4,2))
            BETWEEN ('{start_date}') AND ('{end_date}'))
            AND (CAMIS LIKE '%{keywords}%'
            OR DBA LIKE '%{keywords}%'
            OR BORO LIKE '%{keywords}%'
            OR BUILDING LIKE '%{keywords}%'
            OR STREET LIKE '%{keywords}%' 
            OR ZIPCODE LIKE '%{keywords}%'
            OR PHONE LIKE '%{keywords}%'
            OR [CUISINE DESCRIPTION] LIKE '%{keywords}%'
            OR [ACTION] LIKE '%{keywords}%'
            OR [VIOLATION CODE] LIKE '%{keywords}%'
            OR [VIOLATION DESCRIPTION] LIKE '%{keywords}%'
            OR [CRITICAL FLAG] LIKE '%{keywords}%'
            OR [SCORE] LIKE '%{keywords}%'
            OR [GRADE] LIKE '%{keywords}%'
            OR [INSPECTION TYPE] LIKE '%{keywords}%')
            ORDER BY [INSPECTION DATE] ASC
            ;"""

    db = sqlite3.connect("New York Restaurant.db")
    cursor = db.cursor()
    record = cursor.execute(query)
    data = record.fetchall()

    if data:
        return True
    else:
        return False

# function 13
def view_chart_suburbs(start_date, end_date):
    query = f"""SELECT * , COUNT([VIOLATION CODE]) AS 'NUMBERS OF VIOLATION'
    FROM mytable 
    WHERE (substr([INSPECTION DATE],7,4)
    ||'-'||substr([INSPECTION DATE],1,2)
    ||'-'||substr([INSPECTION DATE],4,2))
    BETWEEN ('{start_date}') AND ('{end_date}')
    GROUP BY [BORO]
    ORDER BY [INSPECTION DATE] ASC
    ;"""

    db = sqlite3.connect("New York Restaurant.db")
    cursor = db.cursor()
    record = cursor.execute(query)
    data = record.fetchall()
    if data:
        return True
    else:
        return False


# function 14
def view_graph_animal_related_case(start_date, end_date, suburb, animal_name):
    query = f"""SELECT *, COUNT([VIOLATION CODE]) AS 'NUMBERS OF VIOLATION'
    FROM mytable 
    WHERE BORO LIKE '%{suburb}%'
    AND [VIOLATION DESCRIPTION] LIKE '%{animal_name}%'
    AND (substr([INSPECTION DATE],7,4)
    ||'-'||substr([INSPECTION DATE],1,2)
    ||'-'||substr([INSPECTION DATE],4,2))
    BETWEEN ('{start_date}') AND ('{end_date}')
    GROUP BY [INSPECTION DATE]
    ORDER BY [INSPECTION DATE] ASC
    ;"""

    db = sqlite3.connect("New York Restaurant.db")
    cursor = db.cursor()
    record = cursor.execute(query)
    data = record.fetchall()
    if data:
        return True
    else:
        return False


# function 15
def compare_cuisine(start_date, end_date, cuisine1, cuisine2):
    query_for_cuisine1 = f"""SELECT * , COUNT([VIOLATION CODE]) AS 'NUMBERS OF VIOLATION'
       FROM mytable 
       WHERE [CUISINE DESCRIPTION] LIKE '%{cuisine1}%'
       AND (substr([INSPECTION DATE],7,4)
       ||'-'||substr([INSPECTION DATE],1,2)
       ||'-'||substr([INSPECTION DATE],4,2))
       BETWEEN ('{start_date}') AND ('{end_date}')
       GROUP BY [INSPECTION DATE]
       ORDER BY [INSPECTION DATE] ASC
       ;"""

    query_for_cuisine2 = f"""SELECT * , COUNT([VIOLATION CODE]) AS 'NUMBERS OF VIOLATION'
       FROM mytable 
       WHERE [CUISINE DESCRIPTION] LIKE '%{cuisine2}%'
       AND (substr([INSPECTION DATE],7,4)
       ||'-'||substr([INSPECTION DATE],1,2)
       ||'-'||substr([INSPECTION DATE],4,2))
       BETWEEN ('{start_date}') AND ('{end_date}')
       GROUP BY [INSPECTION DATE]
       ORDER BY [INSPECTION DATE] ASC
       ;"""

    db = sqlite3.connect("New York Restaurant.db")
    cursor = db.cursor()
    record1 = cursor.execute(query_for_cuisine1)
    data1 = record1.fetchall()

    record2 = cursor.execute(query_for_cuisine2)
    data2 = record2.fetchall()

    if data1 and data2:
        return True
    else:
        return False

# function 16
# Note: this function is taken from compare_cuisine function
def date_object(date):
    """convert a string to datetime object to work with matplotlib."""
    date_object2 = datetime.strptime(date, '%m/%d/%Y')
    return date_object2

# function 17
# Note: this function is a part of search function
def get_column_name():
    """get column name from database to place it in treeview"""
    db = sqlite3.connect("New York Restaurant.db")
    cursor = db.cursor()
    record = cursor.execute("""select * from mytable;""")
    column_name = [name[0] for name in record.description]
    if column_name:
        return True


# function 18
# note: this function is a part of dataset function
# the purpose of testing this function is to check whether the radio button in the main software is worked as required or not
def get_radio_button_value():
    root = Tk()
    root.title('Radio Button Test')
    root.geometry(("400x100"))
    label = Label(root, text="Please select one of the values below and click Ok!")
    label.pack()
    radio_button_value = StringVar()
    radio_button1 = Radiobutton(root, text="Line", variable=radio_button_value, value="Line")
    radio_button1.pack()
    button = Button(root, text="OK", width=25, command= lambda: root.destroy())
    button.pack()
    return radio_button_value.get()


# function 19
# Note: this function is a part of save_new_password function

def write_json_file(filename, text):
    with open(filename, "w") as json_file:
        # convert python object, in this case new_profile(type: dictionary) to json object
        json.dump(text, json_file, indent=4)
        return True


# function 20
# Note: this function is a part of search by date function
# The purpose of testing this function is to make sure that the main software can get the values line by line to place in treeview
def read_data_by_row():
    db = sqlite3.connect("New York Restaurant.db")
    cursor = db.cursor()
    record = cursor.execute("""select * from mytable;""")
    rows = record.fetchall()
    if rows:
        return True
    else:
        return False

