class ACG_Exception:
	def __init__(self):
		self.msg = msg

class ACG_EEPROM_Error(ACG_Exception):
	def __init__(self, msg = None):
		if not msg:
			msg = "EEPROM format error"
		self.msg = msg

class ACG_EEPROM_ValueError(ACG_Exception):
	def __init__(self, msg = None):
		if not msg:
			msg = "Attempted to set an invalid EEPROM value"
		self.msg = msg

class ACG_IOError(ACG_Exception):
	def __init__(self, msg = None):
		if not msg:
			msg = "ACG_ I/O error"
		self.msg = msg

class ACG_BadResponse(ACG_Exception):
	def __init__(self, cmd, resp):
		self.cmd = cmd
		self.resp = resp
		self.msg = "%r is bad response to command %r"%(cmd, resp)

# Following errors defiend by the spec
class ACG_UnknownCommand(ACG_Exception):
	def __init__(self, cmd_id):
		assert(len(cmd_id) == 1)
		self.cmd_id = cmd_id
		self.msg = "Unknown Command: %.2x (%s)"%(ord(cmd_id), cmd_id)

class ACG_Collision(ACG_Exception):
	def __init__(self):
		self.msg = "Collision or CRC/MAC error"

class ACG_CommandFail(ACG_Exception):
	def __init__(self, cmd):
		self.cmd = cmd
		self.msg = "Command failed: %r"%cmd

class ACG_InvalidValue(ACG_Exception):
	def __init__(self, cmd):
		self.cmd = cmd
		self.msg = "Command contained invalid value: %r"%cmd

class ACG_NoTagInField(ACG_Exception):
	def __init__(self):
		self.msg = "No tag in field"

class ACG_OperationMode(ACG_Exception):
	def __init__(self, cmd):
		self.cmd = cmd
		self.msg = "Command invalid in current operating mode: %r"%cmd

class ACG_RangeError(ACG_Exception):
	def __init__(self, cmd):
		self.cmd = cmd
		self.msg = "Command parameter out of range: %r"%cmd

class ACG_AuthFailure(ACG_Exception):
	def __init__(self, cmd):
		self.msg = "Authentication failed: %r"%cmd
