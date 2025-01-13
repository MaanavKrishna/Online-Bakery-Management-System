import mysql.connector,tabulate

mydb = mysql.connector.connect(host="localhost", user="root", passwd="root")
mycursor = mydb.cursor()
mycursor.execute("USE OnlineBakery")

def checktableexists(tablename):
    mycursor.execute("SHOW TABLES LIKE %s", (tablename,))
    rec1 = mycursor.fetchone()
    return rec1

def inventory():
    if checktableexists("inventory"):
        pass
    else:
        mycursor.execute("CREATE TABLE inventory(Item_Number INT PRIMARY KEY, Item_Name VARCHAR(20), Item_Type VARCHAR(20), Price INT, Quantity INT, Mfg DATE, Exp DATE);")

def sales():
    if checktableexists("sales"):
        pass
    else:
        mycursor.execute("CREATE TABLE sales(Date DATE, Item_Number INT, Item_Name VARCHAR(20), Quantity INT, Price INT, Total_Cost INT);")

def addinventory():
    n = int(input("No. Records to be Added:"))
    for i in range(n):
        print("\nRecord:" + str(i + 1))
        itno = int(input("Enter Item Number:"))
        itna = input("Enter Item Name:")
        while True:
            itty = input("Enter Item Type(Snacks/Pastry/Chocolates & Dessert/Cheese & Dairy):")
            if itty in ["Snacks", "Pastry", "Chocolates & Dessert", "Cheese & Dairy"]:
                break
            else:
                print("Not a valid Option:")
        price = int(input("Enter Price:"))
        qty = int(input("Enter Quantity:"))
        mfg = input("Enter Manufacturing Date(YY/MM/DD):")
        exp = input("Enter Expiry Date(YY/MM/DD):")
        mycursor.execute("INSERT INTO inventory VALUES(%s, %s, %s, %s, %s, %s, %s)", (itno, itna, itty, price, qty,mfg,exp))
        mydb.commit()

def addsales():
    n = int(input("No. Records to be Added:"))
    for i in range(n):
        print("\nRecord:" + str(i + 1))
        date = input("Enter Date(YY/MM/DD):")
        itno = int(input("Enter Item Number:"))
        itna = input("Enter Item Name:")
        qty = int(input("Enter Quantity:"))
        price = int(input("Enter Price:"))
        totcos = qty * price
        mycursor.execute("INSERT INTO sales VALUES(%s, %s, %s, %s, %s, %s)", (date, itno, itna, qty, price, totcos))
        mycursor.execute("UPDATE inventory SET Quantity=Quantity-%s WHERE Item_Number=%s", (qty, itno))
        mydb.commit()

def modify(tablename):
    tarfie = input("Enter Field to be modified:")
    if tablename == "inventory":
        if tarfie in ["Item_Number", "Item_Name", "Item_Type", "Price", "Quantity"]:
            tarval = eval(input("Enter Item_Number:"))
            chanval = eval(input("Enter New value:"))
            mycursor.execute("UPDATE %s SET %s=%s WHERE %s=%s" % (tablename, tarfie, chanval, "Item_Number", tarval))
            mydb.commit()
        else:
            print("Field Does not Exist")
    else:
        if tarfie in ["Date","Item_Number", "Item_Name", "Quantity", "Price", "Total Cost"]:
            tarval = eval(input("Enter Item_Number:"))
            chanval = eval(input("Enter New value:"))
            mycursor.execute("UPDATE %s SET %s=%s WHERE %s=%s" % (tablename, tarfie, chanval, "Item_Number", tarval))
            mydb.commit()
        else:
            print("Field Does not Exist")

def search():
    ch = int(input("Search Using\n1.Item Number\n2.Item Name\nOption:"))
    if ch == 1:
        itno = int(input("Enter Item Number:"))
        mycursor.execute("SELECT * FROM Inventory WHERE Item_Number=%s", (itno,))
    elif ch == 2:
        itna = input("Enter Food Name:")
        mycursor.execute("SELECT * FROM Inventory WHERE Food_Name=%s", (itna,))
    rec = mycursor.fetchall()
    header = ["Item Number", "Item Name", "Item Type", "Price", "Quantity"]
    print(tabulate.tabulate(rec, header, tablefmt="grid"))

