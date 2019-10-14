import socket
import time

"""
AUTHOR : Fajarlabs
WHATSAPP : 089663159652
"""

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
			self.s = socket.socket()
			self.s.connect((self.ip, self.port))
		except Exception as e :
			result = False
			print(e)

		return result

	"""
	Function disconnecting socket
	"""
	def disconnect(self):
		result = True
		try :
			if (s != None):
				self.s.close()
		except Exception as e :
			result = False
			print(e)

		return result

	"""
	Function send data
	"""
	def send(self, data):
		result = True
		try :
			self.s.send(data.encode('CP1252'))
		except Exception as e :
			result = False
			print(e)

		return result

	"""
	Function for receiving data
	"""
	def receive(self):
		result = None
		try :
			result = self.s.recv(1024).decode('CP1252')
		except Exception as e :
			result = None
			print(e)

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
	def send_print(self):
		array_pr = []
		array_pr.append(self.format_command("PR4-------------------"+CRLF))
		array_pr.append(self.format_command("PR4SELAMAT DATANG"+CRLF))
		array_pr.append(self.format_command("PR4SELAMAT BERBELANJA"+CRLF))
		array_pr.append(self.format_command("PR4TERIMAKASIH"+CRLF))
		array_pr.append(self.format_command("PR4-------------------"+CRLF))

		for s in array_pr :
			self.send(s)

	""" 
	MAIN PROGRAM PCLESS SERIAL
	"""
	def deploy(self) :

		# always reconnecting forever
		while self.reconnect :
			
			# connect serial ethernet Wizz
			if(self.connect()):

				# Connect OK, reconnect set to False, and command_listen True
				reconnect = False
				command_listen = True

				# waiting command
				while command_listen :
					i = input()
					# sending data
					print("Sending data...")
					cstr = self.cetak_struk()
					for cs in cstr :
						if(self.send(cs) == False):
							# close command & reload connection
							reconnect = True
							command_listen = False
						else :
							print(self.receive())


				# reconnecting...
				print("Reconnecting...")
				time.sleep(1);