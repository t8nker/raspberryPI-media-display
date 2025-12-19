from flask import Flask, render_template_string, request, redirect, send_from_directory
import subprocess
import os
import json
import time

app = Flask(__name__)

# --- CONFIG ---
MEDIA_DIR = "/home/pi/media"
SWITCH_SCRIPT = "/home/pi/switch_playlist.sh"
SERVICE_NAME = "media_looper.service"
SOCKET = "/tmp/mpvsocket"
STATIC_DIR = "/home/pi/static"
THUMB_PATH = os.path.join(STATIC_DIR, "thumb.jpg")

os.makedirs(STATIC_DIR, exist_ok=True)

def mpv_command(cmd):
    payload = json.dumps({"command": cmd}) + "\n"
    try:
        subprocess.run(["echo", payload], text=True)
        subprocess.run(["socat", "-", SOCKET], input=payload, text=True, check=False)
    except:
        pass  # mpv might be down

def get_current_playlist():
    try:
        output = subprocess.check_output(["systemctl", "show", "-p", "ExecStart", SERVICE_NAME], text=True)
        # Adjust this if your run_playlist.sh passes the name differently
        for part in output.split():
            if part.endswith('.txt'):
                return part
    except:
        pass
    return None

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>CRT Control Center</title>
    <style>
        :root {
            --bg: #0a0a0a;
            --card: #111;
            --text: #eee;
            --accent: #c51a4a;
            --play: #2e7d32;
            --pause: #f9a825;
            --danger: #ff3333;
            --glow: 0 0 15px rgba(197,26,74,0.4);
        }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
               background: var(--bg); color: var(--text); margin: 0; padding: 15px; min-height: 100vh; }
        .container { max-width: 480px; margin: 0 auto; }
        .preview-box { width: 100%; aspect-ratio: 16/9; background: #000; border-radius: 16px;
                       overflow: hidden; margin-bottom: 16px; box-shadow: var(--glow); border: 2px solid #333; }
        #live-thumb { width: 100%; height: 100%; object-fit: contain; }
        .refresh-btn { background: #222; color: #888; border: none; padding: 6px 10px;
                       border-radius: 8px; font-size: 0.8rem; cursor: pointer; margin-top: -12px; }
        .status-bar { background: rgba(20,20,20,0.95); padding: 12px; border-radius: 12px;
                      display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;
                      box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
        .time-display { font-family: 'Courier New', monospace; color: #55ff55; font-size: 1.3rem; font-weight: bold; }
        .control-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 24px; }
        button { padding: 18px; font-size: 1.4rem; font-weight: bold; border: none;
                 border-radius: 16px; cursor: pointer; transition: all 0.15s; box-shadow: 0 4px 8px rgba(0,0,0,0.4); }
        button:active { transform: scale(0.94); }
        .btn-nav { background: var(--play); color: white; }
        .btn-pause { background: var(--pause); color: black; }
        .btn-switch { background: var(--accent); color: white; margin: 10px 0; box-shadow: var(--glow); }
        select { background: #222; color: white; padding: 12px; border-radius: 12px; width: 100%; margin-bottom: 10px; }
        .btn-restart { background: #333; color: #aaa; margin: 16px 0; }
        .btn-danger { background: #200; color: var(--danger); }
        h3 { margin: 24px 0 8px; color: #ccc; }
        hr { border: 0; height: 1px; background: #333; margin: 30px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="preview-box">
            <img id="live-thumb" src="/api/thumbnail?t={{ now }}" alt="Live Preview">
        </div>
        <button class="refresh-btn" onclick="refreshThumb()">📸 Refresh Preview</button>

        <div class="status-bar">
            <span style="font-size:0.9rem; color:#888;">{{ active_list or 'Not Running' }}</span>
            <span class="time-display" id="timer">00:00:00</span>
        </div>

        <div class="control-grid">
            <button onclick="control('prev')" class="btn-nav">⏮</button>
            <button onclick="control('pause')" class="btn-pause">⏯</button>
            <button onclick="control('next')" class="btn-nav">⏭</button>
        </div>

        <h3>Switch Playlist</h3>
        <form method="POST" action="/switch">
            <select name="playlist">
                {% for plist in playlists %}
                <option value="{{ plist }}" {% if plist == active_list %}selected{% endif %}>
                    {{ plist.replace('.txt', '') }}
                </option>
                {% endfor %}
            </select>
            <button type="submit" class="btn-switch">Switch Playlist</button>
        </form>

        <hr>
        <button onclick="control('restart')" class="btn-restart">🔄 Restart Player</button>
        <button onclick="control('stop')" class="btn-danger">🛑 Stop Service</button>
    </div>

    <script>
        function refreshThumb() {
            const img = document.getElementById('live-thumb');
            img.src = '/api/thumbnail?t=' + Date.now();
        }
        function control(action) {
            fetch('/control', {
                method: 'POST',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: 'action=' + action
            }).then(r => {
                if (action === 'restart' || action === 'stop') {
                    setTimeout(() => location.reload(), 2000);
                } else if (action !== 'pause') {
                    refreshThumb();
                }
            });
        }
        setInterval(() => {
            fetch('/api/time').then(r => r.text()).then(t => {
                document.getElementById('timer').innerText = t;
            });
        }, 1000);
        window.onload = refreshThumb;
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    playlists = sorted([f for f in os.listdir(MEDIA_DIR) if f.endswith('.txt')])
    active = get_current_playlist()
    return render_template_string(HTML_TEMPLATE, playlists=playlists, active_list=active, now=int(time.time()))

@app.route('/api/time')
def api_time():
    try:
        result = subprocess.check_output(
            f'echo \'{{ "command": ["get_property", "time-pos"] }}\' | socat - {SOCKET}',
            shell=True, text=True
        )
        data = json.loads(result.strip())
        if data.get("data") is not None:
            s = int(float(data["data"]))
            return str(timedelta(seconds=s))[2:10]
    except:
        pass
    return "00:00:00"

@app.route('/api/thumbnail')
def get_thumbnail():
    thumb_path = os.path.join(STATIC_DIR, "thumb.jpg")
    try:
        # We only generate the thumb IF the file doesn't exist
        # or if you want to keep the "one-time" generation logic
        cmd = f'echo \'{{"command": ["screenshot-to-file", "{thumb_path}", "video"]}}\' | socat - {SOCKET}'
        subprocess.run(cmd, shell=True)
        return send_from_directory(STATIC_DIR, "thumb.jpg")
    except:
        return "Error"


@app.route('/switch', methods=['POST'])
def switch():
    playlist = request.form.get('playlist')
    if playlist and playlist.endswith('.txt'):
        subprocess.run(["sudo", SWITCH_SCRIPT, playlist], check=False)
    return redirect('/')

@app.route('/control', methods=['POST'])
def control():
    action = request.form.get('action')
    if action == "next":
        mpv_command(["playlist-next"])
    elif action == "prev":
        mpv_command(["playlist-prev"])
    elif action == "pause":
        mpv_command(["cycle", "pause"])
    elif action == "restart":
        subprocess.run(["sudo", "systemctl", "restart", SERVICE_NAME])
    elif action == "stop":
        subprocess.run(["sudo", "systemctl", "stop", SERVICE_NAME])
        subprocess.run(["sudo", "pkill", "-f", "mpv"])
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)

