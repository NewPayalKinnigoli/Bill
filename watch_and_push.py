import os
import time
import shutil
import subprocess
from datetime import datetime

# ====== Configuration ======
WATCH_FILE = r"D:\bill\BILL.pdf"         # Your billing software output file
REPO_FOLDER = r"C:\Repos\bill"           # Your GitHub local repo folder
TARGET_FILE = os.path.join(REPO_FOLDER, "BILL.pdf")
LOG_FILE = os.path.join(REPO_FOLDER, "log.txt")

# Full path to Git executable
GIT = r"C:\Program Files\Git\cmd\git.exe"

# ====== Utility Functions ======
def log(message):
    """Write a message to both console and log file."""
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    line = f"{timestamp} {message}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def run(cmd):
    """Run a system command and log output/errors."""
    log(f"Running: {cmd}")
    result = subprocess.run(cmd, cwd=REPO_FOLDER, shell=True,
                            capture_output=True, text=True)
    if result.stdout.strip():
        log(result.stdout.strip())
    if result.stderr.strip():
        log(result.stderr.strip())

# ====== Main Git Push Logic ======
def push_changes():
    """Copy the latest BILL.pdf and push to GitHub."""
    try:
        if os.path.exists(WATCH_FILE):
            shutil.copy2(WATCH_FILE, TARGET_FILE)
            log("✅ Copied latest BILL.pdf into repo")
        else:
            log("⚠️ WATCH_FILE missing! Cannot copy.")
            return

        run(f'"{GIT}" add -A')
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        run(f'"{GIT}" commit -m "Auto update BILL.pdf at {ts}" --allow-empty')
        run(f'"{GIT}" push origin main')
        log("✅ Last update successful")
        log("🌐 Public URL: https://newpayalkinnigoli.github.io/Bill/BILL.pdf")

    except Exception as e:
        log(f"❌ Error during push: {e}")

# ====== Watcher ======
def watch_file():
    """Watch for changes in the source BILL.pdf."""
    log(f"👀 Watching for updates: {WATCH_FILE}")
    last_mtime = None
    while True:
        try:
            if os.path.exists(WATCH_FILE):
                mtime = os.path.getmtime(WATCH_FILE)
                if mtime != last_mtime:
                    last_mtime = mtime
                    log("📄 Detected update in BILL.pdf → pushing to GitHub...")
                    push_changes()
            time.sleep(5)
        except Exception as e:
            log(f"❌ Watch loop error: {e}")
            time.sleep(10)

# ====== Start Script ======
if __name__ == "__main__":
    watch_file()
