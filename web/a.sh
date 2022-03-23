wget http://127.0.0.1:5000/s3/getLogs

# start cron : sudo service cron start
# stop cron : sudo service cron stop
# enable cron : sudo systemctl enable cron
# write cron : crontab -e
# 0 0 * * * <name of command> runs every midnight