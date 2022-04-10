import user

userList = []
login = ""

def main():
    #print("Hello World")
    setup()
    login()
    menu()

def setup():
    # Creates files if they don't already exist
    userfile = open("users.txt","a")
    calendarfile = open("calendar.txt","a")
    userfile.close()
    calendarfile.close()
    userfile = open("users.txt","r")
    for aUser in userfile:
        sections = aUser.split(' ')
        userList.append(user.User(sections[0],sections[1],' '.join(sections[2:4:]),sections[4],' '.join(sections[5::8]),sections[8].replace("\n","")))
    print(userList[0].getPassword())
    userfile.close()

def login():
    print("(1): Login\n(2): Create New Account")
    answer = input("Enter Option Number: ")
    if answer == "1":
        userid = input("Enter UserID: ")
        # if UserID exists, ask for password, etc.
        tempUser = False
        for user in userList:
            if user.getUserID() == userid:
                tempUser = user
        # Sets current login to User if password correct
        if tempUser:
            login = ""
            while(not login):
                password = input("Password: ")
                if tempUser.getPassword() == password:
                    login = tempUser   

            print("Successfully Logged in as " + login.getPosition() + "#" + login.getUserID() + "!")
        
def menu():
    # Here is where all menu options will be, such as:
    # Add new member, See Notifications, Class Schedule, Financials of the business (For Treasurer), etc.

main()