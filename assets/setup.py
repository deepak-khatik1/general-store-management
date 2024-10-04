import os

content = '''------------------------------------------------------
                    General Store   
------------------------------------------------------
              Contact No. - 8989898989

                       INVOICE

Date : <<DATE>>                     Time : <<TIME>>

Invoice ID : <<INVOICE>>
Costumer Name : <<NAME>>

<<TABLE>>

Total Amount : Rs.<<AMOUNT>>

------------------------------------------------------'''

with open('..\\draft.txt', 'w') as f:
    f.write(content)

if not(os.path.isdir("..\\auto_bills\\")):
    os.mkdir("..\\auto_bills\\")

if not(os.path.isdir("..\\saved_bills\\")):
    os.mkdir("..\\saved_bills\\")

print("\n--REQURIRED FILES AND FOLDERS CREATED")

input("\nCreating database... please enter after marking sure XAMPP is running")
os.system(r"mysql -u root < database.sql")

print("\n--DATABASE CREATED")

input("\nPlease enter if you want to install required packages")
packages = ["mysql.connector", "tabulate", "fpdf", "termcolor"]
for package in packages:
    os.system(rf"pip install {package}")

print("\n--PROGRAM IS READY TO EXECUTE")