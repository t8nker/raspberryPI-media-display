## Requirements
mpv: The media player that does the heavy lifting.
systemd: This keeps the loop running even if the Pi restarts.

To install the player, run:

Bash

sudo apt update && sudo apt install mpv


## Media Layout
Keep all your media in one main folder so the scripts can find them. Media files can be videos or images.
Example structure:

/home/pi/media/
├── Videos/
├── Images/
├── playlist1.txt
└── playlist2.txt



## Creating Playlists
Playlists are just simple .txt files with one absolute path per line. Example (yourplaylist.txt):

/home/pi/media/Videos/cool_video.mp4
/home/pi/media/Images/cool_art.png


## How it Works
1. The sript (run_playlist.sh)
This script uses mpv to loop your files. It's set up to show images for 5 seconds each and loop the entire list forever. It also has a "fallback" default playlist variable just in case something goes wrong.

2. The systemd service (media_looper.service)
This  tells your Pi to start the loop as soon as it turns on. It runs in the background so you don't need a keyboard or mouse attached.

3. Switching Playlists (switch_playlist.sh)
Instead of editing files manually, you can swap what's playing on your display with one command:

sudo ./switch_playlist.sh yourplaylist1.txt
or
sudo ./switch_playlist.sh yourplaylist2.txt

Note: If your username isn't pi, make sure to change the paths in the scripts and the .service file to match your actual home directory!

