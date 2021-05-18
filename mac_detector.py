#!/bin/python3
#Steve Rosenstein serosenstein@gmail.com
#UniFi Controller New Mac Detector and Alerter
#Make sure you have vardata.py in the same directory as this script or hardcode values below
#5-16-2021
import requests
from tinydb import TinyDB, Query, where
import os
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

#send_prowls will determine if you actually will send out the alerts or just say that you would have, good for debugging and now spamming yourself
send_prowls = vardata.send_prowls
send_emails = vardata.send_emails
send_twilio = vardata.send_twilio
useJSON = vardata.useJSON
#Set this to nothing before we use it later as a global var, probably not the right way to do this
info_string = ""
json_string = ""

#Set all the variable data from vardata.py, you could just hard code them in here too
username = vardata.username
password = vardata.password
controller = vardata.controller
mac_file = vardata.mac_file
if send_prowls:
  apikey = vardata.apikey
  if not [x for x in (apikey) if x is None]:
    pass
  

if send_emails:
  import smtplib, ssl
  sender_email = vardata.sender_email
  smtp_password = vardata.smtp_password
  receiver_email = vardata.receiver_email
  smtp_server = vardata.smtp_server
  smtp_port = vardata.smtp_port
  if not [x for x in (sender_email,smtp_password,receiver_email,smtp_server,smtp_port) if x is None]:
    pass

#Make sure all of the variables are set
if not [x for x in (username, password, controller, mac_file, useJSON) if x is None]:
    pass
if not os.path.isfile(mac_file):
    print ("File does not exist, creating")
    with open(mac_file, 'w') as fp:
      pass

file_object = open(mac_file, 'a')
filesize = os.path.getsize(mac_file)
if filesize != 0 and useJSON:
  try:
   f = open(mac_file)
   json.load(f)
  except ValueError as err:
    exit("Your mac_file " + mac_file + " is not valid, if you tried to switch from non-JSON to JSON you will need to delete the file and let it get recreated")

#Get list of MACs from UniFi Controller
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
headers = {"Accept": "application/json","Content-Type": "application/json"}
data = {'username': username, 'password': password}
s = requests.Session()
#Start a session and get the auth, then list all MACs
r = s.post("https://" + controller + "/api/auth/login", headers = headers,  json = data , verify = False, timeout = 1)
status_code = str(r.status_code)
if status_code != "200":
  exit("Return code for Auth was " + status_code)
data = s.get("https://" + controller + "/proxy/network/api/s/default/stat/sta/", headers = headers, verify = False, timeout = 1).text
json_data = json.loads(data)
def SendTwilio(info):
  from twilio.rest import Client
  twilio_to = vardata.twilio_to 
  twilio_from = vardata.twilio_from
  twilio_sid = vardata.twilio_sid
  twilio_token = vardata.twilio_token
  if not [x for x in (twilio_to,twilio_sid,twilio_token) if x is None]:
    pass
  client = Client(twilio_sid, twilio_token)
  message = client.messages \
                .create(
                     body=info,
                     from_=twilio_from,
                     to=twilio_to)
def SendEmail(info):
 message = "From: " + sender_email + "\n"
 message = str(message) + "To: " + receiver_email + "\n"
 message = str(message) + "Subject: UniFi-Mac-Detector: New Device Alert\n"
 message = str(message) + "\n" + str(info) + "\n"
 print(message)
 try:
  context = ssl.create_default_context()
  with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
    server.login(sender_email, smtp_password)
    server.sendmail(sender_email, receiver_email, message)
  #debug comment
  #print("sending email to " + receiver_email + " with this info " + info)
 except:
  print("Error sending email: " + sys.exc_info()[0]) 
  raise
def SendProwl(info):
 from pushno import PushNotification
 pn = PushNotification(
     "prowl", api_key=apikey, application="UniFi MAC Detector"
 )
 is_valid, res = pn.validate_user()
 if is_valid:
     pn.send(event="New UniFi MAC detected", description=info)
 else:
     print(res)
def UpdateMacFileJSON(json_string):
  insert_query = eval(json_string)
  db = TinyDB(mac_file, sort_keys=True, indent=4, separators=(',', ': '))
  table = db.table('clients')
  table.insert(insert_query)
  db.all()

