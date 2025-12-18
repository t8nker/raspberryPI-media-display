# 📺 Raspberry Pi CRT Media Looper
> A lightweight, persistent media looping system designed for vintage CRT displays.

![Raspberry Pi](https://img.shields.io/badge/Platform-Raspberry%20Pi-C51A4A?style=for-the-badge&logo=Raspberry-Pi)
![MPV](https://img.shields.io/badge/Player-MPV-334455?style=for-the-badge&logo=mpv)
![Bash](https://img.shields.io/badge/Language-Bash-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white)

This project allows you to loop videos and images on a Raspberry Pi connected to a CRT. It runs as a background service, meaning it starts automatically on boot—no desktop environment or mouse required.

---

## 🛠 Requirements
* **Raspberry Pi** (Any model with composite or VGA output)
* **MPV**: The engine that renders video/images to the hardware.
* **Systemd**: To keep the loop running 24/7.

**Install Dependencies:**
```bash
sudo apt update && sudo apt install mpv

## Requirements
mpv: The media player that does the heavy lifting.
systemd: This keeps the loop running even if the Pi restarts.

To install the player, run:

Bash

sudo apt update && sudo apt install mpv


## Media Layout
Keep all your media in one main folder so the scripts can find them. Media files can be videos or images.
Example structure:

/home/pi/media/Videos/
/home/pi/media/Images/
/home/pi/media/
/home/pi/media/playlist2.txt



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




