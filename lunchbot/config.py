import yaml
from copy import deepcopy as copy

from lunchbot.fetchers.ICal import ICal


FETCHER_CONS = {
    "ical": ICal.from_config,
}


def get_fetchers(args: dict) -> dict:
    config = None
    with open(args.config, "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as err:
            print(f'Configuration error "{err}" in config file "{args.config}"!')
            raise err

    fetchers = dict()
    for uid, cfg in config["sources"].items():
        inner_cfg = copy(cfg)
        inner_cfg.pop("type", None)
        fetchers[uid] = FETCHER_CONS[cfg["type"]](inner_cfg)

    return fetchers
