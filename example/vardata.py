#!/bin/python3



#Use tinydb to use JSON based MAC file, if false will just use a flat file
#pip3 install tinydb
useJSON=False

#UniFi Controller info
username="username"
password="password";
controller="10.192.168.192"
mac_file="/home/user/mac.file"

#Prowl API Key, need the pushno package from pip to send Prowl notifications
#pip3 install pushno
send_prowls=True
apikey="123412341234345345345345ABCDABCDABCD1234"


#SMTP Stuff
send_emails=True
sender_email="youruser@gmail.com"
smtp_password="generateapppassword"
receiver_email="youruser@gmail.com"
smtp_server="smtp.gmail.com"
smtp_port="587"

#if needing twilio support you need to install the twilio package from pip
#pip3 install twilio
send_twilio=True
twilio_to="+13038675309"
twilio_from="+16788675309"
twilio_sid="ABDASDF12341234ABDCDAGGHHA12341GGG"
twilio_token="4adf5adf5afdad523fs4gsg23jg2fasd"

