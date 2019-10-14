import threading
import time

"""
AUTHOR : Fajarlabs
WHATSAPP : 089663159652
"""

"""
FLOW APPS PROCESSING PCLESS
"""
class BGFlowControl(object):
    def __init__(self, sclient):
        self.sclient = sclient

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):

    	# reconnecting forever
    	while True :
		    if(self.sclient.connect() == True):
		    	print("Connected...")
		    	while True :
		    		if(self.sclient.receive() == None):
		    			self.sclient.connect()
		    		else :
		    			print(self.sclient.receive())
		    else:
		    	print("Reconnecting...")

		    time.sleep(1)