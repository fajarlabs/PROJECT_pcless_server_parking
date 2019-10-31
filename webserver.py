#!/usr/bin/python

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
import datetime
import sys
import uuid
import re

logging.basicConfig(filename='pcless.log', filemode='a+', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

tm_loop = Timeloop()
response_list = []
pcless = None
timer_timeout = None

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
parser.add_argument("-htm", "--header_thermal", dest="header_thermal", help="Set header thermal")
parser.add_argument("-ttm", "--title_thermal", dest="title_thermal", help="Set title thermal")

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

if (args.header_thermal ==  None):
    print("Header thermal printing is requred!")

if (args.title_thermal ==  None):
    print("Title thermal printing is requred!")

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
            # create UUID code 10 character
            code10 = str(uuid.uuid4().hex[:10]).upper()

            """
            STEP I
            """
            # play voice track
            pcless.send(pcless.voice('2'))
            t_capture = threading.Thread(target=url_to_image, args=(code10,str(args.cctv_url),str(args.cctv_user),str(args.cctv_pass), str(args.path),))
            t_capture.start()
            
            # give more time
            time.sleep(0.2)
            """
            STEP II
            """
            # thermal print number
            datenow = datetime.datetime.now()
            datenow = datenow.strftime("TANGGAL : %d/%m/%Y     %H:%M:%S")
            escpos_command = '' # new line
            escpos_command += '\x1b\x61\x01' # alignment center
            escpos_command += '\x1b\x4d\x00' # set font type A
            escpos_command += '\x1b\x21\x20' # double width
            escpos_command += str(args.header_thermal)+'\x0a'
            escpos_command += '\x1b\x21\x00'
            escpos_command += str(args.title_thermal)+'\x0a'
            escpos_command += '\x0a'
            escpos_command += datenow+'\x0a\x0a'
            escpos_command += '\x1b\x21\x00' # normal text
            escpos_command += '\x1b\x61\x01' # double width
            escpos_command += '\x1d\x6b\x04'+code10+'\x00' # barcode
            escpos_command += '\x1b\x21\x00' # normal text
            escpos_command += '\x1b\x21\x20' # double width
            escpos_command += ' '+re.sub("(.)", r'\1 ',code10) # barcode code
            escpos_command += '\x0a\x0a\x0a'
            escpos_command += '\x1b\x21\x00'
            escpos_command += '*** TERIMAKASIH ***'
            escpos_command += '\x0a\x0a\x0a\x0a\x0a\x0a' # newline cutter
            escpos_command += '\x1d\x56\x00' # full cut paper
            escpos_command += '\x1b\x3f\x0a\x00' # full cut paper
            pcless.send_print(4,escpos_command)

            # give more time
            time.sleep(0.2)

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
    global timer_timeout

    cmd = request.forms.get('cmd')
    data = request.forms.get('data')
    baud_rate_id = request.forms.get('baud_rate_id')
    status = "failed"

    """
    debug form-data
    """
    # print(cmd)
    # print(data)
    # print(baud_rate_id)

    # clear array
    del response_list[:]
    # release loop, set to false
    loop_unlock = False
    # reset timer and start again
    if(timer_timeout != None):
        if(timer_timeout.is_alive()):
            timer_timeout.cancel()
    # create new time
    timer_timeout = Timer(RESPONSE_TIMEOUT, release_lock)
    timer_timeout.start()

    try :
        if (cmd != ""):
            if (cmd == "voice"):
                if(pcless.send(pcless.voice(data)) == True):
                    while True :
                        if loop_unlock : break
                        if(('¦MTOK©' in response_list) and ('¦PLAYEND©' in response_list)): break
                    status = "ok"
            else :
                if(pcless.send(pcless.format_command(cmd))):
                    time.sleep(0.2)
                    status = "ok"
    except Exception as e :
        logging.error(str(e))
        status = 'failed'

    try :
        rv = { "status": status,"response": response_list }
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