#!/bin/bash


curl -LO https://raw.githubusercontent.com/octokit/graphql-schema/master/schema.json
sgqlc-codegen schema --docstrings schema.json github_activity/github_schema.py
python -c 'import github_activity.github_schema'
