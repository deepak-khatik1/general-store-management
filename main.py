# --------------------Imports--------------------

import os
import hashlib
import getpass
from datetime import date, datetime

import mysql.connector as db
from tabulate import tabulate
from fpdf import FPDF
from termcolor import colored

# --------------Database Connection--------------

database = db.connect(user='root', passwd='', host='localhost', database='term2project')
sql = database.cursor()
database.autocommit = True

# ---------------Utility Functions---------------

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)

def Date():
    Date = date.today().strftime("%d-%b-%Y")
    return str(Date)

def Time():
    Time = datetime.now().strftime('%I:%M %p')
    return str(Time)
    
def hashed(obj):
    a = hashlib.md5(obj.encode())
    hash = a.hexdigest()
    return hash

def tabulize(head, content):
    table = tabulate(content, headers=head, tablefmt='pretty')
    return table

def pdf(file):
    pdf = FPDF()   
    pdf.add_page()
    pdf.set_font('Courier', size = 16.5)

    with open(f"{file}.txt", "r") as f:
        for i in f:
            pdf.cell(200, 5.3, txt = i, ln = 1)
    
    pdf.output(f"{file}.pdf")
    os.remove(f"{file}.txt")


def bill_id():
    sql.execute('SELECT bill_id FROM data;')
    ids = sql.fetchall()
    last_id = int(ids[-1][0])
    bill_id = last_id+1
    return str(bill_id)

def products():
    data = []
    sql.execute("SELECT id,name,price,stock FROM products;")
    table = sql.fetchall()
    for i in table:
        data.append(i)
    return data

def data(condition):
    data = []
    sql.execute(f"SELECT date,time,bill_id,costumer_name,phone FROM data where {condition};")
    table = sql.fetchall()
    for i in table:
        data.append(i)
    return data

def cart():
    cart = []
    while True:
        i = input(color('Enter Product_ID, Quantity: ', 'Input'))
        if i=='n':
            break
        else:
            try:
                product, qnt = i.split(',')
                if int(qnt):
                    item = (product, qnt)
                    cart.append(item)
            except Exception as e:
                print(color("Error! Enter details as (product_id,quantity)\n", 'Error'))    
    return cart

def update_stock(update_list):
    for i in update_list:
        sql.execute("UPDATE products SET stock=%s WHERE id=%s;", (i[1], i[0]))
    print(color("STOCK UPDATED", "Error"))

def pID():
    data = []
    sql.execute("SELECT id FROM products;")
    pIDs = sql.fetchall()
    for i in pIDs:
        data.append(i[0])
    return data

def color(text, color):
    if color=='Success':
        output = colored(text, 'green', attrs=['bold'])
    elif color=='Error':
        output = colored(text, 'red', attrs=['bold'])
    elif color=='Text' or color=='Warning':
        output = colored(text, 'yellow', attrs=['bold'])
    elif color=='Input':
        output = colored(text, 'cyan', attrs=['bold'])
    return output


# ----------------Menu Functions----------------

def home():
    clearConsole()
    print('='*50)
    print(' '*19, 'WELCOME')
    print('='*50)
    print()
    
    print('1 -> Generate Bill')
    print('2 -> View Products')
    print('3 -> Stock Report')
    print('4 -> Manage Products')
    print('5 -> Search Records / Save Invoice')
    print('6 -> Change Password')
    print('0 -> Exit')

    print()
    print("="*50)
    print()

