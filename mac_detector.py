#!/bin/python3
#Steve Rosenstein serosenstein@gmail.com
#UniFi Controller New Mac Detector and Alerter
#Make sure you have vardata.py in the same directory as this script or hardcode values below
#5-16-2021
import requests
import os
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import vardata

#send_prowls will determine if you actually will send out the alerts or just say that you would have, good for debugging and now spamming yourself
send_prowls=True
#Set this to nothing before we use it later as a global var, probably not the right way to do this
info_string = ""

#Set all the variable data from vardata.py, you could just hard code them in here too
username = vardata.username
password = vardata.password
controller = vardata.controller
mac_file = vardata.mac_file
apikey = vardata.apikey

#Make sure all of the variables are set
if not [x for x in (username, password, controller, mac_file, apikey) if x is None]:
    pass

#Get list of MACs from UniFi Controller
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
headers = {"Accept": "application/json","Content-Type": "application/json"}
data = {'username': username, 'password': password}
s = requests.Session()
#Start a session and get the auth, then list all MACs
r = s.post("https://" + controller + "/api/auth/login", headers = headers,  json = data , verify = False, timeout = 1)
data = s.get("https://" + controller + "/proxy/network/api/s/default/stat/sta/", headers = headers, verify = False, timeout = 1).text
json_data = json.loads(data)

def SendProwl(info):
 cmd="curl https://prowl.weks.net/publicapi/add -F apikey=" + apikey + " -F application='UniFi' -F priority=1 -F event='NEW DEVICE ON NETWORK' -F description='NEW DEVICE: " + info + "'"
 if send_prowls:
   try:
     os.system(cmd)
   except:
    print("Error sending prowl") 
 else:
   print("Sending Prowls disabled, but would have sent: " + cmd)

def UpdateMacFile(mac):
  print("Appending MAC: " + mac + " to " + mac_file)
  file_object = open(mac_file, 'a')
  file_object.write(mac)
  file_object.write('\n')
  file_object.close()

def CheckMacExists(mac):
  with open(mac_file, 'r') as file:
    for line in file:
      if mac in line.split():
        return True
    else:
       print(mac + " does not exist")
       SendProwl(GetMacInfo(mac))
       UpdateMacFile(mac)

def GetMacInfo(mac):
  print("called getMacInfo with " + mac)
  global info_string
  info_string = ""
  macInfo = s.get("https://" + controller + "/proxy/network/api/s/default/stat/user/" + mac, headers = headers, verify = False, timeout = 1).text   
  Mac_json = json.loads(macInfo)
  for item in Mac_json["data"]:
    try:
        hostname = item['hostname']
        info_string = str(info_string) + "Hostname: " + hostname + " "
    except:
        pass
    try:
        mac = item['mac']
        info_string = str(info_string) + "MAC: " + mac + " "

    except:
        pass
    try:
        oui = item['oui']
        info_string = str(info_string) + "OUI: " + oui + " "

    except:
        pass
    try:
        is_guest = item['is_guest']
        info_string = str(info_string) + "Is Guest: " + is_guest + " "

    except:
        pass
    try:
        is_wired = item['is_wired']
        info_string = str(info_string) + "Is Wired: " + is_wired + " "

    except:
        pass
    try:
        essid = item['essid']
        info_string = str(info_string) + "SSID: " + essid + " "

    except:
        pass
    try:
        ip = item['ip']
        info_string = str(info_string) + "IP: " + ip + " "

    except:
        pass
    try:
        vlan = item['vlan']
        info_string = str(info_string) + "VLAN: " + vlan + " "

    except:
        pass
  return(info_string)

for item in json_data["data"]:
    mac = item['mac']
    if mac:
        CheckMacExists(mac)
