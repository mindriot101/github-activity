#!/bin/bash

set -euo pipefail

mkdir -p github_api
for query in queries/*; do
    module_name=$(echo $query | sed 's#^queries/##' | sed 's/\.graphql$//')
    echo $module_name
    sgqlc-codegen operation --schema schema.json .github_schema github_api/${module_name}.py $query
    # python -c "from github_api.${module_name} import Operations"
done
