import json
import logging
import os
from collections import defaultdict

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
@click.option(
    "-s",
    "--sampling",
    required=False,
    default="3M",
    help="Pandas-compatible resampling value",
)
def render(input, sampling):
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np

    df = pd.read_json(input)
    df["createdAt"] = pd.to_datetime(df["createdAt"])
    df.sort_values(by="createdAt")
    df = df.set_index("createdAt")

    unique_events = df["type"].unique()
    bins = df.resample(sampling).count().index

    xs = defaultdict(list)
    ys = defaultdict(list)
    for l, r in zip(bins[:-1], bins[1:]):
        idx = (df.index >= l) & (df.index < r)
        sample = df[idx]
        counts = sample["type"].value_counts()

        for event in unique_events:
            try:
                val = counts[event]
            except KeyError:
                val = 0

            xs[event].append(l + (r - l) / 2)
            ys[event].append(val)

    bar_bottoms = np.zeros_like(xs[unique_events[0]], dtype=float)

    fig, axis = plt.subplots()
    for key in unique_events:
        y = np.array(ys[key]).astype(float)
        axis.fill_between(
            xs[key],
            bar_bottoms,
            y,
            step="post",
            label=key,
        )
        bar_bottoms = bar_bottoms + y
    axis.legend(loc="best")
    axis.set(xlabel="Time", ylabel="Count")
    fig.autofmt_xdate()
    fig.tight_layout()
    plt.show()
