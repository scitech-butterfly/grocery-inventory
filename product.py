from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql

def product_page(root, mycursor, conn):
    # Function to handle selection of a row in the Treeview
    def select_data(event):
        selected = treeview.selection()
        if selected:
            row = treeview.item(selected[0])['values']
            if row:
                clear()
                idEntry.insert(0, row[0])
                nameEntry.insert(0, row[1])
                priceEntry.insert(0, row[2])

    # Load data into Treeview
    def treeview_data():
        mycursor.execute('SELECT * FROM products')
        products = mycursor.fetchall()
        treeview.delete(*treeview.get_children())
        for product in products:
            treeview.insert('', END, values=product)

    # Search function to find products by Product ID
    def search_product(mycursor, product_id):
        if not product_id:
            messagebox.showwarning("Input Required", "Please enter a Product ID to search.")
            return
        
        query = "SELECT * FROM products WHERE productid = %s"
        mycursor.execute(query, (product_id,))
        result = mycursor.fetchall()

        treeview.delete(*treeview.get_children())
        if result:
            for row in result:
                treeview.insert('', END, values=row)
        else:
            messagebox.showinfo("Not Found", "No product found with the given Product ID.")

    # Save new product data to the database
    def save_data():
        product_id = idEntry.get()
        product_name = nameEntry.get()
        price = priceEntry.get()

        # Check if product name and price are filled
        if not product_name or not price:
            messagebox.showerror("Error", "Product name and price are required.")
            return

        # Check if product_id is an integer
        try:
            product_id = int(product_id)
        except ValueError:
            messagebox.showerror("Error", "Product ID should be an integer.")
            return

        # Check if product_name is not an integer
        if product_name.isdigit():
            messagebox.showerror("Error", "Product name cannot be an integer.")
            return

        # Attempt to insert data into the database
        try:
            mycursor.execute("INSERT INTO products (productid, productname, price) VALUES (%s, %s, %s)",
                            (product_id, product_name, price))
            conn.commit()
            messagebox.showinfo("Success", "Product added successfully!")
            
            # Clear input fields and refresh treeview
            clear()
            treeview_data()
        
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", str(e))


    # Update existing product data in the database
    def update_data():
        product_id = idEntry.get()
        product_name = nameEntry.get()
        price = priceEntry.get()

        if not product_id:
            messagebox.showerror("Error", "Please select a product to update.")
            return

        try:
            mycursor.execute("UPDATE products SET productname=%s, price=%s WHERE productid=%s",
                             (product_name, price, product_id))
            conn.commit()
            messagebox.showinfo("Success", "Product updated successfully!")
            clear()
            treeview_data()
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", str(e))

    # Delete selected product from the database
    '''def delete_data():
        product_id = idEntry.get()

        if not product_id:
            messagebox.showerror("Error", "Please select a product to delete.")
            return

        try:
            mycursor.execute("DELETE FROM products WHERE productid=%s", (product_id,))
            conn.commit()
            messagebox.showinfo("Success", "Product deleted successfully!")
            clear()
            treeview_data()
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", str(e))'''
    
    def delete_data():
    # Get the product ID from the entry field
     product_id = idEntry.get()
    
    # Check if a product ID was provided
     if not product_id:
        messagebox.showerror("Error", "Please select a product to delete.")
        return

    # Confirmation dialog before deletion
     confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this product?")
     if not confirm:
        return

     try:
        # Execute delete query
         mycursor.execute("DELETE FROM products WHERE productid = %s", (product_id,))
         conn.commit()  # Commit the changes to the database

         messagebox.showinfo("Success", "Product deleted successfully!")
        
        # Clear the entry fields and refresh the data view
         clear()
         treeview_data()
    
     except pymysql.MySQLError as e:
         messagebox.showerror("Database Error", f"An error occurred: {e}")

    # Clear entry fields
    def clear():
        idEntry.delete(0, END)
        nameEntry.delete(0, END)
        priceEntry.delete(0, END)

    # GUI setup
    product_window = Frame(root, width=1070, height=567, bg='white')
    product_window.place(x=200, y=100)

    # Title label
    titleLabel = Label(product_window, text='Product Management', font=('times new roman', 18, 'bold'), bg='#FA86C4', fg='white')
    titleLabel.place(x=0, y=0, relwidth=1)

    # Back button
    backImage = PhotoImage(file='back.png')
    backButton = Button(product_window, image=backImage, bd=0, bg='white', cursor='hand2',
                        command=lambda: product_window.destroy())
    backButton.image = backImage
    backButton.place(x=10, y=50)

    # Search frame for finding products by Product ID
    searchFrame = Frame(product_window, bg='white')
    searchFrame.place(x=250, y=80)
    searchLabel = Label(searchFrame, text='Product ID', font=('times new roman', 12), bg='white')
    searchLabel.grid(row=0, column=0, padx=20)
    searchEntry = Entry(searchFrame, font=('times new roman', 12), bg='lightyellow', width=14)
    searchEntry.grid(row=0, column=1)
    searchButton = Button(searchFrame, text='Search Product', font=('times new roman', 12, 'bold'), bg='#BCB88A', fg='white',
                          cursor='hand2', width=12, command=lambda: search_product(mycursor, searchEntry.get()))
    searchButton.grid(row=0, column=2, padx=20)

    # Entry form for adding new products
    formFrame = Frame(product_window, bg='white')
    formFrame.place(x=100, y=150)

    Label(formFrame, text='Product ID:', font=('times new roman', 12), bg='white').grid(row=0, column=0, padx=10, pady=5)
    idEntry = Entry(formFrame, font=('times new roman', 12), bg='lightyellow')
    idEntry.grid(row=0, column=1, padx=10, pady=5)

    Label(formFrame, text='Product Name:', font=('times new roman', 12), bg='white').grid(row=1, column=0, padx=10, pady=5)
    nameEntry = Entry(formFrame, font=('times new roman', 12), bg='lightyellow')
    nameEntry.grid(row=1, column=1, padx=10, pady=5)

    Label(formFrame, text='Price:', font=('times new roman', 12), bg='white').grid(row=2, column=0, padx=10, pady=5)
    priceEntry = Entry(formFrame, font=('times new roman', 12), bg='lightyellow')
    priceEntry.grid(row=2, column=1, padx=10, pady=5)

    buttonFrame = Frame(formFrame, bg="white")
    buttonFrame.grid(row=3, column=0, columnspan=2, pady=20)

    save_button = Button(buttonFrame, text="Save", font=("times new roman", 12, "bold"), bg="#BCB88A", fg="white",
        cursor="hand2", command=save_data)
    save_button.grid(row=0, column=0, padx=10)

    update_button = Button(buttonFrame, text="Update", font=("times new roman", 12, "bold"), bg="#BCB88A", fg="white",
        cursor="hand2", command=update_data)
    update_button.grid(row=0, column=1, padx=10)

    delete_button = Button(buttonFrame, text="Delete", font=("times new roman", 12, "bold"), bg="#BCB88A", fg="white",
        cursor="hand2", command=delete_data)
    delete_button.grid(row=0, column=2, padx=10)

    # Table for displaying the product list
    tableFrame = Frame(product_window, bg='white')
    tableFrame.place(x=100, y=300)

    columns = ("Product ID", "Product Name", "Price")
    treeview = ttk.Treeview(tableFrame, columns=columns, show="headings")
    treeview.heading("Product ID", text="Product ID")
    treeview.heading("Product Name", text="Product Name")
    treeview.heading("Price", text="Price")
    treeview.bind("<Double-1>", select_data)
    treeview.pack(fill=BOTH, expand=True)

    # Scrollbar for the table
    scrollbar = Scrollbar(tableFrame, orient=VERTICAL, command=treeview.yview)
    treeview.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Load initial data into the table
    treeview_data()
    return product_window, mycursor
