#!/usr/bin/python

import acg

if __name__ == '__main__':
	try:
		card = acg.acg(line="/dev/ttyUSB1", tracefile="acgtool.trace")
	except acg.ACG_Exception, e:
		print e.msg

	#eeprom_fn = "acg-eeprom.bin";
	#card.dump_eeprom(eeprom_fn)
	#print "Dumped EEPROM: %s"%eeprom_fn

	try:
		uid = card.select()
		print "found tag with ID %s"%uid
	except acg.ACG_Exception, e:
		print e.msg
	
	for rec in range(0, 0x40):
		for k in [0xaa, 0xbb, 0xff]:
			card.select()
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