def delete(tablename):
    itno = int(input("Enter Item Number:"))
    mycursor.execute("DELETE FROM %s WHERE Food_Number=%s" % (tablename, itno))
    mydb.commit()
    print("Record has successfully been deleted")

def admin():
    while True:
        ch = int(input("\nAdmin Menu\n\t1.Inventory\n\t2.Sales\n\t3.Exit\nOption:"))
        if ch == 1:
            inventory()
            opt = int(input("\nInventory Menu\n\t1.Add\n\t2.Modify\n\t3.Delete\n\t4.Search\nOption:"))
            if opt == 1:
                addinventory()
            elif opt == 2:
                modify("inventory")
            elif opt == 3:
                delete("inventory")
            elif opt == 4:
                search()
            else:
                print("Option does not exist")
        elif ch == 2:
            sales()
            opt = int(input("\nSales Menu\n\t1.Add\n\t2.Modify\n\t3.Delete\nOption:"))
            if opt == 1:
                addsales()
            elif opt == 2:
                modify("sales")
            elif opt == 3:
                delete("sales")
            else:
                print("Option does not exist")
        elif ch == 3:
            break
        else:
            print("Option does not exist")

def user():
    while True:
        ch = int(input("\nUser Menu\n\t1.Inventory\n\t2.Sales\n\t3.Exit\nOption:"))
        if ch == 1:
            inventory()
            opt = int(input("\nInventory Menu\n\t1.Add\n\t2.Modify\n\t3.Search\nOption:"))
            if opt == 1:
                addinventory()
            elif opt == 2:
                modify("inventory")
            elif opt == 3:
                search()
            else:
                print("Option does not exist")
        elif ch == 2:
            sales()
            opt = int(input("\nSales Menu\n\t1.Add\n\t2.Modify\nOption:"))
            if opt == 1:
                addsales()
            elif opt == 2:
                modify("sales")
            else:
                print("Option does not exist")
        elif ch == 3:
            break
        else:
            print("Option does not exist")

def ger():
    while True:
        ch = int(input("\nReport Menu\n\t1.Current Stock\n\t2.Net Profit\n\t3.Exit\nOption:"))
        if ch == 1:
            print("\nCurrent Stock")
            mycursor.execute("SELECT * FROM Inventory")
            rec = mycursor.fetchall()
            headers = ["Item Number", "Item Name", "Item Type", "Price", "Quantity"]
            print(tabulate.tabulate(rec, headers, tablefmt="grid"))
        elif ch == 2:
            op = int(input("\nSales Report\n1.Net Profit For the Day\n2.Net Profit For the month\nOption:"))
            if op == 1:
                mycursor.execute("SELECT SUM(Total_Cost) FROM sales WHERE Date = CURDATE()")
                totprof = mycursor.fetchone()[0]
                print("Net Profit for the Day:", totprof)
            elif op == 2:
                mycursor.execute("SELECT SUM(Total_Cost) FROM sales WHERE MONTH(Date) = MONTH(CURDATE()) AND YEAR(Date) = YEAR(CURDATE())")
                totprof_month = mycursor.fetchone()[0]
                print("Net Profit for the Month:", totprof_month)
            else:
                print("Option does not exist")
        elif ch == 3:
            break
        else:
            print("Option does not exist")

while True:
    op = int(input("--------" * 7 + "Online Bakery Management System" + "--------" * 7 + "\n\nWelcome To FoodBox\n\nMain Menu\n\t1.Admin\n\t2.User\n\t3.Generate Report\n\t4.Exit\nOption:"))
    if op == 1:
        admin()
    elif op == 2:
        user()
    elif op == 3:
        ger()
    elif op == 4:
        break
    else:
        print("Option does not exist")

