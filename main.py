import member
import user
import practice
import random

userList = []
memberList = []
schedule = []
login = ""

def main():
    #print("Hello World")
    setup()
    login()

def setup():
    # Creates files if they don't already exist
    userfile = open("users.txt","a")
    calendarfile = open("calendar.txt","a")
    userfile.close()
    calendarfile.close()
    userfile = open("users.txt","r")
    for userA in userfile:
        sections = userA.split(' ')
        if sections[0] == "M":
            memberList.append(member.Member(sections[0],sections[1],' '.join(sections[2:4:]),sections[4],' '.join(sections[5::8]),sections[8].replace("\n",""),sections[9].replace("\n",""),sections[10].replace("\n","")))
        else:
            userList.append(user.User(sections[0],sections[1],' '.join(sections[2:4:]),sections[4],' '.join(sections[5::8]),sections[8].replace("\n","")))
    userfile.close()
    calendarfile = open("calendar.txt","r")
    for aPractice in calendarfile:
        sections = aPractice.split(' ')
        coach = ""
        members = []
        premembers = []
        if len(sections) > 3:
            premembers = sections[3::]
        for userA in userList:
            if userA.getUserID() == sections[2]:
                coach = userA
            if userA.getUserID() in premembers:
                members.append(userA)
        temp = practice.Practice(sections[0],sections[1],coach)
        for m in memberList:
            temp.addMember(m)
        schedule.append(temp)
    calendarfile.close()


def login():
    print("\nLogin Menu\n----------\n (1): Login\n (2): Create an account\n")
    answer = input("Enter option number: ")
    if answer == "1":
        userid = input("\nEnter your user ID: ")
        # if UserID exists, ask for password, etc.
        tempUser = False
        isMember = False
        for user in userList:
            if user.getUserID() == userid:
                tempUser = user
        if not tempUser:
            for member in memberList:
                if member.getMemberID() == userid:
                    tempUser = member
                    isMember = True
        # Sets current login to User if password correct
        if tempUser:
            login = ""
            password = input("Password: ")
            while(not login):
                if tempUser.getPassword() == password:
                    login = tempUser
                else:
                    password = input("Incorrect password, please re-enter: ")
            if isMember:
                print("Successfully logged in as member " + "#" + login.getMemberID() + "!")
                memberMenu(tempUser)
            else:
                print("Successfully logged in as " + login.getPosition() + "#" + login.getUserID() + "!")
                menu()
    elif answer == "2":
        addUser("M")
                    
def menu():
    # Here is where all menu options will be, such as:
    # Add new member, See Notifications, Class Schedule, Financials of the business (For Treasurer), etc.
    print("\nMenu\n----\n 1) Manage coach list \n 2) View members\n")
    checkInput = False
    answer = input("Enter option number: ")
    while (not checkInput):
        if answer == "1":
            checkInput = True
            manageCoachList()
        elif answer == "2":
            checkInput = True
            viewMembers()
        else:
            answer = input("Incorrect option number, please re-enter: ")


def memberMenu(member):
    #Menu options for members
    print("\nMember Menu\n-----------\n 1) Insert option here...\n 2) ...\n")
    if int(member.getFrequency()) > int(member.getPaid()):            #if the member has skipped payment once
        print("REMINDER: Due to a skipped payment, you are now subject to a penalty fee and possible exclusion from the group.")
    if int(member.getFrequency()) < int(member.getPaid()):
        print("Congratulations! You have not skipped any payments within the past 3 months and you have received a complimentary discount for 10% off one class.")
    checkInput = False
    answer = input("Enter option number: ")
    while (not checkInput):
        if answer == "1":
            checkInput = True
            #do something
        else:
            answer = input("Incorrect option number, please re-enter: ")


def viewSchedule(coach):
    for aPractice in schedule:
        if aPractice.coach == coach:
            print(aPractice)
    input("Press any key to return to menu: ")
    menu()
    return 1

def viewMembers():
    print("\nMember List\n------------")
    print("\nSort Options\n------------\n 1) Member ID (descending)\n 2) Member ID (descending)\n 3) Frequency (descending)\n 4) Frequency (ascending)\n 5) Payment (descending)\n 6) Payment (ascending)\n 7) Return to menu")
    checkInput = False
    while (not checkInput):
        answer = input("\nEnter option number: ")
        if answer == "1" or answer == "2" or answer == "3" or answer == "4" or answer == "5" or answer == "6":
            checkInput = True
            print("\nMember List\n-----------")
            sortPaid(answer)
            input("\nPress any key to return")
            viewMembers()
        elif answer == "7":
            menu()
        else:
            print("Incorrect option number\n")
        

