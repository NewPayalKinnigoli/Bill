# push_pdf_only.py
import os
import time
import shutil
import subprocess
from datetime import datetime

# ---------- CONFIG (change only if needed) ----------
WATCH_FILE = r"D:\bill\BILL.pdf"                   # source file created by billing software
REPO_FOLDER = r"C:\Repos\bill"                     # your repo
TARGET_FILE = os.path.join(REPO_FOLDER, "BILL.pdf")
LOG_FILE = os.path.join(REPO_FOLDER, "log.txt")
GIT = r"C:\Program Files\Git\cmd\git.exe"          # full path to git.exe
POLL_INTERVAL = 5                                   # seconds between checks
# ----------------------------------------------------

def log(msg):
    ts = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    line = f"{ts} {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

def run(cmd):
    log(f"Running: {cmd}")
    result = subprocess.run(cmd, cwd=REPO_FOLDER, shell=True, capture_output=True, text=True)
    if result.stdout and result.stdout.strip():
        log(result.stdout.strip())
    if result.stderr and result.stderr.strip():
        log("ERR: " + result.stderr.strip())
    return result.returncode

def safe_copy(src, dst, retries=3, delay=1):
    for i in range(retries):
        try:
            shutil.copy2(src, dst)
            return True
        except Exception as e:
            log(f"Copy attempt {i+1} failed: {e}")
            time.sleep(delay)
    return False

def push_pdf():
    if not os.path.exists(WATCH_FILE):
        log("⚠️ WATCH_FILE missing, skipping")
        return
    ok = safe_copy(WATCH_FILE, TARGET_FILE)
    if not ok:
        log("❌ Failed to copy PDF after retries")
        return
    log("✅ Copied PDF to repo")
    run(f'"{GIT}" add "BILL.pdf"')
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    run(f'"{GIT}" commit -m "Auto update BILL.pdf at {ts}" --allow-empty')
    rc = run(f'"{GIT}" push origin main')
    if rc == 0:
        log("✅ Push successful")
    else:
        log("❌ Push failed (see above errors)")

def watch_file():
    log(f"Watching: {WATCH_FILE}")
    last_mtime = None
    while True:
        try:
            if os.path.exists(WATCH_FILE):
                m = os.path.getmtime(WATCH_FILE)
                if m != last_mtime:
                    last_mtime = m
                    log("Detected update in BILL.pdf — doing push")
                    push_pdf()
        except Exception as e:
            log(f"Watcher error: {e}")
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    watch_file()
