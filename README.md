# UniFi-MAC-detector
A utility to run on a *nix system against the UniFi Controller to determine if a previously unknown MAC has been discovered on the network

Pre-reqs:

If using Twilio you need to install the twilio package from pip: pip install twilio (or pip3 or whatever)

If using Prowl, you will need to install the pushno package from pip: pip install pushno

An API user created in UniFi Controller as a *LOCAL* Account

The file "vardata.py" should be copied out of the example directory into the main level directory and the variables should be modified to fit your environment

Set whatever kind of notifications you want (email, prowl, twilio) to True or False