def manageCoachList():
    index = 1
    coachList = []
    print("\nCoach List\n----------")
    for user in userList:
        if user.getPosition() == "C":
            coachList.append(user)
            print(" "+ str(index) + ") " + str(user))
            index += 1
    print(" " + str(index) + ") Add coach")
    print(" " + str(index+1) + ") Return to menu")
    answer = input("\nEnter coach or option number: ")
    if answer == str(index+1):
        menu()
    if(answer == str(index)):
        addUser("C")
        return
    selected = coachList[int(answer) - 1]
    print(" 1) View Schedule\n 2) Remove Coach\n 3) Return to menu")
    answer = input("\nEnter option number: ")
    if(answer == "1"):
        viewSchedule(selected)
    elif(answer == "2"):
        removeCoach(selected)
    else:
        manageCoachList()

def addUser(position):
    print("\nCreate Account\n--------------")
    name = input(" Enter name: ")
    num = input(" Enter contact number: ")
    address = input(" Enter address: ")
    password = input(" Enter password: ")
    if position == "M":
        memberid = random.randint(1000,9999)
        f = open("users.txt","a")
        f.write("\n" + position + " " + str(memberid) + " " + name + " " + num + " " + address + " " + password + " " + "0" + " " + "0")
        f.close()
        mmbr = member.Member(position,memberid,name,num,address,password,"0","0")
        memberList.append(mmbr)
        print("\nSuccessfully added member "+"#"+str(memberid)+" "+name+".")
        input("Press any key to redirect to the member menu.")
        memberMenu(mmbr)
    else:
        userid = len(userList)
        f = open("users.txt","a")
        f.write("\n" + position + " " + str(userid) + " " + name + " " + num + " " + address + " " + password)
        f.close()
        userList.append(user.User(position,userid,name,num,address,password))
        print("Successfully added "+position+"#"+str(userid)+" "+name+".")
        input("Press any key to redirect to the user menu.")
        menu()

def removeUser(user):
    # Also have to remove the user from any practices that they signed up for
    f = open("calendar.txt","r")
    lines = f.readlines()
    f.close()
    f = open("calendar.txt","w")
    for line in lines:
        line = line.replace(" "+user.getUserID(),"")
        f.write(line)
    f.close()
    for aPractice in schedule:
        aPractice.removeMember(user)
    # Removing user from users.txt
    index = 0
    found = False
    for i in range(0,len(userList)):
        if userList[i] == user:
            index = i
            found = True
    if found == True:
        userList.remove(user)
    else:
        for i in range (0, len(memberList)):
            if memberList[i] == user:
                index = i
                found = True
    f = open("users.txt","r")
    lines = f.readlines()
    f.close()
    f = open("users.txt","w")
    for i in range(0,len(lines)):
        if index != i:
            f.write(lines[i])
    f.close()
    print("User " + user.getName() + " Removed successfully.")
    input("Press any key to return to menu: ")
    menu()

def removeCoach(coach):
    practices = []
    for i in range(0,len(schedule)):
        if coach == schedule[i].coach:
            f = open("calendar.txt","r")
            lines = f.readlines()
            f.close()
            f = open("calendar.txt","w")
            index = 0
            for line in lines:
                if index != i:
                    f.write(line)
                index += 1
            f.close()
            practices.append(schedule[i])
    for aPractice in practices:
        for member in aPractice.getMemberList():
            member.messageReceive(aPractice.getDate()+" Practice at "+aPractice.getTime()+" with Coach: "+aPractice.getCoach().getName()+" has been cancelled.")
        schedule.remove(aPractice)
    removeUser(coach)

def sortPaid(sort_order):
    paidList = memberList
    if sort_order == "1":
        paidList.sort(key = lambda x: int(x.getMemberID()), reverse=True)
    elif sort_order == "2":
        paidList.sort(key = lambda x: int(x.getMemberID()))
    elif sort_order == "3":
        paidList.sort(key=lambda x: int(x.getFrequency()), reverse=True)
    elif sort_order == "4":
        paidList.sort(key=lambda x: int(x.getFrequency()))
    elif sort_order == "5":
        paidList.sort(key=lambda x: int(x.getPaid()), reverse=True)
    elif sort_order == "6":
        paidList.sort(key=lambda x: int(x.getPaid()))
    for i in memberList:
        print(i)


def manageMemberList():
    return 1

main()