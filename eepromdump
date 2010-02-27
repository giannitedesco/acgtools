#!/usr/bin/python

import acg

if __name__ == '__main__':
	i = 0
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

		eeprom_fn = "acg-eeprom-%d.bin"%i;
		card.dump_eeprom(eeprom_fn)
		print "Dumped EEPROM: %s"%eeprom_fn
		print
		i = i + 1