def UpdateMacFile(info_string):
  print("Appending: " + info_string + " to " + mac_file)
  file_object = open(mac_file, 'a')
  filesize = os.path.getsize(mac_file)
  if filesize != 0:
    with open(mac_file) as f:
      lines = f.readlines()
      last = lines[-1]
      for line in lines:
          if line is last and "\n" not in line:
            file_object.write('\n')
  #make sure the current last line ends with a newline
  file_object.write(info_string)
  file_object.write('\n')
  file_object.close()
def CheckMacExists(mac):
  with open(mac_file, 'r') as file:
    for line in file:
      if mac in line.split():
        return True
    else:
       print(mac + " does not exist")
       if send_prowls:
         SendProwl(GetMacInfo(mac))
       if send_emails:
         SendEmail(GetMacInfo(mac))
       if send_twilio:
         SendTwilio(GetMacInfo(mac))
       macInfo, jsonInfo = GetMacInfo(mac)
       print(macInfo.replace('\n', ' '))
       UpdateMacFile(macInfo.replace('\n', ' '))
      
       #UpdateMacFile(GetMacInfo(mac).replace('\n', ' '))

def CheckMacExistsJSON(mac):
  db = TinyDB(mac_file)
  table = db.table('clients')
  try: 
    result = table.search(where("MAC").matches(mac))
    if not result:
     print(mac + " does not exist")
     info_string, json_string = GetMacInfo(mac)
     json_string = json_string.rstrip(",")
     json_string = "{" + json_string + "}"
     if send_prowls:
       SendProwl(info_string)
     if send_emails:
       SendEmail(info_string)
     if send_twilio:
       SendTwilio(info_string)
     UpdateMacFileJSON(json_string)
  except IndexError:
    pass

def GetMacInfo(mac):
  global info_string
  global json_string 
  info_string = ""
  json_string = ""
  macInfo = s.get("https://" + controller + "/proxy/network/api/s/default/stat/user/" + mac, headers = headers, verify = False, timeout = 1).text   
  Mac_json = json.loads(macInfo)
  for item in Mac_json["data"]:
    try:
        mac = item['mac']
        if(mac):
          info_string = str(info_string) + "MAC: " + mac + "\n"
          json_string = json_string + "'MAC': '" + mac + "',"
    except:
        pass
    try:
        hostname = item['hostname']
        if(hostname):
          info_string = str(info_string) + "Hostname: " + hostname + "\n"
          json_string = json_string + "'Hostname': '" + hostname + "',"
    except:
        pass
    try:
        oui = item['oui']
        if(oui):
          info_string = str(info_string) + "OUI: " + oui + "\n"
          json_string = json_string + "'OUI': '" + oui + "',"
    except:
        pass
    try:
        is_guest = item['is_guest']
        if(is_guest):
          info_string = str(info_string) + "Is Guest: " + is_guest + "\n"
          json_string = json_string + "'Guest': '" + guest + "',"
    except:
        pass
    try:
        is_wired = item['is_wired']
        if(is_wired):
          info_string = str(info_string) + "Is Wired: " + is_wired + "\n"
          json_string = json_string + "'Wired': '" + wired + "',"
    except:
        pass
    try:
        essid = item['essid']
        if(essid):
          info_string = str(info_string) + "SSID: " + essid + "\n"
          json_string = json_string + "'SSID': '" + essid + "',"
    except:
        pass
    try:
        ip = item['ip']
        if(ip):
          info_string = str(info_string) + "IP: " + ip + "\n"
          json_string = json_string + "'IP': '" + ip + "',"
    except:
        pass
    try:
        vlan = item['vlan']
        if(vlan):
          info_string = str(info_string) + "VLAN: " + vlan + "\n"
          json_string = json_string + "'VLAN': '" + vlan + "',"
    except:
        pass
  return(info_string,json_string)

for item in json_data["data"]:
    mac = item['mac']
    if mac:
        if not useJSON: 
          CheckMacExists(mac)
        else:
          CheckMacExistsJSON(mac)
