import argparse
import os

from github_api.client import Client


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--repository", required=True)
    parser.add_argument("-o", "--owner", required=True)
    args = parser.parse_args()

    token = os.environ["GITHUB_API_TOKEN"]

    client = Client(token)

    for event in client.timeline(args.owner, args.repository):
        print(event)
