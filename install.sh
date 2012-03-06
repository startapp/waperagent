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

function checkdeps {
	C=1
	F=false
	echo -en "Checking for $1...\t"
	while [ ! `echo $PATH | cut -d ":" -f $C | wc -c` = "1" ]; do
		if [ -x `echo $PATH | cut -d ":" -f $C`/$1 ]; then F=true; fi
		if [ $F = 'true' ]; then
			echo "[ ok ]"
			return 0;
		fi
		C=$((C+1))
	done
	echo "[fail]"
	return 1
}

function checkdeps_fail {
	echo -e "Please check failing dependencies. Installation aborted!\n"
	exit 1
}

function checkdeps_success {
	echo -e "Dependencies are OK.\n"
}

function copyfile {
	echo -e "  [CP]\t$1"
	cp `basename $1` $1
}

function installation {
	echo "Installing..."
	echo "Version: `./version.sh`"
	echo -n "Checking for root privileges... "
	if [ $EUID -ne 0 ]; then
		echo -e "[fail]\n\nIn order to install, script must be run with root privileges"
		echo -e 'Try "sudo ./install.sh" or "su -c ./install.sh"'
		exit 1
	else
		echo "[ ok ]"
	fi
	copyfile /usr/bin/nwru-online
	copyfile /usr/bin/nwru-notifies
	copyfile /usr/bin/nwru-guiconfig
	copyfile /usr/share/icons/waper-notifies.png
	copyfile /usr/bin/nwru-send-post
	copyfile /usr/bin/nwru-send-post-hludmode
	copyfile /usr/bin/nwru-answer
	copyfile /usr/bin/nwru-answer-on-all-topics
	copyfile /usr/bin/nwru-answer-on-all-topics-bigmode
	copyfile /usr/bin/nwru-answer-on-all-negativepc-topics
	copyfile /usr/bin/nwru-create-topic
	copyfile /usr/bin/nwru-last-users
	copyfile /usr/bin/nwru-send-msg
	copyfile /usr/bin/nwru-recv-msgs
	copyfile /usr/bin/nwru-read-friendlist
	copyfile /usr/bin/nwru-messager
	copyfile /usr/lib/python${PYVER}/waperagent.py
	copyfile /etc/waperagent_conf.py
	chmod a+r /etc/waperagent_conf.py
	echo "Waperagent has been successfully installed!"
	exit 0
}

DEPS_FAIL=false

if ! checkdeps python; then
	DEPS_FAIL=true
fi

if ! checkdeps notify-send; then
	DEPS_FAIL=true
fi

if [ $DEPS_FAIL = "true" ]; then
	checkdeps_fail
else
	checkdeps_success
	installation
	return 0
fi
