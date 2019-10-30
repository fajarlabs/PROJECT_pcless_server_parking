# PCLess to webservices<br />
Create table ticket_log first in postgresql<br/>
file sql -> ticket_log.sql <br />
<br />
How to run this script<br />
> python .\webserver.py -H 0.0.0.0 -P 80 -ctv "http://admin:Spasi2019@192.168.0.100/ISAPI/Streaming/channels/101/picture" -ctvu "admin" -ctvp "Spasi2019" -pth "F:\\DIY\\SOFTWARE\\udp_forwarder\\captures" -plh 192.168.0.50 -plp 5000 -htm "TRANSMART" -ttm "Jl. Raya Pancoran Mas"
<br />
# HOW TO USAGE <br />
usage: webserver.py [-h] [-H HOSTNAME] [-P PORT] [-plh PCLESS_HOST]
                    [-plp PCLESS_PORT] [-ctv CCTV_URL] [-ctvu CCTV_USER]
                    [-ctvp CCTV_PASS] [-pth PATH]

<br />
optional arguments: <br /><br />
  -h, --help            show this help message and exit <br />
  -H HOSTNAME, --hostname HOSTNAME Set hostname <br />
  -P PORT, --port PORT  set port <br />
  -plh PCLESS_HOST, --pcless_host PCLESS_HOST set PC less hostname <br />
  -plp PCLESS_PORT, --pcless_port PCLESS_PORT set PC less port <br />
  -ctv CCTV_URL, --cctv_url CCTV_URL Set CCTV URL <br />
  -ctvu CCTV_USER, --cctv_user CCTV_USER Set CCTV user <br />
  -ctvp CCTV_PASS, --cctv_pass CCTV_PASS Set CCTV pass <br />
  -pth PATH, --path PATH Set path <br />
  -htm HEADER_THERMAL, --header_thermal HEADER_THERMAL Set top header ticket <br />
  -ttm TITLE_THERMAL, --title_thermal TITLE_THERMAL Set title thermal <br /><br />

for windows executable <br />
cd /output/webserver <br />
> webserver.exe -H 0.0.0.0 -P 80 -ctv "http://admin:Spasi2019@192.168.0.100/ISAPI/Streaming/channels/101/picture" <br />
-ctvu "admin" -ctvp "Spasi2019" -pth "F:\\DIY\\SOFTWARE\\udp_forwarder\\captures" -plh 192.168.0.50 -plp 5000 -htm "TRANSMART" -ttm "Jl. Raya Pancoran Mas"

<br />
<br />
#POSTMAN<br/>
<img src="https://i.ibb.co/T45Nkvp/how-request.jpg" />
<br />
#SAMPLE TICKET<br />
<img width="200" height="100" src="https://i.ibb.co/SrRSSss/Whats-App-Image-2019-10-29-at-09-10-47.jpg" /><br />
#TABLE TICKET_LOG
<img width="200" height="100" src="https://i.ibb.co/R4dh325/table-ticket.jpg" />
<br />
#GATEOUT
<img width="200" height="100" src="https://i.ibb.co/swKW9nM/gateout.jpg" />
