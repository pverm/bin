#!/usr/bin/bash

src="~/.config/hexchat/logs"
dst="~/sync/media/logs"
fixlogs="~/scripts/fix_logs.py"

# copy/update logs
rsync -aq $src $dst

# grant all permissions
chmod -R 777 $dst

# remove carriage returns from dir/filenames
python $fixlogs
