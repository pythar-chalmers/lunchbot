import icalendar as ic
import requests as req
import re
import time
from datetime import datetime
from collections import defaultdict as DD

ICAL_FIELDS = [
    "summary",  # vText
    "location",  # vText
    "description",  # vText
    "dtstart",  # vDate
    "dtend",  # vDate
    "dtstamp",  # vDate
    "status",  # vText
]


def dt_to_unix(date: ic.prop.vDDDTypes) -> int:
    return -1 if not date else int(time.mktime(date.dt.timetuple()))


# Wrapper class for ICalendar events
class ICalEvent:
    def __init__(
        self,
        summary: ic.prop.vText,
        location: ic.prop.vText = None,
        description: ic.prop.vText = None,
        dtstart: ic.prop.vDDDTypes = None,
        dtend: ic.prop.vDDDTypes = None,
        dtstamp: ic.prop.vDDDTypes = None,
        status: ic.prop.vText = None,
    ):
        self.sum = str(summary)
        self.loc = str(location)
        self.desc = str(description)
        self.dtstart = dt_to_unix(dtstart)
        self.dtend = dt_to_unix(dtend)
        self.dtstamp = dt_to_unix(dtstamp)
        self.status = str(status)

    def __hash__(self):
        return (self.sum, self.loc, self.dtstart)

    def __eq__(self, other):
        if type(other) == type(self):
            return self.__hash__() == other.__hash__()
        else:
            return False

    def __repr__(self):
        return f'ICalEvent: "{self.sum}" {self.loc=} {self.dtstart=} {self.dtend=} {self.dtstamp=}'


def check_field(field: str, regex: list = []) -> bool:
    match = False
    for reg in regex:
        match |= bool(re.match(reg, field))
    return match


def filter_event_obj(event: ICalEvent, regex: list = [], time: int = 0) -> bool:
    if int(time.time()) < time:  # if in the past then ignore
        return False

    # Find keywords in any string inside the event
    tmp_str = f"{event.sum} {event.loc} {event.desc}"
    return check_field(tmp_str, regex)


class ICal:
    events = []

    def __fetch_data(self) -> str:
        r = req.get(self.url)
        self.status = r.status_code == 200
        if self.status:
            return r.text
        else:
            print(f"WARNING! Unable to fetch contents from ICal link '{self.url}'!")

    def update(self):
        cal_src = self.__fetch_data()

        if not cal_src:
            return

        self.events = []
        cal = ic.Calendar.from_ical(cal_src)
        for comp in cal.walk():  # parse ical
            if comp.name == "VEVENT":
                event = dict()
                for field in ICAL_FIELDS:  # parse only the fields
                    event[field] = comp.get(field)
                self.events.append(ICalEvent(**event))

    def get_events(self, time: int = 0, patterns: list = []) -> list:
        return [ev for ev in self.events if filter_event_obj(ev, patterns, time)]

    def __init__(self, url):
        self.url = url
        self.update()
