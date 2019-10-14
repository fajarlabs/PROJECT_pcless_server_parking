from bottle import route, run, request, response
from json import dumps
from pcless import PCLess
from flowcontrol import BGFlowControl
from devices import get_all_device

"""
AUTHOR : Fajarlabs
WHATSAPP : 089663159652
"""

"""
REGISTER PCLESS
"""
CLIENTS = []
for cfg in get_all_device():
	CLIENTS.append(PCLess(cfg['ip'],cfg['port']))

"""
START BACKGROUND CONTROLLING PCLESS
"""
for obj in CLIENTS :
	BGFlowControl(obj)


"""
WEB SERVICE CONTROLLER
"""
@route('/', method='GET')
def index():
    rv = { "status": "ok", "desc": "ready to communication to devices" }
    response.content_type = 'application/json'
    return dumps(rv)


@route('/cmd/<idx:int>', method='POST')
def command(idx):
    cmd = request.forms.get('cmd')
    data = request.forms.get('data')

    device_reply = None
    if (cmd != ""):
    	if (cmd == "voice"):
		    if(CLIENTS[idx].send(CLIENTS[idx].voice(data)) == True):
		    	device_reply = CLIENTS[idx].receive()
    	elif (cmd == "print"):
    		CLIENTS[idx].send_print()
    		device_reply = CLIENTS[idx].receive()
		    # if(send(format_command(cmd))):
		    # 	device_reply = receive()
		    # 	disconnect()
    	else :
		    if(CLIENTS[idx].send(CLIENTS[idx].format_command(cmd))):
		    	device_reply = receive()

    rv = { "status": "ok", "response": device_reply }
    response.content_type = 'application/json'
    return dumps(rv)

run(host='localhost', port=8080, debug=True)
			