# ------
def generate_bill():
    prd = products()
    crt = cart()
    bill_table = []
    Amount = 0
    remaining_stock_list = []
    reject_list = []

    for i in crt:
        for j in prd:
            if i[0]==j[0]:
                if int(i[1])>int(j[3]):
                    reject_list.append(i[0])
                else:
                    name = str(j[1])
                    price = int(j[2])
                    qnt = int(i[1])
                    amt = price*qnt
                    Amount += amt

                    stock_update = (j[0],str(int(j[3])-int(i[1])))
                    remaining_stock_list.append(stock_update)

                    item = [name, price, qnt, amt]
                    bill_table.append(item)  
                          
    IDs = pID()
    cIDs = []
    for i in crt:
        cIDs.append(i[0])

    for i in cIDs:
        if i not in IDs:
            reject_list.append(i)

    header = ['Item', 'Per Item Cost', 'Quantity', 'Amount']
    Bill = tabulize(header, bill_table)

    print('-'*50)
    Name = input(color("Enter Costumer Name: ", 'Input'))
    Phone = input(color("Enter Contact Number: ", 'Input'))

    with open('draft.txt', 'r') as f:
        draft = f.read()
    

    draft = draft.replace('<<DATE>>'    ,str(Date()))
    draft = draft.replace('<<TIME>>'    ,str(Time()))
    draft = draft.replace('<<INVOICE>>' ,str(bill_id()))
    draft = draft.replace('<<NAME>>'    ,str(Name))
    draft = draft.replace('<<TABLE>>'   ,str(Bill))
    draft = draft.replace('<<AMOUNT>>'  ,str(Amount))
    Invoice = draft

    file = rf'auto_bills\Invoice_{bill_id()}'
    with open(f"{file}.txt", 'w') as f:
        f.write(Invoice)

    with open(f"{file}.txt", 'rb') as f:
        Invoice_binary = f.read()

    pdf(file)

    sql.execute("INSERT INTO data VALUES(%s, %s, %s, %s, %s, %s);", 
               (Date(), Time(), bill_id(), Name, Phone, Invoice_binary))

    update_stock(remaining_stock_list)

    return reject_list

# ------
def view_products():
    head = ['Product ID', 'Name', 'Per item cost', 'Stock']
    table = products()
    if len(table)!=0:
        print(color("Details of all the products : \n", 'Input'))
        print(color(tabulize(head, table), 'Text'))
    else:
        print(color("No Products Found", 'Warning'))

# ------

def stock_report():
    threshold = 3
    reorder_list = []

    for product in products():
        if int(product[3])<threshold:
            reorder_list.append(product)

    if len(reorder_list)>0:
        head = ['Product ID', 'Name', 'Per item cost', 'Stock']
        table = reorder_list

        print(color("Following products are below threshold quantity(3) and need to be reordered:\n", 'Error'))

        print(color(tabulize(head, table), 'Text'))
    else:
        print(color("Stock is sufficient. Nothing to reorder", 'Warning'))


