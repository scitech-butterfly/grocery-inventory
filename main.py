import os
from tkinter import *
from tkinter import messagebox
import pymysql, time
import employee, product, purchases, customers, supplier
from tkinter import ttk
from datetime import datetime


# Database Connection
def connection():
    global mycursor, conn
    try:
        conn = pymysql.connect(host='localhost', user='root', password='Kushagra@99', database='grocery')
        mycursor = conn.cursor()
    except Exception as e:
        messagebox.showerror('Error', f'Something went wrong: {e}. Please ensure MySQL is running and try again.')

# Update Content Function to refresh counts and display welcome message
def update_content():
    global mycursor
    try:
        # Fetch total customers
        mycursor.execute('SELECT * FROM users')
        users = mycursor.fetchall()
        totalEmployeescountLabel.config(text=f'{len(users)}')
    except:
        totalEmployeescountLabel.config(text='0')

    try:
        # Fetch total products
        mycursor.execute('SELECT * FROM Products')
        products = mycursor.fetchall()
        totalProductscountLabel.config(text=f'{len(products)}')
    except:
        totalProductscountLabel.config(text='0')

    try:
        # Fetch total branches
        mycursor.execute('SELECT * FROM Branches')
        branches = mycursor.fetchall()
        totalBranchcountLabel.config(text=f'{len(branches)}')
    except:
        totalBranchcountLabel.config(text='0')

    try:
        # Fetch total purchases (purchases)
        mycursor.execute('SELECT * FROM Purchase')
        purchases = mycursor.fetchall()
        totalpurchasescountLabel.config(text=f'{len(purchases)}')
    except:
        totalpurchasescountLabel.config(text='0')

    time_ = time.strftime('%I:%M:%S %p')
    date_ = time.strftime('%d/%m/%Y')
    subtitleLabel.config(text=f'Welcome to Grocery Inventory System\t\t Date: {date_}\t\t Time: {time_}')
    subtitleLabel.after(500, update_content)


# Functionality Part
current_window = None


def close_current_window():
    global current_window
    if current_window is not None:
        current_window.destroy()
        current_window = None


def employee_form():
    global current_window, mycursor

    close_current_window()

    current_window, mycursor = employee.user_page(window, mycursor, conn)


def supplier_form():
    global current_window, mycursor
    close_current_window()

    current_window, mycursor = supplier.inventory_page(window, mycursor, conn)


def customers_form():
    global current_window, mycursor

    close_current_window()

    current_window, mycursor = customers.customers_page(window, mycursor, conn)


def product_form():
    global current_window, mycursor
    close_current_window()

    current_window, mycursor = product.product_page(window, mycursor, conn)


def purchases_form():
    global current_window
    close_current_window()

    current_window = purchases.purchases_page(window,mycursor, conn)


def exit():
    result = messagebox.askyesno('Confirm', 'Do you want to really exit?')
    if result:
        window.destroy()


def logout():
    window.destroy()
    os.system('python login.py')


# Main window setup
window = Tk()
window.title('Grocery Inventory Management System')
window.geometry('1270x668+0+0')
window.config(bg='white')

# Title Label
titleLabel = Label(window, text='  Grocery Inventory Management System', font=('times new roman', 40, 'bold'),
                   bg='#FFB6C1', fg='#093005', anchor='w', padx=20)
titleLabel.place(x=0, y=0, relwidth=1, height=70)

# Subtitle Label
subtitleLabel = Label(window, text='Welcome to Grocery Inventory Management System\t\t Date:DD-MM-YYYY\t\t Time: HH:MM:SS',
                      font=('times new roman', 15), bg='#708238', fg='white')
subtitleLabel.place(x=0, y=70, relwidth=1, height=30)

# Logout and Exit Buttons
logoutButton = Button(window, text='Logout', font=('times new roman', 20, 'bold'), bg='#568203', fg='white',
                      cursor='hand2', command=lambda: window.destroy())
logoutButton.place(x=1100, y=10, height=50, width=150)

