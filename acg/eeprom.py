from errors import ACG_EEPROM_Error, ACG_EEPROM_ValueError

EEPROM_BYTES 		= 0xf0
EEPROM_READONLY		= 0x0a

PCON1_AUTO_START	= (1<<0)
PCON1_PROTOCOL		= (1<<1)
PCON1_MULTITAG		= (1<<2)
PCON1_NEW_SERIAL_MODE	= (1<<3)
PCON1_LED		= (1<<4)
PCON1_SINGLE_SHOT	= (1<<5)
PCON1_EXT_PROTOCOL	= (1<<6)
PCON1_EXT_ID		= (1<<7)

PCON2_MULTITAG_RESET	= (1<<0)
PCON2_STARTUP_MSG	= (1<<1)
PCON2_BINARY_FRAME2	= (1<<2)
PCON2_NOISY_ENV		= (1<<3)
PCON2_ANTI_COLLISION	= (1<<6)
PCON2_ERR_HANDLING	= (1<<7)

PCON3_AUTO_TIMEOUT	= (1<<0)
PCON3_PAGE_READ		= (1<<2)
PCON3_EXT_REQA		= (1<<6)

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
		return str(self.__bin)
	
	def get_dev_id(self):
		"Device ID"
		return int("".join(map(lambda x:"%.2x"%x,
					self.__bin[0:4])), 16)
	def set_dev_id(self, dev_id):
		"Device ID"
		raise ACG_EEPROM_ValueError("Device ID is read-only")

	def get_admin_data(self):
		"Admin data"
		return int("".join(map(lambda x:"%.2x"%x,
					self.__bin[4:8])), 16)
	def set_admin_data(self, dev_id):
		"Admin data"
		raise ACG_EEPROM_ValueError("Admin data is read-only")

	def __set_byte(self, ofs, byte):
		x = int(byte)
		if x < 0 or x > 0xff:
			raise ACG_EEPROM_ValueError("Byte out of range")
		self.__bin[ofs] = byte

	def get_station_id(self):
		"Station ID"
		return self.__bin[0x0a]
	def set_station_id(self, s_id):
		"Station ID"
		self.__set_byte(0x0a, s_id)
	
	def get_baud_rate(self):
		"Baud Rate"
		baud = self.__bin[0x0c] & 7
		return baud_rates[baud]
	def set_baud_rate(self, rate):
		"Baud Rate"
		if rate < 0 or not rate in baud_rates:
			raise ACG_EEPROM_ValueError("Invalid baud rate")
		self.__bin[0x0c] = chr(baud_rates.index(rate))

	def get_guard(self):
		"Guart tome (ms)"
		return (37.8 * float(self.__bin[0xd])) / 1000.0
	def set_guard(self, guard):
		"Guart tome (ms)"
		try:
			g = float(guard)
		except:
			raise ACG_EEPROM_ValueError("Invalid guard time")
		guard = int(round((g * 1000.0) / 37.8))
		self.__bin[0xd] = guard

	def __get_bit(self, byte, bit):
		return bool(self.__bin[byte] & bit)
	def __set_bit(self, byte, bit, b):
		try:
			set = bool(b)
		except:
			raise ACG_EEPROM_ValueError("Value out of range")
		if set:
			self.__bin[byte] |= bit
		else:
			self.__bin[byte] &= (~bit) & 0xff

	def get_auto_start(self):
		"Auto start"
		return self.__get_bit(0x0b, PCON1_AUTO_START)
	def set_auto_start(self, bit):
		"Auto start"
		self.__set_bit(0xb, PCON1_AUTO_START, bit)

	def get_binary(self):
		"Binary protocol"
		return self.__get_bit(0x0b, PCON1_PROTOCOL)
	def set_binary(self, bit):
		"Binary protocol"
		self.__set_bit(0xb, PCON1_PROTOCOL, bit)

	def get_multitag(self):
		"Multitag"
		return self.__get_bit(0x0b, PCON1_MULTITAG)
	def set_multitag(self, bit):
		"Multitag"
		self.__set_bit(0xb, PCON1_MULTITAG, bit)

	def get_new_serial_mode(self):
		"New serial mode"
		return self.__get_bit(0x0b, PCON1_NEW_SERIAL_MODE)
	def set_new_serial_mode(self, bit):
		"New serial mode"
		self.__set_bit(0xb, PCON1_NEW_SERIAL_MODE, bit)

	def get_program_led(self):
		"Programmed LEDs"
		return self.__get_bit(0x0b, PCON1_LED)
	def set_program_led(self, bit):
		"Programmed LEDs"
		self.__set_bit(0xb, PCON1_LED, bit)

	def get_single_shot(self):
		"Single shot mode"
		return self.__get_bit(0x0b, PCON1_SINGLE_SHOT)
	def set_single_shot(self, bit):
		"Single shot mode"
		self.__set_bit(0xb, PCON1_SINGLE_SHOT, bit)

	def get_ext_protocol(self):
		"Ext. protocol"
		return self.__get_bit(0x0b, PCON1_EXT_PROTOCOL)
	def set_ext_protocol(self, bit):
		"Ext. protocol"
		self.__set_bit(0xb, PCON1_EXT_PROTOCOL, bit)

	def get_ext_id(self):
		"Ext. ID's"
		return self.__get_bit(0x0b, PCON1_EXT_ID)
	def set_ext_id(self, bit):
		"Ext. ID's"
		self.__set_bit(0xb, PCON1_EXT_ID, bit)

	def get_op_1443a(self):
		"op: ISO 1443-A"
		return self.__get_bit(0x0e, OPMODE_1443A)
	def set_op_1443a(self, bit):
		"op: ISO 1443-A"
		self.__set_bit(0xe, OPMODE_1443A, bit)

	def get_op_1443b(self):
		"op: ISO 1443-B"
		return self.__get_bit(0x0e, OPMODE_1443B)
	def set_op_1443b(self, bit):
		"op: ISO 1443-B"
		self.__set_bit(0xe, OPMODE_1443B, bit)

	def get_op_sr176(self):
		"op: SR-176"
		return self.__get_bit(0x0e, OPMODE_SR176)
	def set_op_sr176(self, bit):
		"op: SR-176"
		self.__set_bit(0xe, OPMODE_SR176, bit)

	def get_op_icode(self):
		"op: ICODE"
		return self.__get_bit(0x0e, OPMODE_ICODE)
	def set_op_icode(self, bit):
		"op: ICODE"
		self.__set_bit(0xe, OPMODE_ICODE, bit)

	def get_op_15693(self):
		"op: ISO 15693"
		return self.__get_bit(0x0e, OPMODE_15693)
	def set_op_15693(self, bit):
		"op: ISO 15693"
		self.__set_bit(0xe, OPMODE_15693, bit)

	def get_op_icode_epc(self):
		"op: ICODE-EPC"
		return self.__get_bit(0x0e, OPMODE_ICODE_EPC)
	def set_op_icode_epc(self, bit):
		"op: ICODE-EPC"
		self.__set_bit(0xe, OPMODE_ICODE_EPC, bit)

	def get_op_icode_uid(self):
		"op: ICODE-UID"
		return self.__get_bit(0x0e, OPMODE_ICODE_UID)
	def set_op_icode_uid(self, bit):
		"op: ICODE-UID"
		self.__set_bit(0xe, OPMODE_ICODE_UID, bit)
	
	def get_single_shot_tmo(self):
		"Single shot (ms)"
		return self.__bin[0x0f] * 100
	def set_single_shot_tmo(self, ms):
		"Single shot (ms)"
		try:
			val = int(ms)
		except ValueErrror:
			raise ACG_EEPROM_ValueError("Timeout not integer")
		self.__bin[0x0f] = val / 100

	def get_multitag_reset(self):
		"Multitag reset"
		return not self.__get_bit(0x13, PCON2_MULTITAG_RESET)
	def set_multitag_reset(self, bit):
		"Multitag reset"
		self.__set_bit(0x13, PCON2_MULTITAG_RESET, not bit)

	def get_startup_msg(self):
		"Startup message"
		return not self.__get_bit(0x13, PCON2_STARTUP_MSG)
	def set_startup_msg(self, bit):
		"Startup message"
		self.__set_bit(0x13, PCON2_STARTUP_MSG, not bit)

	def get_binary_frame2(self):
		"Binary frames v2"
		return self.__get_bit(0x13, PCON2_BINARY_FRAME2)
	def set_binary_frame2(self, bit):
		"Binary frames v2"
		self.__set_bit(0x13, PCON2_BINARY_FRAME2, bit)

	def get_noisy_env(self):
		"Noisy environment"
		return self.__get_bit(0x13, PCON2_NOISY_ENV)
	def set_noisy_env(self, bit):
		"Noisy environment"
		self.__set_bit(0x13, PCON2_NOISY_ENV, bit)

	def get_anti_collision(self):
		"ISO Anti-collision"
		return self.__get_bit(0x13, PCON2_ANTI_COLLISION)
	def set_anti_collision(self, bit):
		"ISO Anti-collision"
		self.__set_bit(0x13, PCON2_ANTI_COLLISION, bit)

	def get_err_handling(self):
		"ISO Err handling"
		return not self.__get_bit(0x13, PCON2_ERR_HANDLING)
	def set_err_handling(self, bit):
		"ISO Err handling"
		self.__set_bit(0x13, PCON2_ERR_HANDLING, not bit)

	def get_reset_time(self):
		"Reset time (ms)"
		return self.__bin[0x14]
	def set_reset_time(self, ms):
		"Reset time (ms)"
		self.__set_byte(0x14, ms)

	def get_recover_time(self):
		"Recover time (ms)"
		val = self.__bin[0x15] 
		pcon2 = self.__bin[0x13]
		mult = (pcon2 & ((1<<4)|(1<<5))) >> 4
		return val * mult
	def set_recover_time(self, ms):
		"Recover time (ms)"
		mult = ms >> 8
		if mult > 3:
			raise ACG_EEPROM_ValueError("Recover time out of range")
		if mult:
			d = {}
			for m in [1, 2, 3]:
				if ms / m > 0xff:
					continue
				d[ms % m] = m
			keys = d.keys()
			keys.sort()
			try:
				mult = d[keys[0]]
			except:
				raise ACG_EEPROM_ValueError( \
						"Recover time out of range")
			val = int(round(float(ms) / float(mult)))
		else:
			val = ms
		self.__set_byte(0x15, val)
		pcon2 = self.__bin[0x13]
		pcon2 &= ~((1<<4)|(1<<5)) & 0xff
		pcon2 |= mult << 4
		self.__set_byte(0x13, pcon2)

	def get_afi(self):
		"AFI"
		return self.__bin[0x16]
	def set_afi(self, ms):
		"AFI"
		self.__set_byte(0x16, ms)

	def __get_timeslice(self, ofs):
		return float(self.__bin[ofs]) * 0.3
	def __set_timeslice(self, ofs, val):
		try:
			f = float(val)
		except ValueError:
			raise ACG_EEPROM_ValueError("Bad timeslice count")
		self.__set_byte(ofs, int(round(f / 0.3)))
	
	def get_tmo_1443a(self):
		"Timeout ISO 1443-A"
		return self.__get_timeslice(0x17)
	def set_tmo_1443a(self, val):
		"Timeout ISO 1443-A"
		return self.__set_timeslice(0x17, val)

	def get_tmo_1443b(self):
		"Timeout ISO 1443-B"
		return self.__get_timeslice(0x18)
	def set_tmo_1443b(self, val):
		"Timeout ISO 1443-B"
		return self.__set_timeslice(0x18, val)

	def get_tmo_sr176(self):
		"Timeout SR-176"
		return self.__get_timeslice(0x19)
	def set_tmo_sr176(self, val):
		"Timeout SR-176"
		return self.__set_timeslice(0x19, val)

	def get_tmo_15693(self):
		"Timeout ISO 15693"
		return self.__get_timeslice(0x1a)
	def set_tmo_15693(self, val):
		"Timeout ISO 15693"
		return self.__set_timeslice(0x1a, val)

	def get_auto_tmo(self):
		"Auto timeout"
		return not self.__get_bit(0x1b, PCON3_AUTO_TIMEOUT)
	def set_auto_tmo(self, bit):
		"Auto timeout"
		self.__set_bit(0x1b, PCON3_AUTO_TIMEOUT, not bit)

	def get_page_read(self):
		"Page Read Mode"
		return self.__get_bit(0x1b, PCON3_PAGE_READ)
	def set_page_read(self, bit):
		"Page Read Mode"
		self.__set_bit(0x1b, PCON3_PAGE_READ, bit)

	def get_ext_reqa(self):
		"Ext. REQA"
		return self.__get_bit(0x1b, PCON3_EXT_REQA)
	def set_ext_reqa(self, bit):
		"Ext. REQA"
		self.__set_bit(0x1b, PCON3_EXT_REQA, bit)


	def __dump(self, src, length=16):
		FILTER = ''.join([(len(repr(chr(x)))==3) \
			and chr(x) or '.' for x in range(256)])
		N = 0
		result=''
		while src:
			s,src = src[:length],src[length:]
			hexa = ' '.join(["%02X"%ord(x) for x in s])
			s = s.translate(FILTER)
			result += "  %04X %-*s %s\n" % (N, length, s, hexa)
			N+=length
		return result
	def print_info(self):
		fields = [
			("0x%.8x", eeprom.get_dev_id),
			("0x%.8x", eeprom.get_admin_data),
			("0x%.2x", eeprom.get_station_id),
			("%i", eeprom.get_baud_rate),
			("%.3f", eeprom.get_guard),
			("%r", eeprom.get_auto_start),
			("%r", eeprom.get_binary),
			("%r", eeprom.get_multitag),
			("%r", eeprom.get_new_serial_mode),
			("%r", eeprom.get_program_led),
			("%r", eeprom.get_single_shot),
			("%r", eeprom.get_ext_protocol),
			("%r", eeprom.get_ext_id),
			("%r", eeprom.get_op_1443a),
			("%r", eeprom.get_op_1443b),
			("%r", eeprom.get_op_sr176),
			("%r", eeprom.get_op_icode),
			("%r", eeprom.get_op_15693),
			("%r", eeprom.get_op_icode_epc),
			("%r", eeprom.get_op_icode_uid),
			("%u", eeprom.get_single_shot_tmo),
			("%r", eeprom.get_multitag_reset),
			("%r", eeprom.get_startup_msg),
			("%r", eeprom.get_binary_frame2),
			("%r", eeprom.get_noisy_env),
			("%r", eeprom.get_anti_collision),
			("%r", eeprom.get_err_handling),
			("%u", eeprom.get_reset_time),
			("%u", eeprom.get_recover_time),
			("%u", eeprom.get_afi),
			("%.3f", eeprom.get_tmo_1443a),
			("%.3f", eeprom.get_tmo_1443b),
			("%.3f", eeprom.get_tmo_sr176),
			("%.3f", eeprom.get_tmo_15693),
			("%r", eeprom.get_auto_tmo),
			("%r", eeprom.get_page_read),
			("%r", eeprom.get_ext_reqa),
		]

		for (fmt, getter) in fields:
			val = getter(self)
			print ("  %-18s: %s"%(getter.__doc__, fmt))%val

		print "  Slack data:"
		print self.__dump("".join(map(chr, self.__bin[0x1c:0x80])))
		print "  User data:"
		print self.__dump("".join(map(chr, self.__bin[0x80:])))
