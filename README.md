# UniFi-MAC-detector
A utility to run against the UniFi Controller to determine if a previously unknown MAC has been discovered on the network

You can schedule it in cron or some other utility to run at whatever interval you want

Pre-reqs:

If using Twilio you need to install the twilio package from pip: pip install twilio (or pip3 or whatever)

If using Prowl, you will need to install the pushno package from pip: pip install pushno

If using email, and using Gmail (and probably some other providers), you may need to create an app password if you have 2FA enabled, read more here: https://support.google.com/accounts/answer/185833

An API user created in UniFi Controller as a *LOCAL* Account

The file "vardata.py" should be copied out of the example directory into the main level directory and the variables should be modified to fit your environment

Set whatever kind of notifications you want (email, prowl, twilio) to True or False

You can either save the mac_file as a regular flat file (useJSON=False) or as a JSON encoded file (useJSON=True).  If you do decide to use JSON you will also need the tinydb package installed:
pip3 install tinydb
