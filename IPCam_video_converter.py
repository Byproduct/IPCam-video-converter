import tkinter as tk
import tkinter.font as tkFont
import sys
from IVC_directory_scanner import *
from IVC_video_calculator import *
from IVC_downloader import *


# Check that wget.exe and ffmpeg.exe exist
if not os.path.isfile("wget.exe") or not os.path.isfile("ffmpeg.exe"):
    print("This program requires wget.exe and ffmpeg.exe in the same folder.")
    sys.exit()


# Default configuration, loaded from config.txt.
# These values are only what is displayed in the text fields by default. The user can edit the fields freely.
try:
    with open ("config.txt", "r") as f:
        data = f.readlines()
except:
    print("Error reading configuration file (config.txt)")
    sys.exit()
default_camera_address = data[3].rstrip()
default_camera_login = data[5].rstrip()
default_camera_password = data[7].rstrip()

# Create empty directories if they don't exist
if not os.path.isdir("data"):
    os.mkdir("data")
if not os.path.isdir("downloaded_videos"):
    os.mkdir("downloaded_videos")
if not os.path.isdir("output_videos"):
    os.mkdir("output_videos")



# GUI layout - row numbers for GUI elements
row_camera_address = 1
row_camera_login = row_camera_address + 1
row_camera_password = row_camera_login + 1
row_downloadbutton = row_camera_password + 1
row_local_directory = row_downloadbutton + 1
row_total_videos = row_local_directory + 1
row_first_date = row_total_videos + 1
row_last_date = row_first_date + 1
row_mergethreshold = row_last_date + 1
row_mergethreshold_note = row_mergethreshold + 1
row_discardthreshold = row_mergethreshold_note + 1      # not used at the moment
row_discardthreshold_note = row_discardthreshold + 1    # not used at the moment
row_final_videos = row_discardthreshold_note + 1


menu_main = tk.Tk()
menu_main.title("IPCam video converter")


# Fonts
normal_font = tkFont.Font(family="Calibri", size=20)
bold_font = tkFont.Font(family="Calibri", size=22, weight="bold")
huge_font = tkFont.Font(family="Calibri", size=30, weight="bold")
smaller_font = tkFont.Font(family="Calibri", size=12)


label_title = tk.Label(menu_main, font=bold_font, text="IPcam video converter", height=3)
label_title.grid(row=0, column=0, columnspan=2)


# input fields for camera address / login / password. No security (presumed user is using their own camera accessible only in their local network)
label_camera_address = tk.Label(menu_main, font=normal_font, text="Camera address / directory:")
label_camera_address.grid(row=row_camera_address, column=0, padx=10, sticky="nw")
entry_camera_address = tk.Entry(menu_main, font=normal_font)
entry_camera_address.insert(0, default_camera_address)
entry_camera_address.grid(row=row_camera_address, column=1, padx=10, sticky="new")

label_camera_login = tk.Label(menu_main, font=normal_font, text="Camera username:")
label_camera_login.grid(row=row_camera_login, column=0, padx=10, sticky="nw")
entry_camera_login = tk.Entry(menu_main, font=normal_font)
entry_camera_login.insert(0, default_camera_login)
entry_camera_login.grid(row=row_camera_login, column=1, padx=10, sticky="new")

label_camera_password = tk.Label(menu_main, font=normal_font, text="Password:\n")
label_camera_password.grid(row=row_camera_password, column=0, padx=10, sticky="nw")
entry_camera_password = tk.Entry(menu_main, font=normal_font)
entry_camera_password.insert(0, default_camera_password)
entry_camera_password.grid(row=row_camera_password, column=1, padx=10, sticky="new")


# Download videos button
def downloadfiles():
    update_download_date()
    text_downloaddate.set(check_download_date())
    address = entry_camera_address.get()
    login = entry_camera_login.get()
    password = entry_camera_password.get()
    download_videos(address, login, password)
    os.execl(sys.executable, sys.executable, *sys.argv)                     # closes and restarts the program to scan directory again and update information on screen etc

button_downloadfiles = tk.Button(menu_main, font=normal_font, text="Download videos\nfrom camera", command=downloadfiles, relief='groove', borderwidth=5, bg='#BBBBDD')
button_downloadfiles.grid(row=row_downloadbutton, column=0, padx=10, sticky="nw")

text_downloaddate = tk.StringVar()
text_downloaddate.set(check_download_date())
label_downloaddate = tk.Label(menu_main, font=normal_font, textvariable=text_downloaddate, justify='left')
label_downloaddate.grid(row=row_downloadbutton, column=1, padx=10, pady=10, sticky="W")


# Total (downloaded) videos on disk, date of first and last video. set into string variables (_sv) so they can be updated after they're downloaded.
label_local_directory_text = tk.Label(menu_main, font=bold_font, text="Downloaded videos")
label_local_directory_text.grid(row=row_local_directory, column=0, padx=10, sticky="nsw")

