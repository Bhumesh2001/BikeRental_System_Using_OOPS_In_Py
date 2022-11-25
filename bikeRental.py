import mysql.connector as mysql
import time,json
import datetime

con = mysql.connect(
    host='localhost',
    user='root',
    password='1',
    database='bikeShop'
)
mycursor = con.cursor()

q = 'SELECT * FROM bikeStock'
mycursor.execute(q)
bikeStockInfo = mycursor.fetchall()

Cqery = 'SELECT * FROM CustomerData'
mycursor.execute(Cqery)
Customer_data = mycursor.fetchall()

# ---------------classes--------------#

class Admin_Accounts:

    def intro(self):
        try:
            opt = int(input('Welcome to Accounts::\n\n1.Sign up\n2.Log in\n3.Exit\n'))
            if opt == 1:
                return 1
            elif opt == 2:
                return 2
            elif opt == 3:
                Start()
            else:
                print('------ Invalid request\n')
                return admin_accounts.intro()
        except:
            print('------ Invalid request\n')
            return admin_accounts.intro()

    def SignUp(self,admin_name,admin_pass,admin_email):
        query2 = f"SELECT * FROM AdminData where Email='{admin_email}'"
        mycursor.execute(query2)
        adminData = mycursor.fetchall()
        for info in adminData:
            if admin_email in info:
                print('------You have already an account with this Email\n')
                return False
                break
        else:
            query = 'INSERT INTO AdminData(Name,Password,Email) VALUES(%s,%s,%s)'
            val = (admin_name,admin_pass,admin_email)
            mycursor.execute(query,val)
            con.commit()
            return True

    def Login(self,admin_email,admin_pass):
        query3 = "SELECT * FROM AdminData"
        mycursor.execute(query3)
        udata = [];
        Admin_Data = mycursor.fetchall()
        for userData in Admin_Data:
            udata.append(userData[1])
            udata.append(userData[2])
        if admin_email in udata:
            if admin_pass in udata:
                return True
            else:
                print('------ Wrong password\n')
                return False
        else:
            print('------ There is no account with this Email\n')
            return False

class Admin_Bike_Store:

    def __init__(self,bikeData):
        self.BikeInfo= bikeData

    def Show_bike(self):
        q1 = 'SELECT * FROM bikeStock'
        mycursor.execute(q1)
        bikeStock_data = mycursor.fetchall()
        count = 0
        print('------ Bikes in Our Store:------\n')
        for bike in bikeStock_data :
            count += 1
            print(f'-----{count}. {bike[0]}-----{bike[1]} per Hour----LEFT IN STOCK_({bike[2]})-----')
        print()
        return count
    
    def Add_Stock(self,bikeInfoList):
        allbikeName = {};
        for bike_Name in bikeStockInfo:
            allbikeName.update({bike_Name[0]:bike_Name[2]})
        for Namebike in bikeInfoList:
            if Namebike[0] in allbikeName:
                query5 = f"UPDATE bikeStock SET Quantity='{Namebike[2]+allbikeName[Namebike[0]]}' WHERE bikeName='{Namebike[0]}'"
                mycursor.execute(query5)
                con.commit()
            else:
                selectQuery = 'SELECT * FROM LoginUser'
                mycursor.execute(selectQuery)
                loginEamil = mycursor.fetchall()

                SelQuery = f'SELECT Name FROM AdminData WHERE Email="{loginEamil[0][0]}"'
                mycursor.execute(SelQuery)
                name = mycursor.fetchall()

                query5 = f"INSERT INTO bikeStock(bikeName,Price,Quantity,Admin) VALUES('{Namebike[0]}','{Namebike[1]}','{Namebike[2]}','{name[0][0]}')"
                mycursor.execute(query5)
                con.commit()

        print('Added successfully...\n')
    def Delete_Stock(self,serNolist):
        serNo = 0;
        for bikeN in bikeStockInfo:
            serNo += 1
            if serNo in serNolist:
                Query8 = f'DELETE FROM bikeStock WHERE bikeName="{bikeN[0]}"'
                mycursor.execute(Query8)
                con.commit()
        print('deleted successfully....\n')

