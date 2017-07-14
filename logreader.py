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

        self.log = open(self.logpath,'r')#, encoding="utf8")
        self.log.readline()
        self.log.readline()
        line = self.log.readline()
        character = re.search("(?<=Listener: ).*", line)
        if character:
            character = character.group(0)
        else:
            raise BadLogException("not character log")
        print character

        while line:
            lastPos=self.log.tell()
            line = self.log.readline()
            if not line:
                self.log.seek(lastPos)
                print "Nuthing"
            else:
                print line,
                if "Undocking from" in line:
                    print "Undocking"
                if "You have defended" in line:
                    print "Plex completed"
                if "Your docking request has been accepted" in line:
                    print "Docking"

if __name__ == '__main__':
    log=LogReader()
