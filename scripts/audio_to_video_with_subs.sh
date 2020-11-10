# https://superuser.com/questions/1041816/combine-one-image-one-audio-file-to-make-one-video-using-ffmpeg

ffmpeg -loop 1 -i black_1280x720.png -i 021-_The_Gun_of_Ticonderoga.mp3 -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest out.mp4

# https://stackoverflow.com/questions/21363334/how-to-add-font-size-in-subtitles-in-ffmpeg-video-filter

ffmpeg -i out.mp4 -vf subtitles="021-_The_Gun_of_Ticonderoga.mp3.srt:force_style='Fontsize=30'" out_with_subs.mp4