class Customer_Accounts:
    
    def Intro(self):
        try:
            opt2 = int(input('Welcome to Accounts::\n\n1.Sign up\n2.Log in\n3.Exit\n'))
            if opt2 == 1:
                return 1
            elif opt2 == 2:
                return 2
            elif opt2 == 3:
                Start()
            else:
                print('------ Invalid request\n')
                return customer_accounts.Intro()
        except:
            print('------ Invalid request\n')
            return customer_accounts.Intro()
    
    def Sign_Up(self,customer_name,customer_contact_no,customer_pass,customer_age):
        Clist = [];
        for Cdata in Customer_data:
            Clist.append(Cdata[1])
        if Customer_data == [] or Customer_data != []:
            if customer_contact_no not in Clist:
                sqlQry = f'INSERT INTO CustomerData(Name,ContactNo,Password,Age) VALUES("{customer_name}","{customer_contact_no}","{customer_pass}","{customer_age}")'
                mycursor.execute(sqlQry)
                con.commit()
                return True
            else:
                print('------You have already an account with this Mobaile No.:\n')
                return False

    def Login(self,customer_contact_No,customer_Pass):
        CustomerMo = [];
        for mobile in Customer_data:
            CustomerMo.append(mobile[1])
            CustomerMo.append(mobile[2])
        if Customer_data == [] or Customer_data != []:
            if customer_contact_No in CustomerMo:
                if customer_Pass in CustomerMo:
                    return True
                else:
                    print('\n------ Wrong password\n')
                    return False
            else:
                print('------ There is no account with this Mobile No.:\n')
                return False

class Customer_Bike_Store:

    def Rent(self,userBike,Rented_time,Rented_date,BikeCost,CusName,customer_contact_no):
        q = 'SELECT * FROM bikeStock'
        mycursor.execute(q)
        bikeStock2 = mycursor.fetchall()
        for bike5 in bikeStock2: 
            if bike5[0] in userBike:
                Count_bike = userBike.count(bike5[0])
                updateQuery = f'UPDATE bikeStock SET Quantity={bike5[2]-Count_bike} WHERE bikeName="{bike5[0]}"'
                mycursor.execute(updateQuery)
                con.commit()

        RentQuery = f'INSERT INTO RentedBikeData (RentedBikes,RentedTime,RentedDate,TotalRent,CustomerName,CustomerMo) VALUES("{userBike}","{Rented_time}","{Rented_date}",{BikeCost},"{CusName}",{customer_contact_no})'
        mycursor.execute(RentQuery)
        con.commit()
        print('bikes rented successfully....')  

    
    def Return(self,Customer_contact_no,Customer_pass):
        ReturnQuery = 'SELECT * FROM RentedBikeData'
        mycursor.execute(ReturnQuery)
        RetedData = mycursor.fetchall()
        allNumber = [];
        for Number in RetedData:
            allNumber.append(Number[5])
        for passw in Customer_data:
            allNumber.append(passw[2])

        if Customer_contact_no in allNumber:
            if Customer_pass in allNumber:
                Time = time.localtime()
                endTime = time.strftime("%H:%M:%S", Time)
                timeLi = endTime.split(':')

                timeQuery = f'SELECT RentedTime,TotalRent,RentedBikes FROM RentedBikeData WHERE CustomerMo={Customer_contact_no}'
                mycursor.execute(timeQuery)
                rentedTime = mycursor.fetchall()
                allNamebike = []
                for Data in rentedTime:

                    l = Data[2][1:-1].replace(","," ").split("'")
                    for n in l:
                        if len(n) < 1 or "  " in n:
                            l.remove(n)
                    for n in l:
                        allNamebike.append(n)

                    RentedTime = Data[0]
                    Rtime = Data[0].split(':')

                    minute1 = (int(timeLi[1]) - int(Rtime[1]))
                    hour1 = (int(timeLi[0]) - int(Rtime[0]))

                    totalPricebyHour = (int(timeLi[0]) - int(Rtime[0])) * Data[1]
                    totalPricebyMinute = (int(timeLi[1]) - int(Rtime[1])) * Data[1]
                    
                QueryName = f'SELECT RentedBikes FROM RentedBikeData WHERE CustomerMo={Customer_contact_no}'
                mycursor.execute(QueryName)
                AllRentedBikes = mycursor.fetchall()
                name_bike = []
                for info in AllRentedBikes:
                    name_bike.append(info[0])

                if minute1 > 30 or minute1 < 60:
                    print(f'\n-------Your have taken these bikes {name_bike} at this time {RentedTime}')
                    print(f'-------Your total cost of rent is {totalPricebyMinute} for all bikes\n------ Do you want to return bikes:\n------ 1.Yes\n------ 2.No\n')
                    def askAgain():
                        choice = int(input('\n-------Enter your option :- '))
                        if choice == 1:
                            q9 = 'SELECT * FROM bikeStock'
                            mycursor.execute(q9)
                            bikeStockdata = mycursor.fetchall()
                            for BIKe in bikeStockdata:  
                                if BIKe[0] in l:
                                    countb = allNamebike.count(BIKe[0])
                                    updateQuery55 = f'UPDATE bikeStock SET Quantity={BIKe[2]+countb} WHERE bikeName="{BIKe[0]}"'
                                    mycursor.execute(updateQuery55)
                                    con.commit()
                            bikeDelete = f'DELETE FROM RentedBikeData WHERE CustomerMo={Customer_contact_no}'
                            mycursor.execute(bikeDelete)
                            con.commit()
                        else:
                            return False
                    askAgain()
                else:
                    if minute1 < 30:
                        print(f'\n-------Your have taken these bikes {name_bike} at this time {RentedTime}')
                        print(f'-------Your total cost of rent is for all bikes\n------ Do you want to return bikes:\n------ 1.Yes\n------ 2.No\n')
                        askAgain()
                    else:
                        print(f'\n-------Your have taken these bikes {name_bike} at this time {RentedTime}')
                        print(f'-------Your total cost of rent is {totalPricebyHour} for all bikes\n------ Do you want to return bikes:\n------ 1.Yes\n------ 2.No\n')
                        askAgain()
            else:
                print('-------Wrong Password\n')    
                return False
        else:
            print('------ You have not taken any bikes on rent: Bye:\n')
            return False

    def ChooseBike(self):
        cost = 0;   
        totalBikes = 0;
        bikeArr = [];
        while True:
            opt3 = int(input("------ Want to Rent or No\n\n    1.Rent\n    2.Enough\n    3.Don't wanna rent\n"))
            if opt3 == 1:
                bikeQty = admin_bike_store.Show_bike()
                userChoice = int(input('------ Enter the seriel number of that bike you want:------\n'))
                if userChoice > bikeQty or userChoice < 1:
                    print('------ sorry, your request is Invalid:------')
                    return 0
                else:
                    counting = 0;
                    q2 = 'SELECT * FROM bikeStock'
                    mycursor.execute(q2)
                    bikeStockInfo2 = mycursor.fetchall()
                    for cbike in bikeStockInfo2:
                        counting += 1
                        if counting == userChoice:
                            print(f'------ You will be charged {cbike[1]} per Hour for this Bike:')
                            bike_count = int(input(f"------ How many {cbike[0]} you want to Rent:------\n"))
                            if cbike[2] == 0:
                                print(f'------Sorry {cbike[0]} Stock is Empty\n')
                            elif bike_count > cbike[2]:
                                print(f'------ Sorry, {cbike[0]} are only {cbike[2]} left in our stock\n')
                                return 0
                            elif bike_count <= 0:
                                print('------ Invalid request: \n')
                                return 0
                            for bCount in range(bike_count):
                                bikeArr.append(cbike[0])
                                cost += cbike[1]
                            
                            totalBikes += bike_count

            elif opt3 == 2:
                if bikeArr != []:
                    print('------ Thank you, Have a nice Day:')
                    print(f'------ Totally you will be charged {cost} per Hour for all bikes:\n')
                    bikeInfo = [bikeArr,totalBikes,cost]
                    return bikeInfo
                else:
                    print('--------Your Are Not Selected Any Bike:\n')
            elif opt3 == 3:
                print('------ No problem: thank you for visiting:\n')
                return 0
            else:
                print('------ Invalid request:\n')


