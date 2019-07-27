class EventsStorage:
    def __init__(self, path):
        self.fa = open(path,'a')
        self.fr = open(path,'r')
    def readFromFile(self):
        self.fr.seek(0)
        return self.fr.read().split("\n")
    def saveToFile(self,ipt,slot):
        self.fa.write(ipt+'^'+str(slot)+'\n')
        self.fa.flush()