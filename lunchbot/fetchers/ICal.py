import icalendar as ic
import requests as req


class ICal:
    events = dict()

    def __fetch_data(self) -> str:
        r = req.get(self.url)
        if r.status_code == 200:
            return r.text
        else:
            raise f"Unable to fetch iCalendar content from {self.url=}"

    def update(self):
        cal_src = self.__fetch_data()
        cal = ic.Calendar.from_ical(cal_src)
        for comp in cal.walk():
            print(comp)
            # if comp.name == "VEVENT":
            #     print(comp.get('summary'))
            #     print(comp.get('dtstart'))
            #     print(comp.get('dtend'))
            #     print(comp.get('dtstamp'))

    def __init__(self, url):
        self.url = url
        self.update()
