# 📺 Loop Image/Video Playlist on a raspberry PI 
![Raspberry Pi](https://img.shields.io/badge/Platform-Raspberry%20Pi-C51A4A?style=for-the-badge&logo=Raspberry-Pi)
![MPV](https://img.shields.io/badge/Player-MPV-334455?style=for-the-badge&logo=mpv)
![Bash](https://img.shields.io/badge/Language-Bash-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white)

This project allows you to loop videos and images on a Raspberry Pi connected to a display. It runs as a background service, meaning it starts automatically on boot—no desktop environment or mouse required.

I use this code to display images and videos on a small 5 inch CRT using a rf modulator
---

## 🛠 Requirements
* **Raspberry Pi** 
* **MPV**: The engine that renders video/images to the hardware.
* **Systemd**: To keep the loop running 24/7.

**Install Dependencies:**
```bash
sudo apt update && sudo apt install mpv
```

## Media Layout
Keep all your media in one main folder so the scripts can find them. Media files can be videos or images.
Example structure:
```bash
/home/pi/
├── media/               <-- Your media files go here
│   ├── Videos/
│   ├── Images/
│   ├── salemplaylist.txt  <-- Default playlist
│   └── my_art.txt         <-- yourplaylist
├── run_playlist.sh     
└── switch_playlist.sh   
```

## Creating Playlists
Playlists are just simple .txt files with one absolute path per line. Example (yourplaylist.txt):
```
/home/pi/media/Images/trippy_pattern.png
/home/pi/media/Videos/vhs_glitch.mp4
/home/pi/media/Images/scary_face.jpg
```
## How to Use
Move the media_looper.service file to /etc/systemd/system/ and enable it:
```bash
sudo systemctl enable media_looper.service
sudo systemctl start media_looper.service
```
Switch Playlists on the Fly
Use the controller script to swap between different media lists without stopping the Pi:
```bash
sudo ./switch_playlist.sh yourplaylist.txt
```

### Optional: Web Remote Control
Copy the webui.service to /etc/systemd/system/:
```sudo cp systemd/webui.service /etc/systemd/system/

Then:
sudo systemctl daemon-reload
sudo systemctl enable --now webui.service

Access at http://your-pi-ip:8080
Dependencies: sudo apt install python3-flask socat
```
## Important Note
This project assumes your username is pi. If you are using a different username, you must update the paths in:
```
media_looper.service (The ExecStart and User lines)
run_playlist.sh (The MEDIA_DIR variable)
switch_playlist.sh (The SERVICE path)
```