class StoreInherit(Admin_Bike_Store):

    def __init__(self,bikeData1):
        self.bikeD = bikeData1

    def Show(self):
        super().Show_bike()

    def Add(self,bikeInfoList):
        super().Add_Stock(bikeInfoList)
    
    def delete(self,serList):
        super().Delete_Stock(serList)

# ---------------objects-------------- #

admin_accounts = Admin_Accounts()
admin_bike_store = Admin_Bike_Store(bikeStockInfo)

customer_accounts = Customer_Accounts()
customer_bike_Store = Customer_Bike_Store()

StoreData = StoreInherit(Admin_Bike_Store) 

# -----------------BODY----------------#

def Start():
    try:
        Person = int(input('------ Who are you?\n\n------1.Admin\n------2.Customer\n'))
        if Person == 1:
            def AdminAccounts():
                ask = admin_accounts.intro()
                if ask == 1:
                    [admin_name,admin_pass,admin_email] = Admin_signinData()
                    bool1 = admin_accounts.SignUp(admin_name,admin_pass,admin_email)
                    if bool1:
                        print('------ Account Created Successfully: now you are a admin:\n')
                        Admin_Fun()
                    else:
                        AdminAccounts()
                elif ask == 2:
                    admin_email = input('------ Enter your Email: ')
                    admin_pass = input('------ Enter your password: ')
                    logQuery = 'SELECT * FROM LoginUser'
                    mycursor.execute(logQuery)
                    loginUser1 = mycursor.fetchall()
                    gmailArr = []
                    for gmail in loginUser1:
                        gmailArr.append(gmail[0])
                    if admin_email in gmailArr:
                        updQuery = f'UPDATE LoginUser SET UserEmail="{admin_email}" WHERE UserEmail="{admin_email}"'
                        mycursor.execute(updQuery)
                        con.commit()
                    else:
                        loginQuery = f"INSERT INTO LoginUser(UserEmail) VALUES('{admin_email}')"
                        mycursor.execute(loginQuery)
                        con.commit()
                    print()
                    val = admin_accounts.Login(admin_email,admin_pass)
                    if val:
                        Admin_Fun()
                    else:
                        AdminAccounts()
            AdminAccounts()
        elif Person == 2:
            def CustomerAccounts():
                ask2 = customer_accounts.Intro()
                if ask2 == 1:
                    [customer_name,customer_contact_no,customer_pass,customer_age] = Customer_signinData()
                    bool2 = customer_accounts.Sign_Up(customer_name,customer_contact_no,customer_pass,customer_age)
                    if bool2:
                        print('------ Account Created Successfully: now you are a Customer:\n')
                        Customer_func(customer_contact_no,customer_pass)
                    else:
                       CustomerAccounts()
                elif ask2 == 2:
                    try:
                        customer_contact_No = int(input("------ Enter your contact no: "))
                        customer_Pass = input("------ Enter your password: ")
                        Val = customer_accounts.Login(customer_contact_No,customer_Pass)
                        if Val:
                            Customer_func(customer_contact_No,customer_Pass)
                        else:
                            CustomerAccounts()
                    except:
                        print('--------Invalid Request\n')
                        CustomerAccounts()
            CustomerAccounts()
        else:
            print('--------Invalid Request\n')
            Start()
    except:
        print('--------Invalid Request\n')
        Start()

