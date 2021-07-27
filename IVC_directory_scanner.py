import os
import sys

# returns a readable version of video date and time (first and last video in the gui). E.g. 2021-07-20, 18:12:00
def create_timestring(filename):
    try:
        splitname = filename.split('_')
        date = splitname[0][1:]             # video date, YYMMDD     (removed 'A' at the beginning)
        year = 2000 + int(date[:-4])
        year = str(year)
        month = str(date[2:-2])
        month = month.zfill(2)
        day = str(date[4:])
        day = day.zfill(2)
        starttime = splitname[1]            # video start time, HHMMSS
        starthour = str(starttime[:-4])
        startminute = str(starttime[2:-2])
#    startsecond = str(starttime[4:])
    except:
        print("\nError processing downloaded_videos directory, check that there is only .264 video files and nothing else.\nFor example interrupted downloads can leave temporary files.\nIf all else fails, try emptying that directory altogether.\nExiting.")
        sys.exit()
    return year + "-" + month + "-" + day + ",  " + starthour + ":" + startminute


# returns the number of videos in the downloads folder, and the time of first and last videos
def scan_directory():
    directory = "downloaded_videos"
    filelist = []
    filelist = next(os.walk(directory))[2]
    filelist.sort()

    if len(filelist) > 1:
        firstvideo = filelist[0]
        lastvideo = filelist[len(filelist) - 1]
        firsttime = create_timestring(firstvideo)
        lasttime = create_timestring(lastvideo)
        return len(filelist), firsttime, lasttime
    else:
        return 0, "no videos found", "no videos found"


# returns a list of filenames in the downloads folder
def get_filenames():
    directory = "downloaded_videos"
    filelist = next(os.walk(directory))[2]
    filelist.sort()
    return filelist
