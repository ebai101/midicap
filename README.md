# midicap.py

always on MIDI recorder. listens to an incoming MIDI port, every 10 seconds without input it saves all the recent output to a file. requires python 3

## setup
from the project folder:
```
python3 -m venv venv
pip install -r requirements.txt
```
in midicap.py, define OUTPUT_DIR as the directory where you want the MIDI files to be saved

in midicap.sh, change FOLDER_PATH to the path of the **folder containing the midicap.py script**

## runing at boot (macOS)
in com.ethan.midicap.plist, change PATH_TO_MIDICAP.SH to the full path to midicap.sh

from the project folder:
`ln -s com.ethan.midicap.plist ~/Library/LaunchAgents/com.ethan.midicap.plist`
