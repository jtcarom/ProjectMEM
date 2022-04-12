import member
import user
import practice
import random

userList = []
memberList = []
schedule = []
login = ""
treasurerIndex = 0

def main():
    #print("Hello World")
    setup()
    login()

def setup():
    # Creates files if they don't already exist
    userfile = open("users.txt","a")
    userfile.close()
    calendarfile = open("calendar.txt","a")
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
    print("\nLogin Menu\n----------\n (1): Login\n (2): Create an account\n (3): Exit System\n")
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
                menu(tempUser)
    elif answer == "2":
        addUser("M")
    elif answer == "3":
        exit()
    else:
        print("Sorry, please enter in 1, 2 or 3.")
                    
def menu(user):
    # Here is where all menu options will be, such as:
    # Add new member, See Notifications, Class Schedule, Financials of the business (For Treasurer), etc.
    print("\nMenu\n----\n 1) Manage coach list \n 2) View members\n 3) Manage Coach Schedule\n 4) Logout")
    checkInput = False
    answer = input("Enter option number: ")
    while (not checkInput):
        if answer == "1":
            checkInput = True
            manageCoachList()
        elif answer == "2":
            checkInput = True
            viewMembers()
        elif answer == "3":
            checkInput = True
            manageSchedule(user)
        elif answer == "4":
            checkInput = True
            login()
        else:
            answer = input("Incorrect option number, please re-enter: ")


def memberMenu(member):
    #Menu options for members
    print("\nMember Menu\n-----------\n 1) Insert option here...\n 2) Pay Outstanding Payment\n3) Join a Practice\n4) View My Schedule\n")
    if int(member.getFrequency()) > int(member.getPaid()):            #if the member has skipped payment once
        print("REMINDER: Due to a skipped payment, you are now subject to a penalty fee and possible exclusion from the group.")
    if int(member.getFrequency()) < int(member.getPaid()):
        print("Congratulations! You have not skipped any payments within the past 3 months and you have received a complimentary discount for 10%% off one class.")
    checkInput = False
    answer = input("Enter option number: ")
    while (not checkInput):
        if answer == "1":
            checkInput = True
        elif answer == "2":
            if int(member.getFrequency()) > int(member.getPaid()):
                payPractice(member)
                amount = 10.0
                fee = 5.0
                userList[treasurerIndex].messageReceive("M#"+member.getMemberID()+" has paid an outstanding payment of"+str(amount+fee)+".")
                input("Enter any key to return to menu: ")
                memberMenu(member)
            else:
                print("You have no outstanding payments to make.")
        elif answer == "3":
            joinPractice(member)
        elif answer == "4":
            viewMemberSchedule(member)
        else:
            answer = input("Incorrect option number, please re-enter: ")

def viewMemberSchedule(member):
    print("Your Practices:\n")
    for aPractice in schedule:
        if member in aPractice.getMemberList():
            print(aPractice)
    input("Press any key to return to menu")
    memberMenu(member)

def viewSchedule(coach):
    for aPractice in schedule:
        if aPractice.getCoach() == coach:
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
        userid = random.randint(1000,9999)
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
        if user.getPosition != "M":
            line = line.replace(" "+user.getUserID(),"")
        else:
            line = line.replace(" "+user.getMemberID(),"")
        f.write(line)
    f.close()
    for aPractice in schedule:
        aPractice.removeMember(user)
    # Removing user from users.txt
    f = open("users.txt","r")
    lines = f.readlines()
    f.close()
    f = open("users.txt","w")
    for line in lines:
        sections = line.split(' ')
        if user.getPosition() == "M":
            if user.getMemberID() != sections[1]:
                f.write(line)
        else:
            if user.getUserID() != sections[1]:
                f.write(line)
    f.close()
    print("User " + user.getName() + " Removed successfully.")
    input("Press any key to return to menu: ")
    menu()

def removeCoach(coach):
    practices = []
    for i in range(0,len(schedule)):
        if coach == schedule[i].coach:
            removePractice(i)
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

def removePractice(index):
    f = open("calendar.txt","r")
    lines = f.readlines()
    f.close()
    f = open("calendar.txt","w")
    i = 0
    for line in lines:
        if index != i:
            f.write(line)
        i += 1
    f.close()
    for member in memberList:
        if member in prac.getMemberList():
            member.messageReceive(prac.getDate()+" Practice at "+prac.getTime()+" with Coach: "+prac.getCoach().getName()+" has been cancelled.")
        del schedule[index]
    return 1

def removePracticeMembers(index):
    stillRemoving = True
    while(stillRemoving):
        for i in range(0,len(schedule[index].getMemberList())):
            print(" "+str(i+1)+") "+str(schedule[index].getMemberList()[i]))
        answer = input("Select Member Number to Remove: ")
        mem = schedule[index].getMemberList()[int(answer)-1]
        removeAPracticeMember(index,int(answer)-1)
        print("M#"+mem.getMemberID()+" has been removed.")
        answer = input("Would you like to remove another member? \"Y\" or \"N\"")
        if answer == "N":
            stillRemoving = False
    return 1

