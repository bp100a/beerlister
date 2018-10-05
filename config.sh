#!/usr/bin/env bash

# Exit script if you try to use an uninitialized variable.
set -o nounset

# Exit script if a statement returns a non-true return value.
set -o errexit

# Use the error status of the first failure, rather than that of the last item in a pipeline.
set -o pipefail

# generate a configuration file from environment variables
echo \"\"\"secret values known only to DevOps\"\"\" > config.py
echo "BUILD_NUMBER=" $CIRCLE_BUILD_NUM >> config.py
echo "REDIS_HOST=" \"$REDIS_HOST\" >> config.py
echo "REDIS_PORT=" $REDIS_PORT >> config.py
echo "REDIS_PASSWORD=" \"$REDIS_PASSWORD\" >> config.py
