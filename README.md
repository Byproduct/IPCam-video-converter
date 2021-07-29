# IPcam video converter
This is a program for downloading, combining and converting videos from an IP camera into a format that is easier to browse.

I wrote it for a generic camera that is used with a phone app called "CamHi" and produces video files named "AYYMMDD_hhmmss_hhmmss.264", for example "A210714_003551_003605.264". <br />

![image of the camera](https://github.com/Byproduct/IPCam-video-converter/blob/main/documentation/camera.png)





## Installation
This program is made for windows, and requires:
- wget.exe in the same folder - available [here](gnuwin32.sourceforge.net/packages/wget.htm) (download -> binaries -> zip)
- ffmpeg.exe in the same folder - available [here](https://ffmpeg.org/download.html) ("get packages and executable files")

A windows .exe is included. If you compile this yourself, you'll also need:
- Python (written with version 3.9.6)
- [ffmpeg-python](https://github.com/kkroening/ffmpeg-python) (pip install ffmpeg-python)


## Troubleshooting
I haven't tested this program on many systems. If it doesn't run, try launching it from the command line and see if you get any kind of a helpful message. 

If you get just a python error instead of anything helpful, let me know and I'll see if it can be fixed!

## Purpose

If you have a motion-detecting camera outside, and it creates short video clips (e.g. 15 seconds), you can end up with thousands of recordings for example if it rains, when bugs or birds are flying in view, etc. This program will help you with that.

![phone app screenshot](https://github.com/Byproduct/IPCam-video-converter/blob/main/documentation/phoneapp2.png)<br />
Browsing through thousands of videos through this phone app is practically impossible. Even if you happen to know exactly the date and time you want, it's still extremely impractical. 

If you download the entire contents of the camera on your PC, and remove the directory structure, things will improve:
![264 files](https://github.com/Byproduct/IPCam-video-converter/blob/main/documentation/264files.png)<br />
Better, but not quite there yet. This is still difficult to make sense of, thousands of files are difficult to browse, and the ".264" format isn't playable on most systems by default.

So the purpose of this program is to turn the above into this:
![mp4 files](https://github.com/Byproduct/IPCam-video-converter/blob/main/documentation/mp4files.png)<br />
...which is perhaps accessible to human beings. :) In this example the camera was recording almost around the clock (hence the large number of merged videos), but this program can be helpful in less extreme scenarios too.

## Usage
This is what the program looks like:<br />
![gui](https://github.com/Byproduct/IPCam-video-converter/blob/main/documentation/GUI.png)<br />

You can set the default address/login/password in the config.txt file so you don't have to type it every time. If you're not sure what the address of your camera is, you can use for example the [IP Camera Viewer](https://www.deskshare.com/ip-camera-viewer.aspx) to search for cameras in your local network.

Clicking the download button starts the download of all video files on the camera, skipping already existing files. It can take a long time, depending on your setup and amount of videos. A new window should pop up and the file names should indicate which day it is currently downloading.

Once the download has completed, you'll see how many files you have, and an estimate of how many final videos you'll end up with after processing. You can adjust this with the "merge threshold" slider. For example if the merge threshold is 15 minutes, it means that it will keep combining videos until the next video is taken 15 minutes or more after the previous video.

Finally, the "process videos" button combines the videos and creates new mp4 files. A visitor in your camera will now appear in one video instead of dozens of videos. :)

There are no directories to set. The program folder contains folders "downloaded_videos" and "output_videos". Save the videos you want to keep elsewhere, and you can clear these folders of the large data.

## Disclaimer (you have full privacy)
This program will not change anything in your camera and will not spy on you in any way. For example, it will not delete downloaded videos, it will not save any information (besides saving the video files locally on your computer), and it will not connect anywhere else besides your camera. However, this program is open source and I can guarantee full privacy only if you downloaded it directly from my github (https://github.com/Byproduct). 

## Let me know if you found this useful. :)
I have no idea how popular this type of camera (this specific file format) is. I made this program mainly for myself, but if you've found it useful I'd love to hear it! You can drop me a line in discord Byproduct#9084 or email at byproduct@iki.fi.
