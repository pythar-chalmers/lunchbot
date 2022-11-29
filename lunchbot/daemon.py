from lunchbot.discord_gateway import alert_lunch
import lunchbot.config as config

from collections import defaultdict as DD
from time import sleep as delay
from datetime import datetime
import threading
import pytz
import logging

FETCHERS: dict = {}
FETCHER_EVENTS = DD(list)


def update_tick():
    logging.info("Checking for event updates...")
    for _, fetcher in FETCHERS.items():
        fetcher.update()

    date = datetime.now()
    aware_date = pytz.utc.localize(date)
    for uid, fetcher in FETCHERS.items():
        FETCHER_EVENTS[uid] = fetcher.get_events(aware_date)

        # If we have new events then alert
        if len(FETCHER_EVENTS[uid]) >= 1:
            alert_lunch(FETCHER_EVENTS[uid])

    logging.info("Waiting for next update tick...")


def init(args):
    cfg = config.get_config(args.config)

    logging.basicConfig(
        format="%(asctime)s | %(levelname)s: %(message)s",
        filename=args.logfile,
        encoding="utf-8",
        level=logging.INFO,
    )

    global FETCHERS
    FETCHERS = config.get_fetchers(cfg)

    logging.info("LunchBot daemon started.")

    # thread = threading.Timer(int(args.interval), update_tick)
    # thread.start()

    while True:
        update_tick()  # Initial update tick
        delay(int(args.interval))

    logging.info("LunchBot daemon shutdown.")
