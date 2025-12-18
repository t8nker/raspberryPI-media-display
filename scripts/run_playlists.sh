#!/bin/bash

# put your playlists in this folder
MEDIA_DIR="/home/pi/media/" 

# THE BACKUP LIST
# put a filename here so it doesnt crash if u forget to type one
DEFAULT_LIST="playlist1.txt" # please change to curated playlist

# check if we gave it a name
if [ -n "$1" ]; then
PLAYLIST="$1" 
else
  echo "You didnt give me a name! Using $DEFAULT_LIST"
PLAYLIST="$DEFAULT_LIST" 
fi

# add the folder and the name together
PATH_TO_FILE="${MEDIA_DIR}/${PLAYLIST}" 

# make sure mpv is actually there
if ! command -v mpv &> /dev/null
then
echo "mpv is missing! do: sudo apt install mpv"
exit
fi

echo "Trying to play: $PATH_TO_FILE"

# LOOP
while true
do
# check if the file exists and has stuff in it
if [ -s "$PATH_TO_FILE" ]
then
        echo "Playing now..."
        # the display duration is 5 seconds for images, change "image-display-duration=5" if you want to change duration
        mpv --vo=drm --fullscreen --loop-playlist --no-terminal --image-display-duration=5 --playlist="$PATH_TO_FILE"
else
echo "ERROR: $PATH_TO_FILE is empty or missing!"
echo "Trying the default one: $DEFAULT_LIST"
        
        if [ -s "${MEDIA_DIR}/${DEFAULT_LIST}" ]
        then
        mpv --vo=drm --fullscreen --loop-playlist --no-terminal --image-display-duration=5 --playlist="${MEDIA_DIR}/${DEFAULT_LIST}"
        else
            echo "Everything is missing. please edit 'DEFAULT_LIST= ' "
            sleep 60 
        fi
fi
    # Wait 5 seconds before trying again if it closes
    sleep 5 
done