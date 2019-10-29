#!/usr/bin/python

import numpy as np
import cv2
import uuid
import requests
from requests.auth import HTTPDigestAuth
from pcless_db import add_ticket
import logging
 
# METHOD #1: OpenCV, NumPy, and urllib
def url_to_image(img_uuid, url, username, password, path_output):

	filename = ""

	try :
		resp = requests.get(url, auth=HTTPDigestAuth(username, password), stream=True).raw
		image = np.asarray(bytearray(resp.read()), dtype="uint8")
		image = cv2.imdecode(image, cv2.IMREAD_COLOR)

		filename = img_uuid+".png"
		cv2.imwrite(path_output+"/"+str(uuid.uuid4().hex)+".png",image)
	except Exception as e :
		logging.error(str(e))
	finally :
		try :
			add_ticket(img_uuid, filename)
		except Exception as e2 :
			logging.error(str(e2))

if __name__ == "__main__" :
	url_to_image("http://admin:Spasi2019@192.168.0.100/ISAPI/Streaming/channels/101/picture","admin","Spasi2019", "F:\\DIY\\SOFTWARE\\udp_forwarder\\captures")