def Admin_signinData():
    admin_name = input('------ Enter your name: ')
    admin_email = input('------ Enter your Email: ')
    admin_pass = input('------ Enter your password: ')
    return [admin_name,admin_pass,admin_email]


def Customer_signinData():
    customer_name = input("------ Enter your name: ")
    customer_contact_no = int(input("------ Enter your contact no: "))
    customer_pass = input("------ Enter your password: ")
    customer_age = int(input("------ Enter your age: "))
    return [customer_name,customer_contact_no,customer_pass,customer_age] 


def Admin_Fun():
    Bike_Stock_arr = [{'Royal Enfield Classic 350':[500,5],'Yamaha R15S':[400,5],'TVS Apache RTR 160':[300,5],'TVS Raider':[200,5],'KTM 390 Duke':[100,5]}]
    if bikeStockInfo == []:
        for Bike in Bike_Stock_arr:
            for bikeName in Bike:
                query4 = f"INSERT INTO bikeStock(bikeName,Price,Quantity,Admin) VALUES('{bikeName}','{Bike[bikeName][0]}','{Bike[bikeName][1]}','ByDefault')"
                mycursor.execute(query4)
                con.commit()
    
    print('WELCOME TO YOUR BIKE RENTAL STORE: \n')
    while True:
        try:
            admin_choice = int(input('------ What you want to do?\n\n------1.See Stock\n------2.Add Stock\n------3.Delete Stock\n------4.Exit\n'))
            if admin_choice == 1:
                admin_bike_store.Show_bike()
            elif admin_choice == 2:
                addData()
            elif admin_choice == 3:
                delete_Data()
            elif admin_choice == 4:
                print('--------BY-------\n')
                break
            else:
                print('------ Invalid request:\n')
        except:
            print('------ Invalid request:\n')

