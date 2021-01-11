from ics import Calendar, Event
from ics import alarm
from datetime import datetime,timedelta
c = Calendar()
e = Event()
e.name = "My cool event"
e.begin = '2021-01-11T20:30:27.216884+02:00'
e.end = '2021-01-11T20:55:27.216884+02:00'
e.alarms.append(alarm.custom.CustomAlarm(trigger=timedelta(0,100),repeat=2,duration=timedelta(0,10),action='Action'))
e.alarms.append(alarm.custom.CustomAlarm(trigger=timedelta(0,10),repeat=None,duration=None,action='Action'))
e.description = 'Description'
c.events.add(e)
c.events
# [<Event 'My cool event' begin:2014-01-01 00:00:00 end:2014-01-01 00:00:01>]
with open('my2.ics', 'w') as my_file:
    my_file.writelines(c)
# and it's done !