from threading import Thread as thread
from debug import Print
import config
class Thread(thread):
	def __init__(self):
		thread.__init__(self)

	def MakeThread(self, mgr):
		self.mgr = mgr
		self.running = 1

	def run(self):
		while self.running:
			buf = self.mgr.file.read(config.RADIO_FRAME_BUFFER)
			if len(buf) == 0:
				self.running = 0
				break
			self.mgr.frames.append(buf)