def removeAPracticeMember(index,memIndex):
    schedule[index].removeMember(memberList[memIndex])
    f = open("calendar.txt")
    lines = f.readlines()
    f.close()
    f = open("calendar.txt","w")
    for i in range(0,len(lines)):
        line = lines[i]
        if i == index:
            line = line.replace(" "+memberList[memIndex].getMemberID(),"")
        f.write(line)
    f.close()
    prac = schedule[index]
    memberList[memIndex].messageReceive("You have been removed from the "+prac.getDate()+
    " Practice at "+prac.getTime()+" with Coach "+prac.getCoach().getName()+". Please contact "+prac.getCoach().getNumber()+" for more details.")
    return 1

def addPracticeMembers(index):
    stillAdding = True
    while(stillAdding):
        for i in range(0,len(memberList)):
            print(" "+str(i+1)+") "+str(memberList[i]))
        answer = input("Enter Member Number to Add: ")
        mem = memberList[int(answer)-1]
        addAPracticeMember(index,int(answer)-1)
        print("M#"+mem.getMemberID()+" has been added.")
        answer = input("Would you like to add another member? \"Y\" or \"N\": ")
        if answer == "N":
            stillAdding = False
    return 1

def addAPracticeMember(index,memIndex):
    schedule[index].addMember(memberList[memIndex])
    f = open("calendar.txt")
    lines = f.readlines()
    f.close()
    f = open("calendar.txt","w")
    for i in range(0,len(lines)):
        line = lines[i]
        if i == index:
            line = line.replace("\n","")
            line = line + " " + memberList[memIndex].getMemberID()
            if(index != len(schedule)-1):
                line = line + "\n"
        f.write(line)
    f.close()
    prac = schedule[index]
    memberList[memIndex].messageReceive("You have been added to the "+prac.getDate()+
    " Practice at "+prac.getTime()+" with Coach "+prac.getCoach().getName()+". Please contact "+prac.getCoach().getNumber()+" for more details.")
    return 1

def addPractice(coach):
    date = input("Please Enter Date of Practice \"mm/dd\": ")
    time = input("Please Enter Time of Practice \"hh:mm-hh:mm(AM/PM)\": ")
    f = open("calendar.txt","a")
    f.write("\n"+date+" "+time+" "+coach.getUserID())
    schedule.append(practice.Practice(date,time,coach))
    print(date+" Practice at "+time+" has been added.")
    input("Enter any key to return to menu: ")
    menu(coach)

def manageSchedule(coach):
    for i in range(0,len(schedule)):
        if schedule[i].getCoach() == coach:
            print(" "+str(i+1)+") - "+str(schedule[i]))
    answer = input("Enter Practice Number to Manage,\"A\" to add a Practice or \"E\" to exit back to menu: ")
    if answer == "A":
        addPractice(coach)
    elif answer == "E":
        menu(coach)
    prac = schedule[int(answer) - 1]
    print("Would you like to:\n1) Cancel Practice\n2) Add a Member\n3) Remove a Member")
    option = input("Enter Option Number: ")
    if option == "1":
        removePractice(int(answer) - 1)
    elif option == "2":
        addPracticeMembers(int(answer)-1)
    elif option == "3":
        removePracticeMembers(int(answer) - 1)
    input("Enter any key to return to menu: ")
    menu(coach)

def joinPractice(mem):
    for i in range(0,len(schedule)):
        print(" "+str(i+1)+") "+str(schedule[i]))
    answer = input("Enter Practice # you would like to join or \"E\" if you would like to exit to the menu: ")
    if answer == "E": 
        menu()
    index = int(answer)-1
    addAPracticeMember(index,memberList.index(mem))
    userList[userList.index(schedule[index].getCoach())].messageReceive("M#"+mem.getMemberID()+" "+mem.getName()+" has joined your "+schedule[index].getDate()+" practice at "+schedule[index].getTime())
    userList[treasurerIndex].messageReceive("M#"+mem.getMemberID()+" "+mem.getName()+" has joined Coach "+schedule[index].getCoach().getName()+"'s "+schedule[index].getDate()+" practice at "+schedule[index].getTime())
    input("Enter any key to return to menu: ")
    memberMenu(mem)

def payPractice(mem):
    print("Payment Methods:\n1) Credit Card\n2) Debit")
    input("Enter Option Number")
    input("Please Tap Card, then enter any key: ")
    memberList[memberList.index(mem)].pay()
    userfile = open("users.txt","r")
    lines = userfile.lines()
    userfile.close()
    userfile = open("users.txt","w")
    for line in lines:
        sections = line.split(' ')
        if mem.getMemberID() == sections[1]:
            line = line.replace(sections[10].replace("\n",""),memberList[memberList.index(mem)].getPaid())
        userfile.write(line)
    userfile.close()
    print("Payment Processed.")
    return 1

main()