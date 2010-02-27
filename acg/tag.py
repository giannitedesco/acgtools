from errors import *
class tag:
	TAG_TYPE_UNKNOWN 	= 0
	TAG_TYPE_ISO_1443A	= 1
	TAG_TYPE_ISO_1443B	= 2

	CASCADE_LEVEL1	= 0
	CASCADE_LEVEL2	= 1
	CASCADE_LEVEL3	= 2

	def __init__(self, bin):
		if len(bin) == 4:
			self.type = self.TAG_TYPE_UNKNOWN
			self.typename = "unknown"
		elif len(bin) in [5, 8, 11]:
			self.type = self.TAG_TYPE_ISO_1443A
			self.typename = "ISO 1443-A"
			self.cascade = bin[0]
			bin = bin[1:]
		elif len(bin) == 12:
			self.type = self.TAG_TYPE_ISO_1443B
			self.typename = "ISO 1443-B"
			ext = bin[4:]
			bin = bin[:4]
			print ext
		else:
			raise ACG_BadTag(bin, "Unexpected length: %u"%len(bin))

		slen = len(bin) - 1
		self.serial = sum(bin[i] << ((slen - i) * 8) \
					for i in range(slen, -1, -1))
	def __str__(self):
		return "tag(0x%x)"%self.serial
