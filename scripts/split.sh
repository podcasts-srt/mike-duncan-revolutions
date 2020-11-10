# https://unix.stackexchange.com/questions/280767/how-do-i-split-an-audio-file-into-multiple
ffmpeg -i 021-_The_Gun_of_Ticonderoga.mp3 -f segment -segment_time 1795 -c copy out%03d.mp3
