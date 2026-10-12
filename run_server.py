# ====================================================================
# Standalone Web Server Launcher for College Club System
# Automatically starts Flask and opens http://127.0.0.1:5000 in your browser
# ====================================================================

import os
import sys
import webbrowser
import threading
import time

# Ensure working directory is set to where the executable/script is located
if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))
else:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

import app

def open_browser():
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    threading.Thread(target=open_browser, daemon=True).start()
    print("=" * 65)
    print("  College Club Event Management System - Web Server")
    print("=" * 65)
    print("  Server is active on: http://127.0.0.1:5000")
    print("  Opening browser automatically...")
    print("  Keep this window open while using the app.")
    print("  Press Ctrl+C to stop the server.\n")
    app.app.run(debug=False, port=5000, host="127.0.0.1")
