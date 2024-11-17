from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql


def user_page(root, mycursor, conn):
    # Functionality Part

    def id_exists(id):
        mycursor.execute('SELECT COUNT(*) FROM Users WHERE userid=%s', (id,))
        result = mycursor.fetchone()
        return result[0] > 0

    def select_data(event):
        selected = treeview.selection()
        content = treeview.item(selected)
        if content['values']:
            row = content['values']
            clear()
            userIdEntry.insert(0, row[0])
            userIdEntry.config(state='readonly')
            usernameEntry.insert(0, row[1])
            passwordEntry.insert(0, row[2])
            roleCombobox.set(row[3])
            branchIdEntry.insert(0, row[4])

    def treeview_data():
        mycursor.execute('SELECT * FROM Users')
        users = mycursor.fetchall()
        treeview.delete(*treeview.get_children())
        for user in users:
            treeview.insert('', END, values=user)

    def clear(value=False):
        if value:
            treeview.selection_remove(treeview.selection())
        userIdEntry.config(state=NORMAL)
        userIdEntry.delete(0, END)
        usernameEntry.delete(0, END)
        passwordEntry.delete(0, END)
        roleCombobox.current(0)
        branchIdEntry.delete(0, END)

    def delete_data():
        selected_item = treeview.selection()
        if not selected_item:
            messagebox.showerror('Error', 'Select data to delete', parent=user_window)
        else:
            result = messagebox.askyesno('Confirm', 'Do you really want to delete?', parent=user_window)
            if result:
                mycursor.execute('DELETE FROM Users WHERE userid=%s', (userIdEntry.get(),))
                conn.commit()
                treeview_data()
                clear()
                messagebox.showinfo('Success', 'Data is deleted', parent=user_window)

    def update_data():
        selected_item = treeview.selection()

        if not selected_item:
            messagebox.showerror('Error', 'Select data to update', parent=user_window)

        else:
            userid = userIdEntry.get()
            username = usernameEntry.get()
            password = passwordEntry.get()
            role = roleCombobox.get()
            branchid = branchIdEntry.get()

            mycursor.execute('SELECT username, password, role, branchid FROM Users WHERE userid=%s', (userid,))
            current_data = mycursor.fetchone()

            new_data = (username, password, role, branchid)

            if current_data == new_data:
                messagebox.showinfo('No Changes', 'No changes detected', parent=user_window)
            else:
                mycursor.execute(
                    'UPDATE Users SET username=%s, password=%s, role=%s, branchid=%s WHERE userid=%s',
                    (username, password, role, branchid, userid)
                )
                conn.commit()
                treeview_data()
                clear()
                messagebox.showinfo('Success', 'Data is updated', parent=user_window)

    def save_data():
        userid = userIdEntry.get()
        username = usernameEntry.get()
        password = passwordEntry.get()
        role = roleCombobox.get()
        branchid = branchIdEntry.get()

        # Check if all fields are filled
        if not (userid and username and password and role and branchid):
            messagebox.showerror('Error', 'All fields are required', parent=user_window)
            return
        
        # Check if User ID is an integer
        try:
            userid = int(userid)
        except ValueError:
            messagebox.showerror('Error', 'User ID can only be an integer', parent=user_window)
            return

        # Check if User ID already exists
        if id_exists(userid):
            messagebox.showerror('Error', 'User ID already exists', parent=user_window)
            return

        # Check if Branch ID exists as a foreign key
        mycursor.execute('SELECT 1 FROM branches WHERE branchid = %s', (branchid,))
        if mycursor.fetchone() is None:
            messagebox.showerror('Error', 'Branch ID not present', parent=user_window)
            return

        # If all checks pass, insert data
        try:
            mycursor.execute(
                'INSERT INTO Users (userid, username, password, role, branchid) VALUES (%s, %s, %s, %s, %s)',
                (userid, username, password, role, branchid)
            )
            conn.commit()
            
            # Refresh treeview data and show success message
            treeview_data()
            messagebox.showinfo('Success', 'Data is saved', parent=user_window)
            
            # Clear the input fields
            clear()
        
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}", parent=user_window)
            conn.rollback()  # Roll back any changes if there's an error


    def search():
        if searchEntry.get() == '':
            messagebox.showerror('Error', 'Enter value to search', parent=user_window)
        elif search_combobox.get() == 'Search By':
            messagebox.showerror('Error', 'Please select an option', parent=user_window)
        else:
            mycursor.execute(f'SELECT * FROM Users WHERE {search_combobox.get()} LIKE %s', ('%' + searchEntry.get() + '%',))
            result = mycursor.fetchall()
            if len(result) == 0:
                messagebox.showerror('Error', 'No record found', parent=user_window)
            else:
                treeview.delete(*treeview.get_children())
                for user in result:
                    treeview.insert('', END, values=user)

    def show_data():
        treeview_data()
        searchEntry.delete(0, END)
        search_combobox.set('Search By')

    def back_func():
        user_window.place_forget()

    # GUI
    user_window = Frame(root, width=1070, height=567, bg='white')
    user_window.place(x=200, y=100)

    titleLabel = Label(user_window, text='Manage User Details', font=('Arial', 16, 'bold'), bg='#FA86C4', fg='white')
    titleLabel.place(x=0, y=0, relwidth=1)
    backImage = PhotoImage(file='back.png')
    backButton = Button(user_window, image=backImage, bd=0, cursor='hand2', bg='white', command=back_func)
    backButton.image = backImage
    backButton.place(x=10, y=30)
    treeviewFrame = Frame(user_window, bg='white')
    treeviewFrame.place(x=0, y=50, relwidth=1, height=235)

    # Search Frame
    searchFrame = Frame(treeviewFrame, bg='white')
    searchFrame.pack()
    search_combobox = ttk.Combobox(
        searchFrame, values=('userid', 'username', 'role', 'branchid'),
        state='readonly', justify = CENTER, font=('goudy old style', 12), width=15
    )
    search_combobox.grid(row=0, column=0, padx=20, pady=10)
    search_combobox.set('Search By')
    searchEntry = Entry(searchFrame, font=('goudy old style', 12), bg='lightyellow')
    searchEntry.grid(row=0, column=1)
    searchButton = Button(searchFrame, text='Search', font=('times new roman', 12), bg='#BCB88A', fg='black', width=10,
                          command=search)
    searchButton.grid(row=0, column=2, padx=20)
    showButton = Button(searchFrame, text='Show All', font=('times new roman', 12), bg='#BCB88A', fg='black', width=10,
                        command=show_data)
    showButton.grid(row=0, column=3)

    # Treeview
    treeviewFrame = Frame(user_window, bg='white')
    treeviewFrame.place(x=0, y=100, relwidth=1, height=300)

    scrolly = Scrollbar(treeviewFrame, orient=VERTICAL)
    scrollx = Scrollbar(treeviewFrame, orient=HORIZONTAL)
    treeview = ttk.Treeview(treeviewFrame, columns=('userid', 'username', 'password', 'role', 'branchid'),
                            yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

    scrolly.pack(side=RIGHT, fill=Y)
    scrollx.pack(side=BOTTOM, fill=X)
    scrollx.config(command=treeview.xview)
    scrolly.config(command=treeview.yview)
    treeview.pack()
    treeview.heading('userid', text='UserID')
    treeview.heading('username', text='Username')
    treeview.heading('password', text='Password')
    treeview.heading('role', text='Role')
    treeview.heading('branchid', text='BranchID')

    treeview.column('userid', width=80)
    treeview.column('username', width=140)
    treeview.column('password', width=140)
    treeview.column('role', width=100)
    treeview.column('branchid', width=80)
    treeview['show'] = 'headings'

    # Details Frame with Grid Layout for Buttons
    detailsFrame = Frame(user_window, bg='white')
    detailsFrame.place(x=0, y=300, relwidth=1, height=150)  # Increase height to fit buttons

    userIdLabel = Label(detailsFrame, text='UserID', font=('times new roman', 12), bg='white')
    userIdLabel.grid(row=0, column=0, padx=(60, 10), sticky='w')
    userIdEntry = Entry(detailsFrame, font=('times new roman', 12), bg='lightyellow')
    userIdEntry.grid(row=0, column=1, pady=15)

    usernameLabel = Label(detailsFrame, text='Username', font=('times new roman', 12), bg='white')
    usernameLabel.grid(row=0, column=2, padx=(60,10), sticky='w')
    usernameEntry = Entry(detailsFrame, font=('times new roman', 12), bg='lightyellow')
    usernameEntry.grid(row=0, column=3)

    passwordLabel = Label(detailsFrame, text='Password', font=('times new roman', 12), bg='white')
    passwordLabel.grid(row=1, column=0, padx=20, sticky='w')
    passwordEntry = Entry(detailsFrame, font=('times new roman', 12), bg='lightyellow')
    passwordEntry.grid(row=1, column=1, pady=15)

    roleLabel = Label(detailsFrame, text='Role', font=('times new roman', 12), bg='white')
    roleLabel.grid(row=1, column=2, padx=20, sticky='w')
    roleCombobox = ttk.Combobox(detailsFrame, values=('Manager', 'Cashier'), state='readonly',
                                font=('times new roman', 12), width=18)
    roleCombobox.grid(row=1, column=3)
    roleCombobox.set('Manager')

    branchIdLabel = Label(detailsFrame, text='BranchID', font=('times new roman', 12), bg='white')
    branchIdLabel.grid(row=2, column=0, padx=20, sticky='w')
    branchIdEntry = Entry(detailsFrame, font=('times new roman', 12), bg='lightyellow')
    branchIdEntry.grid(row=2, column=1, pady=15)
    # buttons

    buttonFrame = Frame(user_window, bg='white')

    buttonFrame.place(x=260, y=520)
    # Configure button layout
    addButton = Button(buttonFrame, text='Save', font=('times new roman', 12), bg='#BCB88A', fg='black', width=10,
                       command=save_data)
    addButton.grid(row=0, column=0, padx=20)
    updateButton = Button(buttonFrame, text='Update', font=('times new roman', 12), bg='#BCB88A', fg='black', width=10, command=update_data)
    updateButton.grid(row=0, column=1, padx=20)
    deleteButton = Button(buttonFrame, text='Delete', font=('times new roman', 12), bg='#BCB88A', fg='black', width=10, command=delete_data)
    deleteButton.grid(row=0, column=2, padx=20)
    clearButton = Button(buttonFrame, text='Clear', font=('times new roman', 12), bg='#BCB88A', fg='black', width=10,
                         command=lambda: clear(True))
    clearButton.grid(row=0, column=3, padx=20)

    treeview_data()
    treeview.bind('<ButtonRelease-1>', select_data)

    return user_window, mycursor
