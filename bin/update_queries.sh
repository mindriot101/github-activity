#!/bin/bash

set -euo pipefail

mkdir -p github_activity
for query in queries/*; do
    module_name=$(echo $query | sed 's#^queries/##' | sed 's/\.graphql$//')
    echo $module_name
    filename=github_activity/${module_name}.py
    sgqlc-codegen operation --schema schema.json .github_schema ${filename} $query
    python -c "from github_activity.${module_name} import Operations"
    black -q $filename
done
