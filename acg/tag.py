from errors import *
from util import bin2uint,bin2asc
class tag:
	TAG_TYPE_UNKNOWN 	= 0
	TAG_TYPE_ISO_1443A	= 1
	TAG_TYPE_ISO_1443B	= 2

	CASCADE_LEVEL1		= 0
	CASCADE_LEVEL2		= 1
	CASCADE_LEVEL3		= 2

	BAUD_UNKNOWN		= 0
	FRAME_SIZE_UNKNOWN	= 0

	def __init__(self, bin, baud=None, fsz=None):
		if len(bin) == 4:
			self.type = self.TAG_TYPE_UNKNOWN
			self.typename = "unknown"
		elif len(bin) == 12:
			self.type = self.TAG_TYPE_ISO_1443B
			self.typename = "ISO 1443-B"
			a = bin[4:8]
			p = bin[8:11]
			c = bin[11:]
			self.app_data = bin2uint(a)
			self.protocol = bin2uint(p)
			self.cid = bin2uint(c)
			bin = bin[:4]
			print ext
		elif len(bin) in [5, 8, 11]:
			self.type = self.TAG_TYPE_ISO_1443A
			self.typename = "ISO 1443-A"
			self.cascade = bin[0]
			self.ats = None
			bin = bin[1:]
		else:
			self.type = self.TAG_TYPE_ISO_1443A
			self.typename = "ISO 1443-A"
			self.cascade = bin[0]
			bin = bin[1:]

			uid_len = 0
			for x in [4, 7, 10]:
				if x + bin[x] == len(bin):
					uid_len = x
					break
			if not uid_len:
				raise ACG_BadTag(bin,
					"Unexpected length: %u"%len(bin))
			else:
				self.ats = bin[uid_len:]
				bin = bin[:uid_len]

		self.serial_len = len(bin)
		self.serial = bin2uint(bin)
		self.serial_str = bin2asc(bin)
		self.baud = baud and baud or self.BAUD_UNKNOWN
		self.frame_size = fsz and fsz or self.FRAME_SIZE_UNKNOWN

	def __str__(self):
		return "tag(0x%x)"%self.serial
	def __cmp__(a, b):
		return a.serial - b.serial
