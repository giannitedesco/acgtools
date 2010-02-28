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
	bin = bytearray()
	r = range(0, bytes << 3, 8)
	r.reverse()
	for i in r:
		cur = (uint >> i) & 0xff
		bin.append(chr(cur))
	return bin
