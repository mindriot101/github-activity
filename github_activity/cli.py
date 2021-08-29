import argparse
import json
import logging
import os

from github_activity.client import Client


logging.basicConfig(level=logging.WARNING)
# root logger for the package
logger = logging.getLogger("github_activity")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--repository", required=True)
    parser.add_argument("-O", "--owner", required=True)
    parser.add_argument("-b", "--branch", required=True)
    parser.add_argument("-v", "--verbose", action="count", default=0)
    parser.add_argument(
        "-o", "--output", required=False, type=argparse.FileType("w"), default="-"
    )
    args = parser.parse_args()

    if args.verbose == 1:
        logger.setLevel(logging.INFO)
    elif args.verbose > 1:
        logger.setLevel(logging.DEBUG)

    token = os.environ["GITHUB_API_TOKEN"]

    client = Client(token)

    results = []
    for event in client.timeline(args.owner, args.repository, args.branch):
        logger.debug(f"event: {event.to_dict()}")
        results.append(event.to_dict())

    json.dump(results, args.output, indent=2)
