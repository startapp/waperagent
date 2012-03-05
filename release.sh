#!/bin/bash

mkdir waperagent-`./version.sh`
cp * waperagent-`./version.sh`
cat waperagent/waperagent_conf.py | sed -e "s/default_login = '.*'/default_login = ''/" > waperagent-`./version.sh`/waperagent_conf.py.tmp
cat waperagent/waperagent_conf.py.tmp | sed -e "s/default_password = '.*'/default_password = ''/" > waperagent-`./version.sh`/waperagent_conf.py
rm waperagent-`./version.sh`/*.tmp waperagent-`./version.sh`/*.pyc
rm waperagent/waperagent-`./version.sh`.tar.gz
tar -cvzf releases/waperagent-`./version.sh`.tar.gz waperagent-`./version.sh`
rm -rf waperagent-`./version.sh`
