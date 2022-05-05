# Created by Craig Freiwald for IST 402
# 2/13/2022
# latest revision: 2/19/2022
import json
import sqlite3
from tkinter import *
from tkinter import ttk, messagebox


class Feedback:

    def __init__(self, master):

        self.frame_header = ttk.Frame(master)
        self.frame_header.pack()

        self.logo = PhotoImage(file='tour_logo.gif')
        ttk.Label(self.frame_header, image=self.logo).grid(row=0, column=0, rowspan=2)
        ttk.Label(self.frame_header, text='Thanks for Exploring!').grid(row=0, column=1)
        ttk.Label(self.frame_header, wraplength=450,
                  text=("We're glad you chose Explore California for your recent adventure. "
                        "Please tell us what you thought about the 'Desert to Sea' tour.")).grid(row=1, column=1)

        self.frame_content = ttk.Frame(master)
        self.frame_content.pack()

        ttk.Label(self.frame_content, text='Name:').grid(row=0, column=0, padx=5, sticky='sw')
        ttk.Label(self.frame_content, text='Email:').grid(row=0, column=1, padx=5, sticky='sw')
        ttk.Label(self.frame_content, text='Comments:').grid(row=2, column=0, columnspan=2, padx=5, sticky='sw')
        ttk.Label(self.frame_content, text='Tour State:').grid(row=4, column=0, padx=5, sticky='sw')
        ttk.Label(self.frame_content, text='Tour Guide:').grid(row=4, column=1, padx=5, sticky='sw')
        ttk.Label(self.frame_content, text='Satisfaction:').grid(row=8, column=0, columnspan=2, padx=5, sticky='sw')

        self.entry_name = ttk.Entry(self.frame_content, width=24)
        self.entry_email = ttk.Entry(self.frame_content, width=24)
        self.text_comments = Text(self.frame_content, width=50, height=10)

        self.entry_name.grid(row=1, column=0, padx=5, sticky='w')
        self.entry_email.grid(row=1, column=1, padx=5, sticky='w')
        self.text_comments.grid(row=3, column=0, columnspan=2)

        # Dropdown State selection
        self.state = StringVar()
        self.combobox = ttk.Combobox(self.frame_content, textvariable=self.state, values=
        ('California', 'Nevada', 'Oregon', 'Arizona', 'New Mexico'))
        self.combobox.grid(row=5, column=0, padx=5, sticky='w')

        # Check Box Answers
        self.guide1 = StringVar()
        self.guide2 = StringVar()

        self.cb1 = ttk.Checkbutton(self.frame_content, text='Clem')
        self.cb1.grid(row=5, column=1, padx=5, sticky='w')
        self.cb1.config(variable=self.guide1, onvalue='Clem', offvalue='Not Selected')

        self.cb2 = ttk.Checkbutton(self.frame_content, text='Cletus')
        self.cb2.grid(row=6, column=1, padx=5, sticky='w')
        self.cb2.config(variable=self.guide2, onvalue='Cletus', offvalue='Not Selected')

        # Radiobutton
        self.rating = StringVar()
        ttk.Radiobutton(self.frame_content, text='Satisfied', variable=self.rating, value='satisfied'
                        ).grid(row=9, column=0, padx=5, sticky='w')
        ttk.Radiobutton(self.frame_content, text='Not satisfied', variable=self.rating, value='not satisfied'
                        ).grid(row=10, column=0, padx=5, sticky='w')

        ttk.Button(self.frame_content, text='Submit', command=self.submit).grid(row=11, column=0, padx=5, sticky='e')
        ttk.Button(self.frame_content, text='Clear', command=self.clear).grid(row=11, column=1, padx=5, sticky='w')
        ttk.Button(self.frame_content, text='Submit to Flat File', command=self.subFlat).grid(row=12, column=0, padx=5,
                                                                                              sticky='w')
        ttk.Button(self.frame_content, text='Submit to JSON File', command=self.subJSON).grid(row=13, column=0, padx=5,
                                                                                              sticky='w')
        ttk.Button(self.frame_content, text='Submit to SQLite DB', command=self.subDB).grid(row=14, column=0, padx=5,
                                                                                            sticky='w')

    # Submit form contents to console method
    def submit(self):
        print('Name: {}'.format(self.entry_name.get()))
        print('Email: {}'.format(self.entry_email.get()))
        print('Comments: {}'.format(self.text_comments.get(1.0, 'end')))
        print('State: {}'.format(self.combobox.get()))
        print('Tour Guide: {}'.format(self.guide1.get() + ' ' + self.guide2.get()))
        print('Satisfaction: {}'.format(self.rating.get()))
        self.clear()
        messagebox.showinfo(title="Explore California Feedback", message="Comments Submitted!")

    # clear the form contents method
    def clear(self):
        self.entry_name.delete(0, 'end')
        self.entry_email.delete(0, 'end')
        self.text_comments.delete(1.0, 'end')
        self.combobox.set('')
        self.guide1.set('Not Selected')
        self.guide2.set('Not Selected')
        self.rating.set('')

    # Dump form contents to flat file method
    def subFlat(self):
        formInput = (self.entry_name.get() + '\n' + self.entry_email.get() + '\n' + self.text_comments.get(1.0, 'end')
                     + self.combobox.get() + self.guide1.get() + '\n' + self.guide2.get() + '\n' + self.rating.get() + '\n')
        output = open('flatFileDump.txt', 'a')
        for line in formInput:
            output.write(line)
        output.write('\n')
        output.close()

        print('Form contents dumped to flat file')
        self.clear()
        messagebox.showinfo(title="Explore California Feedback", message="Comments dumped to Flat File!")

    # Dump form contents to JSON method
    def subJSON(self):
        x = {"Name": self.entry_name.get(), "Email": self.entry_email.get(),
             "Comments": self.text_comments.get(1.0, 'end'),
             "State": self.combobox.get(), "Guide 1": self.guide1.get(), "Guide 2": self.guide2.get(),
             "Rating": self.rating.get()}
        y = json.dumps(x, indent=4)

        with open("dumpJSONhere.json", "r+") as out_file:
            json.dump(y, out_file)
        out_file.close()

        print('Form contents dumped to JSON file')
        self.clear()
        messagebox.showinfo(title="Explore California Feedback", message="Comments dumped to JSON File!")

    # Dump form contents to SQLite Database method
    def subDB(self):
        conn = sqlite3.connect('formSubmissions.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS reviews
                     (name text, email text, comments text, state text, guide1 text, guide2 text, rating text)''')
        c.execute("""
        INSERT INTO reviews
        VALUES (?,?,?,?,?,?,?)
        """, (self.entry_name.get(), self.entry_email.get(), self.text_comments.get(1.0, 'end'), self.combobox.get(),
              self.guide1.get(), self.guide2.get(), self.rating.get()))

        conn.commit()

        # Print DB contents to console to check if submission was valid
        c.execute("SELECT * FROM reviews")
        items = c.fetchall()
        for item in items:
            print(item)

        conn.close()
        print('Form contents dumped to SQLite Database')
        self.clear()
        messagebox.showinfo(title="Explore California Feedback", message="Comments dumped to SQLite Database!")


def main():
    root = Tk()
    feedback = Feedback(root)
    root.mainloop()


if __name__ == "__main__": main()
