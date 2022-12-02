import icalendar as ic
import requests as req
import re
import time
from datetime import datetime, date
from collections import defaultdict as DD
from pytz import UTC
import pytz
import logging

DEFAULT_ICON_URL = "https://avatars.githubusercontent.com/u/38406360"
DEFAULT_DATETIME = datetime(1970, 1, 1, tzinfo=UTC)

ICAL_FIELDS = [
    "summary",  # vText
    "location",  # vText
    "description",  # vText
    "dtstart",  # vDate
    "dtend",  # vDate
    "dtstamp",  # vDate
    "status",  # vText
]


def get_date(date_obj: ic.prop.vDDDTypes) -> datetime:
    # vDDDTypes to Datetime
    if not date_obj:
        return DEFAULT_DATETIME

    # Fix eventual "date" types.
    if type(date_obj.dt) == date:
        date_obj.dt = datetime.combine(date_obj.dt, datetime.min.time())

    date_obj.dt = date_obj.dt.replace(tzinfo=UTC)

    return date_obj.dt


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
        icon_url: str = DEFAULT_ICON_URL,
    ):
        self.title = str(summary)
        self.location = str(location)
        self.desc = str(description)
        self.dtstart = get_date(dtstart)
        self.dtend = get_date(dtend)
        self.dtstamp = get_date(dtstamp)
        self.status = str(status)
        self.icon_url = icon_url

    def __hash__(self):
        return hash((self.title, self.location, self.dtstart))

    def __eq__(self, other):
        if type(other) == type(self):
            return self.__hash__() == other.__hash__()
        else:
            return False

    def __repr__(self):
        return f'ICalEvent: "{self.title}" {self.location=} {self.dtstart=} {self.dtend=} {self.dtstamp=}'


def check_field(field: str, pattern: str = "") -> bool:
    return re.search(pattern, field, re.IGNORECASE) != None


def filter_event_obj(
    event: ICalEvent,
    pattern: str = "",
    cur_date: datetime = DEFAULT_DATETIME,
) -> bool:
    # Find keywords in any string inside the event
    tmp_str = f"{event.title} {event.location} {event.desc}"
    logging.info(
        f"\n\t{cur_date=} {type(cur_date)=}\n\t{event.dtend=} {type(event.dtend)=}"
    )
    return check_field(tmp_str, pattern) and cur_date <= event.dtend


class ICal:
    events: list[ICalEvent] = []
    seen: set[ICalEvent] = set()
    pattern = ""

    def __fetch_data(self) -> str:
        r = req.get(self.url)
        self.status = r.status_code == 200
        if self.status:
            return r.text
        else:
            logging.warning(
                f"Unable to fetch contents from ICal link '{self.url}' {self.status=}!"
            )
            return ""

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
                ical_event = ICalEvent(**event, icon_url=self.icon_url)
                logging.info(f"\t[{self.url}] Checking event: {ical_event}")
                self.events.append(ical_event)

    def get_events(self, cur_date: datetime = DEFAULT_DATETIME) -> list:
        found_events: set[ICalEvent] = {
            ev for ev in self.events if filter_event_obj(ev, self.pattern, cur_date)
        }
        new_events = found_events - self.seen
        self.seen = self.seen.union(found_events)

        return list(new_events)

    def __init__(
        self,
        url: str,
        pattern: str = "",
        icon_url: str = DEFAULT_ICON_URL,
    ):
        self.url = url
        self.pattern = pattern
        self.icon_url = icon_url
        self.update()


# Builders
def ical_from_config(config: dict):
    return ICal(**config)


def ical_from_cfg(cfg: dict):
    return ICal(cfg["url"])
