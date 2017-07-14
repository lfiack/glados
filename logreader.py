import os
import datetime
import time
import re

class LogReader():
    def __init__(self):
        self.path = os.environ['HOME'] + "/documents/eve/logs/Gamelogs/"

        # Find the latest log file
        fileLatest=""
        fileTimeLatest = datetime.datetime(year=datetime.MINYEAR,month=1,day=1)
        self.logStr = ""
        for filename in os.listdir(self.path):
            timeString = filename.strip(".txt")
            try:
                fileTime = datetime.datetime.strptime(timeString, "%Y%m%d_%H%M%S")
            except ValueError:
                continue
            if fileTime > fileTimeLatest:
                fileTimeLatest = fileTime
                fileLatest=filename
        self.logpath = self.path+fileLatest

        # Open the latest log file
        self.log = open(self.logpath,'r')#, encoding="utf8")
        # Read the first two lines, then the line that contains the character name
        self.log.readline()
        self.log.readline()
        line = self.log.readline()
        character = re.search("(?<=Listener: ).*", line)
        if character:
            character = character.group(0)
        else:
            raise BadLogException("not character log")
        print "Playing " + character

        # Read the rest of the file
        loop = True
        while loop:
            loop,self.logStr = self.read()
            if(self.logStr):
                print self.logStr

    def read(self):
        lastPos=self.log.tell()
        line = self.log.readline()
        if not line:
            self.log.seek(lastPos)
            return False, ""
        else:
            if "Undocking from" in line:
                return True, "undocking"
            if "You have defended" in line:
                return True, "plex completed"
            if "Your docking request has been accepted" in line:
                return True, "docking"
            return True, ""

# Test
if __name__ == '__main__':
    log=LogReader()
    while True:
        loop = True
        while loop:
            loop,s=log.read()
            if s:
                print s
