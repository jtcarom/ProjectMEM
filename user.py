class User:
    position = ""
    name = ""
    number = ""
    address = ""
    userid = ""
    password = ""
    messages = []

    def __init__(self,position,userid,name,num,address,password):
        self.position = position
        self.userid = userid
        self.name = name
        self.number = num
        self.address = address
        self.password = password

    def __eq__(self, other):
        return self.userid == other.getUserID()

    def getMessage(self):
        if self.messages:
            return self.messages.pop()
        else:
            return ""

    def messageReceieve(self,message):
        self.messages.append(message)

    def messageCount(self):
        return len(self.messages)
    
    def getUserID(self):
        return self.userid

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