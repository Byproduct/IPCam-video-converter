from datetime import datetime
import os

# returns the last time videos were downloaded (date stored in a text file)
def check_download_date():
    download_date_text = "never"
    try:
        f = open("data/downloaddate.txt", "r")
        download_date_text = f.read()
    except:
        pass
    return "Videos last downloaded:\n" + download_date_text + "\n\n"

# saves the current time as the latest download time
def update_download_date():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d,   %H:%M:%S")

    try:
        f = open("data/downloaddate.txt", "w")
        f.write(current_time)
        f.close()
    except:
        pass

# opens the downloader (wget) in a new window. If it runs in the console in the background, it may seem like the program just hangs.
def download_videos(ipaddress, username, password):
    launchstring = "start /wait cmd /c wget.exe -nH -nc --cut-dirs=100 -r -P downloaded_videos -A .264 " + ipaddress + " --user " + username + " --password " + password
    os.system(launchstring)