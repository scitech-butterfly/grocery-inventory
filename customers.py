from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql


def customers_page(root, mycursor, conn):
    # Functionality Part

    def id_exists(id):
        mycursor.execute('SELECT COUNT(*) FROM customers WHERE customerid=%s', (id,))
        result = mycursor.fetchone()
        return result[0] > 0

    def treeview_data():
        mycursor.execute('SELECT * FROM customers')
        customers = mycursor.fetchall()
        treeview.delete(*treeview.get_children())
        for customer in customers:
            treeview.insert('', END, values=customer)

    def clear():
        customersIdEntry.config(state=NORMAL)
        customersIdEntry.delete(0, END)
        firstNameEntry.delete(0, END)
        lastNameEntry.delete(0, END)
        phoneEntry.delete(0, END)
        emailEntry.delete(0, END)

    def delete_data():
        selected_item = treeview.selection()
        if not selected_item:
            messagebox.showerror('Error', 'Select data to delete', parent=customers_window)
        else:
            result = messagebox.askyesno('Confirm', 'Do you really want to delete?', parent=customers_window)
            if result:
                item = treeview.item(selected_item)
                customer_id = item['values'][0]
                mycursor.execute('DELETE FROM customers WHERE customerid=%s', (customer_id,))
                conn.commit()
                treeview_data()
                clear()
                messagebox.showinfo('Success', 'Data is deleted', parent=customers_window)

    def add_data():
        if not (customersIdEntry.get() and firstNameEntry.get() and lastNameEntry.get() and phoneEntry.get() and emailEntry.get()):
            messagebox.showerror('Error', 'All fields are required', parent=customers_window)
        elif id_exists(customersIdEntry.get()):
            messagebox.showerror('Error', 'ID already exists', parent=customers_window)
        else:
            mycursor.execute('INSERT INTO customers VALUES (%s, %s, %s, %s, %s)', (
                customersIdEntry.get(), firstNameEntry.get(), lastNameEntry.get(),
                phoneEntry.get(), emailEntry.get()
            ))
            conn.commit()
            treeview_data()
            messagebox.showinfo('Success', 'Data is saved', parent=customers_window)
            clear()

    # GUI Frame
    customers_window = Frame(root, width=1070, height=567, bg='white')
    customers_window.place(x=200, y=100)

    backImage = PhotoImage(file='back.png')
    backButton = Button(customers_window, image=backImage, bd=0, bg='white', cursor='hand2',
                        command=lambda: customers_window.destroy())
    backButton.image = backImage
    backButton.place(x=10, y=50)

    titleLabel = Label(customers_window, text='Manage Customer Details', font=('Arial', 15, 'bold'), bg='#FA86C4', fg='white')
    titleLabel.place(x=0, y=0, relwidth=1)

    logo = PhotoImage(file='customers.png')
    label = Label(customers_window, image=logo, bg='white')
    label.image = logo
    label.place(x=30, y=120)

    # Details Frame
    detailsFrame = Frame(customers_window, bg='white')
    detailsFrame.place(x=500, y=60)

    customersIdLabel = Label(detailsFrame, text='Customer ID', font=('times new roman', 13), bg='white')
    customersIdLabel.grid(row=0, column=0, padx=20, pady=10, sticky='w')
    customersIdEntry = Entry(detailsFrame, font=('times new roman', 13), bg='lightyellow', width=26)
    customersIdEntry.grid(row=0, column=1, padx=20, pady=10, sticky='w')

    firstNameLabel = Label(detailsFrame, text='First Name', font=('times new roman', 13), bg='white')
    firstNameLabel.grid(row=1, column=0, padx=20, pady=10, sticky='w')
    firstNameEntry = Entry(detailsFrame, font=('times new roman', 13), bg='lightyellow', width=26)
    firstNameEntry.grid(row=1, column=1, padx=20, pady=10, sticky='w')

    lastNameLabel = Label(detailsFrame, text='Last Name', font=('times new roman', 13), bg='white')
    lastNameLabel.grid(row=2, column=0, padx=20, pady=10, sticky='w')
    lastNameEntry = Entry(detailsFrame, font=('times new roman', 13), bg='lightyellow', width=26)
    lastNameEntry.grid(row=2, column=1, padx=20, pady=10, sticky='w')

    phoneLabel = Label(detailsFrame, text='Phone Number', font=('times new roman', 13), bg='white')
    phoneLabel.grid(row=3, column=0, padx=20, pady=10, sticky='w')
    phoneEntry = Entry(detailsFrame, font=('times new roman', 13), bg='lightyellow', width=26)
    phoneEntry.grid(row=3, column=1, padx=20, pady=10, sticky='w')

    emailLabel = Label(detailsFrame, text='Email ID', font=('times new roman', 13), bg='white')
    emailLabel.grid(row=4, column=0, padx=20, pady=10, sticky='w')
    emailEntry = Entry(detailsFrame, font=('times new roman', 13), bg='lightyellow', width=26)
    emailEntry.grid(row=4, column=1, padx=20, pady=10, sticky='w')

    # Buttons
    buttonFrame = Frame(customers_window, bg='white')
    buttonFrame.place(x=665, y=300)

    addButton = Button(buttonFrame, text='Add', font=('times new roman', 12, 'bold'), width=8, fg='white',
                       bg='#BCB88A', cursor='hand2', command=add_data)
    addButton.grid(row=0, column=0, padx=8)

    deleteButton = Button(buttonFrame, text='Delete', font=('times new roman', 12, 'bold'), width=8, fg='white',
                          bg='#BCB88A', cursor='hand2', command=delete_data)
    deleteButton.grid(row=0, column=2, padx=8)

    # Treeview Frame
    treeviewFrame = Frame(customers_window, bg='white')
    treeviewFrame.place(x=530, y=340, height=200, width=500)

    scrolly = Scrollbar(treeviewFrame, orient=VERTICAL)
    scrollx = Scrollbar(treeviewFrame, orient=HORIZONTAL)

    treeview = ttk.Treeview(treeviewFrame, columns=('customerid', 'firstname', 'lastname', 'phone', 'email'),
                            yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

    scrolly.pack(side=RIGHT, fill=Y)
    scrollx.pack(side=BOTTOM, fill=X)

    scrolly.config(command=treeview.yview)
    scrollx.config(command=treeview.xview)
    treeview.pack(fill=BOTH, expand=1)
    treeview.heading('customerid', text='Customer ID')
    treeview.heading('firstname', text='First Name')
    treeview.heading('lastname', text='Last Name')
    treeview.heading('phone', text='Phone Number')
    treeview.heading('email', text='Email ID')

    treeview.column('customerid', width=80)
    treeview.column('firstname', width=120)
    treeview.column('lastname', width=120)
    treeview.column('phone', width=120)
    treeview.column('email', width=160)
    treeview['show'] = 'headings'

    # Load data into Treeview
    treeview_data()
    return customers_window, mycursor
