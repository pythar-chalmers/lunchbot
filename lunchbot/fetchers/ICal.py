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
        self.title = str(summary)
        self.location = str(location)
        self.desc = str(description)
        self.dtstart = dt_to_unix(dtstart)
        self.dtend = dt_to_unix(dtend)
        self.dtstamp = dt_to_unix(dtstamp)
        self.status = str(status)

    def __hash__(self):
        return hash((self.title, self.location, self.dtstart))

    def __eq__(self, other):
        if type(other) == type(self):
            return self.__hash__() == other.__hash__()
        else:
            return False

    def __repr__(self):
        return f'ICalEvent: "{self.title}" {self.location=} {self.dtstart=} {self.dtend=} {self.dtstamp=}'

    def to_discord_str(self):
        return "Event?"


def check_field(field: str, pattern: str = "") -> bool:
    return re.search(pattern, field, re.IGNORECASE) != None


def filter_event_obj(event: ICalEvent, pattern: str = "", t: int = 0) -> bool:
    # Find keywords in any string inside the event
    tmp_str = f"{event.title} {event.location} {event.desc}"
    check = (
        check_field(tmp_str, pattern) and t <= event.dtstart + 6000000
    )  # TODO: remove offset
    return check


class ICal:
    events = []
    seen = set()
    pattern = ""

    def __fetch_data(self) -> str:
        r = req.get(self.url)
        self.status = r.status_code == 200
        if self.status:
            return r.text
        else:
            print(
                f"WARNING! Unable to fetch contents from ICal link '{self.url}' {self.status=}!"
            )

    def update(self):
        cal_src = self.__fetch_data()

        if not cal_src:
            return

        self.events = []
        cal = ic.Calendar.from_ical(cal_src)
        for comp in cal.walk():  # parse ical
            if comp.name == "VEVENT":  # TODO: make future proof
                event = dict()
                for field in ICAL_FIELDS:  # parse only the fields
                    event[field] = comp.get(field)
                self.events.append(ICalEvent(**event))

    def get_events(self, t: int = 0) -> list:
        found_events = set(
            [ev for ev in self.events if filter_event_obj(ev, self.pattern, t)]
        )
        new_events = found_events - self.seen
        self.seen = self.seen.union(found_events)

        return list(new_events)

    def __init__(self, url: str, pattern: str = ""):
        self.url = url
        self.pattern = pattern
        self.update()

    def from_config(config: dict):
        return ICal(**config)


def ical_from_cfg(cfg: dict):
    return ICal(cfg["url"])
