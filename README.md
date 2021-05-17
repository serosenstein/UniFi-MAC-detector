# UniFi-MAC-detector
A utility to run on a *nix system against the UniFi Controller to determine if a previously unknown MAC has been discovered on the network

Pre-reqs:

*Nix system  (needed for curl command because I'm too lazy to write the ProwlAPI call in Python or import a 3rd party library)

An API user created in UniFi Controller as a *LOCAL* Account

The file "vardata.py" should be copied out of the example directory into the main level directory and the variables should be modified to fit your environment


If you plan on using twilio integration you need to install the twilio python package with (or similiar):
pip3 install twilio 