# ------
def manage_products():
    
    def add():
        n = int(input(color('\nEnter the number of Products you want to add: ', 'Input')))
        print(color('\nEnter details in form - << product_id,product_name,price,stock >>', 'Text'))
        print('-'*50)

        rejection=False
        success=0

        products = []

        i = 0
        while i<n:
            try:
                a = input(color(f'Enter details of product {i+1}: ', 'Input'))
                x,y,z,s = a.split(',')
                if int(z):
                    item = (x,y,z,s) 
                    products.append(item)
                    i+=1
                
            except Exception as e:
                print(color("Error! Enter details in correct format\n", 'Error'))
             
   
        print('-'*50)
        IDs = pID()
        rej_lst = []
        for i in products:
            if i[0] in IDs:
                rej_lst.append(i[0])
                rejection = True
            else:
                sql.execute('''INSERT INTO products (id,name,price,stock)
                            VALUES(%s, %s, %s, %s);''', (i[0], i[1], i[2], i[3]))
                success += 1

        return rejection,success,rej_lst,products

    def edit():
        prd = products()
        edit_list = []
        
        print(color("\n--- Enter 'n' when all Product IDs are entered ---", 'Text'))
        print('-'*50)
        while True:
            a = input(color('Enter Product ID : ', 'Input'))
            if a == 'n':
                break
            else:
                edit_list.append(a)

        print('-'*50)
  
        update_list = []
        for i in edit_list:
            for j in prd:
                if i == j[0]:
                    while True:
                        try:
                            a = input(color(
                            f"Enter new (name,price,stock) for '{j[0]}' ({j[1]},{j[2]},{j[3]}): ", 'Input'))

                            name, price, stock = a.split(',')
                            if int(price) and int(stock):
                                item = (name, price, stock, i)
                                update_list.append(item)
                                break 
                        except Exception as e:
                            print(color("Error! Enter details in correct format\n", 'Error'))

        reject_list = []
        IDs = pID()
        for i in edit_list:
            if i not in IDs:
                reject_list.append(i)

        for i in update_list:
            sql.execute("UPDATE products SET name=%s, price=%s, stock=%s WHERE id=%s;",
                       (i[0], i[1], i[2], i[3]))

        return reject_list, update_list, edit_list 

    while True:
        print('='*50)
        print(' '*16, 'MANAGE PRODUCTS')
        print('='*50)
        print()
        print('1 -> Add Products')
        print('2 -> Edit Products')
        print('0 -> Go Back')
        print()
        print("="*50)
        choice = input('\nEnter your choice: ')

        if choice=='1':
            print('_'*50)
            try:
                R, S, R_lst, Prds= add()
                if R:
                    print(color(f"{R_lst} already assigned, use different Product ID", 'Text'))
                    print(color(f"\n{S} out of {len(Prds)} products added SUCCESSFULLY",
                                'Success'))
                elif not(R):
                    print(color('All products added SUCCESSFULLY', 'Success'))

            except ValueError:
                print(color("\nError !!!  Try Again", 'Error'))

            print('-'*50)
            input("\nPress Enter to choose again...")
            clearConsole()
        
        elif choice=='2':
            try:
                R, S, T= edit()
                if len(R)>0 and len(S)>0:
                    print('-'*50)
                    print(color(f"{R} NOT FOUND", 'Warning'))
                elif len(R)>0:     
                    print(color(f"{R} NOT FOUND", 'Warning'))
                
                if len(R)==0 and len(S)>0:
                    print('-'*50)
                    print(color("All products edited SUCCESSFULLY", 'Success'))
                else:
                   print(color(f"\n{len(S)} out of {len(T)} products edited SUCCESSFULLY",
                               'Success'))

            except ValueError:
                print(color("\nError !!!  Try Again", "Error"))                
            
            print('-'*50)
            input("\nPress Enter to choose again...")
            clearConsole()

        elif choice=='0':
            break
        
        else:
            clearConsole()


# ------
def search_records():

    header = ['Date', 'Time', 'Invoice ID', 'Name', 'Phone']

    def src_by_date(_date):
        cnd = f"date LIKE '%{_date}%'"
        dt = data(cnd)
        print()
        if len(dt)!=0:
            print(color(tabulize(header,dt), 'Text'))
            print()
        else:
            print(color("No Record Found", 'Warning'))

    def src_by_name(_name):
        cnd = f"costumer_name LIKE '%{_name}%'"
        dt = data(cnd)
        print()
        if len(dt)!=0:
            print(color(tabulize(header,dt), 'Text'))
            print()
        else:
            print(color("No Record Found", 'Warning'))

    def src_by_invoice(_invoice):
        cnd = f"bill_id = {_invoice}"
        dt = data(cnd)
        print()
        if len(dt)!=0:
            print(color(tabulize(header,dt), 'Text'))
            print()
        else:
           print(color("No Record Found", 'Warning'))

    def src_by_phone(_phone):
        cnd = f"phone = {_phone}"
        dt = data(cnd)
        print()
        if len(dt)!=0:
            print(color(tabulize(header,dt), 'Text'))
            print()
        else:
            print(color("No Record Found", 'Warning'))

    def get_invoice(_id):
        try:
            sql.execute(f"SELECT costumer_name, invoice FROM data WHERE bill_id = {_id};")
            data = sql.fetchall()

            name = data[0][0]
            binary = data[0][1]

            file = rf"saved_bills\({name})_Invoice_{_id}"
            with open(f"{file}.bin", 'wb') as f:
                f.write(binary)
            os.rename(f"{file}.bin", f"{file}.txt")


            if os.path.exists(f"{file}.pdf")==False:
                pdf(file)
                print(color('\nInvoice Saved SUCCESSFULLY', 'Success'))
            else:
                print(color("\nInvoice already present in the Folder", 'Warning'))
                os.remove(f"{file}.txt")
        
        except Exception as e:
            print(color("\nInvalid Invoice ID, try again :(", 'Error'))
        
    while True:
        print('='*50)
        print(' '*17, 'SEARCH RECORDS')
        print('='*50)
        print()
        print('1 -> Search by DATE')
        print('2 -> Search by NAME')
        print('3 -> Search by INVOICE')
        print('4 -> Search by PHONE')
        print('5 -> Get Invoice (ID Required)')
        print('0 -> Go Back')
        print()
        print("="*50)
        choice = input('\nEnter your choice: ')

        if choice=='1':
            print('-'*50)
            a = input(color('Enter Date in form - << 01-Jan-2001 >> : ', 'Input'))
            src_by_date(a)

            print('-'*50)
            input("\nPress Enter to choose again...")
            clearConsole()

        elif choice=='2':
            print('-'*50)
            a = input(color('Enter Name: ', 'Input'))
            src_by_name(a)

            print('-'*50)
            input("\nPress Enter to choose again...")
            clearConsole()

        elif choice=='3':
            print('-'*50)
            a = input(color('Enter Invoice ID: ', 'Input'))

            try:
                src_by_invoice(a)

            except Exception as e:
                print(color("\nInvalid ID... Try again :(", 'Error'))

            print('-'*50)

            input("\nPress Enter to choose again...")
            clearConsole()


        elif choice=='4':
            print('-'*50)
            a = input(color('Enter Contact Number: ', 'Input'))

            try:
                src_by_phone(a)

            except Exception as e:
                print(color("\nInvalid Number... Try again :(", 'Error'))

            print('-'*50)

            input("\nPress Enter to choose again...")
            clearConsole()

        elif choice=='5':
            print('-'*50)
            a = input(color('Enter Invoice ID: ', 'Input'))
            get_invoice(a)

            print('-'*50)
            input("\nPress Enter to choose again...")
            clearConsole()

        elif choice=='0':
            break
        
        else:
            clearConsole()

