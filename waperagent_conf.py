#coding=utf-8

default_login = ''
default_password = ''
notifies_cmd = 'notify-send -i /usr/share/icons/hicolor/48x48/apps/distributor-logo.png "Waper Agent" "\xd0\xa3 \xd0\xb2\xd0\xb0\xd1\x81 %s \xd0\xbd\xd0\xb0 \xd1\x83\xd1\x87\xd0\xb5\xd0\xb4\xd0\xba\xd0\xb5 %s\\!"'
graphic_viewer_cmd = 'viewnior "%s"'
notifies_browser_open = 'google-chrome http://waper.ru/office/notify &'
refresh_time = '15'
exclude_topics = '699694,378388'

def init(self):
	global wa_class, exclude_topics
	wa_class = self
	exclude_topics = exclude_topics.split(',')
