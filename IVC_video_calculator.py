from IVC_directory_scanner import get_filenames
import sys
import datetime

# creates dateobjects of filenames so that their dates/times can be compared easily
def create_dateobjects (filelist):
    dateobjects = []
    try:
        for videoname in filelist:
            splitname = videoname.split('_')
            date = splitname[0][1:]  # video date, YYMMDD     (removed 'A' at the beginning)
            year = 2000 + int(date[:-4])
            month = int(date[2:-2])
            day = int(date[4:])
            starttime = splitname[1]  # video start time, HHMMSS
            starthour = int(starttime[:-4])
            startminute = int(starttime[2:-2])
            startsecond = int(starttime[4:])
            # endtime = int(splitname[2][:-4])    # video end time, HHMMSS (removed '.264 at the end) - not needed at the moment.

            dateobject = datetime.datetime(year, month, day, starthour, startminute, startsecond)
            dateobjects.append(dateobject)
    except:
        print("\nError processing downloaded_videos directory, check that there is only .264 video files and nothing else.\nFor example interrupted downloads can leave temporary files.\nIf all else fails, try emptying that directory altogether.\nExiting.")
        sys.exit()
    return dateobjects

# Returns the number of videos the merging process would result in (but without actually merging the videos)
def calculate_final_videos(mergethreshold_m):
    mergethreshold = mergethreshold_m * 60            # thresholds are entered in minutes, but difference in video times is calculated in seconds
    # discardthreshold = discardthreshold_m * 60      # discard threshold is not used at the moment - see main program

    filelist = get_filenames()                        # list of filenames in the downloaded videos directory

    dateobjects = []
    dateobjects = create_dateobjects(filelist)        # create dateobjects of the filenames so that their times can be compared easily

    final_videos = 0
    # index_of_first_video_in_merged_series = 0       # for discard threshold, not used at the moment
    for i in range(0,len(dateobjects)-1):
        if i==0:                                      # first video is a special case
            pass
        elif i==len(dateobjects)-1:                   # last video is also a special case
            final_videos = final_videos + 1
        else:                                         # otherwise, increment the number of final videos by one if it is the last video in a series.
            timedifference = dateobjects[i] - dateobjects[i-1]
            if timedifference.total_seconds() < mergethreshold:
                pass
            if timedifference.total_seconds() >= mergethreshold:
                final_videos = final_videos + 1

                # for discard threshold, not used at the moment
                # videolength = dateobjects[i] - dateobjects[index_of_first_video_in_merged_series]
                # if videolength.total_seconds() >= discardthreshold:                 # except if the video is longer than discard threshold, in which case cancel the +1 done
                #     final_videos = final_videos - 1
                # index_of_first_video_in_merged_series = i+1

    return final_videos     # number of final videos, integer