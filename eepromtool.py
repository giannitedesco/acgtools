#!/usr/bin/python

import sys, readline, acg

class EEPROMShell(acg.eeprom):
	def __help(self, arg):
		"Print this help message"
		print "Builtin Commands:"
		keys = self.__builtins.keys()
		keys.sort()
		for k in keys:
			v = self.__builtins[k]
			print "  %s - %s"%(k, v.__doc__)
		print

		keys = self.__cmds.keys()
		keys.sort()
		print "EEPROM Variables:"
		for k in keys:
			(fmt, getter, cast, setter) = self.__cmds[k]
			print "  %-16s : %s"%(k, getter.__doc__)
		print

	def __dump_info(self, arg):
		"Print EEPROM settings"
		self.print_info()

	def __write(self, arg):
		"Write EEPROM to file"
		print "Writing to: %s"%self.__fn
		f = open(self.__fn, 'w')
		f.write(self.binary())
		f.close()
		print "Done"

	def get_filename(self):
		"Filename of the EEPROM (for writing)"
		return self.__fn
	def set_filename(self, fn):
		"Filename of the EEPROM (for writing)"
		try:
			self.__fn = str(fn)
		except ValueError:
			raise acg.ACG_EEPROM_ValueError("Bad filename")

	def __float(self, arg):
		"Floating point"
		return float(arg)
	def __int(self, arg):
		"Integer decimal/hexadecimal"
		return int(arg, 0)
	def __bool(self, arg):
		"Boolean"
		if arg.lower() in ["yes", "on", "true", "1"]:
			return True
		if arg.lower() in ["no", "off", "false", "0"]:
			return False
		raise ValueError

	def __init__(self, fn):
		self.__cmds = {
			"dev_id": ("0x%.8x", self.get_dev_id,
					self.__int, self.set_dev_id),
			"admin_data": ("0x%.8x", self.get_admin_data,
					self.__int, self.set_admin_data),
			"station_id": ("0x%.2x", self.get_station_id,
					self.__int, self.set_station_id),
			"baud_rate": ("%i", self.get_baud_rate,
					self.__int, self.set_baud_rate),
			"guard_time": ("%.3f", self.get_guard,
					self.__float, self.set_guard),
			"auto_start": ("%r", self.get_auto_start,
					self.__bool, self.set_auto_start),
			"binary_proto": ("%r", self.get_binary,
					self.__bool, self.set_binary),
			"multitag": ("%r", self.get_multitag,
					self.__bool, self.set_multitag),
			"new_serial_mode": ("%r", self.get_new_serial_mode,
					self.__bool, self.set_new_serial_mode),
			"program_led": ("%r", self.get_program_led,
					self.__bool, self.set_program_led),
			"single_shot": ("%r", self.get_single_shot,
					self.__bool, self.set_single_shot),
			"ext_protocol": ("%r", self.get_ext_protocol,
					self.__bool, self.set_ext_protocol),
			"ext_id": ("%r", self.get_ext_id,
					self.__bool, self.set_ext_id),
			"op_1443a": ("%r", self.get_op_1443a,
					self.__bool, self.set_op_1443a),
			"op_1443b": ("%r", self.get_op_1443b,
					self.__bool, self.set_op_1443b),
			"op_sr176": ("%r", self.get_op_sr176,
					self.__bool, self.set_op_sr176),
			"op_icode": ("%r", self.get_op_icode,
					self.__bool, self.set_op_icode),
			"op_15693": ("%r", self.get_op_15693,
					self.__bool, self.set_op_15693),
			"op_icode_epc": ("%r", self.get_op_icode_epc,
					self.__bool, self.set_op_icode_epc),
			"op_icode_uid": ("%r", self.get_op_icode_uid,
					self.__bool, self.set_op_icode_uid),
			"single_shot_tmo": ("%u", self.get_single_shot_tmo,
					self.__int, self.set_single_shot_tmo),
			"multitag_reset": ("%r", self.get_multitag_reset,
					self.__bool, self.set_multitag_reset),
			"startup_msg": ("%r", self.get_startup_msg,
					self.__bool, self.set_startup_msg),
			"binary_frame2": ("%r", self.get_binary_frame2,
					self.__bool, self.set_binary_frame2),
			"noisy_env": ("%r", self.get_noisy_env,
					self.__bool, self.set_noisy_env),
			"anti_collision": ("%r", self.get_anti_collision,
					self.__bool, self.set_anti_collision),
			"err_handling": ("%r", self.get_err_handling,
					self.__bool, self.set_err_handling),
			"reset_time": ("%u", self.get_reset_time,
					self.__int, self.set_reset_time),
			"recover_time": ("%u", self.get_recover_time,
					self.__int, self.set_recover_time),
			"afi": ("%u", self.get_afi,
					self.__int, self.set_afi),
			"timeout_1443a": ("%.3f", self.get_tmo_1443a,
					self.__float, self.set_tmo_1443a),
			"timeout_1443b": ("%.3f", self.get_tmo_1443b,
					self.__float, self.set_tmo_1443b),
			"timeout_sr176": ("%.3f", self.get_tmo_sr176,
					self.__float, self.set_tmo_sr176),
			"timeout_15693": ("%.3f", self.get_tmo_15693,
					self.__float, self.set_tmo_15693),
			"auto_timeout": ("%r", self.get_auto_tmo,
					self.__bool, self.set_auto_tmo),
			"page_read": ("%r", self.get_page_read,
					self.__bool, self.set_page_read),
			"ext_reqa": ("%r", self.get_ext_reqa,
					self.__bool, self.set_ext_reqa),
			"filename": ("%s", self.get_filename,
					str, self.set_filename),
		}

		self.__builtins = {
			"?": self.__help,
			"h": self.__help,
			"p": self.__dump_info,
			"w": self.__write,
		}

		self.__fn = fn
		f = open(fn, 'r')
		bin = f.read()
		f.close()
		acg.eeprom.__init__(self, bin)

	def __do_set(self, var, val):
		if not self.__cmds.has_key(var):
			print "%s: No such variable"%var
			return
		try:
			(fmt, getter, cast, setter) = self.__cmds[var]
			setter(cast(val))
		except ValueError, e:
			print "ERROR: setting %s: expected %s"%(var,
							cast.__doc__)
		except acg.ACG_EEPROM_ValueError, e:
			print "ERROR: setting %s: %s"%(var, e.msg)
		self.__do_get(var)
		return

	def __do_get(self, var):
		if not self.__cmds.has_key(var):
			print "%s: No such variable"%var
			return

		(fmt, getter, cast, setter) = self.__cmds[var]
		print ("%s = %s"%(var, fmt))%getter()

	def prompt(self):
		return "eeprom> "

	def command(self, cmd):
		tok = cmd.split(None, 1)

		if len(tok) == 2:
			self.__do_set(tok[0], tok[1])
			return
		else:
			tok.append(None)

		if self.__builtins.has_key(tok[0]):
			self.__builtins[tok[0]](tok[1])
			return

		self.__do_get(tok[0])

if __name__ == '__main__':
	eeprom_fn = sys.argv[1]
	try:
		shell = EEPROMShell(eeprom_fn)
	except acg.ACG_Exception, e:
		print e.msg

	while True:
		try:
			line = raw_input(shell.prompt())
		except EOFError:
			print
			break
		except KeyboardInterrupt:
			print
			continue

		try:
			shell.command(line);
		except KeyboardInterrupt:
			continue
