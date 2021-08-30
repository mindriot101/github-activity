import json
import logging
import os

import click

from github_activity.client import Client


logging.basicConfig(level=logging.WARNING)
# root logger for the package
logger = logging.getLogger("github_activity")


@click.group()
@click.option("-v", "--verbose", count=True)
def main(verbose):
    if verbose == 1:
        logger.setLevel(logging.INFO)
    elif verbose > 1:
        logger.setLevel(logging.DEBUG)


@main.command()
@click.option("-O", "--owner", type=str, required=True)
@click.option("-r", "--repository", type=str, required=True)
@click.option("-b", "--branch", type=str, required=True)
@click.option("-o", "--output", type=click.File(mode="w"), required=False, default="-")
def generate(owner, repository, branch, output):
    token = os.environ["GITHUB_API_TOKEN"]

    client = Client(token)

    results = []
    for event in client.timeline(owner, repository, branch):
        logger.debug(f"event: {event.to_dict()}")
        results.append(event.to_dict())

    json.dump(results, output, indent=2)


@main.command()
def render():
    pass
