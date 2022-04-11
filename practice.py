import user
class Practice:
    date = ""
    time = ""
    coach = False
    memberList = []

    def __init__(self,date,time,coach):
        self.date = date
        self.time = time
        self.coach = coach

    def __eq__(self, other):
        return self.coach == other.getCoach() and self.date == other.getDate() and self.time == other.getTime()

    def __str__(self):
        returnstr = self.date+" Practice at: "+self.time+"\nCoach: "+str(self.coach)+"\nMembers:"
        for member in self.memberList:
            returnstr += "\n"+str(member)
        return returnstr

    def getCoach(self):
        return self.coach

    def getDate(self):
        return self.date

    def getTime(self):
        return self.time

    def addMember(self,member):
        self.memberList.append(member)
    
    def getMemberList(self):
        return self.memberList
    
    def removeMember(self,member):
        if member in self.memberList:
            self.memberList.remove(member)