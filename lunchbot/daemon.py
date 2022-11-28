# https://calendar.google.com/calendar/ical/dtek.se_0tavt7qtqphv86l4stb0aj3j88%40group.calendar.google.com/public/basic.ics"

from lunchbot.fetchers.ICal import ICal

fetchers = {
    "dtek": ICal(
        "https://calendar.google.com/calendar/ical/dtek.se_0tavt7qtqphv86l4stb0aj3j88%40group.calendar.google.com/public/basic.ics"
    )  # DTEK calendar
}


def update_tick():
    for fetcher in fetchers:
        fetcher.update()


def init():
    pass
