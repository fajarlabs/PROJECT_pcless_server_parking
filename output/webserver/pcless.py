import socket
import time
import sys
import logging

# MUST USE BEETWEEN FORMAT
# CONST DATA FORMAT 
HEADER = "\xa6"
FOOTER = "\xa9"
CRLF = "\r\n"

class PCLess(object):

	def __init__(self, ip, port):
		self.s = None
		self.reconnect = True
		self.ip = ip
		self.port = port
		self.track_flow = 0
	
	# command format 
	def format_command(self, cmd):
		return HEADER+cmd+FOOTER

	"""
	Function to generate format 0000X
	"""
	def fill_zero(self, max_zero, data):
		result = str(data)
		for i in range(max_zero-1):
			result = str(0)+result

		return result


	"""
	Function to connecting socket
	"""
	def connect(self):
		result = True
		try :
			self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.s.connect((self.ip, self.port))
			# self.s.setblocking(1)
			# self.s.settimeout(10)
		except Exception as e :
			result = False
			logging.error(str(e))

		return result

	""" 
	COMMAND GLOBAL FUNCTION
	VOICE CALL SPEAKER
	"""
	def voice(self, data):
		return self.format_command("MT"+self.fill_zero(5,data))

	"""
	COMMAND GLOBAL FUNCTION
	PRINT STRUCT
	"""
	def send_print(self, baud_rate_id, data_print, is_crlf=True):
		if(is_crlf == True):
			self.send(self.format_command("PR"+str(baud_rate_id)+str(data_print)+CRLF))
		else :
			self.send(self.format_command("PR"+str(baud_rate_id)+str(data_print)))

	"""
	Function disconnecting socket
	"""
	def disconnect(self):
		result = True
		try :
			if (self.s != None):
				self.s.close()
		except Exception as e :
			result = False
			logging.error(str(e))

		return result

	"""
	Function send data
	"""
	def send(self, data):
		result = True
		try :
			self.s.send(data.encode('CP1252'))
		except Exception as e :
			logging.error(str(e))
			result = False
			# error reconnecting
			if(type(e).__name__ == 'OSError'):
				self.connect()

		return result

	"""
	Function for receiving data
	"""
	def receive(self):
		result = None
		try :
			result = self.s.recv(1024).decode('CP1252')
		except Exception as e :
			logging.error(str(e))
			# error reconnecting
			if(type(e).__name__ == 'OSError'):
				self.connect()
				time.sleep(1)
			if(type(e).__name__ == 'ConnectionResetError'):
				self.connect()
				time.sleep(1)
		return result