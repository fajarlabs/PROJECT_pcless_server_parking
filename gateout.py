from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from bottle import route, run, request, response
from json import dumps
import threading, queue
from threading import Timer
import logging
import serial
import time

logging.basicConfig(filename='gateout.log', filemode='a+', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

RESPONSE_TIMEOUT = 5.0 #seconds
loop_unlock = False
timer_timeout = None
response_list = []
""" 
----------------------------------------------------------------------------------------------------------
FUNCTION TO STOP ITERATE (WHILE)
----------------------------------------------------------------------------------------------------------
"""
def release_lock():
    global loop_unlock
    loop_unlock = True

# create the application
app = QApplication([])
app.setQuitOnLastWindowClosed(False)

# create the icon
icon = QIcon("pcless.ico")

# create the tray icon 
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)

# this will print a message 
def print_msg():
	alert = QMessageBox()
	alert.setText('You clicked the button!')
	alert.exec_()

# create the menu for tray icon
menu = QMenu()

# add one item to menu 
action = QAction("Info")
menu.addAction(action)
action.triggered.connect(print_msg)

# add exit item to menu 
exitAction = QAction("&Exit")
menu.addAction(exitAction)
exitAction.triggered.connect(exit)

# add the menu to the tray
tray.setContextMenu(menu)

"""
----------------------------------------------------------------------------------------
Serial configuration
----------------------------------------------------------------------------------------
"""
ser = serial.Serial()
ser.port = 'COM5'
ser.baudrate = 9600
ser.bytesize = 8
ser.parity = 'N'
ser.stopbits = 1
ser.timeout = None
ser.xonxoff = 0
ser.rtscts = 0

# connect serial
try :
	ser.open()
except Exception as e :
	logging.error(str(e))

def task_connect():
	global ser
	try  :
		if(ser.isOpen() == False):
			try :
				ser.open()
			except Exception as e :
				print(e)
				logging.error(str(e))
		else :
			bytesToRead = ser.inWaiting()
			serial_decode = ser.read(bytesToRead).decode()
			if (serial_decode != ''):
				response_list.append(serial_decode)
	except Exception as e :
		print(e)
		logging.error(str(e))

	try :
		bytesToRead = ser.inWaiting()
		serial_response += ser.read(bytesToRead).decode()
	except Exception as e :
		logging.error(str(e))

# check connection in every 2 seconds
timer_reconnect = QtCore.QTimer()
#timer_reconnect.setSingleShot(True) # only once
timer_reconnect.timeout.connect(task_connect)
timer_reconnect.start(100)

"""
----------------------------------------------------------------------------------------
Microservice controller (Bottle Framework)
----------------------------------------------------------------------------------------
"""

@route('/', method='GET')
def index():
    rv = { "status": "ok", "desc": "ready to communication to devices" }
    response.content_type = 'application/json'
    return dumps(rv)

@route('/cmd', method='POST')
def command():
	global ser
	global loop_unlock
	global timer_timeout

	# clear result
	del response_list[:]

	# reet lock loop
	loop_unlock = False

	# reset timer and start again
	if(timer_timeout != None):
		if(timer_timeout.is_alive()):
			timer_timeout.cancel()

	# timer response
	timer_timeout = Timer(RESPONSE_TIMEOUT, release_lock)
	timer_timeout.start()

	# get request
	cmd = request.forms.get('cmd')
	status = "failed"
	desc = ""

	# send serial command
	ser.write(cmd.encode())

	while True :
		# release lock
		if loop_unlock : break

		# check caracter '#' is exist
		if ('*TRIG1OK#' in response_list) or \
		('*OUT1ONOK#' in response_list) or \
		('*OUT1OFFOK#' in response_list) or \
		('*OPEN1OK#' in response_list) :
			desc = "complete"
			status = "ok"
			break
		
		time.sleep(0.2)

	try :
		rv = { "status": status, "response": response_list, "description": desc }
		response.content_type = 'application/json'
	except Exception as e :
		print(e)

	return dumps(rv)

webservice = threading.Thread(target=run, kwargs=dict(host='localhost',port=8080), daemon=True)
webservice.start()

# start application execution 
app.exec_()