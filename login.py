import os
from tkinter import *
from tkinter import messagebox
import smtplib
import email_password
import time, threading
import pymysql


def connection():
    global mycursor, conn

    try:
        # Establish the connection
        conn = pymysql.connect(host='localhost', user='root', password='Kushagra@99')
        mycursor = conn.cursor()
    except:
        messagebox.showerror('Error', 'Unable to connect to the database. Please ensure MySQL is running.')
        return

    # Create and use the database
    mycursor.execute('CREATE DATABASE IF NOT EXISTS grocery')
    mycursor.execute('USE grocery')

    # Create the Customers table
    mycursor.execute('''
        CREATE TABLE IF NOT EXISTS Customers (
            customerid INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            phone VARCHAR(15),
            email VARCHAR(100)
        )
    ''')

    # Create the Products table
    mycursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            productid INT AUTO_INCREMENT PRIMARY KEY,
            productname VARCHAR(100),
            price DECIMAL(10, 2)
        )
    ''')

    # Create the Users table
    mycursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            userid INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE,
            password VARCHAR(50),
            role VARCHAR(50),
            branchid INT,
            FOREIGN KEY (branchid) REFERENCES Branches(branchid) ON DELETE SET NULL
        )
    ''')

    # Create the Branches table
    mycursor.execute('''
        CREATE TABLE IF NOT EXISTS Branches (
            branchid INT AUTO_INCREMENT PRIMARY KEY,
            branch_name VARCHAR(100),
            city VARCHAR(100),
            phone VARCHAR(15)
        )
    ''')

    # Create the BranchInventory table
    mycursor.execute('''
        CREATE TABLE IF NOT EXISTS BranchInventory (
            branchinventory_id INT AUTO_INCREMENT PRIMARY KEY,
            branchid INT,
            productid INT,
            quantity INT,
            FOREIGN KEY (branchid) REFERENCES Branches(branchid) ON DELETE CASCADE,
            FOREIGN KEY (productid) REFERENCES Products(productid) ON DELETE CASCADE
        )
    ''')

    # Create the Purchase table
    mycursor.execute('''
        CREATE TABLE IF NOT EXISTS Purchase (
            purchase_id INT AUTO_INCREMENT PRIMARY KEY,
            date DATE,
            customerid INT,
            productid INT,
            quantity INT,
            billamount DECIMAL(10, 2),
            payment_method VARCHAR(50),
            FOREIGN KEY (customerid) REFERENCES Customers(customerid) ON DELETE SET NULL,
            FOREIGN KEY (productid) REFERENCES Products(productid) ON DELETE SET NULL
        )
    ''')

    # Commit the changes
    conn.commit()

# Initialize the connection
connection()





def check_empty_emp_data():
    mycursor.execute('SELECT COUNT(*) FROM emp_data')
    count = mycursor.fetchone()[0]
    return count == 0


def login(event=None):
    if empIdEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showerror('Error', 'Fields cannot be empty')
    else:
        # Check if the users table is empty
        mycursor.execute('SELECT COUNT(*) FROM users')
        count = mycursor.fetchone()[0]
        
        if count == 0:
            # Use default credentials if no users are found
            if empIdEntry.get() == '1' and passwordEntry.get() == '1234':
                messagebox.showinfo('Success', 'Login is successful')
                os.environ['USERID'] = empIdEntry.get()
                root.destroy()
                os.system('python main.py')
            else:
                messagebox.showerror('Error', 'No user data found. Please log in using default admin credentials.')
        else:
            # Authenticate against the users table
            mycursor.execute('SELECT role FROM users WHERE userid=%s AND password=%s',
                             (empIdEntry.get(), passwordEntry.get()))
            user = mycursor.fetchone()
            
            if user is None:
                messagebox.showerror('Error', 'Invalid User ID or Password')
            else:
                messagebox.showinfo('Success', 'Login is successful')
                os.environ['USERID'] = empIdEntry.get()
                root.destroy()
                if user[0] == 'manager':
                    os.system('python main.py')
                else:
                    os.system('python billing.py')


logo_index = 0


def animate():
    global logo_index
    logoLabel.config(image=login_logos[logo_index])
    logo_index = (logo_index + 1) % len(login_logos)  # Move to the next image, wrapping around
    logoLabel.after(5000, animate)  # Schedule the next animation frame


def toggle_password():
    if passwordEntry.cget('show') == '*':
        passwordEntry.config(show='')
        toggle_button.config(image=open_eye_img)
    else:
        passwordEntry.config(show='*')
        toggle_button.config(image=close_eye_img)


root = Tk()
root.geometry('1000x600+50+50')
root.resizable(0, 0)
root.config(bg='#ACE1AF')
root.title('Login')
login_logos = [
    PhotoImage(file='login_logo1.png'),
    PhotoImage(file='login_logo2.png'),
    PhotoImage(file='login_logo3.png'),
    PhotoImage(file='login_logo4.png'),
    PhotoImage(file='login_logo5.png'),
    PhotoImage(file='login_logo6.png'),
    PhotoImage(file='login_logo7.png')
]
title = Label(root, text='Inventory Management System', font=('times new roman', 40), bg='#FA86C4', fg='white')
title.place(x=0, y=0, relwidth=1)
logoLabel = Label(root, bg='white')
logoLabel.place(x=20, y=100)
rightFrame = Frame(root, bg='#FFB6C1', height=500, width=400)
rightFrame.place(x=620, y=100)
logo = PhotoImage(file='up_green.png')
employeelogoLabel = Label(rightFrame, image=logo, height=200, width=200, bg='#FFB6C1', bd=0)
employeelogoLabel.grid(row=0, column=0, pady=20)

empIdLabel = Label(rightFrame, text='Employee Id', font=('times new roman', 15), bg='#FFB6C1')
empIdLabel.grid(row=1, column=0, sticky='w', padx=50)
empIdEntry = Entry(rightFrame, font=('times new roman', 15))
empIdEntry.grid(row=2, column=0, sticky='w', padx=50)

passwordLabel = Label(rightFrame, text='Password', font=('times new roman', 15), bg='#FFB6C1')
passwordLabel.grid(row=3, column=0, sticky='w', padx=50, pady=(10, 0))

passwordEntry = Entry(rightFrame, font=('times new roman', 15), show='*')
passwordEntry.grid(row=4, column=0, sticky='w', padx=(50, 0))

open_eye_img = PhotoImage(file='open_eye.png')
close_eye_img = PhotoImage(file='close_eye.png')

toggle_button = Button(rightFrame, image=close_eye_img, command=toggle_password, bd=0, bg='#FFB6C1',
                       activebackground='lightgray')
toggle_button.place(x=260, y=295)


loginButton = Button(rightFrame, text='Login', font=('times new roman', 14), width=20, bg='#BCB88A', cursor='hand2',
                     fg='white',
                     command=login)
loginButton.grid(row=6, column=0, pady=(20, 30), padx=50)

animate()

connection()
# Bind the Enter key to the login function
root.bind('<Return>', login)
root.mainloop()
