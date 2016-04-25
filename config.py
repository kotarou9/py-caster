import time

RADIO_FRAME_BUFFER=4096
RADIO_TYPE="mp3"
RADIO_BURST_ON_CONNECT=4096
RADIO_HOST="ani-radio.ga"
RADIO_PORT=7654
RADIO_DIRECTORY="/etc/music/*."
RADIO_PLAYLIST="playlist.lst"
RADIO_USE="d"
RADIO_LISTENERS=32
RADIO_RATE=10000
RADIO_WAIT=1
RADIO_FPS=60
DEBUG=True # prints messages
# see termcolor doc
DEBUG_ERROR_COLOR="red"
DEBUG_ERROR_BG=None
DEBUG_ERROR_ATTR=['bold']
DEBUG_INFO_COLOR="cyan"
DEBUG_INFO_BG=None
DEBUG_INFO_ATTR=['bold']
DEBUG_SONG_CHANGE_COLOR="yellow"
DEBUG_SONG_CHANGE_BG=None
DEBUG_SONG_CHANGE_ATTR=['bold']
DEBUG_TIME_COLOR="blue"
DEBUG_TIME_BG=None
DEBUG_TIME_ATTR=["underline"]
DEBUG_LOGFILE="radio.log"
# add color to logfile note: text editers like nano/vi wont display terminal colors
DEBUG_LOGFILE_COLOR=False
RADIO_HEADERS="HTTP/1.0 200 OK\nDate: %s\nServer: py-caster://v.0.1/22-APR-2016\npc-type: %s\npc-rate: %sms\npc-fps: %i\npc-wait: %ss\npc-max-listeners: %i\npc-frame-buffer: %i\nContent-Type: audio/mpeg\nCache-Control: no-cache, no-store, must-revalidate\nPragma: no-cache\nExpires: 0\n\n" % (time.strftime('%l:%M%p %Z on %b %d, %Y'), RADIO_TYPE, RADIO_RATE, RADIO_FPS, RADIO_WAIT, RADIO_LISTENERS, RADIO_FRAME_BUFFER)

