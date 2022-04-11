import user
import practice

userList = []
schedule = []
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
    for userA in userfile:
        sections = userA.split(' ')
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
        for member in members:
            temp.addMember(member)
        schedule.append(temp)
    calendarfile.close()


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
    input("Press any key to manage coach list: ")
    manageCoachList()

def viewSchedule(coach):
    for aPractice in schedule:
        if aPractice.coach == coach:
            print(aPractice)
    input("Press any key to return to menu: ")
    menu()
    return 1

def manageCoachList():
    index = 1
    coachList = []
    print("Coach List:\n")
    for user in userList:
        if user.getPosition() == "C":
            coachList.append(user)
            print(str(index) + ") " + str(user))
            index += 1
    print(str(index) + ") Add coach")
    answer = input("Enter Coach or Option Number: ")
    if(answer == str(index)):
        addUser()
        return
    selected = coachList[int(answer) - 1]
    print("1) View Schedule\n2) Remove Coach")
    answer = input("Enter Option Number: ")
    if(answer == "1"):
        viewSchedule(selected)
    else:
        removeCoach(selected)

def addUser():
    return 1

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
    for i in range(0,len(userList)):
        if userList[i] == user:
            index = i
    userList.remove(user)
    f = open("users.txt","r")
    lines = f.readlines()
    f.close()
    f = open("users.txt","w")
    for i in range(0,len(lines)):
        if index != i:
            f.write(lines[i])
    f.close()
    print("User " + user.getName() + " Removed Successfully.")
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

def manageMemberList():
    return 1

main()