from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
from tkinter import filedialog

def purchases_page(root, mycursor, conn):
    def export_to_excel():
        data = [tree.item(item)['values'] for item in tree.get_children()]

        if not data:
            messagebox.showwarning("No Data", "No data available to export.")
            return

        columns = [col for col in tree["columns"]]
        df = pd.DataFrame(data, columns=columns)
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Export Success", f"Data exported to {file_path}")

    def search():
        if searchEntry.get() == '':
            messagebox.showerror('Error', 'Enter Purchase ID to search', parent=purchases_window)
            return
        
        purchase_id = searchEntry.get()
        query = "SELECT * FROM purchase WHERE purchaseid = %s"
        mycursor.execute(query, (purchase_id,))
        purchase_data = mycursor.fetchall()

        if not purchase_data:
            messagebox.showerror('Error', 'No purchase found with the provided Purchase ID', parent=purchases_window)
            return

        display_purchase_data(purchase_data)

    def reset():
        searchEntry.delete(0, END)
        display_purchases()

    '''def display_purchases():
        try:
            query = """
                SELECT purchaseid, date, customerid, productid, quantity, billamount, payment_method
                FROM purchase
            """
            mycursor.execute(query)
            purchase_data = mycursor.fetchall()

            # Display data in the Treeview
            display_purchase_data(purchase_data)

        except Exception as e:
            print(f"Error fetching purchase records: {e}")

    def display_purchase_data(data):
        for item in tree.get_children():
            tree.delete(item)
        for row in data:
            tree.insert("", "end", values=row)'''
    def display_purchases():
        try:
            # Select all purchase records from the purchase table
            query = "SELECT * FROM purchase"
            mycursor.execute(query)
            purchase_data = mycursor.fetchall()

            # Call helper function to display data in Treeview
            display_purchase_data(purchase_data)

        except Exception as e:
            print(f"Error fetching purchase records: {e}")
            messagebox.showerror("Database Error", f"Error fetching purchase records: {e}")

    def display_purchase_data(data):
        # Clear existing entries in the Treeview
        for item in tree.get_children():
            tree.delete(item)
        
        # Insert each row from data into the Treeview
        for row in data:
            tree.insert("", "end", values=row)


    purchases_window = Frame(root, width=1070, height=567, bg='white')
    purchases_window.place(x=200, y=100)

    titleLabel = Label(purchases_window, text='Purchase Management', font=('times new roman', 18, 'bold'), bg='#FA86C4', fg='white')
    titleLabel.place(x=0, y=0, relwidth=1)

    backImage = PhotoImage(file='back.png')
    backButton = Button(purchases_window, image=backImage, bd=0, bg='white', cursor='hand2',
                        command=lambda: purchases_window.destroy())
    backButton.image = backImage
    backButton.place(x=10, y=50)

    searchFrame = Frame(purchases_window, bg='white')
    searchFrame.place(x=250, y=80)

    purchaseIDLabel = Label(searchFrame, text='Purchase ID', font=('times new roman', 12), bg='white')
    purchaseIDLabel.grid(row=0, column=0, padx=20)
    searchEntry = Entry(searchFrame, font=('times new roman', 12), bg='lightyellow', width=14)
    searchEntry.grid(row=0, column=1)
    searchButton = Button(searchFrame, text='Search', font=('times new roman', 12, 'bold'), bg='#BCB88A', fg='white',
                          cursor='hand2', width=8, command=search)
    searchButton.grid(row=0, column=2, padx=20)

    purchases_table_frame = Frame(purchases_window, bg='white', bd=3, relief=RIDGE)
    purchases_table_frame.place(x=20, y=130, height=350, width=1000)

    scrolly = Scrollbar(purchases_table_frame, orient=VERTICAL)
    scrollx = Scrollbar(purchases_table_frame, orient=HORIZONTAL)
    tree = ttk.Treeview(purchases_table_frame, columns=("purchaseid", "date", "customerid", "productid", "quantity", "billamount", "payment_method"),
                        xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)

    scrollx.pack(side=BOTTOM, fill=X)
    scrolly.pack(side=RIGHT, fill=Y)
    scrollx.config(command=tree.xview)
    scrolly.config(command=tree.yview)

    for col in ["purchaseid", "date", "customerid", "productid", "quantity", "billamount", "payment_method"]:
        tree.heading(col, text=col.capitalize())
        tree.column(col, anchor=W, width=120)

    tree['show'] = 'headings'
    tree.pack(fill=BOTH, expand=1)

    exportButton = Button(purchases_window, text="Export to Excel", font=('times new roman', 12, 'bold'), bg='#BCB88A', fg='white',
                          cursor='hand2', command=export_to_excel)
    exportButton.place(x=450, y=500)

    resetButton = Button(purchases_window, text="Clear", font=('times new roman', 12, 'bold'), bg='#BCB88A', fg='white',
                         cursor='hand2', command=reset)
    resetButton.place(x=580, y=500)

    display_purchases()
