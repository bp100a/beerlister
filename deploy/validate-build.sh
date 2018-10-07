#!/usr/bin/env bash

# Validates the current STAGE alias
#
# Usage:
#   validate_build.sh
#

aws lambda invoke --invocation-type RequestResponse --function-name TapList --qualifier STAGE --region us-east-1 --payload file://tests/data/ListBreweries.json ListBreweries.out
if ! grep -q 'Here are the breweries I know' ListBreweries.out; then
   exit 1
fi

aws lambda invoke --invocation-type RequestResponse --function-name TapList --qualifier STAGE --region us-east-1 --payload file://tests/data/GetTapListIntent_TwinElephant.json TwinElephant.out
if ! grep -q 'on tap at Twin Elephant' TwinElephant.out; then
   exit 2
fi

aws lambda invoke --invocation-type RequestResponse --function-name TapList --qualifier STAGE --region us-east-1 --payload file://tests/data/GetTapListIntent_Alementary.json Alementary.out
if ! grep -q 'on tap at Alementary' Alementary.out; then
   exit 3
fi

# nothing wrong, clean exit
exit 0
