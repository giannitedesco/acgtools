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
	l = len(binary)
	return sum(binary[i] << ((l - i) * 8) for i in range(0, l))
