class ACGException:
	pass

class ACGUnknownCommand(ACGException):
	pass

class ACGCollision(ACGException):
	pass

class ACGCommandFail(ACGException):
	pass

class ACGInvalidValue(ACGException):
	pass

class ACGNoTagInField(ACGException):
	pass

class ACGOperationMode(ACGException):
	pass

class ACGRangeError(ACGException):
	pass

class ACGAuthFailed(ACGException):
	pass
