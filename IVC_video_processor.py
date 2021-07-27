from os import system, name
import sys
from IVC_directory_scanner import get_filenames
from IVC_video_calculator import create_dateobjects
import ffmpeg

# creates a list of filenames and whether to include, merge or discard them
def create_joblist(mergethreshold_m):
    mergethreshold = mergethreshold_m * 60
#    discardthreshold_m = 60
#    discardthreshold = discardthreshold_m * 60

    filelist = get_filenames()                                    # gets a list of files in the downloaded_videos directory
    dateobjects = create_dateobjects(filelist)                    # turns this list into dateobjects so that their times can be compared easily
    joblist = []

    for i in range(0, len(dateobjects) - 1):
        job = f"{i};{filelist[i]};{dateobjects[i]}"
        if i < len(dateobjects) - 2:
            timedifference = dateobjects[i+1] - dateobjects[i]
            if timedifference.total_seconds() < mergethreshold:   # if this video and the next were recorded around the same time (below the specified threshold in minutes), flag this video as to be merged with the next one.
                job += ";MERGENEXT"
        job += "\n"
        joblist.append(job)

    try:
        with open('data/joblist.txt', 'w') as f:
            for job in joblist:
                f.write(job)
    except:
        print("Unable to open joblist.txt for writing.")
        sys.exit()


def clear_screen():
    # for windows
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def convert_videos(mergethreshold):
    try:
        create_joblist(mergethreshold)
        with open('data/joblist.txt') as f:
            joblist = f.read().splitlines()
    except:
        print("\nUnable to open joblist.txt for reading.")
        sys.exit()

    clear_screen()
    print("IPcam video merger")
    print("------------------\n")

    # count total number of encode tasks for progress bar
    encode_tasks = 0
    for job in joblist:
        if 'MERGENEXT' not in job:
            encode_tasks = encode_tasks + 1

    i = 0
    encode_progress = 0
    firstvideo = True
    video_filenames = []
    firstvideo_index = 0
    fistvideo_date = ""
    videolength = 0  # number of 15s videos merged in one

    for job in joblist:
        splitline = job.split(';')

        if firstvideo == True:
            video_filenames = []
            firstvideo_index = i
            firstvideo_date = splitline[2]
            videolength = 0
            firstvideo = False

        videolength = videolength + 1
        video_filenames.append(splitline[1])

        if 'MERGENEXT' not in job:                         # if this is the last video in a series
            encode_progress = encode_progress + 1
            # print progress
            progress = int((encode_progress + 1) / encode_tasks * 100)
            clear_screen()
            progressbar1 = ""
            progressbar2 = ""
            print("Encoding task " + str(encode_progress) + " of " + str(encode_tasks))
            print("Working...")
            print("[", end="")
            for x in range(0, int(progress / 2)):
                progressbar1 = progressbar1 + "#"
            for x in range(int(progress / 2), 50):
                progressbar2 = progressbar2 + " "
            print(progressbar1 + progressbar2 + "] " + str(progress) + " %")

            # create a temporary list of input files for ffmpeg. For multiple videos, this format seems to accept only a textfile? At least I couldn't make anything else work.
            # example of required line inside the text file:
            # file '../downloaded_videos/A210214_122208_122222.264'
            temp_vidlist = ""
            for filename in video_filenames:
                temp_vidlist = temp_vidlist + "file '../downloaded_videos/" + filename + "'\n"
            temp_vidlist = temp_vidlist[:-1]  # remove last line break which would cause an error
            f = open('data/temp_vidlist.txt', 'w')
            f.write(temp_vidlist)
            f.close()

            if videolength == 1:
                print("Encoding single video " + str(i))
            if videolength > 1:
                print("Merging " + str(videolength) + " videos " + str(firstvideo_index) + "–" + str(i))

            #encode
            if videolength == 1:
                output_filename = 'output_videos/' + firstvideo_date[:-9] + " at time " + firstvideo_date[11] + firstvideo_date[12] + '.' + firstvideo_date[14] + firstvideo_date[15] + '.mp4'
            if videolength > 1:
                output_filename = 'output_videos/' + firstvideo_date[:-9] + " at time " + firstvideo_date[11] + firstvideo_date[12] + '.' + firstvideo_date[14] + firstvideo_date[15] + ' (merged ' + str(videolength) + ' videos).mp4'
            (
                ffmpeg
                    .input('data/temp_vidlist.txt', format='concat', safe=0)
                    .output(output_filename, c='copy', loglevel='quiet')
                    .overwrite_output()                                                 # todo: find a way to skip instead of overwrite existing files. Question in github waiting for answer atm
                    .run()
            )
            firstvideo = True

        i=i+1  # encoder loop ends

    # todo: print progress one last time to show a full progress bar
    clear_screen()
    input("\nVideo merging complete. ^__^\n\n")


with open('data/mergethreshold.txt') as f:
    lines = f.read()
mergethreshold = int(str(lines))
convert_videos(mergethreshold)