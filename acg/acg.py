from errors import *
from eeprom import *
from serio import serio
from tag import tag, iso1443a, iso1553b
from util import asc2bin, bin2asc
import time

class acg:
	def __read_eeprom_byte(self, ofs):
		cmd = "rp%.2X"%ofs
		resp = self.__trancieve(cmd)
		if len(resp) != 2:
			raise ACG_BadResponse(cmd, resp)
		try:
			byte = int(resp, 16)
		except ValueError:
			raise ACG_BadResponse(cmd, resp)
		return byte
		
	def __read_eeprom(self):
		eeprom = ''
		for i in range(0, EEPROM_BYTES):
			byte = self.__read_eeprom_byte(i)
			eeprom += chr(byte)
		return eeprom
	
	def __flash_eeprom(self, bin):
		assert(len(bin) == EEPROM_BYTES)
		bin = bin[EEPROM_READONLY:]
		for i in range(0, EEPROM_BYTES - EEPROM_READONLY):
			cmd = "wp%.2X%.2X"%(i + EEPROM_READONLY, ord(bin[i]))
			resp = self.__trancieve(cmd)

	def __hard_reset(self):
		# Startup message may be disabled in EEPROM
		self.__serio.tx("x")
		self.__banner = self.__serio.peekbuffer(0.25)

		# If device starts in continuous read mode then send a
		# command to abort that and retrieve the tag list
		self.__serio.tx(".")
		ret = self.__serio.rx()
		while len(ret) and ret != 'S' and ret != '?':
			ret = self.__serio.peekbuffer(0.15)
		self.__cont_read = False

		self.__pcon = self.__read_eeprom_byte(0xb)
		self.__pcon3 = self.__read_eeprom_byte(0x1b)
		self.__ext_reqa = bool(self.__pcon3 & (1<<6))
		self.__ext_id = bool(self.__pcon & (1<<7))

		# Finally the device ought to be in a predictable state
		# phew

	def __init__(self, line="/dev/ttyUSB0", baud=460800, tracefile=None):
		self.__serio = serio(line, baud, tracefile)
		self.__cont_read = True
		self.__hard_reset()
		self.__eeprom = None

	def __rx(self, cmd):
		ret = self.__serio.rx()
		if len(ret) == 0:
			raise ACG_IOError("Reader returned nothing")
		if len(ret) == 1:
			if ret[0] == '?':
				raise ACG_UnknownCommand(cmd[0])
			if ret[0] == 'C':
				raise ACG_Collision
			if ret[0] == 'F':
				raise ACG_CommandFail(cmd)
			if ret[0] == 'I':
				raise ACG_InvalidValue(cmd)
			if ret[0] == 'N':
				raise ACG_NoTagInField
			if ret[0] == 'O':
				raise ACG_OperationMode(cmd)
			if ret[0] == 'R':
				raise ACG_RangeError(cmd)
			if ret[0] == 'X':
				raise ACG_AuthFailure(cmd)
			if ret[0] == 'S' and not cmd in ['c', '.']:
				print "warn: interleaving commands with " + \
					"cont. read is dangerous"
				self.__cont_read = False
		return ret

	def __trancieve(self, cmd):
		self.__serio.tx(cmd)
		return self.__rx(cmd)

	def dump_eeprom(self, filename):
		if not self.__eeprom:
			self.__eeprom = eeprom(self.__read_eeprom())
		f = open(filename, 'w')
		f.write(self.__eeprom.binary())
		f.close()

	def flash_eeprom(self, filename):
		f = open(filename, 'r')
		img = eeprom(f.read())
		f.close()
		self.__flash_eeprom(img.binary())
		self.__hard_reset()

	def get_eeprom(self):
		self.__eeprom = eeprom(self.__read_eeprom())
		return self.__eeprom

	def __rate_settings(self, byte):
		hi = byte >> 4
		lo = byte & 0xf
		rate = {
			0x0: 106,
			0x2: 212,
			0x4: 424,
			0x8: 848
		}
		fsztab = [16, 24, 32, 40, 48, 64, 96, 128, 256]
		baud = None
		fsz = None
		if rate.has_key(lo):
			baud = rate[lo]
		if hi < len(fsztab):
			fsz = fsztab[hi]
		return (baud, fsz)

	def __parse_tag(self, cmd, uid):
		if not self.__ext_id:
			return tag(uid)

		if self.__ext_reqa:
			if len(uid) in [6, 9, 12]:
				t = iso1443a(uid[2:], reqa = uid[:2])
			elif len(uid) == 13: # ??????
				t = iso1553b(uid[0:4],
						app = uid[4:8],
						protocol = uid[8:11],
						cid = uid[11])
			else:
				raise ACG_BadResponse(cmd, bin2asc(uid))
		else:
			if len(uid) in [5, 8, 11]:
				t = iso1443a(uid[1:], cascade = uid[0])
			elif len(uid) == 12:
				t = iso1553b(uid[0:4],
						app = uid[4:8],
						protocol = uid[8:11],
						cid = uid[11])
			else:
				raise ACG_BadResponse(cmd, bin2asc(uid))
		return t

	def __parse_htag(self, cmd, resp):
		speed = ord(resp[-1:])
		uid = resp[:-1]

		if not self.__ext_id:
			t = self.__parse_tag(cmd, uid)
		else:
			ats = []
			if self.__ext_reqa:
				iso1443a = [12, 9, 6]
			else:
				iso1443a = [11, 8, 5]
			for i in iso1443a:
				if len(uid) < i:
					continue
				if len(uid) == uid[i] + i:
					ats.append(i)
			if len(ats):
				a = ats[0]
				t = self.__parse_tag(cmd, uid[:a])
				t.set_rats(uid[a:])
			else:
				t = self.__parse_tag(cmd, uid)

		(baud, fsz) = self.__rate_settings(speed)
		t.set_hispeed(baud, fsz)
		return t

	def select(self, stag = None):
		if stag == None:
			cmd = "s"
		else:
			cmd = "m%s\r"%stag.serial_str

		uid = asc2bin(self.__trancieve(cmd))
		t = self.__parse_tag(cmd, uid)

		if stag != None and t != stag:
			raise ACG_NoTagInField

		return t

	def hselect(self, stag = None):
		if stag == None:
			cmd = "h08"
		else:
			self.__trancieve("h18")
			cmd = "m%s\r"%stag.serial_str

		uid = asc2bin(self.__trancieve(cmd))
		t = self.__parse_htag(cmd, uid)

		if stag != None and t != stag:
			raise ACG_NoTagInField

		return t

	def multi_select(self):
		uid = self.__serio.tx("m\r")
		uid = self.__rx('m\r')
		ret = []
		while len(uid) > 2:
			t = self.__parse_tag("m\r", asc2bin(uid))
			ret.append(t)
			uid = self.__rx('m\r')
		return ret

	def continuous_read(self):
		if not self.__cont_read:
			self.__serio.tx("c")
			self.__cont_read = True

		uid = self.__rx('c')
		if uid == 'S':
			self.__cont_read = False
			return None
		return self.__parse_tag('c', asc2bin(uid))
	
	def abort_continuous_read(self):
		if not self.__cont_read:
			return
		ret = self.__trancieve(".")
		while ret != 'S':
			print "additional tags after abort"
			ret = self.__rx('.')
		self.__cont_read = False

	def apdu(self, pdu):
		ret = self.__trancieve("t%.2x1f02%s"%(len(pdu) + 1,
							bin2asc(pdu)))
		bin = asc2bin(ret)
		if len(bin) < 4:
			raise ACG_IOError("Bad PDU response: %s"%ret)
		bin = bin[2:]
		return (bin[:-2], ord(bin[-2:-1]), ord(bin[-1:]))

	def mifare_readblock(self, rec):
		return self.__trancieve("r%.2x"%rec)

	def mifare_login(self, rec, k, keydata = None):
		cmd = 'l%.2x%.2x\r'%(rec, k)
		try:
			ret = self.__trancieve(cmd)
		except ACG_NoTagInField:
			self.select()
			ret = self.__trancieve(cmd)
		if ret == 'L':
			return True
		else:
			return False
