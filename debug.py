from termcolor import colored
import config, time
def log(msg):
	try:
		f=open(config.DEBUG_LOGFILE, 'r')
		l=f.read()
		f.close()
		msg = l + msg
		f=open(config.DEBUG_LOGFILE, "w")
		f.write(msg + '\n')
		f.close()
	except:
		f=open(config.DEBUG_LOGFILE, "w")
                f.write(msg + '\n')
                f.close()

def Print(mode, text):
	mode = mode.lower()
	if config.DEBUG:
		tstr = "%s" % time.strftime('%l:%M:%S%p on %b %d, %Y')
		tcstr = colored(tstr, config.DEBUG_TIME_COLOR, config.DEBUG_TIME_BG, attrs=config.DEBUG_TIME_ATTR)
		msg = "%s - " % tcstr
		ncmsg = "%s - " % tstr
		if mode == "info":
			ncmsg += text
			msg += colored(text, config.DEBUG_INFO_COLOR, config.DEBUG_INFO_BG, attrs=config.DEBUG_INFO_ATTR) 
		elif mode == "error":
			text = "ERROR - "
			ncmsg += text
			msg += colored(text, config.DEBUG_ERROR_COLOR, config.DEBUG_ERROR_BG, attrs=config.DEBUG_ERROR_ATTR) 
		elif mode == "sc":
			ncmsg += text
			msg += colored(text, config.DEBUG_SONG_CHANGE_COLOR, config.DEBUG_CHANGE_SONG_BG, attrs=config.DEBUG_SONG_CHANGE_ATTR)
		if config.DEBUG_LOGFILE_COLOR: log(msg)
		else: log(ncmsg)
		print(msg)
