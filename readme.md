# PCLess to webservices
How to run this script<br />
> python .\webserver.py -H 0.0.0.0 -P 80 -ctv "http://admin:Spasi2019@192.168.0.100/ISAPI/Streaming/channels/101/picture" -ctvu "admin" -ctvp "Spasi2019" -pth "F:\\DIY\\SOFTWARE\\udp_forwarder\\captures" -plh 192.168.0.50 -plp 5000
<br />
# HOW TO USAGE
usage: webserver.py [-h] [-H HOSTNAME] [-P PORT] [-plh PCLESS_HOST]
                    [-plp PCLESS_PORT] [-ctv CCTV_URL] [-ctvu CCTV_USER]
                    [-ctvp CCTV_PASS] [-pth PATH]

<br/>
optional arguments: <br />
  -h, --help            show this help message and exit <br />
  -H HOSTNAME, --hostname HOSTNAME Set hostname <br />
  -P PORT, --port PORT  set port <br />
  -plh PCLESS_HOST, --pcless_host PCLESS_HOST set PC less hostname <br />
  -plp PCLESS_PORT, --pcless_port PCLESS_PORT set PC less port <br />
  -ctv CCTV_URL, --cctv_url CCTV_URL Set CCTV URL <br />
  -ctvu CCTV_USER, --cctv_user CCTV_USER Set CCTV user <br />
  -ctvp CCTV_PASS, --cctv_pass CCTV_PASS Set CCTV pass <br />
  -pth PATH, --path PATH Set path <br />