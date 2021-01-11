from ics import Calendar,Event,alarm
from datetime import datetime,timedelta
import sys
from tkinter import messagebox
import win32api
import json

class LocalAlarm:
    def __init__(self,event,alarm):
        self.begin = event.begin.timestamp
        self.end = event.end.timestamp
        self.eventName = event.name
        self.eventDescription = event.description
        self.trigger = alarm.trigger
        self.action = alarm.action
        self.repeat = alarm.repeat


class LocalAlarmJson:
    def __init__(self,event,alarm):
        self.begin = event['begin']
        self.end = event['end']
        self.eventName = event['name']
        self.eventDescription = event['description']
        self.trigger = LocalTrigger(alarm['trigger'])
        self.action = alarm['action']
        self.repeat = alarm['repeat']

class LocalTrigger:
    def __init__(self,trigger):
        self.seconds = trigger['seconds']
        self.days = trigger['days']

class LocalCalender:
    def __init__(self):
        pass

    def parseICS(self,file):
        calendarContent = open(file,'r').read()
        self.c = Calendar(calendarContent)
        self.listOfEvents = list(self.c.timeline)
        self.listOfAlarms = []
        self.listOfEvents = sorted(self.listOfEvents,key = lambda ev: ev.end)
        for e in self.listOfEvents:
            alarms = sorted(e.alarms,key = lambda a:a.trigger.seconds + a.trigger.days*86400,reverse=True)
            for al in alarms:
                self.listOfAlarms.append(LocalAlarm(e,al))

    def normalizeICSFile(self):
        while True:
            currentStamp = datetime.now().timestamp()
            e = self.listOfEvents[0]
            if e.end.timestamp < currentStamp:
                self.listOfEvents.pop(0)
            else:
                break

    def parseJSON(self,file):
        calendarContent = json.load(open('my.json','r'))
        events = sorted(calendarContent['events'],key = lambda ev: ev['end'])
        self.listOfAlarms = []
        for e in events:
            alarms = sorted(e['alarms'],key = lambda a:a['trigger']['seconds'] + a['trigger']['days']*86400,reverse=True)
            print(alarms)
            for al in alarms:
                self.listOfAlarms.append(LocalAlarmJson(e,al))
                print(self.listOfAlarms)

    def startInterval(self):
        while len(self.listOfAlarms) > 0:
            currStamp = datetime.now().timestamp()
            al = self.checkTimestampOnIcs(currStamp)
            currStamp = datetime.now().timestamp()
            trigg = al.trigger.seconds + al.trigger.days * 86400 + currStamp
            if trigg >= al.begin and trigg <= al.end:
                # messagebox.showinfo('Alarm')
                # messagebox.showwarning('Action:' + al.action + '\n' + 'Event Name:' + e.name + '\n' + 'Description:' + e.description)
                alarmMsg = 'Action:' + al.action + '\n' + 'Event Name:' + al.eventName + '\n' + 'Description:' + al.eventDescription
                win32api.MessageBox(0,alarmMsg,'Alarm')
                if al.repeat != None:
                    if al.repeat > 0:
                        al.repeat -= 1
                    if al.repeat == 0:
                        self.listOfAlarms.remove(al)
                else:
                    self.listOfAlarms.remove(al)

    def checkTimestampOnIcs(self,currStamp):
        while len(self.listOfAlarms) > 0:
            if self.listOfAlarms[0].end < currStamp:
                self.listOfAlarms.pop(0)
            else:
                break
        if len(self.listOfAlarms) > 0:
            return self.listOfAlarms[0]
        return None

    def launchCalendar(self,type,file):
        if type == 'json':
            self.parseJSON(file)
        else:
            self.parseICS(file)
        self.startInterval()


localCalendar = LocalCalender()
if len(sys.argv) > 1:
    if '.' in sys.argv[1]:
        if sys.argv[1].split('.')[1] == 'json':
            localCalendar.launchCalendar('json',sys.argv[1].strip())
        elif sys.argv[1].split('.')[1] == 'ics':
            localCalendar.launchCalendar('ics',sys.argv[1].strip())
        else:
            print('Wrong Format')