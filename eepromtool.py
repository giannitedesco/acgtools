#!/usr/bin/python

import acg
import sys

def read_eeprom(bin):
	try:
		eeprom = acg.eeprom(bin)
		eeprom.print_info()
	except acg.ACG_Exception, e:
		print e.msg

if __name__ == '__main__':
	for fn in sys.argv[1:]:
		print "reading: %s"%fn
		f = open(fn, 'r')
		bin = f.read()
		f.close()
		read_eeprom(bin)
