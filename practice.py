import user
class Practice:
    date = ""
    coach = False
    memberList = []

    def __init__(self,date,coach):
        self.date = date
        self.coach = coach

    def getCoach(self):
        return self.coach

    def getDate(self):
        return self.date

    def addMember(self,member):
        self.memberList.append(member)
    
    def getMemberList(self):
        return self.memberList
    
    def removeMember(self,member):
        if member in self.memberList:
            self.memberList.remove(member)