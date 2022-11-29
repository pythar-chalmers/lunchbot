import argparse
from lunchbot.daemon import init as init_daemon

parser = argparse.ArgumentParser(prog="LunchBot Daemon", description="Free lunch!")
parser.add_argument(
    "-i", "--interval", default=600, help="Interval between each fetcher update."
)
parser.add_argument(
    "-r",
    "--regex-file",
    default="patterns/lunch.txt",
    help="File containing regex patterns (seperated by linebreak).",
)
parser.add_argument(
    "-c",
    "--config",
    default="config.yml",
    help="The config file.",
)
parser.add_argument(
    "-l",
    "--logfile",
    default="lunchbot.log",
    help="Output logfile.",
)

if __name__ == "__main__":
    args = parser.parse_args()

    init_daemon(args)
