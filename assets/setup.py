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
    
os.system(r"mysql -u root < database.sql")

input("Program is ready to Execute")