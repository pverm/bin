#!/usr/bin/bash

# remove old logs
if [ -d "/home/pascal/sync/media/logs" ]; then
  rm -r /home/pascal/sync/media/logs
fi

# make fresh copy of logs
cp -R /home/pascal/.config/hexchat/logs/ /home/pascal/sync/media/

# grant all permissions
chmod -R 777 /home/pascal/sync/media/logs/

# remove carriage returns from dir/filenames
python /home/pascal/scripts/fix_logs.py
