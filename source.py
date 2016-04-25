import select, time, config, glob, socket, traceback, sys
from FrameThread import Thread
from debug import Print
from random import shuffle

class Stream(object):
	def __init__(self):
		self.count = 3
		self.songs = self.getSongs()
		self.file = open(self.songs[self.count], 'rb')
		self.running = False
		self.frames = []
		self.buf = None
		self.wait = False
		self.nbuf = None
		self.listeners = 0
		self.socket = socket.socket()
		self.connections = list()
		self.total = 0
		self.st = 0
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.bind()
		self.cf = 0
		self.do_next = False
		self.par = {}
		self.connection = None

	def setDefaults(self, con):
		self.par[con] = {}
		self.par[con]['fps'] = config.RADIO_FPS
		self.par[con]['remove'] = False


	def addFps(self, n=1):
		self.par[self.connection]['fps'] += n
	

        def minusFps(self, n=1):
                self.par[self.connection]['fps'] -= n

	def remove(self):
		self.par[self.connection]['remove'] = True

	def _remove(self):
		if self.par[self.connection]['remove']:
			del self.par[self.connection]

	def bind(self):
		self.socket.bind((config.RADIO_HOST, config.RADIO_PORT))
		self.socket.listen(config.RADIO_LISTENERS)
		

	def getSongs(self):
		return glob.glob(config.RADIO_DIRECTORY + config.RADIO_TYPE)

	def makeFrames(self):
		while True:
			frame = self.file.read(config.RADIO_FRAME_BUFFER)
			if len(frame) == 0:
				break
			else:
				self.frames.append(frame)

	def blankFrame(self, bytes=None):
		f=open("a-bin/blank.mp3", "rb")
		if bytes == None: binary=f.read()
		else: binary=f.read(int(bytes))
		f.close()
		return binary

	def getFrame(self):
		try: return self.frames[0]
		except: return None

	def new(self):
		self.frames = list()
		self.makeFrames()
		self.st = time.time()
		self.total = 0

	def removeFrame(self):
		frame = self.getFrame()
		if frame != None: 
			self.frames.remove(frame)
			return True
		else:
			return False

	def next(self):
		c=self.count - 1
		if c>=len(self.songs): self.count = 0
		else: self.count += 1
		self.file = open(self.songs[self.count], 'rb')
		self.new()
		self.wait = False
		Print("sc", "[SONG_CHANGE][SONG==%s]" % (self.songs[self.count]))

	def main(self):
		sec = 0
		mili = 0
		w_mili = 0
		self.makeFrames()
		Print("info", "[settings][FRAMES==%i][MAX_LISTENERS==%s][FPS==%i][SONGS==%i][URL==http://%s:%i/<any>.%s]" % (len(self.frames), config.RADIO_LISTENERS, config.RADIO_FPS, len(self.getSongs()), config.RADIO_HOST, config.RADIO_PORT, config.RADIO_TYPE))
		self.running = True
		self.nbuf = self.getFrame()
		self.st = time.time()
		self.connections.append(self.socket)
		while self.running:
			try:
				self.buf = self.nbuf
				self.nbuf = self.getFrame()
				if self.buf != None:
					self.total += len(self.buf)
				elif self.buf == None:
					if self.do_next:
						et = time.time()
						br = self.total*0.008/(et-self.st)
						Print("info", "Sent %d bytes in %d seconds (%fkbps)" % (self.total, et-self.st, br))
						self.next()
	
				rl, wl, xl = select.select(self.connections, [], [], 0)
            			for sock in rl:
                			if sock == self.socket:
                    				con, ip = self.socket.accept()
                    				con.send(config.RADIO_HEADERS)
						self.setDefaults(con)
						self.listeners += 1
                    				self.connections.append(con)
                			else:
                    
                    				try:
							self.connection = sock
                        				if self.buf != None:
								# send buf/frame until None
								if not self.wait: 
									if len(self.frames) != 0:
										sock.send(self.buf)
										self.cf += 1
										self.wait = True
                            
                    				except:
                        				self.connections.remove(sock)
							self.listeners -= 1
							self.remove()
				mili +=1
				if mili == 10000:
					sec = 1
					mili = 0
				if len(self.frames) != 0:
                        		if self.do_next:
                                		self.do_next = False
                                        	self.wait = True
                        	else:
                                        self.do_next = True
                                        self.wait = True
				# did some research and fps did needed to be added
				w_mili += 1
				if sec == 1:
					if self.cf == self.par[self.connection]['fps']:
						Print("info", "%i frames pausing for %s seconds" % (config.RADIO_FPS, config.RADIO_WAIT))
						self.cf = 0
						sec=0
						time.sleep(config.RADIO_WAIT)
						Print("info", "resuming stream")
					elif self.cf > self.par[self.connection]['fps']:
						fb = config.RADIO_FPS - self.cf
						Print('info', "frame ahead frames %i" % fb)
						#self.minusFps(2)
						sec=0
					elif self.cf < self.par[self.connection]['fps']:
						if self.listeners > 0:
							fb = config.RADIO_FPS - self.cf
							#self.addFps(2)
							Print("info", "%i frames behind" % fb)
							sec=0
				if w_mili == self.par[self.connection]['rate']:
					w_mili = 0
					self.removeFrame()
					self.wait = False

				self._remove()

			except Exception as e:
                                e= e
                        except KeyboardInterrupt, err:
                                e=traceback.format_exc()
                                Print('error', "KeyboardInterrupt detected")
                                break

if __name__=="__main__":
	strm = Stream()
	strm.main()
