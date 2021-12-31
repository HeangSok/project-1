import tkinter.messagebox
from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from datetime import datetime
from tkcalendar import *
import pandas as pd
import sqlite3
import os


# todo:-----------define_function------------
def dataset():
    print("Note: if there is a warning named: '140217952814784date_time', this means that the date_time function is forced to quite in the middle of running. \n To solve this problem, we can comment out the date_time function, but it is not recommended as it might affect other codes.")

    def acknowlegement():
        """Acknowledgement message."""
        tkinter.messagebox.showinfo("Acknowledgement", "I would like to express my gratitude to Dr Gervase Tuxworth and James Baker who have helped me in carrying out this project.")
        print("Note: If you run this software on MAC, the OS shows unexpected warning sometimes.",
              "\n\t  Some widgets, especially messagebox, in tkinter are not compatible with MAC OS.")

    def openfile():
        """Open a new dataset."""
        file= filedialog.askopenfile(initialdir=".",
                                     title="Select CSV File Only",
                                     filetypes=(("CSV files", "*.csv"), ("DB files", "*.db"), ("All Files", "*.*")))  # this function doesn't work well on mac
        try:
            label_file["text"] = file.name  # get a raw path name from the file object
        except:
            pass

    def insert_data_treeview(column_name, rows):
        count = 0
        # set header to the treeview
        my_treeview["columns"] = column_name
        my_treeview["show"] = "headings"
        for header in my_treeview["columns"]:
            my_treeview.heading(header, text=header)

        # insert data into the treeview
        for row in rows:
            if count % 2 == 0:
                my_treeview.insert(parent="", index="end", iid=count, text="",
                                   value=row,
                                   tags=("blue_row"))
            else:
                my_treeview.insert(parent="", index="end", iid=count, text="",
                                   value=row,
                                   tags=("white_row"))
            count += 1


    def loadfile():
        """Load datasets to the treeview."""
        global count, df, raw_filename
        path = label_file["text"]
        file_name = f"{path}"
        raw_filename = path.split("/")
        raw_filename = raw_filename[-1]
        # raw_filename = raw_filename[-1].replace(".csv", "")

        if file_name != "Please Select CSV or DB File Only!":
            if "csv" in raw_filename:
                try:
                    df = pd.read_csv(file_name)

                    clear_my_treeview()

                    raw_filename = raw_filename.replace(".csv", "")
                    # create a database and connect
                    db = sqlite3.connect(f"{raw_filename}.db")
                    cursor = db.cursor()
                    # convert dataframe to sqlite and set the table name to mytable
                    data_type = {"INSPECTION DATE": "TEXT"} if raw_filename == "New York Restaurant" else None
                    df.to_sql(name='mytable', con=db, if_exists='replace', index=False, dtype=data_type)  # add df to a table in sqlite

                    # execute the query and store the result
                    record = (cursor.execute("""SELECT * FROM mytable;"""))

                    # get the name of each column from the database
                    column_name = [name[0] for name in record.description]
                    # get the rows from the database
                    rows = record.fetchall()
                    # insert data to treeview
                    insert_data_treeview(column_name, rows)

                    db.close()
                except FileNotFoundError:
                    tkinter.messagebox.showerror("Error", "FileNotFoundError. Please try again!")

                # finally:
                #     print("Note: If you run this software on MAC, the OS shows unexpected warning sometimes.",
                #           "\n\t  Some widgets, especially messagebox, in tkinter are not compatible with MAC OS.")

            elif "db" in raw_filename:
                try:
                    clear_my_treeview()

                    # create a database and connect
                    db = sqlite3.connect(f"{raw_filename}")
                    cursor = db.cursor()

                    # execute the query and store the result
                    record = (cursor.execute("""SELECT * FROM mytable;"""))

                    # get the name of each column from the database
                    column_name = [name[0] for name in record.description]
                    # get the rows from the database
                    rows = record.fetchall()

                    # insert data to treeview
                    insert_data_treeview(column_name, rows)

                    db.close()
                except FileNotFoundError:
                    tkinter.messagebox.showerror("Error", "FileNotFoundError. Please try again!")

                # finally:
                #     print("Note: If you run this software on MAC, the OS shows unexpected warning sometimes.",
                #           "\n\t  Some widgets, especially messagebox, in tkinter are not compatible with MAC OS.")

        else:
            tkinter.messagebox.showerror("Error", "FileNotFoundError. Please try again!")
            print("Note: If you run this software on MAC, the OS shows unexpected warning sometimes.",
                  "\n\t  Some widgets, especially messagebox, in tkinter are not compatible with MAC OS.")


    def clear_my_treeview():
        """Clear the treeview."""
        my_treeview.delete(*my_treeview.get_children())  # delete only the content and the header will be kept


    def search(code="", can_plot=False, animal_case=False, suburb="", animal_name="" ):

        clear_my_treeview()
        path = label_file["text"]
        file_name = f"{path}"
        raw_filename = path.split("/")
        raw_filename = raw_filename[-1]

        if file_name != "Please Select CSV or DB File Only!":
            if "csv" in raw_filename:
                raw_filename = raw_filename.replace(".csv", "")
            elif "db" in raw_filename:
                raw_filename = raw_filename.replace(".db", "")
            try:
                db = sqlite3.connect(f"{raw_filename}.db")
                cursor = db.cursor()

                record = cursor.execute(code)

                # get the name of each column from the database
                column_name = [name[0] for name in record.description]
                # get the rows from the database
                rows = record.fetchall()
                # insert data to treeview
                insert_data_treeview(column_name, rows)

                if animal_case:
                    try:
                        sub = rows[0][2]
                    except:
                        sub = suburb
                    x = [i[8] for i in rows]
                    new_format_x=[]
                    for j in x:
                        date_object = datetime.strptime(j, '%m/%d/%Y')
                        date = date_object.strftime('%d/%m/%Y')
                        new_format_x.append(date)
                    y = [i[-1] for i in rows]
                    plt.rcParams["figure.autolayout"] = True
                    plt.figure("Task4", figsize=(12,7))
                    plt.title(f"Animal Related Case In: {sub}")
                    plt.xlabel("Date")
                    plt.xticks(rotation=90)
                    plt.tick_params(axis='x', labelsize=6)
                    plt.ylabel("Numbers of Violation Related to Animal")
                    plt.plot(new_format_x,y, label=animal_name, color='purple')
                    plt.legend(loc="upper left")
                    plt.grid()

                    plt.show()

                db.close()
            except FileNotFoundError:
                tkinter.messagebox.showerror("Error", "FileNotFoundError. Please try again!")
        else:
            tkinter.messagebox.showerror("Error", "FileNotFoundError. Please try again!")
            print("Note: If you run this software on MAC, the OS shows unexpected warning sometimes.",
                  "\n\t  Some widgets, especially messagebox, in tkinter are not compatible with MAC OS.")

    def search_by_date():
        """For a user-selected period, retrieve all inspection details"""
        # convert date formate to yyyy-mm-dd because sqlite have limitation on date searching
        start = start_date_task1_entry.get()
        start = start.replace("/","")
        use_start = start[4:] + "-" + start[:2] + "-" + start[2:4]

        # convert date formate to yyyy-mm-dd because sqlite have limitation on date searching
        end = end_date_task1_entry.get()
        end = end.replace("/","")
        use_end = end[4:] + "-" + end[:2] + "-" + end[2:4]

        # As Sqlite doesn't have a date type you will need to do string comparison to achieve this.
        query = f"""SELECT * FROM mytable 
        WHERE (substr([INSPECTION DATE],7,4)
        ||'-'||substr([INSPECTION DATE],1,2)
        ||'-'||substr([INSPECTION DATE],4,2))
        BETWEEN ('{use_start}') AND ('{use_end}')
        ORDER BY [INSPECTION DATE] ASC
        ;"""
        search(code=query)

    def search_by_date_keyword():
        """For a user-selected period, retrieve all violations that contain a keyword (user entered)."""
        # convert date formate to yyyy-mm-dd because sqlite have limitation on date searching
        start = start_date_task2_entry.get()
        start = start.replace("/","")
        use_start = start[4:] + "-" + start[:2] + "-" + start[2:4]


        # convert date formate to yyyy-mm-dd because sqlite have limitation on date searching
        end = end_date_task2_entry.get()
        end = end.replace("/","")
        use_end = end[4:] + "-" + end[:2] + "-" + end[2:4]
        keywords = keyword_task2_entry.get()


        # As Sqlite doesn't have a date type you will need to do string comparison to achieve this.
        query = f"""SELECT * FROM mytable 
        WHERE ((substr([INSPECTION DATE],7,4)
        ||'-'||substr([INSPECTION DATE],1,2)
        ||'-'||substr([INSPECTION DATE],4,2))
        BETWEEN ('{use_start}') AND ('{use_end}'))
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
        if keywords != "":
            search(code=query)
        else:
            tkinter.messagebox.showinfo("Empty Fields", "Please! Fill in all required entry fields.")
            print("Note: If you run this software on MAC, the OS shows unexpected warning sometimes.",
                  "\n\t  Some widgets, especially messagebox, in tkinter are not compatible with MAC OS.")

    def view_chart_suburbs():
        """For a user-selected period, plot the distribution of violations over the different suburbs"""
        # convert date formate to yyyy-mm-dd because sqlite have limitation on date searching
        start = start_date_task3_entry.get()
        start = start.replace("/","")
        use_start = start[4:] + "-" + start[:2] + "-" + start[2:4]

        # convert date formate to yyyy-mm-dd because sqlite have limitation on date searching
        end = end_date_task3_entry.get()
        end = end.replace("/","")
        use_end = end[4:] + "-" + end[:2] + "-" + end[2:4]
        user_choices = radio_button_value.get()


        query = f"""SELECT * , COUNT([VIOLATION CODE]) AS 'NUMBERS OF VIOLATION'
        FROM mytable 
        WHERE (substr([INSPECTION DATE],7,4)
        ||'-'||substr([INSPECTION DATE],1,2)
        ||'-'||substr([INSPECTION DATE],4,2))
        BETWEEN ('{use_start}') AND ('{use_end}')
        GROUP BY [BORO]
        ORDER BY [INSPECTION DATE] ASC
        ;"""
        if user_choices != "":
            # clear_my_treeview()
            path = label_file["text"]
            file_name = f"{path}"
            raw_filename = path.split("/")
            raw_filename = raw_filename[-1]

            if file_name != "Please Select CSV or DB File Only!":
                if "csv" in raw_filename:
                    raw_filename = raw_filename.replace(".csv", "")
                elif "db" in raw_filename:
                    raw_filename = raw_filename.replace(".db", "")
                try:
                    db = sqlite3.connect(f"{raw_filename}.db")
                    cursor = db.cursor()

                    record_1 = cursor.execute(query)

                    # get the name of each column from the database for suburb1
                    column_name = [name[0] for name in record_1.description]
                    # get the rows from the database
                    rows = record_1.fetchall()
                    # insert data to treeview
                    # insert_data_treeview(column_name, rows)
                    # working with matplot lib
                    x = [i[2] for i in rows]
                    y = [i[-1] for i in rows]
                    plt.rcParams["figure.autolayout"] = True
                    plt.figure("Task3", figsize=(12, 7))
                    plt.title(f"Plot The Distribution of Violations Over The Different Suburbs From {use_start} To {use_end}.")
                    plt.xlabel("Suburbs")
                    plt.ylabel("Numbers of Violation")

                    if user_choices == "line":
                        plt.plot(x, y, 'o-', label= "Violations", color='purple', lw=0.7, ms=5)
                        plt.legend(loc="upper left")
                        plt.show()
                    elif user_choices == "bar":
                        plt.bar(x, y, color=["green", "orange", "red", "purple", "blue"])
                        for i in range(len(y)):
                            plt.text(i, y[i], y[i])
                        plt.show()
                    elif user_choices == "pie":
                        plt.xlabel("")
                        plt.ylabel("")
                        y = [int(i[-1]) for i in rows]
                        z = sum(y)
                        plt.pie(y, labels=x, autopct=lambda p: '{:.0f}'.format(p * z / 100))
                        plt.legend(title="Suburbs")
                        plt.show()
                    elif user_choices == "scatter":
                        plt.scatter(x, y, color="green")
                        for i in range(len(x)):
                            plt.annotate(y[i], (x[i], y[i] + 1))

                        plt.show()

                    db.close()
                except FileNotFoundError:
                    tkinter.messagebox.showerror("Error", "FileNotFoundError. Please try again!")
            else:
                tkinter.messagebox.showerror("Error", "FileNotFoundError. Please try again!")
                print("Note: If you run this software on MAC, the OS shows unexpected warning sometimes.",
                      "\n\t  Some widgets, especially messagebox, in tkinter are not compatible with MAC OS.")
        else:
            tkinter.messagebox.showinfo("Empty Fields", "Please! Select a type of graph.")
            print("Note: If you run this software on MAC, the OS shows unexpected warning sometimes.",
                  "\n\t  Some widgets, especially messagebox, in tkinter are not compatible with MAC OS.")

    def view_graph_animal_related_case():
        """Analyse the cases related to animals, e.g., rats, mice or others, and their trend over time and
    distribution over suburbs"""
        # convert date formate to yyyy-mm-dd because sqlite have limitation on date searching
        start = start_date_task4_entry.get()
        start = start.replace("/","")
        use_start = start[4:] + "-" + start[:2] + "-" + start[2:4]

        # convert date formate to yyyy-mm-dd because sqlite have limitation on date searching
        end = end_date_task4_entry.get()
        end = end.replace("/","")
        use_end = end[4:] + "-" + end[:2] + "-" + end[2:4]
        keywords = suburb_task4_entry.get()
        animal = animal_task4_entry.get()

        can = True
        query = f"""SELECT *, COUNT([VIOLATION CODE]) AS 'NUMBERS OF VIOLATION'
        FROM mytable 
        WHERE BORO LIKE '%{keywords}%'
        AND [VIOLATION DESCRIPTION] LIKE '%{animal}%'
        AND (substr([INSPECTION DATE],7,4)
        ||'-'||substr([INSPECTION DATE],1,2)
        ||'-'||substr([INSPECTION DATE],4,2))
        BETWEEN ('{use_start}') AND ('{use_end}')
        GROUP BY [INSPECTION DATE]
        ORDER BY [INSPECTION DATE] ASC
        ;"""
        if keywords != "" and animal != "":
            search(code=query, animal_case=can, animal_name=animal, suburb=keywords)
        else:
            tkinter.messagebox.showinfo("Empty Fields", "Please! Fill in all required entry fields.")
            print("Note: If you run this software on MAC, the OS shows unexpected warning sometimes.",
                  "\n\t  Some widgets, especially messagebox, in tkinter are not compatible with MAC OS.")

    def compare_cuisine():
        """Compare the numbers of violation between two different cuisines."""
        # convert date formate to yyyy-mm-dd because sqlite have limitation on date searching
        start = start_date_task5_entry.get()
        start = start.replace("/", "")
        use_start = start[4:] + "-" + start[:2] + "-" + start[2:4]

        # convert date formate to yyyy-mm-dd because sqlite have limitation on date searching
        end = end_date_task5_entry.get()
        end = end.replace("/", "")
        use_end = end[4:] + "-" + end[:2] + "-" + end[2:4]
        cuisine1 = cuisine1_task5_entry.get()
        cuisine2 = cuisine2_task5_entry.get()

        query_for_cuisine1 = f"""SELECT * , COUNT([VIOLATION CODE]) AS 'NUMBERS OF VIOLATION'
           FROM mytable 
           WHERE [CUISINE DESCRIPTION] LIKE '%{cuisine1}%'
           AND (substr([INSPECTION DATE],7,4)
           ||'-'||substr([INSPECTION DATE],1,2)
           ||'-'||substr([INSPECTION DATE],4,2))
           BETWEEN ('{use_start}') AND ('{use_end}')
           GROUP BY [INSPECTION DATE]
           ORDER BY [INSPECTION DATE] ASC
           ;"""

        query_for_cuisine2 = f"""SELECT * , COUNT([VIOLATION CODE]) AS 'NUMBERS OF VIOLATION'
           FROM mytable 
           WHERE [CUISINE DESCRIPTION] LIKE '%{cuisine2}%'
           AND (substr([INSPECTION DATE],7,4)
           ||'-'||substr([INSPECTION DATE],1,2)
           ||'-'||substr([INSPECTION DATE],4,2))
           BETWEEN ('{use_start}') AND ('{use_end}')
           GROUP BY [INSPECTION DATE]
           ORDER BY [INSPECTION DATE] ASC
           ;"""

        if cuisine1 != "" and cuisine2 != "":
            clear_my_treeview()
            path = label_file["text"]
            file_name = f"{path}"
            raw_filename = path.split("/")
            raw_filename = raw_filename[-1]

            if file_name != "Please Select CSV or DB File Only!":
                if "csv" in raw_filename:
                    raw_filename = raw_filename.replace(".csv", "")
                elif "db" in raw_filename:
                    raw_filename = raw_filename.replace(".db", "")
                try:
                    db = sqlite3.connect(f"{raw_filename}.db")
                    cursor = db.cursor()

                    record_1 = cursor.execute(query_for_cuisine1)

                    # get the name of each column from the database for suburb1
                    cuisine1_column_name = [name[0] for name in record_1.description]
                    # get the rows from the database
                    cuisine1_rows = record_1.fetchall()

                    record_2 = cursor.execute(query_for_cuisine2)

                    # get the name of each column from the database for suburb1
                    cuisine2_column_name = [name[0] for name in record_2.description]
                    # get the rows from the database
                    cuisine2_rows = record_2.fetchall()
                    # insert data to treeview
                    all_rows = cuisine1_rows + cuisine2_rows
                    insert_data_treeview(cuisine1_column_name, all_rows)
                    # working with matplot lib

                    try:
                        sub1 = cuisine1_rows[0][7]
                        sub2 = cuisine2_rows[0][7]
                    except:
                        sub1 = cuisine1
                        sub2 = cuisine2

                    # plot1 data
                    cuisine1_x = [i[8] for i in cuisine1_rows]
                    cuisine1_new_format_x = []
                    for j in cuisine1_x:
                        date_object = datetime.strptime(j, '%m/%d/%Y')
                        date = date_object.strftime('%m/%Y')
                        cuisine1_new_format_x.append(date)
                    suburb1_y = [i[-1] for i in cuisine1_rows]
                    # plot2 data
                    cuisine2_x = [i[8] for i in cuisine2_rows]
                    cuisine2_new_format_x = []
                    for j in cuisine2_x:
                        date_object2 = datetime.strptime(j, '%m/%d/%Y')
                        date2 = date_object2.strftime('%m/%Y')
                        cuisine2_new_format_x.append(date2)
                    suburb2_y = [i[-1] for i in cuisine2_rows]

                    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(12, 7))
                    ax1.plot(cuisine1_new_format_x, suburb1_y, 'o--', label=sub1, color='purple', lw=0.7, ms=2)
                    ax2.plot(cuisine2_new_format_x, suburb2_y, 'o--', label=sub2, color='green', lw=0.7, ms=2)

                    ax1.legend(loc="upper left")
                    ax1.set_title(f"Compare The Number of Violations Between {sub1} & {sub2} Cuisine")
                    ax1.set_ylabel(f"Numbers Of Violation: {sub1} Cuisine")
                    ax1.grid()

                    ax2.legend(loc="upper left")
                    ax2.set_xlabel("Date [mm/yyyy]")
                    ax2.set_ylabel(f"Numbers Of Violation: {sub2} Cuisine")
                    ax2.grid()

                    plt.xticks(rotation=90)
                    plt.tick_params(axis='x', labelsize=6)
                    plt.show()

                    db.close()
                except FileNotFoundError:
                    tkinter.messagebox.showerror("Error", "FileNotFoundError. Please try again!")
            else:
                tkinter.messagebox.showerror("Error", "FileNotFoundError. Please try again!")
                print("Note: If you run this software on MAC, the OS shows unexpected warning sometimes.",
                      "\n\t  Some widgets, especially messagebox, in tkinter are not compatible with MAC OS.")
        else:
            tkinter.messagebox.showinfo("Empty Fields", "Please! Fill in all required entry fields.")
            print("Note: If you run this software on MAC, the OS shows unexpected warning sometimes.",
                  "\n\t  Some widgets, especially messagebox, in tkinter are not compatible with MAC OS.")

    # todo:-----------initial_configure------------
    # window configuration
    WINDOW_SIZE = "1350x710"
    dataset_window = Tk()
    dataset_window.title('New York Restaurant Inspection')
    icon = PhotoImage(file=os.path.join('images', 'griffthuni.png'))  # use os to make the path works for cross platform
    dataset_window.iconphoto(False, icon)  # note this window icon don't work on mac
    dataset_window.geometry(WINDOW_SIZE)  # set window size
    dataset_window.pack_propagate(False)  # tell the widow that don't resize yourself based on the content
    dataset_window.resizable(0,0)  # don't allow the user to resize the window

    # dataset frame
    data_frame = LabelFrame(dataset_window, text="Dataset")
    data_frame.pack(fill="x", pady=3, padx=5)

    # set ttk widget's styles and configuration
    ttk_styles = ttk.Style()
    ttk_styles.theme_use('default') # give a colorful header

    # configure color for the working field
    ttk_styles.configure("Treeview",
                         background="white",
                         foreground="black",
                         rowheight=20,
                         fieldbackground="white")

    ttk_styles.map("Treeview", background=[("selected", "light pink")])  # change the color when we select a particular row
    ttk_styles.map("TNotebook", background=[("selected", "light green")])


    # create scrollbars
    scrollbary = Scrollbar(data_frame, orient="vertical")
    scrollbary.pack(side="right", fill="y")
    scrollbarx = Scrollbar(data_frame, orient="horizontal")
    scrollbarx.pack(side="bottom", fill="x")

    # create the treeview and attach the scrollbar
    # note: if you put a treeview inside the labelframe the height command in labelframe won't work; you have to set the height in treeview instead
    my_treeview = ttk.Treeview(data_frame, xscrollcommand=scrollbarx.set, yscrollcommand=scrollbary.set, selectmode="extended", height=17)
    my_treeview.pack(anchor=W)
    scrollbary.config(command=my_treeview.yview)  # tell the scrollbar which tree view you want to attach
    scrollbarx.config(command=my_treeview.xview)

    # set color to rows
    my_treeview.tag_configure("white_row", background="white")
    my_treeview.tag_configure("blue_row", background="light blue")

    # set dummy columns
    my_treeview['columns'] = ("column1", "column2", "column3", "column4", "column5", "column6", "column7", "column8", "column9", "column10","column11"  )


    # open file frame
    openfile_frame= LabelFrame(dataset_window, text="Open Files")
    openfile_frame.pack(fill="x", pady=3, padx=5)

    label_file = Label(openfile_frame, text="Please Select CSV or DB File Only!", fg="gray")
    label_file.pack(anchor=W, padx=10, pady=10)
    load_button = Button(openfile_frame, text="Load File", width=15, highlightbackground="light yellow", command= lambda: loadfile()) # background command is not working on mac use highlightbackground
    load_button.pack(anchor=W, padx=10, side="left", pady=10)
    open_button = Button(openfile_frame, text="Open File", width=15, highlightbackground="light yellow",  command= lambda: openfile()) # todo: add command
    open_button.pack(anchor=W, side="left", pady=10)

    # assignmnt task frame
    task_frame= LabelFrame(dataset_window, text="Assignment Tasks")
    task_frame.pack(fill="x", pady=3, padx=5)

    # footer
    home = Button(dataset_window, text="Acknowledgement", command= lambda: acknowlegement())
    home.place(x=545, y=660)
    leave_program = Button(dataset_window, text="Exit", command= lambda: quit(), width=15)
    leave_program.place(x=665, y=660)
    # copy_right_label = Label(dataset_window, text="7810ICT SOFTWARE TECHNOLOGIES", fg="blue", font=("Party LET", 25))
    # copy_right_label.place(x=570, y=700)

    # add window table to assignment task
    tab_frame = ttk.Notebook(task_frame)
    task1 = Frame(task_frame)
    task2 = Frame(task_frame)
    task3 = Frame(task_frame)
    task4 = Frame(task_frame)
    task5 = Frame(task_frame)
    tab_frame.add(task1, text="View by Date")
    tab_frame.add(task2, text="View by Date & Keyword")
    tab_frame.add(task3, text="View Violations by Suburbs")
    tab_frame.add(task4, text="View Animal Related Cases")
    tab_frame.add(task5, text="Compare Violation")
    tab_frame.pack(fill="x", pady=3, padx=5)

    # taks1 buttons and labels
    # todo: start date
    start_date = Label(task1, text="Start Date: ")
    start_date.grid(row=0, column=0, pady=10)

    start_date_task1_entry = DateEntry(task1, selectmode="day",
                       date_pattern="mm/dd/yyyy",
                       selectforeground="red",
                       foreground='white',
                       normalforeground='green',
                       selectbackground="light blue")
    start_date_task1_entry.grid(row=0, column=1, pady=10)
    start_date_task1_entry._top_cal.overrideredirect(False) # need this line of code of the DataEntry widget won't work

    # todo: end date
    end_date = Label(task1, text="    End Date: ")
    end_date.grid(row=0, column=2, pady=10)
    end_date_task1_entry = DateEntry(task1, selectmode="day",
                       date_pattern="mm/dd/yyyy",
                       selectforeground="red",
                       foreground='white',
                       normalforeground='green',
                       selectbackground="light blue")
    end_date_task1_entry.grid(row=0, column=3, pady=10)
    end_date_task1_entry._top_cal.overrideredirect(False) # need this line of code of the DataEntry widget won't work

    search_task1_button = Button(task1, text="Search", width=10, command=lambda: search_by_date())
    search_task1_button.grid(row=0, column=4, pady=10, padx=10)
    to_do1 = Label(task1, text="=> Assignment Task: For a user-selected period, retrieve all inspection details.")
    to_do1.grid(row=1, column=0, columnspan=4, sticky=W)

    # taks2 buttons and labels
    # todo: start date
    start_date = Label(task2, text="Start Date: ")
    start_date.grid(row=0, column=0, pady=10)

    start_date_task2_entry = DateEntry(task2, selectmode="day",
                       date_pattern="mm/dd/yyyy",
                       selectforeground="red",
                       foreground='white',
                       normalforeground='green',
                       selectbackground="light blue")
    start_date_task2_entry.grid(row=0, column=1, pady=10)
    start_date_task2_entry._top_cal.overrideredirect(False) # need this line of code of the DataEntry widget won't work

    # todo: end date
    end_date = Label(task2, text="    End Date: ")
    end_date.grid(row=0, column=2, pady=10)
    end_date_task2_entry = DateEntry(task2, selectmode="day",
                       date_pattern="mm/dd/yyyy",
                       selectforeground="red",
                       foreground='white',
                       normalforeground='green',
                       selectbackground="light blue")
    end_date_task2_entry.grid(row=0, column=3, pady=10)
    end_date_task2_entry._top_cal.overrideredirect(False) # need this line of code of the DataEntry widget won't work
    keyword_task2_label = Label(task2, text="Keyword: ")
    keyword_task2_label.grid(row=0, column=4, pady=10, padx=(15,0))
    keyword_task2_entry = Entry(task2, width=20)
    keyword_task2_entry.grid(row=0, column=5, pady=10)
    search_task2_button = Button(task2, text="Search", width=10, command= lambda: search_by_date_keyword())
    search_task2_button.grid(row=0, column=6, pady=10, padx=10)

    to_do2 = Label(task2, text="=> Assignment Task: For a user-selected period, retrieve all violations that contain a keyword.")
    to_do2.grid(row=1, column=0, columnspan=6, sticky=W)

    # taks3 buttons and labels
    # todo: start date
    start_date = Label(task3, text="Start Date: ")
    start_date.grid(row=0, column=0, pady=10)

    start_date_task3_entry = DateEntry(task3, selectmode="day",
                       date_pattern="mm/dd/yyyy",
                       selectforeground="red",
                       foreground='white',
                       normalforeground='green',
                       selectbackground="light blue")
    start_date_task3_entry.grid(row=0, column=1, pady=10)
    start_date_task3_entry._top_cal.overrideredirect(False) # need this line of code of the DataEntry widget won't work

    # todo: end date
    end_date = Label(task3, text="    End Date: ")
    end_date.grid(row=0, column=2, pady=10)
    end_date_task3_entry = DateEntry(task3, selectmode="day",
                       date_pattern="mm/dd/yyyy",
                       selectforeground="red",
                       foreground='white',
                       normalforeground='green',
                       selectbackground="light blue")
    end_date_task3_entry.grid(row=0, column=3, pady=10)
    end_date_task3_entry._top_cal.overrideredirect(False) # need this line of code of the DataEntry widget won't work

    radio_button_value = StringVar()

    line_radio_button = Radiobutton(task3, text="Line View", variable=radio_button_value, value="line")
    line_radio_button.grid(row=0, column=4)
    bar_radio_button = Radiobutton(task3, text="Bar View", variable=radio_button_value, value="bar")
    bar_radio_button.grid(row=0, column=5)
    pie_radio_button = Radiobutton(task3, text="Pie View", variable=radio_button_value, value="pie")
    pie_radio_button.grid(row=0, column=6)
    scatter_radio_button = Radiobutton(task3, text="Scatter View", variable=radio_button_value, value="scatter")
    scatter_radio_button.grid(row=0, column=7)
    search_task3_button = Button(task3, text="View", width=10, command=lambda:view_chart_suburbs())
    search_task3_button.grid(row=0, column=8, pady=10, padx=1)

    to_do3 = Label(task3, text="=> Assignment Task: For a user-selected period, plot the distribution of violations over the different suburbs.")
    to_do3.grid(row=1, column=0, columnspan=8, sticky=W)

    # taks4 buttons and labels
    # todo: start date
    start_date = Label(task4, text="Start Date: ")
    start_date.grid(row=0, column=0, pady=10)

    start_date_task4_entry = DateEntry(task4, selectmode="day",
                       date_pattern="mm/dd/yyyy",
                       selectforeground="red",
                       foreground='white',
                       normalforeground='green',
                       selectbackground="light blue")
    start_date_task4_entry.grid(row=0, column=1, pady=10)
    start_date_task4_entry._top_cal.overrideredirect(False) # need this line of code of the DataEntry widget won't work

    # todo: end date
    end_date = Label(task4, text="    End Date: ")
    end_date.grid(row=0, column=2, pady=10)
    end_date_task4_entry = DateEntry(task4, selectmode="day",
                       date_pattern="mm/dd/yyyy",
                       selectforeground="red",
                       foreground='white',
                       normalforeground='green',
                       selectbackground="light blue")
    end_date_task4_entry.grid(row=0, column=3, pady=10)
    end_date_task4_entry._top_cal.overrideredirect(False) # need this line of code of the DataEntry widget won't work
    suburb_task4_label = Label(task4, text="Suburb/Borough: ")
    suburb_task4_label.grid(row=0, column=4, pady=10, padx=(15,0))
    suburb_task4_entry = Entry(task4, width=20)
    suburb_task4_entry.grid(row=0, column=5, pady=10)

    animal_task4_label = Label(task4, text="Animal: ")
    animal_task4_label.grid(row=0, column=6, pady=10, padx=(15,0))
    animal_task4_entry = Entry(task4, width=20)
    animal_task4_entry.grid(row=0, column=7, pady=10)
    search_task4_button = Button(task4, text="View Graph & Dataset", width=25, command=lambda: view_graph_animal_related_case())
    search_task4_button.grid(row=0, column=8, pady=10, padx=15)

    to_do4 = Label(task4, text="=> Assignment Task: Analyse the cases related to animals, e.g., rats, mice or others, and their trend over time and distribution over suburbs.")
    to_do4.grid(row=1, column=0, columnspan=8, sticky=W)

    # taks5 buttons and labels
    # todo: start date
    start_date = Label(task5, text="Start Date: ")
    start_date.grid(row=0, column=0, pady=10)

    start_date_task5_entry = DateEntry(task5, selectmode="day",
                       date_pattern="mm/dd/yyyy",
                       selectforeground="red",
                       foreground='white',
                       normalforeground='green',
                       selectbackground="light blue")
    start_date_task5_entry.grid(row=0, column=1, pady=10)
    start_date_task5_entry._top_cal.overrideredirect(False) # need this line of code of the DataEntry widget won't work

    # todo: end date
    end_date = Label(task5, text="    End Date: ")
    end_date.grid(row=0, column=2, pady=10)
    end_date_task5_entry = DateEntry(task5, selectmode="day",
                       date_pattern="mm/dd/yyyy",
                       selectforeground="red",
                       foreground='white',
                       normalforeground='green',
                       selectbackground="light blue")
    end_date_task5_entry.grid(row=0, column=3, pady=10)
    end_date_task5_entry._top_cal.overrideredirect(False) # need this line of code of the DataEntry widget won't work
    cuisine1_task5_label = Label(task5, text="Cuisine_1: ")
    cuisine1_task5_label.grid(row=0, column=4, pady=10, padx=(15,0))
    cuisine1_task5_entry = Entry(task5, width=20)
    cuisine1_task5_entry.grid(row=0, column=5, pady=10)
    cuisine2_task5_label = Label(task5, text="Cuisine_2: ")
    cuisine2_task5_label.grid(row=0, column=6, pady=10, padx=(15,0))
    cuisine2_task5_entry = Entry(task5, width=20)
    cuisine2_task5_entry.grid(row=0, column=7, pady=10)
    search_task5_button = Button(task5, text="View Graph & Dataset", width=25, command=lambda: compare_cuisine())
    search_task5_button.grid(row=0, column=8, pady=10, padx=15)

    to_do5 = Label(task5, text="=> Assignment Task: Compare the numbers of violation between two different cuisines over a period of time.")
    to_do5.grid(row=1, column=0, columnspan=8, sticky=W)

    dataset_window.mainloop()

# dataset()