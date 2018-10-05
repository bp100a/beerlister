# generate a configuration file from environment variables
echo \"\"\"secret values known only to DevOps\"\"\"
echo "BUILD_NUMBER=" $CIRCLE_BUILD_NUM >> config.py
echo "REDIS_HOST=" \"$REDIS_HOST\" >> config.py
echo "REDIS_PORT=" $REDIS_PORT >> config.py
echo "REDIS_PASSWORD=" \"$REDIS_PASSWORD\" >> config.py

