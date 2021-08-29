import argparse
import logging
import os

from github_activity.client import Client


logging.basicConfig(level=logging.WARNING)
# root logger for the package
logger = logging.getLogger("github_activity")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--repository", required=True)
    parser.add_argument("-o", "--owner", required=True)
    parser.add_argument("-v", "--verbose", action="count", default=0)
    args = parser.parse_args()

    if args.verbose == 1:
        logger.setLevel(logging.INFO)
    elif args.verbose > 1:
        logger.setLevel(logging.DEBUG)

    token = os.environ["GITHUB_API_TOKEN"]

    client = Client(token)

    for event in client.timeline(args.owner, args.repository):
        print(event)
