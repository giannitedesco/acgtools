# This file is part of actools
# Copyright (c) 2010 Gianni Tedesco
# This is free software released under the terms of the GNU GPL v3
import dbus, gobject
from dbus.mainloop.glib import DBusGMainLoop

class NotRFID(Exception):
	def __init__(self):
		Exception.__init__(self)

class RFIDDevice:
	def __init__(self, sys, id):
		proxy = sys.get_object('org.freedesktop.Hal', '%s'%id)
		devtable = {
			(0x0403, 0xdd20) : 460800,
		}

		try:
			subsys = proxy.GetProperty("info.subsystem",
				dbus_interface="org.freedesktop.Hal.Device")
			assert(subsys == "tty")
		except:
			raise NotRFID

		self.tty = proxy.GetProperty("serial.device",
				dbus_interface="org.freedesktop.Hal.Device")
		self.udi = proxy.GetProperty("serial.originating_device",
				dbus_interface="org.freedesktop.Hal.Device")

		proxy = sys.get_object('org.freedesktop.Hal', '%s'%self.udi)
		try:
			subsys = proxy.GetProperty("info.subsystem",
				dbus_interface="org.freedesktop.Hal.Device")
			assert(subsys == "usb")
		except:
			raise NotRFID

		vendor_id = proxy.GetProperty("usb.vendor_id",
			dbus_interface="org.freedesktop.Hal.Device")
		product_id = proxy.GetProperty("usb.product_id",
			dbus_interface="org.freedesktop.Hal.Device")

		if not devtable.has_key((vendor_id, product_id)):
			raise NotRFID

		self.suggested_baud = devtable[(vendor_id, product_id)]

		self.vendor_id = vendor_id
		self.product_id = product_id
		self.vendor = proxy.GetProperty("usb.vendor",
				dbus_interface="org.freedesktop.Hal.Device")
		self.product = proxy.GetProperty("usb.product",
				dbus_interface="org.freedesktop.Hal.Device")
		self.id = id

		self.tty = str(self.tty)
		self.vendor = str(self.vendor)
		self.product = str(self.product)
	def __str__(self):
		return self.tty

def __cb_add(sysbus, id):
	try:
		return RFIDDevice(sysbus, id)
	except NotRFID:
		return None

def __prime_devlist(sysbus):
	ret = {}
	proxy = sysbus.get_object('org.freedesktop.Hal',
					"/org/freedesktop/Hal/Manager")
	devs = proxy.GetAllDevices(
			dbus_interface="org.freedesktop.Hal.Manager")
	for x in devs:
		d = __cb_add(sysbus, x)
		if not d:
			continue
		ret[x] = d
	return ret

def get_devlist():
	ml = DBusGMainLoop(set_as_default=True)
	sys = dbus.SystemBus(mainloop=ml)
	return __prime_devlist(sys).values()
