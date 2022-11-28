from lunchbot.fetchers.ICal import ICal
from lunchbot.discordbot import alert_lunch
import lunchbot.config as config
from collections import defaultdict as DD
import threading
import time

FETCHERS = {}
FETCHER_EVENTS = DD(list)


def update_tick():
    print("Checking for event updates...")
    for _, fetcher in FETCHERS.items():
        fetcher.update()

    for uid, fetcher in FETCHERS.items():
        FETCHER_EVENTS[uid] = fetcher.get_events(int(time.time()))
        if len(FETCHER_EVENTS[uid]) >= 1:
            alert_lunch(FETCHER_EVENTS[uid])

    print(f"Waiting for next update tick...")


def init(args: dict):
    global FETCHERS
    FETCHERS = config.get_fetchers(args)

    print("LunchBot daemon started.")
    update_tick()  # Initial update tick

    thread = threading.Timer(args.interval, update_tick)
    thread.start()
