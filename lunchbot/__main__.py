import argparse
import lunchbot.daemon

parser = argparse.ArgumentParser(prog="LunchBot Daemon", description="Free lunch!")
parser.add_argument("-i", "--interval", default=600, help="Interval between each fetcher update.")

if __name__ == "__main__":
    args = parser.parse_args()
    print(args)
