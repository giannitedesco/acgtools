from errors import ACG_EEPROM_Error, ACG_EEPROM_ValueError

EEPROM_BYTES 		= 0xf0

PCON1_AUTO_START	= (1<<0)
PCON1_PROTOCOL		= (1<<1)
PCON1_MULTITAG		= (1<<2)
PCON1_NEW_SERIAL_MODE	= (1<<3)
PCON1_LED		= (1<<4)
PCON1_SINGLE_SHOT	= (1<<5)
PCON1_EXT_PROTOCOL	= (1<<6)
PCON1_EXT_ID		= (1<<7)

OPMODE_1443A		= (1<<0)
OPMODE_1443B		= (1<<1)
OPMODE_SR176		= (1<<2)
OPMODE_ICODE		= (1<<3)
OPMODE_15693		= (1<<4)
OPMODE_ICODE_EPC	= (1<<5)
OPMODE_ICODE_UID	= (1<<6)

baud_rates = [9600, 19200, 38400, 57600, 115200, 230400, 460800, -1]

class eeprom:
	def __init__(self, eeprom):
		if len(eeprom) != EEPROM_BYTES:
			raise ACG_EEPROM_Error("expected %u bytes, got %u"%(
					len(eeprom), EEPROM_BYTES))
		self.__bin = bytearray(eeprom)
		return
	
	def binary(self):
		return self.__bin
	
	def get_dev_id(self):
		return int("".join(map(lambda x:"%.2x"%x,
					self.__bin[0:4])), 16)
	def set_dev_id(self, dev_id):
		raise ACG_EEPROM_ValueError("Device ID is read-only")

	def get_admin_data(self):
		return int("".join(map(lambda x:"%.2x"%x,
					self.__bin[4:8])), 16)
	def set_admin_data(self, dev_id):
		raise ACG_EEPROM_ValueError("Admin data is read-only")
	
	def get_station_id(self):
		return self.__bin[0x0a]
	def set_station_id(self, s_id):
		x = int(s_id)
		if x < 0 or x > 0xff:
			raise ACG_EEPROM_ValueError()
		self.__bin[0x0a] = chr(s_id)
	
	def get_baud_rate(self):
		baud = self.__bin[0x0c] & 7
		return baud_rates[baud]
	def set_baud_rate(self, rate):
		if rate < 0 or not rate in baud_rates:
			raise ACG_EEPROM_ValueError()
		self.__bin[0x0c] = chr(baud_rates.index(rate))

	def get_guard(self):
		return (37.8 * float(self.__bin[0xd])) / 1000.0
	def set_guard(self, guard):
		try:
			g = float(guard)
		except:
			raise ACG_EEPROM_ValueError()
		guard = int(round((g * 1000.0) / 37.8))
		self.__bin[0xd] = guard

	def print_info(self):
		print "Device ID:  0x%.8x"%self.get_dev_id()
		print "Admin Data: 0x%.8x"%self.get_admin_data()
		print "Station ID: 0x%.2x"%self.get_station_id()
		print "Baud rate:  %i"%self.get_baud_rate()
		print "Guard time: %.3f ms"%self.get_guard()

		pcon1 = self.__bin[0x0b]
		if pcon1 & PCON1_AUTO_START:
			print "PCON1:  AUTO_START"
		else:
			print "PCON1:  NO AUTO_START"
		if pcon1 & PCON1_PROTOCOL:
			print "PCON1:  PROTOCOL: BINARY"
		else:
			print "PCON1:  PROTOCOL: ASCII"
		if pcon1 & PCON1_MULTITAG:
			print "PCON1:  MULTI_TAG"
		else:
			print "PCON1:  SINGLE_TAG"
		if pcon1 & PCON1_NEW_SERIAL_MODE:
			print "PCON1:  NEW_SERIAL_MODE"
		else:
			print "PCON1:  OLD_SERIAL_MODE"
		if pcon1 & PCON1_LED:
			print "PCON1:  AUTOMATIC LED"
		else:
			print "PCON1:  PROGRAMMED LED"
		if pcon1 & PCON1_SINGLE_SHOT:
			print "PCON1:  SINGLE_SHOT MODE"
		else:
			print "PCON1:  NO SINGLE_SHOT MODE"
		if pcon1 & PCON1_EXT_PROTOCOL:
			print "PCON1:  EXTENDED PROTOCOL (ISO14443-4 WTX + CHAIN)"
		else:
			print "PCON1:  NO EXTENDED PROTOCOL"
		if pcon1 & PCON1_EXT_ID:
			print "PCON1:  EXTENDED ID"
		else:
			print "PCON1:  NO EXTENDED ID"

		opmode = self.__bin[0x0e]
		if opmode & OPMODE_1443A:
			print "OPMODE: ISO 1443-A"
		if opmode & OPMODE_1443B:
			print "OPMODE: ISO 1443-B"
		if opmode & OPMODE_SR176:
			print "OPMODE: SR176"
		if opmode & OPMODE_ICODE:
			print "OPMODE: ICODE"
		if opmode & OPMODE_15693:
			print "OPMODE: ISO 15693"
		if opmode & OPMODE_ICODE_EPC:
			print "OPMODE: ICODE EPC"
		if opmode & OPMODE_ICODE_UID:
			print "OPMODE: ICODE UID"
