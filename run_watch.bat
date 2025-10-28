@echo off
REM Run watcher minimized on user logon
cd /d "C:\Repos\bill"
start "" /min "C:\Users\PayalFashion\AppData\Local\Programs\Python\Python314\python.exe" "C:\Repos\bill\watch_and_push.py"
exit
