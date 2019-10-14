def get_all_device():
	result = []
	with open("devices.txt", 'r') as f:
		for line in f:
			config = {}
			line = str(line.rstrip())
			ip, port = line.split(":")
			config["ip"] = ip
			config["port"] = int(port)
			result.append(config)

	return result
