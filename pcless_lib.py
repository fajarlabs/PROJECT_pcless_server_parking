#!/usr/bin/python

import numpy as np
import cv2
import uuid
import requests
from requests.auth import HTTPDigestAuth
from pcless_db import add_ticket
import logging
 
# METHOD #1: OpenCV, NumPy, and urllib
def url_to_image(url, username, password, path_output):

	result = None

	try :
		resp = requests.get(url, auth=HTTPDigestAuth(username, password), stream=True).raw
		image = np.asarray(bytearray(resp.read()), dtype="uint8")
		image = cv2.imdecode(image, cv2.IMREAD_COLOR)

		img_uuid = str(uuid.uuid4().hex)
		filename = img_uuid+".png"

		cv2.imwrite(path_output+"/"+str(uuid.uuid4().hex)+".png",image)

		add_ticket(img_uuid, filename)
	except Exception as e :
		loggine.error(str(e))

if __name__ == "__main__" :
	url_to_image("http://admin:Spasi2019@192.168.0.100/ISAPI/Streaming/channels/101/picture","admin","Spasi2019", "F:\\DIY\\SOFTWARE\\udp_forwarder\\captures")