def asc2bin(ascii):
	"Convert ASCII to bytestring"
	arr = []
	while len(ascii) >= 2:
		arr.append(chr(int(ascii[:2], 16)))
		ascii = ascii[2:]
	assert(len(ascii)==0)
	return bytearray(arr)

def bin2asc(binary):
	"Convert bytestring to ASCII"
	return "".join(map(lambda x:"%.2x"%x, binary))

def bin2uint(binary):
	"Convert big-endian binary integer to python integer"
	return int("".join(map(lambda x:"%.2x"%x,binary)), 16)

def uint2bin(uint, bytes=4):
	"Convert python integer to a big endian binary encoding"
	bin = bytearray()
	r = range(0, bytes << 3, 8)
	r.reverse()
	for i in r:
		cur = (uint >> i) & 0xff
		bin.append(chr(cur))
	return bin

def print_tag(tag):
	print "Found %s tag with serial 0x%s"%(tag.typename, tag.serial_str)
	if tag.iso1443a:
		clevel = {
				tag.CASCADE_LEVEL1: 1,
				tag.CASCADE_LEVEL2: 2,
				tag.CASCADE_LEVEL3: 3,
			}
		if clevel.has_key(tag.cascade):
			print "  Cascade level %u"%clevel[tag.cascade]
		if tag.reqa != None:
			print "  REQA response: %s"%bin2asc(tag.reqa)
		if tag.rats != None:
			print "  RATS: %s"%bin2asc(tag.rats)
	if tag.iso1443b:
		pass
	if tag.baud != None or tag.frame_size != None:
		print "  Baud rate %uk, frame size %u bytes"%(
			tag.baud and tag.baud or "UNKNOWN",
			tag.frame_size and tag.frame_size or "UNKNOWN")

