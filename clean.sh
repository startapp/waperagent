#!/bin/bash

cat waperagent_conf.py | sed -e "s/default_login = '.*'/default_login = ''/" > waperagent_conf.py.tmp
cat waperagent_conf.py.tmp | sed -e "s/default_password = '.*'/default_password = ''/" > waperagent_conf.py
rm *.tmp *.pyc