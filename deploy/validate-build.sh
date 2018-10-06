#!/usr/bin/env bash

# Validates the current STAGE alias
#
# Usage:
#   validate_build.sh
#

aws lambda invoke --invocation-type RequestResponse --function-name TapList --qualifier STAGE --region us-east-1 --payload file://tests/data/ListBreweries.json ListBreweries.out
if grep -q 'Here are the breweries I know' ListBreweries.out; then
   exit 0
fi

# there's something wrong with response, get out
exit 255
