#!/usr/bin/python

import acg

def do_device(card):
	eeprom_fn = "acg-eeprom.bin";
	#card.dump_eeprom(eeprom_fn)
	#print "Dumped EEPROM: %s"%eeprom_fn
	#print "Flashing EEPROM: %s"%eeprom_fn
	#card.flash_eeprom(eeprom_fn)

	try:
		uid = card.select()
		print "found tag with ID %s"%uid
	except acg.ACG_Exception, e:
		print e.msg
		raise SystemExit
	
	for rec in range(0, 0x40):
		for k in [0xaa, 0xbb, 0xff]:
			try:
				card.select()
			except acg.ACG_NoTagInField:
				print "Card went away"
				raise SystemExit
			try:
				ret = card.mifare_login(rec, k)
			except acg.ACG_Exception, e:
				ret = False
			if not ret:
				continue
			try:
				data = card.mifare_readblock(rec)
			except:
				data = "NO DATA"
			print "transport key rec 0x%.2x (%.2X): %s"%(
					rec, k, data)
if __name__ == '__main__':
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

		do_device(card)

