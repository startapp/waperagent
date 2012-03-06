#!/bin/bash

PYVER='2.6'

python --version 2> ~/.pyver
PYVER=`cat ~/.pyver | grep -o 2\.[0-9]`
rm ~/.pyver

function help_usage {
	echo -e "Usage: ./instal.sh [-p python2-version] [-h]"
	exit 0;
}

while getopts hp: option
do
	case $option in
		h) help_usage ;;
		p) PYVER=$OPTARG ;;
		?) help_usage ;;
	esac
done

function removefile {
	echo -e "  [RM]\t$1"
	rm $1
}

function uninstallation {
	echo "Uninstalling..."	
	echo "Version: `./version.sh`"
	echo -n "Checking for root privileges... "
	if [ $EUID -ne 0 ]; then
		echo -e "[fail]\n\nIn order to install, script must be run with root privileges"
		echo -e 'Try "sudo ./uninstall.sh" or "su -c ./uninstall.sh"'
		exit 1
	else
		echo "[ ok ]"
	fi
	removefile /usr/bin/nwru-online
	removefile /usr/bin/nwru-notifies
	removefile /usr/bin/nwru-guiconfig
	removefile /usr/share/icons/waper-notifies.png
	removefile /usr/bin/nwru-send-post
	removefile /usr/bin/nwru-send-post-hludmode
	removefile /usr/bin/nwru-answer
	removefile /usr/bin/nwru-answer-on-all-topics
	removefile /usr/bin/nwru-answer-on-all-topics-bigmode
	removefile /usr/bin/nwru-answer-on-all-negativepc-topics
	removefile /usr/bin/nwru-create-topic
	removefile /usr/bin/nwru-last-users
	removefile /usr/bin/nwru-recv-msgs
	removefile /usr/bin/nwru-send-msg
	removefile /usr/bin/nwru-read-friendlist
	removefile /etc/waperagent_conf.py
	removefile /usr/lib/python${PYVER}/waperagent.py
	echo "Waperagent has been successfully uninstalled!"
	exit 0
}

uninstallation
return 0
