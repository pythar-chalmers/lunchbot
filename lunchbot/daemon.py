from lunchbot.fetchers.ICal import ICal
from lunchbot.parse_patterns import get_patterns
import threading
import time

START_TIME = int(time.time())
PATTERNS = []

fetchers = {
    "dtek": ICal(
        "https://calendar.google.com/calendar/ical/dtek.se_0tavt7qtqphv86l4stb0aj3j88%40group.calendar.google.com/public/basic.ics"
    )  # DTEK calendar
}


def update_tick():
    print("Updating fetchers...")
    for fetcher in fetchers:
        fetcher.update()
    print("Done.")


def init(args):
    PATTERNS = get_patterns(args.regex_file)

    thread = threading.Timer(args.interval, update_tick)
    thread.start()
    print("LunchBot daemon started.")
