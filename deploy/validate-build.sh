#!/usr/bin/env bash

# Validates the current STAGE alias
#
# Usage:
#   validate_build.sh
#

aws lambda invoke --invocation-type RequestResponse --function-name TapList --qualifier STAGE --payload file://../tests/data/ListBreweries.json ListBreweries.out
