# This file is part of actools
# Copyright (c) 2010 Gianni Tedesco
# This is free software released under the terms of the GNU GPL v3
from errors import *
from util import bin2uint,bin2asc

class tag:
	def __init__(self, id):
		self.serial = id
		self.serial_str = bin2asc(id)
		self.baud = None
		self.frame_size = None
		self.typename = "UNKNOWN"
		self.iso1443a = False
		self.iso1443b = False
	def set_hispeed(self, baud, frame_size):
		self.baud = baud
		self.frame_size = frame_size
	def __cmp__(a, b):
		if None == b:
			return 1
		return bin2uint(a.serial) - bin2uint(b.serial)
	
class iso1443a(tag):
	CASCADE_LEVEL1		= 0
	CASCADE_LEVEL2		= 1
	CASCADE_LEVEL3		= 2
	def  __init__(self, id, cascade=None, reqa=None):
		assert(len(id) in [4, 7, 10])
		tag.__init__(self, id)
		self.typename = "ISO 1443-A"
		self.iso1443a = True
		self.cascade = cascade
		self.reqa = reqa
		self.rats = None
	def set_rats(self, rats):
		self.rats = rats

class iso1443b(tag):
	def __init__(self, id, app=None, protocol=None, cid=None):
		assert(len(id) == 12)
		tag.__init__(self, id)

		self.typename = "ISO 1443-B"
		self.iso1443b = True

		if app:
			assert(len(app) == 4)
		if protocol:
			assert(len(protocol) == 3)
		if cid:
			assert(len(cid) == 1)

		self.app = app
		self.protocol = protocol
		self.cid = cid
		
