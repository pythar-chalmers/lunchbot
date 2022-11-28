#!/usr/bin/env python

import icalendar as ic
import requests as req

CALENDAR_URL = "https://calendar.google.com/calendar/ical/dtek.se_0tavt7qtqphv86l4stb0aj3j88%40group.calendar.google.com/public/basic.ics"

def get_icalendar_source(url: str) -> str:
    r = req.get(url)
    if r.status_code == 200:
        return r.text
    else:
        raise f"Unable to fetch iCalendar content from {url=}"

def get_events(url: str):
    cal_src = get_icalendar_source(url)
    cal = ic.Calendar(cal_src)
    print(cal.events)

if __name__ == "__main__":
    get_events(CALENDAR_URL)
