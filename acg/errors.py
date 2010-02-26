class ACGException:
	pass

class ACGIOError(ACGException):
	pass

class ACGBadResponse(ACGException):
	def __init__(self, cmd, resp):
		self.cmd = cmd
		self.resp = resp

# Following errors defiend by the spec
class ACGUnknownCommand(ACGException):
	def __init__(self, cmd_id):
		assert(len(cmd_id) == 1)
		self.cmd_id = cmd_id
		self.msg = "Unknown Command: %.2x"%ord(cmd_id)

class ACGCollision(ACGException):
	pass

class ACGCommandFail(ACGException):
	def __init__(self, cmd):
		self.cmd = cmd

class ACGInvalidValue(ACGException):
	def __init__(self, cmd):
		self.cmd = cmd

class ACGNoTagInField(ACGException):
	pass

class ACGOperationMode(ACGException):
	def __init__(self, cmd):
		self.cmd = cmd

class ACGRangeError(ACGException):
	def __init__(self, cmd):
		self.cmd = cmd

class ACGAuthFailed(ACGException):
	pass
