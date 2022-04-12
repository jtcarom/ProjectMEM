class Member:
    position = ""
    name = ""
    number = ""
    address = ""
    memberid = ""
    password = ""
    frequency = ""
    paid = ""
    messages = []

    def __init__(self,position,memberid,name,num,address,password,frequency,paid):
        self.position = position
        self.memberid = memberid
        self.name = name
        self.number = num
        self.address = address
        self.password = password
        self.frequency = frequency
        self.paid = paid

    def __eq__(self, other):
        return self.memberid == other.getMemberID()

    def __str__(self):
        return self.position+"#"+str(self.memberid) + " - " + self.name + " | Contact: " + self.number + " | Frequency: " + self.frequency + " | Payments: " + self.paid

    def getMessage(self):
        if self.messages:
            return self.messages.pop()
        else:
            return ""

    def messageReceive(self,message):
        self.messages.append(message)

    def messageCount(self):
        return len(self.messages)
    
    def getMemberID(self):
        return self.memberid

    def getPosition(self):
        return self.position
    
    def getName(self):
        return self.name
    
    def getNumber(self):
        return self.number

    def getAddress(self):
        return self.address

    def getPassword(self):
        return self.password

    def getFrequency(self):
        return self.frequency

    def getPaid(self):
        return self.paid

    def pay(self):
        self.paid = str(int(self.paid)+1)
        return 1