import logging
from bottle import route, run, request, response
from json import dumps
from pcless import PCLess
from timeloop import Timeloop
from datetime import timedelta
import time
from threading import Timer
import threading
import configparser
from argparse import ArgumentParser
from pcless_lib import url_to_image
import sys

logging.basicConfig(filename='pcless.log', filemode='a+', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

tm_loop = Timeloop()
response_list = []
pcless = None
timer_response = None

RESPONSE_TIMEOUT = 30.0 #seconds
loop_unlock = False

"""
----------------------------------------------------------------------------------------------------------
REGISTER PCLESS
----------------------------------------------------------------------------------------------------------
"""
parser = ArgumentParser()
parser.add_argument("-H", "--hostname", dest="hostname", help="Set hostname")
parser.add_argument("-P", "--port", dest="port", help="set port")
parser.add_argument("-plh", "--pcless_host", dest="pcless_host", help="set PC less hostname")
parser.add_argument("-plp", "--pcless_port", dest="pcless_port", help="set PC less port")
parser.add_argument("-ctv", "--cctv_url", dest="cctv_url", help="Set CCTV URL")
parser.add_argument("-ctvu", "--cctv_user", dest="cctv_user", help="Set CCTV user")
parser.add_argument("-ctvp", "--cctv_pass", dest="cctv_pass", help="Set CCTV pass")
parser.add_argument("-pth", "--path", dest="path", help="Set path")

args = parser.parse_args()

if (args.hostname == None):
    print("Hostname is required!")
    sys.exit()

if (args.port == None):
    print("Port is required!")
    sys.exit()

if (args.pcless_host == None):
    print("PCLess host is required!")
    sys.exit()

if (args.pcless_port == None):
    print("PCLess Port is required!")
    sys.exit()

if (args.cctv_url == None):
    print("CCTV url is required!")
    sys.exit()

if (args.cctv_user == None):
    print("CCTV user is required!")
    sys.exit()

if (args.cctv_pass== None):
    print("CCTV pass is required!")
    sys.exit()

if (args.path ==  None):
    print("Path directory for save image is requred!")

pcless = PCLess(str(args.pcless_host) ,int(args.pcless_port))

"""
----------------------------------------------------------------------------------------------------------
INITIALIZE BACKGROUND RECEIVER & WORKFLOW
TIMER BACKGROUND CONTROLLIN G PCLESS
----------------------------------------------------------------------------------------------------------
"""
@tm_loop.job(interval=timedelta(seconds=0))
def workflow_job():
    global pcless
    global args
    
    # read new serial value
    rspv = pcless.receive()
    response_list.append(rspv)

    """
    START LOGIC WORFLOW
    """
    if(rspv == '¦IN1ON©'):
        if(pcless.track_flow < 1):
            pcless.send(pcless.voice('1'))
            pcless.track_flow += 1
    
    if(rspv == '¦IN2ON©'):
        if((pcless.track_flow > 0) and (pcless.track_flow < 2)):

            """
            STEP I
            """
            # play voice track
            pcless.send(pcless.voice('2'))
            t_capture = threading.Thread(target=url_to_image, args=(str(args.cctv_url),str(args.cctv_user),str(args.cctv_pass), str(args.path),))
            t_capture.start()
            
            """
            STEP II
            """

            # thermal print number
            time.sleep(0.1)
            pcless.send_print(4,'------------------------------------------------')
            time.sleep(0.1)
            pcless.send_print(4,'               SELAMAT DATANG                   ')
            time.sleep(0.1)
            pcless.send_print(4,'         Jumat, 21-12-2019 | 21:15              ')                      
            time.sleep(0.1)
            pcless.send_print(4,'         ACC0234102394534952323444              ')
            time.sleep(0.1)
            pcless.send_print(4,' JANGAN MENINGGALKAN TIKEN DAN BARANG BERHARGA  ')
            time.sleep(0.1)
            pcless.send_print(4,'      ANDA, KENDARAAN INAP WAJIB LAPOR          ')
            time.sleep(0.1)

            """
            STEP III
            """
            # save picture

            """
            STEP IV
            """
            # save database

            pcless.track_flow = 0

"""
----------------------------------------------------------------------------------------------------------
CHECK PCLESS CONNECTION
----------------------------------------------------------------------------------------------------------
"""
while True :
    if(pcless.connect()):
        print('Connected...')
        logging.info('Application started')
        break
    else :
        print('Reconnecting...')
        break
    time.sleep(1)

""" 
----------------------------------------------------------------------------------------------------------
FUNCTION TO STOP ITERATE (WHILE)
----------------------------------------------------------------------------------------------------------
"""
def release_lock():
    global loop_unlock
    loop_unlock = True

"""
----------------------------------------------------------------------------------------------------------
WEB SERVICE CONTROLLER
----------------------------------------------------------------------------------------------------------
"""
@route('/', method='GET')
def index():
    rv = { "status": "ok", "desc": "ready to communication to devices" }
    response.content_type = 'application/json'
    return dumps(rv)


@route('/cmd', method='POST')
def command():
    global response_list
    global pcless
    global loop_unlock
    global timer_response

    cmd = request.forms.get('cmd')
    list_data = request.forms.getlist('data[]')
    data = request.forms.get('data')
    baud_rate_id = request.forms.get('baud_rate_id')
    status = "failed"

    """
    debug form-data
    """
    # print(cmd)
    # print(list_data)
    # print(data)
    # print(baud_rate_id)

    # clear array
    del response_list[:]
    # release loop, set to false
    loop_unlock = False
    # reset timer and start again
    if(timer_response != None):
        if(timer_response.is_alive()):
            timer_response.cancel()
    # create new time
    timer_response = Timer(RESPONSE_TIMEOUT, release_lock)

    try :
        if (cmd != ""):
            if (cmd == "voice"):
                if(pcless.send(pcless.voice(data)) == True):
                    timer_response.start()
                    while True :
                        if loop_unlock : break
                        if(('¦MTOK©' in response_list) and ('¦PLAYEND©' in response_list)): break
                    status = "ok"
            elif (cmd == "print"):
                for item_data in list_data : 
                    pcless.send_print(int(baud_rate_id), item_data)
                    time.sleep(0.2)
                status = "ok"
            else :
                if(pcless.send(pcless.format_command(cmd))):
                    time.sleep(0.2)
                    status = "ok"
    except Exception as e :
        print(e)

    try :
        rv = { "status": "ok", "response": response_list }
        response.content_type = 'application/json'
    except Exception as e :
        print(e)

    return dumps(rv)

"""
----------------------------------------------------------------------------------------------------------
MAIN PROGRAM
----------------------------------------------------------------------------------------------------------
"""
tm_loop.start(block=False)
run(host='0.0.0.0', port=80, debug=True)