# This file is part of actools
# Copyright (c) 2010 Gianni Tedesco
# This is free software released under the terms of the GNU GPL v3
import os
class RFIDDevice:
	def __init__(self, fn, lineno, tty, baud = None):
		self.vendor_id = None
		self.product_id = None
		self.vendor = None
		self.product = None
		self.udi = None
		self.vendor = None
		self.product = None

		self.id = "%s:%u"%(fn, lineno)
		if baud == None:
			self.suggested_baud = 460800
		else:
			self.suggested_baud = baud
		self.tty = tty

def __cb_add(sysbus, id):
	try:
		return RFIDDevice(sysbus, id)
	except NotRFID:
		return None

def get_devlist():
	cfn = os.path.join(os.environ["HOME"], ".acgtools")
	f = open(cfn, 'r')
	lines = f.readlines()
	del f

	lines = map(lambda x:x.rstrip("\r\n"), lines)

	ret = []
	i = 0
	for x in lines:
		i += 1
		if not len(x):
			continue
		if x[0] == '#':
			continue
		args = x.split(None, 1)
		tty = args[0]
		if len(args) > 1:
			baud = int(args[1])
		else:
			baud = None

		ret.append(RFIDDevice(cfn, i, tty, baud))
	return ret
		
