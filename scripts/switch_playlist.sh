#!/bin/bash

# --- CONFIG STUFF ---
SERVICE="/etc/systemd/system/media_looper.service"
S_NAME="media_looper.service"
RUN_SCRIPT="/home/pi/run_playlist.sh"


# make sure we are root
if [ "$EUID" -ne 0 ]
  then echo "RUN AS SUDO PLEASE!"
  exit
fi


# get the name of the txt file
LIST=$1

if [ -z "$LIST" ]
then
echo "You forgot to type the playlist name!"
echo "usage: sudo ./switch_playlist.sh names.txt"
exit
fi

echo "Switching to: $LIST"

# Stop the service first
sudo systemctl stop $S_NAME
# kill mpv just in case it is stuck
sudo pkill -9 mpv
sleep 2

# Added a safety net (.bak) just in case this breaks the file!
sudo sed -i.bak "s|ExecStart=.*|ExecStart=/bin/bash $RUN_SCRIPT $LIST|" $SERVICE

echo "Reloading..."
sudo systemctl daemon-reload
echo "Starting again..."
sudo systemctl start $S_NAME

# Check if it worked
if [ $? -eq 0 ]
        then
        echo "DONE!"
        echo "Playing $LIST now."
else
        echo "It didnt work :("
        echo "Check the backup file at $SERVICE.bak"
fi

exit