def Customer_func(customer_contact_no,customer_pass):
    Bike_Stock_arr1 = [{'Royal Enfield Classic 350':[500,5],'Yamaha R15S':[400,5],'TVS Apache RTR 160':[300,5],'TVS Raider':[200,5],'KTM 390 Duke':[100,5]}]
    if bikeStockInfo == []:
        for Bike12 in Bike_Stock_arr1:
            for bikeName in Bike12:
                query6 = f"INSERT INTO bikeStock(bikeName,Price,Quantity,Admin) VALUES('{bikeName}','{Bike12[bikeName][0]}','{Bike12[bikeName][1]}','ByDefault')"
                mycursor.execute(query6)
                con.commit()
    print('\nWELCOME TO YOUR BIKE RENTAL STORE: \n')
    while True:
        try:
            User_Action = int(input("------ WHAT YOU WANT TO DO ------\n\n------ 1. RENT FROM US: \n------ 2. RETURN TO US: \n------ 3. EXIT: \n\n"))
            if User_Action == 1:
                userBike = customer_bike_Store.ChooseBike()
                if userBike != 0:
                    BikeCost = userBike[2]
                    confirm = int(input(f"------ Do you want to Rent these bikes {userBike[0]}.\n------1.Yes\n------2.No\n"))
                    if confirm == 1:
                        cName = [];
                        for Mobile in Customer_data:
                            if customer_contact_no == Mobile[1]:
                                cName.append(Mobile[0])
                        CusName = cName[0]
                        t = time.localtime()
                        Rented_time = time.strftime("%H:%M:%S", t)

                        current_time = datetime.datetime.now()
                        day,month,year =  current_time.day,current_time.month,current_time.year
                        Rented_date = f'{day}:{month}:{year}'
                        customer_bike_Store.Rent(userBike[0],Rented_time,Rented_date,BikeCost,CusName,customer_contact_no)

                    elif confirm == 2:
                        print('------ Thank you. No problem. Come again\n')
                    else:
                        print('------ Invalid request:\n')

            elif User_Action == 2:
                Customer_contact_no = int(input("------ Enter your contact Number: "))
                Customer_pass = input("------ Enter your password: ")
                response =  customer_bike_Store.Return(Customer_contact_no,Customer_pass)
                if response:
                    print('\n------ Thanks for Visiting:\n')
                else:
                    print('\n------ Thank you for Returning. Come again: And Have a Nice day:\n')

            elif User_Action == 3:
                print('------ THANK YOU FOR VISITING OUR STORE. \n------ HAVE A NICE DAY -----\n')
                break
            else:
                print('-------Invalid Requets------\n')
        except:
            print('-------Invalid Requets------\n')

def addData():
    bikeInfoList = []
    count1 = 0;
    while True:
        try:
            if count1 < 1:
                opt1 = int(input("------ 1.Add\n------ 2.Don't Add\n"))
                if opt1 == 1:
                    def EnterBike():
                        bike_name = input('------ Enter Bike name:\n')
                        bike_prize = int(input(f'------ Enter Bike rent for {bike_name} you want to charge per hour:\n'))
                        bike_qty = int(input(f'------ Enter quantity of {bike_name} you want to Add:\n'))
                        infoBike = tuple((bike_name,bike_prize,bike_qty))
                        bikeInfoList.append(infoBike)
                    EnterBike()
                    count1 +=1
                elif opt1 == 2:
                    print('------ Ok no data added to stock:\n')
                    break
                else:
                    print('------ Invalid request:\n')
            else:
                opt2 = int(input("------ 1.Add\n------ 2.Enough\n------ 3.Don't Add\n"))
                if opt2 == 1:
                    EnterBike()
                    count1 +=1
                elif opt2 == 2:
                    StoreData.Add(bikeInfoList)
                    break
                elif opt2 == 3:
                    print('------ Ok no data added to stock:\n')
                    break
                else:
                    print('-------Invalid Requests\n')
        except:
            print('-------Invalid Requests\n')

def delete_Data():
    serList = [];
    count2 = 0;
    while True:
        try:
            if count2 < 1:
                opt4 = int(input("------ 1.Delete\n------ 2.Don't Delete\n"))
                if opt4 == 1:
                    def showData():
                        StoreData.Show()
                        bikeCount = int(len(bikeStockInfo))
                        bike_index = int(input("------ Enter seriel number of that bike which you want to remove from stock:\n"))
                        if bike_index <= bikeCount:
                            serList.append(bike_index)
                        else:
                            print('You Entered wrong ser No.\n Please Enter Correct Ser No.\n')
                            showData()
                    showData()
                    count2 += 1
                elif opt4 == 2:
                    print('------ Ok no data deleted from stock:\n')
                    break
                else:
                    print('------ Invalid request:\n')
            else:
                opt5 = int(input("------ 1.Delete\n------ 2.Enough\n------ 3.Don't Delete\n"))
                if opt5 == 1:
                    showData()
                    count2 += 1
                elif opt5 == 2:
                    StoreData.delete(serList)
                    break
                elif opt5 == 3:
                    print('------ Ok no data deleted from stock:\n')
                    break
                else:
                    print('------ Invalid request:\n')
        except:
            print('------ Invalid request:\n')
Start()