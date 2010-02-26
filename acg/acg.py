from errors import *
from serio import serio

class acg:
	def __init__(self, line="/dev/ttyUSB0", baud=460800, tracefile=None):
		self.__serio = serio(line, baud, tracefile)
	def select(self):
		self.__serio.tx("s")
		uid = self.__serio.rx()
		print uid
