# UniFi-MAC-detector
A utility to run against the UniFi Controller to determine if a previously unknown MAC has been discovered on the network

You can schedule it in cron or some other utility to run at whatever interval you want

Pre-reqs:

If you want to install all requirements for all features you can do: pip3 install -r requirements.txt

You can also only install the pip modules that you will be using:

If using Twilio you need to install the twilio package from pip: pip3 install twilio

If using Prowl, you will need to install the pushno package from pip: pip3 install pushno

If using tinydb (useJSON=True), you will need to install tinydb package from pip: pip3 install tinydb

If using email, and using Gmail (and probably some other providers), you may need to create an app password if you have 2FA enabled, read more here: https://support.google.com/accounts/answer/185833

An API user created in UniFi Controller as a *LOCAL* Account

The file "vardata.py" should be copied out of the example directory into the main level directory and the variables should be modified to fit your environment

Set whatever kind of notifications you want (email, prowl, twilio) to True or False

You can either save the mac_file as a regular flat file (useJSON=False) or as a JSON encoded file (useJSON=True).