total_files, first_date, last_date = scan_directory()
total_files_sv = tk.StringVar()
first_date_sv = tk.StringVar()
last_date_sv = tk.StringVar()
total_files_sv.set(total_files)
first_date_sv.set(first_date)
last_date_sv.set(last_date)

label_total_videos_text = tk.Label(menu_main, font=normal_font, text="Total videos on disk:")
label_total_videos_text.grid(row=row_total_videos, column=0, padx=10, sticky="nw")
label_total_videos_value = tk.Label(menu_main, font=normal_font, textvariable=total_files_sv)
label_total_videos_value.grid(row=row_total_videos, column=1, padx=10, sticky="nw")

label_first_date_text = tk.Label(menu_main, font=normal_font, text="First video:")
label_first_date_text.grid(row=row_first_date, column=0, padx=10, sticky="nw")
label_first_date_value = tk.Label(menu_main, font=normal_font, textvariable=first_date_sv)
label_first_date_value.grid(row=row_first_date, column=1, padx=10, sticky="nw")

label_last_date_text = tk.Label(menu_main, font=normal_font, text="Last video:\n")
label_last_date_text.grid(row=row_last_date, column=0, padx=10, sticky="nw")
label_last_date_value = tk.Label(menu_main, font=normal_font, textvariable=last_date_sv)
label_last_date_value.grid(row=row_last_date, column=1, padx=10, sticky="nw")

final_videos_sv = tk.StringVar()

def recalculate_final_videos(event):
    mergethreshold = slider_mergethreshold.get()
    # discardthreshold = slider_discardthreshold.get()
    final_videos_sv.set("\n" + str(calculate_final_videos(mergethreshold)))


# merge threshold slider
label_mergethreshold = tk.Label(menu_main, font=normal_font, text="Merge threshold:")
label_mergethreshold.grid(row=row_mergethreshold, column=0, padx=10, sticky="SW")
slider_mergethreshold = tk.Scale(menu_main, from_=0, to=30, orient='horizontal', troughcolor='#BBBBDD', command=recalculate_final_videos)
slider_mergethreshold.grid(row=row_mergethreshold, column=1, padx=10, pady=5, sticky="NEW")
slider_mergethreshold.set(10)
label_mergethreshold_note = tk.Label(menu_main, font=smaller_font, text="Combine videos within this many minutes\n")
label_mergethreshold_note.grid(row=row_mergethreshold_note, column=1, padx=10, sticky="N")


# "discard threshold" not implemented at the moment.
# It is used for discarding very long videos (for example if it rains and the camera just records continuously for hours)
# In practice it seems easier to simply delete these files after they're created.

# label_discardthreshold = tk.Label(menu_main, font=normal_font, text="Discard threshold:")
# label_discardthreshold.grid(row=row_discardthreshold, column=0, padx=10, sticky="W")
# slider_discardthreshold = tk.Scale(menu_main, from_=0, to=120, orient='horizontal', troughcolor='#BBBBDD', command=recalculate_final_videos)
# slider_discardthreshold.grid(row=row_discardthreshold, column=1, padx=10, pady=5, sticky="NEW")
# slider_discardthreshold.set(60)
# label_discardthreshold_note = tk.Label(menu_main, font=smaller_font, text="Discard combined videos exceeding this many minutes\n")
# label_discardthreshold_note.grid(row=row_discardthreshold_note, column=1, padx=10, sticky="N")


# Number of final videos
label_final_videos = tk.Label(menu_main, font=bold_font, text="\nVideos after processing:\n")
label_final_videos.grid(row=row_final_videos, column=0, padx=10, sticky="NW")
label_final_videos_value = tk.Label(menu_main, font=bold_font, textvariable=final_videos_sv)
label_final_videos_value.grid(row=row_final_videos, column=1, padx=10, sticky="NW")


# The big start button
def convert_videos():
    mergethreshold = slider_mergethreshold.get()
#    discardthreshold = slider_discardthreshold.get()
    mergesetting = open("data/mergethreshold.txt", "w")
    mergesetting.write(str(mergethreshold))
    mergesetting.close()
    launchstring = "start /wait cmd /c python IVC_video_processor.py"        # opens in a new window (if it runs in the console in the background, it may seem like the program just hangs).
    os.system(launchstring)

button_convertvideos = tk.Button(menu_main, font=huge_font, text="PROCESS\nVIDEOS", relief='groove', borderwidth=10, width=20, bg='#BBBBDD', command=convert_videos)
button_convertvideos.grid(row=row_final_videos + 1, rowspan=3, column=0, columnspan=2, padx=10, sticky="NSEW")


menu_main.mainloop()