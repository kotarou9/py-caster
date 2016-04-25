from glob import glob
from mutagen.mp3 import MP3
files=glob("/etc/music/*.mp3")
file=files[0]
mp3 = MP3(file)
print(mp3.info.bitrate/1000)