# Frame for Employee Count
cust_frame = Frame(window, bg='#FC9483', bd=3, relief=RIDGE)
cust_frame.place(x=400, y=125, height=170, width=280)
Label(cust_frame, text='Total Employees', font=('arial', 15, 'bold'), bg='#FC9483', fg='white').pack()
totalEmployeescountLabel = Label(cust_frame, text='0', font=('arial', 30, 'bold'), bg='#FC9483', fg='white')
totalEmployeescountLabel.pack()

# Frame for Product Count
prod_frame = Frame(window, bg='#71ad6a', bd=3, relief=RIDGE)
prod_frame.place(x=780, y=125, height=170, width=280)
Label(prod_frame, text='Total Products', font=('arial', 15, 'bold'), bg='#71ad6a', fg='white').pack()
totalProductscountLabel = Label(prod_frame, text='0', font=('arial', 30, 'bold'), bg='#71ad6a', fg='white')
totalProductscountLabel.pack()

# Frame for Branch Count
branch_frame = Frame(window, bg='#ACE1AF', bd=3, relief=RIDGE)
branch_frame.place(x=400, y=310, height=170, width=280)
Label(branch_frame, text='Total Branches', font=('arial', 15, 'bold'), bg='#ACE1AF', fg='white').pack()
totalBranchcountLabel = Label(branch_frame, text='0', font=('arial', 30, 'bold'), bg='#ACE1AF', fg='white')
totalBranchcountLabel.pack()

# Frame for purchases Count
purchases_frame = Frame(window, bg='#FA86C4', bd=3, relief=RIDGE)
purchases_frame.place(x=780, y=310, height=170, width=280)
Label(purchases_frame, text='Total purchases', font=('arial', 15, 'bold'), bg='#FA86C4', fg='white').pack()
totalpurchasescountLabel = Label(purchases_frame, text='0', font=('arial', 30, 'bold'), bg='#FA86C4', fg='white')
totalpurchasescountLabel.pack()

# left menu
leftFrame = Frame(window, bd=2, relief=RIDGE, bg='white')
leftFrame.place(x=0, y=102, width=200, height=565)
leftLogo = PhotoImage(file='logo.png')
leftLabel = Label(leftFrame, image=leftLogo)
leftLabel.pack()

employeeLogo = PhotoImage(file='employee.png')
employeeButton = Button(leftFrame, text='Employee', image=employeeLogo, compound=LEFT,
                        font=('times new roman', 19, 'bold'), bg='white', cursor='hand2', bd=3, anchor='w', padx=10,
                        command=employee_form)
employeeButton.pack(fill=X)
supplierLogo = PhotoImage(file='supplier.png')
supplierButton = Button(leftFrame, text='Branches', image=supplierLogo, compound=LEFT,
                        font=('times new roman', 19, 'bold'), bg='white', cursor='hand2', bd=3, anchor='w', padx=10,
                        command=supplier_form)
supplierButton.pack(fill=X)
categoryLogo = PhotoImage(file='category.png')
customersButton = Button(leftFrame, text='Customers', image=categoryLogo, compound=LEFT,
                        font=('times new roman', 19, 'bold'), bg='white', cursor='hand2', bd=3, anchor='w', padx=10,
                        command=customers_form)
customersButton.pack(fill=X)
productLogo = PhotoImage(file='product.png')
productButton = Button(leftFrame, text='Product', image=productLogo, compound=LEFT,
                       font=('times new roman', 19, 'bold'), bg='white', cursor='hand2', bd=3, anchor='w', padx=10,
                       command=product_form)
productButton.pack(fill=X)
purchasesLogo = PhotoImage(file='sales.png')
purchasesButton = Button(leftFrame, text='Purchases', image=purchasesLogo, compound=LEFT, font=('times new roman', 19, 'bold'),
                     bg='white', cursor='hand2', bd=3, anchor='w', padx=10, command=purchases_form)
purchasesButton.pack(fill=X)

exitLogo = PhotoImage(file='exit.png')
exitButton = Button(leftFrame, text='Exit', image=exitLogo, compound=LEFT, font=('times new roman', 19, 'bold'),
                    bg='white', cursor='hand2', bd=3, anchor='w', padx=10, command=exit)
exitButton.pack(fill=X)



connection()
update_content()

window.mainloop()
