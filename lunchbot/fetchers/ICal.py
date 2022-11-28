import icalendar as ic
import requests as req
import re
from collections import defaultdict as DD

ICAL_FIELDS = [
    "summary",  # vText
    "dtstart",  # Date
    "dtend",  # Date
    "dtstamp",  # Date
    "location",  # vText
    "description",  # vText
    "status",  # vText
]


def check_field(field: str, regex: list = []) -> bool:
    match = False
    for reg in regex:
        match |= bool(re.match(reg, field))
    return match


def filter_event_obj(event: dict, regex: list = []) -> bool:
    match = False
    match |= check_field(event["summary"], regex)
    match |= check_field(event["location"], regex)
    match |= check_field(event["description"], regex)

    return match


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
                self.events.append(event)

    def get_events(self, time: int, patterns: list = []) -> list: # TODO: make time thing work
        return [ev for ev in self.events if filter_event_obj(ev, patterns)]

    def __init__(self, url):
        self.url = url
        self.update()
        # self.get_events(0)
