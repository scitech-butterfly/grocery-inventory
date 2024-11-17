from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql


def inventory_page(root, mycursor, conn):
    # Functionality Part

    def id_exists(id):
        mycursor.execute('SELECT COUNT(*) FROM branchinventory WHERE branchinventoryid=%s', (id,))
        result = mycursor.fetchone()
        print("Checking ID:", id, "Exists:", result[0])  # Debugging line to check result
        return result[0] > 0


    def select_data(event):
        selected = treeview.selection()
        content = treeview.item(selected)
        if content['values']:
            row = content['values']
            clear()
            branchInventoryEntry.insert(0, row[0])
            branchInventoryEntry.config(state='readonly')
            branchEntry.insert(0, row[1])
            productEntry.insert(0, row[2])
            quantityEntry.insert(0, row[3])

    def treeview_data():
        # Modify the query to include the branchname and productname by using JOIN
        query = '''
        SELECT bi.branchinventoryid, b.branchname, p.productname, bi.quantity
        FROM branchinventory bi
        JOIN branches b ON bi.branchid = b.branchid
        JOIN products p ON bi.productid = p.productid
        '''
        mycursor.execute(query)
        inventory_items = mycursor.fetchall()

        # Clear existing rows
        treeview.delete(*treeview.get_children())

        # Insert new rows with the branch name and product name
        for item in inventory_items:
            treeview.insert('', END, values=item)


    def clear(value=False):
        if value:
            treeview.selection_remove(treeview.selection())
        branchInventoryEntry.config(state=NORMAL)
        branchInventoryEntry.delete(0, END)
        branchEntry.delete(0, END)
        productEntry.delete(0, END)
        quantityEntry.delete(0, END)

    def delete_data():
        selected_item = treeview.selection()
        if not selected_item:
            messagebox.showerror('Error', 'Select data to delete', parent=inventory_window)
        else:
            result = messagebox.askyesno('Confirm', 'Do you really want to delete?', parent=inventory_window)
            if result:
                mycursor.execute('DELETE FROM branchinventory WHERE branchinventoryid=%s', (branchInventoryEntry.get(),))
                conn.commit()
                treeview_data()
                clear()
                messagebox.showinfo('Success', 'Data is deleted', parent=inventory_window)

    def update_data():
        selected_item = treeview.selection()

        if not selected_item:
            messagebox.showerror('Error', 'Select data to update', parent=inventory_window)
        else:
            # Get the new data entered by the user
            new_branch = branchEntry.get()
            new_product = productEntry.get()
            new_quantity = quantityEntry.get()

            # Update the data
            mycursor.execute(
                'UPDATE branchinventory SET branchid=%s, productid=%s, quantity=%s WHERE branchinventoryid=%s',
                (new_branch, new_product, new_quantity, branchInventoryEntry.get()))
            conn.commit()
            treeview_data()
            clear()
            messagebox.showinfo('Success', 'Data is updated', parent=inventory_window)

    '''def save_data():
        bi = branchInventoryEntry.get()
        be = branchEntry.get()
        pe = productEntry.get()
        qe= quantityEntry.get()
        if not (bi  and be and pe and qe):
            messagebox.showerror('Error', 'All fields are required', parent=inventory_window)
        elif id_exists(bi):
            messagebox.showerror('Error', 'Branch inventory ID already exists', parent=inventory_window)
        else:
            mycursor.execute('INSERT INTO branchinventory VALUES (%s, %s, %s, %s)', (
                bi, be, pe, qe))
            conn.commit()
            treeview_data()
            messagebox.showinfo('Success', 'Data is saved', parent=inventory_window)
            clear()'''
    
    def save_data():
        bi = branchInventoryEntry.get()
        be = branchEntry.get()
        pe = productEntry.get()
        qe = quantityEntry.get()

        # Ensure all fields are filled
        if not (bi and be and pe and qe):
            messagebox.showerror('Error', 'All fields are required', parent=inventory_window)
            return

        # Check if the branch inventory ID already exists
        if id_exists(bi):
            messagebox.showerror('Error', 'Branch inventory ID already exists', parent=inventory_window)
            return

        try:
            # Insert data into the database
            mycursor.execute('INSERT INTO branchinventory (branchinventoryid, branchid, productid, quantity) VALUES (%s, %s, %s, %s)', (
                bi, be, pe, qe))
            conn.commit()
            
            # Update the treeview to reflect changes and show success message
            treeview_data()
            messagebox.showinfo('Success', 'Data is saved', parent=inventory_window)
            
            # Clear the entry fields after saving
            clear()
        
        except pymysql.MySQLError as e:
            # Handle any database error and show it to the user
            messagebox.showerror("Database Error", f"An error occurred: {e}", parent=inventory_window)
            conn.rollback()  # Rollback in case of error


    def search():
        if searchEntry.get() == '':
            messagebox.showerror('Error', 'Enter value to search', parent=inventory_window)
        else:
            mycursor.execute('SELECT * FROM branchinventory WHERE branchinventoryid = %s', (searchEntry.get(),))
            result = mycursor.fetchall()
            if not result:
                messagebox.showerror('Error', 'No record found', parent=inventory_window)
            else:
                treeview.delete(*treeview.get_children())
                for item in result:
                    treeview.insert('', END, values=item)

    def show_data():
      query = '''
            SELECT bi.branchinventoryid, b.branchid, b.branchname, p.productid, p.productname, bi.quantity
            FROM branchinventory bi
            JOIN branches b ON bi.branchid = b.branchid
            JOIN products p ON bi.productid = p.productid
            '''
    
      try:
        # Execute the query to fetch all records
        mycursor.execute(query)
        inventory_items = mycursor.fetchall()

        # Clear existing rows in the treeview
        treeview.delete(*treeview.get_children())

        # Insert all rows into the treeview
        for item in inventory_items:
            treeview.insert('', END, values=item)

        # Clear the search entry to remove any filters
        searchEntry.delete(0, END)
    
      except pymysql.MySQLError as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

    def back_func():
        inventory_window.place_forget()

    # GUI Layout
    inventory_window = Frame(root, width=1070, height=567, bg='white')
    inventory_window.place(x=200, y=100)

    titleLabel = Label(inventory_window, text='Manage Inventory Details', font=('Arial', 15, 'bold'), bg='#FA86C4',
                       fg='white')
    titleLabel.place(x=0, y=0, relwidth=1)

    backImage = PhotoImage(file='back.png')
    backButton = Button(inventory_window, image=backImage, bd=0, bg='white', cursor='hand2', command=back_func)
    backButton.image = backImage
    backButton.place(x=10, y=50)

    leftFrame = Frame(inventory_window, bg='white')
    leftFrame.place(x=10, y=100)

    branchInventoryLabel = Label(leftFrame, text='Branch Inventory ID', font=('times new roman', 13, 'bold'), bg='white')
    branchInventoryLabel.grid(row=0, column=0, sticky='w', padx=(10, 20))
    branchInventoryEntry = Entry(leftFrame, font=('times new roman', 13), bg='white')
    branchInventoryEntry.grid(row=0, column=1, pady=20, sticky='w')

    branchLabel = Label(leftFrame, text='Branch ID', font=('times new roman', 13, 'bold'), bg='white')
    branchLabel.grid(row=1, column=0, sticky='w', padx=(10, 20))
    branchEntry = Entry(leftFrame, font=('times new roman', 13), bg='white')
    branchEntry.grid(row=1, column=1, sticky='w')

    productLabel = Label(leftFrame, text='Product ID', font=('times new roman', 13, 'bold'), bg='white')
    productLabel.grid(row=2, column=0, sticky='w', padx=(10, 20))
    productEntry = Entry(leftFrame, font=('times new roman', 13), bg='white')
    productEntry.grid(row=2, column=1, pady=20, sticky='w')

    quantityLabel = Label(leftFrame, text='Quantity', font=('times new roman', 13, 'bold'), bg='white')
    quantityLabel.grid(row=3, column=0, sticky='w', padx=(10, 20))
    quantityEntry = Entry(leftFrame, font=('times new roman', 13), bg='white')
    quantityEntry.grid(row=3, column=1, pady=20, sticky='w')

    # Buttons
    buttonFrame = Frame(inventory_window, bg='white')
    buttonFrame.place(x=140, y=470)

    saveButton = Button(buttonFrame, text='Save', font=('times new roman', 12, 'bold'), width=8, fg='white',
                        bg='#BCB88A', cursor='hand2', command=save_data)
    saveButton.grid(row=0, column=0, padx=8)
    updateButton = Button(buttonFrame, text='Update', font=('times new roman', 12, 'bold'), width=8, fg='white',
                          bg='#BCB88A', cursor='hand2', command=update_data)
    updateButton.grid(row=0, column=1, padx=8)
    deleteButton = Button(buttonFrame, text='Delete', font=('times new roman', 12, 'bold'), width=8, fg='white',
                          bg='#BCB88A', cursor='hand2', command=delete_data)
    deleteButton.grid(row=0, column=2, padx=8)
    clearButton = Button(buttonFrame, text='Clear', font=('times new roman', 12, 'bold'), width=8, fg='white',
                         bg='#BCB88A', cursor='hand2', command=lambda: clear(True))
    clearButton.grid(row=0, column=3, padx=8)

    searchFrame = Frame(inventory_window, bg='white')
    searchFrame.place(x=565, y=115)

    searchLabel = Label(searchFrame, text='Inventory ID', font=('times new roman', 13, 'bold'), bg='white')
    searchLabel.grid(row=0, column=0, padx=20)
    searchEntry = Entry(searchFrame, font=('times new roman', 13), bg='lightyellow', width=14)
    searchEntry.grid(row=0, column=1)
    searchButton = Button(searchFrame, text='Search', font=('times new roman', 12, 'bold'), bg='#BCB88A', fg='white',
                          cursor='hand2', width=8, command=search)
    searchButton.grid(row=0, column=2, padx=20)

    showButton = Button(searchFrame, text='Show All', font=('times new roman', 12, 'bold'), width=8, fg='white',
                        bg='#BCB88A', cursor='hand2', command=show_data)
    showButton.grid(row=0, column=3, padx=20)

    # Treeview for displaying branchinventory data
    treeviewFrame = Frame(inventory_window, bg='white')
    treeviewFrame.place(x=500, y=150)

    columns = ('Branch Inventory ID', 'Branch ID', 'Branch Name', 'Product ID', 'Product Name', 'Quantity')
    treeview = ttk.Treeview(treeviewFrame, columns=columns, show='headings')

    treeview.heading('Branch Inventory ID', text='Branch Inventory ID')
    treeview.heading('Branch ID', text='Branch ID')
    treeview.heading('Branch Name', text='Branch Name')
    treeview.heading('Product ID', text='Product ID')
    treeview.heading('Product Name', text='Product Name')
    treeview.heading('Quantity', text='Quantity')

    treeview.column('Branch Inventory ID', width=100)
    treeview.column('Branch ID', width=75)
    treeview.column('Branch Name', width=100)
    treeview.column('Product ID', width=75)
    treeview.column('Product Name', width=100)
    treeview.column('Quantity', width=75)

    treeview.pack(fill=BOTH, expand=True)

    treeview.bind('<ButtonRelease-1>', select_data)

    treeview_data()


