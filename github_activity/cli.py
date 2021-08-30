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
@click.argument("input", type=click.File(mode="r"))
def render(input):
    import pandas as pd
    import matplotlib.pyplot as plt

    df = pd.read_json(input)
    df["createdAt"] = pd.to_datetime(df["createdAt"])
    df.sort_values(by="createdAt")
    df = df.set_index("createdAt")

    fig, axis = plt.subplots()
    for (typ, g) in df.groupby("type"):
        d = g.resample("1Y").count()
        x = d.index
        y = d["type"]
        axis.bar(x=x.values, height=y.values, label=typ, width=1.0)
    axis.legend(loc="best")
    fig.autofmt_xdate()
    fig.tight_layout()
    plt.show()
