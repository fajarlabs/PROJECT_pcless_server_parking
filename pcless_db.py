#!/usr/bin/python

import psycopg2
import configparser
import logging

def get_ini():
	try :
		config = configparser.ConfigParser()
		config.read('database.ini')
		return {
			"hostname" : str(config['DATABASE']['hostname']),
			"port" : int(config['DATABASE']['port']), 
			"username" : str(config['DATABASE']['username']), 
			"password" : str(config['DATABASE']['password']),
			"database" : str(config['DATABASE']['database'])
		}
	except Exception as e :
		logging.error(str(e))

def add_ticket(uuid, image):
	config = get_ini()
	try :
		conn = psycopg2.connect(host=config["hostname"],
		                        port=config["port"],
		                        user=config["username"],
		                        password=config["password"],
		                        database=config["database"])

		cursor = conn.cursor()
		cursor.execute("INSERT INTO ticket_log (id, image) VALUES(%s, %s)", (uuid, image))
		conn.commit()
		cursor.close()
		conn.close()
	except Exception as e:
		logging.error(str(e))

if __name__ == "__main__" :
	add_ticket("FFFDDSJFJD123342", "contoh.png")