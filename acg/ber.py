class Tag:
	def __init__(self, binary):
		bin = binary
		self.idb = bin[0]
		itag = self.idb
		len = 1
		done = False
		if (bin[0] & 0x1f) == 0x1f:
			shift = 8
			for char in bin[1:]:
				itag <<= shift
				itag |= char & 0x7f
				shift = 7
				len += 1
				if not char & 0x80:
					done = True
					break
		else:
			done = True
		if not done:
			raise Exception("Decode Error")

		clsmap = {0:"universal", 1:"application",
			2:"context-specific", 3:"private"}
		self.tag = itag
		self.len = len
		self.cls = (self.idb & 0xc0) >> 6
		self.constructed = (self.idb & 0x20) >> 5
		self.clsname = clsmap[self.cls]

	def __int__(self):
		return self.tag
	def __len__(self):
		return self.len
	def __str__(self):
		return "Tag(%s%s 0x%x)"%(\
			self.constructed and "constructed " or "",
			self.clsname,
			self.tag)
	def __repr__(self):
		return "Tag(0x%x)"%self.tag

class Len:
	def __init__(self, binary):
		bin = binary
		if not bin[0] & 0x80:
			l = bin[0] & 0x7f
			ll = 0
		else:
			ll = bin[0] & 0x7f
			chars = bin[1:ll + 1]
			if len(chars) < ll:
				raise Exception("Decode Error")
			l = 0
			for char in chars:
				l <<= 8
				l |= char
		self.len = l
		self.llen = ll + 1
	def __int__(self):
		return self.len
	def __len__(self):
		return self.llen
	def __str__(self):
		return "Len(%s%u)"%(self.llen == 1 and 's' or 'l', self.len)
	def __repr__(self):
		return "Len(%u)"%self.len

class taglen:
	def __init__(self, bin):
		tag = Tag(bin)
		bin = bin[len(tag):]

		tln = Len(bin)
		bin = bin[len(tln):]

		self.tag = tag
		self.len = tln
	def __len__(self):
		return len(self.tag) + len(self.len)
	def __str__(self):
		return "taglen(%s, %s)"%(self.tag, self.len)
	def __repr__(self):
		return "taglen(%s, %s)"%(self.tag, self.len)

class tlv:
	def pretty_print(self, indent = 0):
		tabs = ''.join("  " for i in range(indent))
		print tabs + ".tag = 0x%x"%int(self.tag)
		print tabs + ".cls = %s"%self.tag.clsname
		print tabs + ".len = %u / 0x%x"%(int(self.len), int(self.len))
		if self.tag.constructed:
			for x in self:
				x.pretty_print(indent + 1)
		
	def __init__(self, binary):
		bin = binary
		tag = Tag(bin)
		bin = bin[len(tag):]

		tln = Len(bin)
		bin = bin[len(tln):]

		self.tag = tag
		self.len = tln

		if len(bin) < int(tln):
			raise Exception("Decode error")

		self.tag = tag
		self.len = tln
		self.val = bin[:int(tln)]
		self.__len = len(self.tag) + len(self.len) + len(self.val)

		self.__items = []
		bin = self.val
		if self.tag.constructed:
			while len(bin):
				item = tlv(bin)
				self.__items.append(item)
				bin = bin[len(item):]

	def __iter__(self):
		return self.__items.__iter__()
	def __getitem__(self, idx):
		return self.__items[idx]
	def __len__(self):
		return self.__len
	def __str__(self):
		return "tlv(%s, %s)"%(self.tag, self.len)
	def __repr__(self):
		return "tlv(%s, %s)"%(self.tag, self.len)
