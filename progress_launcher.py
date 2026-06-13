  GNU nano 5.6.1                                               /usr/local/bin/progress_launcher.py                                                         
#!/usr/bin/env python3

import time
import subprocess

percent = 0

while percent <= 100:
    print(f"\rProgress: {percent}%", end="")
    time.sleep(1)
    percent += 1

# коли досяг 100%
print("\nDone! Launching wish.md...")

subprocess.Popen(["cat", "/usr/bin/wish.md"])
