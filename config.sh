#!/bin/sh

# Exit script if you try to use an uninitialized variable.
set -o nounset

# Exit script if a statement returns a non-true return value.
set -o errexit

# generate a configuration file from environment variables
# (overwrite bogus file that already exists)
echo \"\"\"secret values known only to DevOps\"\"\" > config.py
echo "BUILD_NUMBER =" $CIRCLE_BUILD_NUM >> config.py
echo "REDIS_HOST =" \"$REDIS_HOST\" >> config.py
echo "REDIS_PORT =" $REDIS_PORT >> config.py
echo "REDIS_PASSWORD =" \"$REDIS_PASSWORD\" >> config.py
