#!/usr/bin/python

import acg

if __name__ == '__main__':
	card = acg.acg(line="/dev/ttyUSB1", tracefile="acgtool.trace")

	eeprom_fn = "acg-eeprom.bin";
	card.dump_eeprom(eeprom_fn)
	print "Dumped EEPROM: %s"%eeprom_fn

	try:
		uid = card.select()
		print "found tag with ID %s"%uid
	except acg.ACGNoTagInField:
		print "no tag in field"
