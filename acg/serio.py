# This file is part of actools
# Copyright (c) 2010 Gianni Tedesco
# This is free software released under the terms of the GNU GPL v3
from serial import Serial

class serio:
	def __init__(self, line, baud, tracefile=None):
		self.__s = Serial(line, baud, timeout=None)
		if tracefile:
			self.__trace = open(tracefile, 'w')
		self.flush_buffers()

	def trace(self, line):
		self.__trace.write(line + '\n')
		self.__trace.flush()

	def tx(self, cmd):
		#cmd = cmd + '\r\n'
		self.trace(">>> %r"%cmd)
		self.__s.write(cmd)

	def peekbuffer(self, tmo=0):
		self.__s.setTimeout(tmo)
		ret = self.rx()
		self.__s.setTimeout(None)
		return ret

	def rx(self):
		ret = self.__s.readline()
		if ret[-1:] == '\n':
			ret = ret[:-1]
		if ret[-1:] == '\r':
			ret = ret[:-1]
		self.trace("<<< %r"%ret)
		return ret
	
	def flush_buffers(self):
		self.__s.flushInput()
		self.__s.flushOutput()
		self.trace("--- flushed buffers")
