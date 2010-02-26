#!/usr/bin/python

import acg

if __name__ == '__main__':
	try:
		card = acg.acg(line="/dev/ttyUSB1", tracefile="acgtool.trace")
	except acg.ACG_Exception, e:
		print e.msg

	eeprom_fn = "acg-eeprom.bin";
	card.dump_eeprom(eeprom_fn)
	print "Dumped EEPROM: %s"%eeprom_fn

	try:
		uid = card.select()
		print "found tag with ID %s"%uid
	except acg.ACG_Exception, e:
		print e.msg
