#!/usr/bin/python

import acg, sys

if __name__ == '__main__':
	eeprom_fn = sys.argv[1]
	for dev in acg.get_devlist():
		print dev.vendor
		print dev.product
		print "%s @ %u baud"%(dev.tty, dev.suggested_baud)
		try:
			card = acg.acg(line=dev.tty,
					baud = dev.suggested_baud,
					tracefile="acgtool.trace")
		except acg.ACG_Exception, e:
			print "ERROR: %s"%e.msg
			print
			continue

		print "Flash device with EEPROM %s? [y/N]"%eeprom_fn
		x = raw_input()
		if not len(x):
			continue
		if x[0] == 'y' or x[0] =='Y':
			print "Flashing EEPROM..."
			card.flash_eeprom(eeprom_fn)
			print "OK"
		print