# ------
def change_password():
    i = getpass.getpass(prompt = color("Enter New password: ", 'Input'))
    c = getpass.getpass(prompt = color("Confirm password: ", 'Input'))
    
    if i==c:
        i = hashed(i)
        sql.execute("UPDATE credentials SET password=%s;", (i,))
        print(color('\nPassword changed SUCCESSFULLY', 'Success'))
        print('\n','\\'*50, sep='')
    else:
        print(color("\nPassword doesn't match, try again :(", 'Error'))
        print('\n','\\'*50, sep='')

# ----------------__main__----------------

clearConsole()
pd = getpass.getpass(prompt = color("Enter password: ", 'Input'))
pd = hashed(pd)

sql.execute("SELECT * FROM credentials;")
password = sql.fetchall()

if pd==password[0][0]:
    while True:
        home()
        choice = input('Enter your choice : ')

        
        if choice=='1':
            print('\n','/'*50,'\n', sep='')
            print(color("------ Enter 'n' when all Items are entered ------", 'Text'))
            print('-'*50)
            R = generate_bill()
    
            if len(R)>0:
                print('-'*50)
                print(color(f"\n{R} NOT FOUND", 'Warning'))
            
            print(color('\nInvoice generated SUCCESSFULLY\n', 'Success'))

            print('\\'*50)
            input('\nPress Enter to choose again...')

        elif choice=='2':
            print('\n','/'*50,'\n', sep='')
            view_products()
            print('\n','\\'*50, sep='')
            input('\nPress Enter to choose again...')
        
        elif choice=='3':
            print('\n','/'*50,'\n', sep='')
            stock_report()
            print('\n','\\'*50, sep='')
            input('\nPress Enter to choose again...')

        elif choice=='4':
            clearConsole()
            manage_products()
            
        elif choice=='5':
            clearConsole()
            search_records()

        elif choice=='6':
            print('\n','/'*50,'\n', sep='')
            change_password()
            input('\nPress Enter to choose again...')

        elif choice=='0':
            break
        
        else:
            clearConsole()

else:
    print('-'*50)
    print(color("Access Denied :(", "Error"))
    input("\nPress Enter to try again")
    print('-'*50)
    clearConsole()
    os.system('main.py')