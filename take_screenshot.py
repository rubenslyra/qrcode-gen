import subprocess, time, os, sys
from PIL import Image, ImageGrab

# Launch the app
proc = subprocess.Popen(
    [sys.executable, "qrcode_gen.py"],
    cwd=os.path.dirname(os.path.abspath(__file__)),
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
)

# Wait for window to appear and render
time.sleep(3)

# Take screenshot
screenshot = ImageGrab.grab()
screenshot.save("screenshot_app.png")

# Kill the app
proc.terminate()
proc.wait(timeout=5)

print("Screenshot saved: screenshot_app.png")
