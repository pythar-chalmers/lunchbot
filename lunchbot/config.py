import yaml
from copy import deepcopy as copy

from lunchbot.fetchers.ICal import ical_from_config


FETCHER_CONS = {
    "ical": ical_from_config,
}


def get_config(path: str = "config.yml") -> dict:
    with open(path, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as err:
            print(f'Configuration error "{err}" in config file "{args.config}"!')
            raise err

config = get_config()

def get_fetchers(config: dict) -> dict:
    fetchers = dict()
    for uid, cfg in config["sources"].items():
        inner_cfg = copy(cfg)
        inner_cfg.pop("type", None)
        fetchers[uid] = FETCHER_CONS[cfg["type"]](inner_cfg)

    return fetchers
