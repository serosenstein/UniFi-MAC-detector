# UniFi-MAC-detector
A utility to run on a *nix system against the UniFi Controller to determine if a previously unknown MAC has been discovered on the network

Pre-reqs:
*Nix system  (needed for curl command because I'm too lazy to write the ProwlAPI call in Python or import a 3rd party library)
An API user created in UniFi Controller as a *LOCAL* Account
vardata.py in the same directory as mac_detector.py. It should contain all variables, here is an example:

#!/bin/python3
username="APIUSER";
password="APIPASSWORD";
controller="1.2.3.4"
mac_file="/path/to//mac.file.txt"
apikey="123412341234ABCDEFG123412341234657891034"
