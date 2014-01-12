#!/usr/bin/env python
#coding=utf8

from curl import *
import pycurl
import sys
import os
import re


class ReceivedMessage:
    def __init__(self, time, from_id, from_login, text):
        self.time = time;
        self.from_id = from_id;
        self.from_login = from_login;
        self.text = text;
    def __str__(self):
        return self.from_login+'['+self.time+']'+'> '+self.text;
    def __repr__(self):
        return str(self);

class User:
    def __init__(self, uid, login):
        self.uid = uid;
        self.login = login;
    def __str__(self):
        return 'User '+self.login+' ['+self.uid+']';
    def __repr__(self):
        return str(self);


class WaperAgentCannotAuth(Exception):
    pass;

class WaperAgentCannotLoadConfig(Exception):
    pass;
    
class WaperAgentCannotSendPost(Exception):
    pass;

class WaperAgent(Curl):
    def ask_captcha(self, pg):
        cimg = re.findall(r'/login/captcha_[0-9]+\.jpg', pg)[0];
        f = open('cimg.jpg', 'w');
        f.write(self.get('http://waper.ru'+cimg));
        f.close();
        os.popen(self.config.graphic_viewer_cmd%'cimg.jpg' + ' &');
        return raw_input('CAPTCHA> ');
    def init(self):
        sys.path += [os.path.expanduser('~/'), '/etc'];
        self.config = __import__('waperagent_conf');
        try:
            self.config.init(self);
        except:
            pass
    def auth(self, login='', passwd='', captcha=''):
        if login == '' or passwd == '':
            login = self.config.default_login;
            passwd = self.config.default_password;
        if captcha=='':
            res = self.post("http://waper.ru/login/", {'u_login': login, 'u_passwd': passwd});
        else:
            res = self.post("http://waper.ru/login/", {'u_login': login, 'u_passwd': passwd, 'u_code': captcha});
        #print res
        if res.find('ошибка')!=1 and res.find('ошибки')!=-1:
            #sys.stderr.write('ERROR!\n\n\n'+str(res));
            return self.auth(login, passwd, self.ask_captcha(res));
        rr = re.compile(r'<a href="/user/([0-9]+).*?">Моя анкета</a>', re.DOTALL);
        fnd = rr.findall(res);
        #print fnd;
        self.uid = fnd[0];
    def post_to_forum(self, topicid, text, num=0):
        res = self.post('http://waper.ru/office/group/forum/write/?id='+str(topicid), {'_h': 'ю', 'text': text, 'send': 'Отправить'});
        if (res.find('Ошибка') !=-1) or (res.find('ошибка') !=-1) or (res.find('ОШИБКА') !=-1) or (res.find('не участвуете') !=-1):
            raise WaperAgentCannotSendPost;
        if num != 0: print 'Post #'+str(num)+' sent';
    def answer_in_forum(self, pid, text, num=0):
        res = self.get('http://waper.ru/r/p.r/?pid='+str(pid));
        #print res;
        if (res.find('Ошибка') !=-1) or (res.find('ошибка') !=-1) or (res.find('ОШИБКА') !=-1) or (res.find('не участвуете') !=-1):
            raise WaperAgentCannotSendPost;
        regex = re.compile(r'\/office\/group\/forum\/write\/\?id=([0-9]+)\&amp\;uid=([0-9]+)\&amp\;pid\=([0-9]+)');
        target=regex.findall(res)[0];
        res = self.post('http://waper.ru/office/group/forum/write/?id='+target[0]+'&uid='+target[1]+'&pid='+target[2], {'_h': 'ю', 'text': text, 'private':'0', 'send': 'Отправить'});
        #print res;
        if num != 0: print 'Post #'+str(num)+' sent';
    def create_topic(self, forumid, topic, text, num=0):
        try: res = self.post('http://waper.ru/office/group/forum/write/?fid='+str(forumid), {'_h': 'ю', 'subj': topic, 'text': text, 'send': 'Отправить'});
        except: return
        if res.find('Ошибка')!=-1:
            sys.stderr.write('ERROR!\n\n\n'+str(res));
            raise WaperAgentCannotSendPost;
        if num != 0: print 'Topic #'+str(num)+' sent';
    def count_pages(self, page):
        res = self.get(page);
        regex = re.compile(r'page=([0-9]+)">[0-9]+</a>(?:</div>|<br/>)', re.DOTALL);
        rr = regex.findall(res);
        #print rr;
        if(len(rr)==0): return 1;
        return int(rr[0]);
    def get_online_users(self):
        res = self.get_full('http://waper.ru/user/online', mode='?');
        regex = re.compile(r'/user/([0-9]+)');
        return regex.findall(res);

    def get_full(self, url, mode='&', args={}):
        cp = self.count_pages(url);
        res = '';
        for i in xrange(1, cp+1):
            sys.stderr.write('Getting page #%s\n'%i)
            if mode==0:
                args.update({'page':str(i)});
                res += self.get(url, args);
            else:
                res += self.get(url+mode+'page='+str(i), args);
        #print res;
        return res;
    def get_all_topics_ids(self, forumid):
        res = self.get('http://waper.ru/forum/'+str(forumid));
        #print res;
        regex = re.compile(r'<a href="/forum/topic/([0-9]+)">(.+)</a>');
        rr = regex.findall(res);
        if(len(rr)==0): return 1;
        return rr;

    def __check(self, tmp, regex):
        _regex = re.compile(regex);
        res = _regex.findall(tmp);
        if len(res)==1:
            return 1;
        else: return 0;

    def _check(tmp):
        if self.__check(tmp, r'[0-9]+ ответ[а-я]*') or self.__check(tmp, r'[0-9]+ сообщени[а-я]*'): return 1;
        else: return 0;

    def checknewmsg(self):
        tmp = self.get('http://waper.ru/office/');
        return self._check(tmp);

    def getnewmsg(self, *args):
        return self.getnewmsg_forum(*args);
    def getnewmsg_forum(self):
        tmp = self.get('http://waper.ru/office/notify/');
        #print tmp;
        regex = re.compile(r'/forum/post/[0-9]+');
        url = 'http://waper.ru'+regex.findall(tmp)[0];
        res = self.get(url);
        #print res;
        regex = re.compile(r'<div class="r.h"?">.*?<a name="(.*?)">.*?<a href="/user/.*?">(.*?)</a>.*?<div>(.*?)</div>', re.DOTALL);
        post = regex.findall(res)[0];
        #print post;
        return post;
    def user_find(self, login):
        try:
            return int(login);
        except:
            res = self.get('http://waper.ru/user/search?ageFrom=&ageTo=&sex=0&lo=0&sort=0', {'login':login, 'ageFrom':'0', 'ageTo':'0', 'sex':'0', 'lo':'0', 'sort':'0'});
            #print res;
            regex = re.compile(r'<a href="/user/([0-9]+)">'+login+'</a>', re.DOTALL);
            rr = regex.findall(res);
            #print rr;
            return rr[0];
    def send_privmsg(self, to, text):
        uid = self.user_find(to);
        res = self.post('http://waper.ru/office/talk/outbox/say.php?id='+str(uid)+'&amp;r=0&amp;mid=0', {'_h':'!', '_h':'ю', 'text':text, 'send':'Отправить'});
    def recv_privmsg(self, full=0):
        if full:
            res = self.get_full('http://waper.ru/office/talk/inbox/');
        else:
            res = self.get('http://waper.ru/office/talk/inbox/');
        regex = re.compile(r'<div class="msgh"><small class="info">(.*?)</small>, <a href="/user/(.*?)">(.*?)</a>.*?<div class="body">(.*?)<br/><small>.*?</div>', re.DOTALL);
        msgs = regex.findall(res);
        msgs.reverse();
        msgobjs = [];
        for m in msgs:
            msgobjs.append(ReceivedMessage(*m));
        return msgobjs;

    def read_friends(self, uid=0):
        if uid==0: uid=self.uid;
        uid = self.user_find(uid);
        res = self.get_full('http://waper.ru/user/friend/?id='+str(uid));
        regex = re.compile(r'<a href="/user/([0-9]+)">(.*?)</a><br/>', re.DOTALL);
        friends = regex.findall(res);
        userobjs = [];
        for f in friends:
            userobjs.append(User(*f));
        return userobjs;

    def post_to_chat(self, chatid, text, num=0):
        try: res = self.post('http://waper.ru/office/group/chat/say.php?id='+str(chatid)+'&uid=0', {'text': text});
        except: return
        if res.find('Ошибка')!=-1:
            sys.stderr.write('ERROR!\n\n\n'+str(res));
            raise WaperAgentCannotSendPost;
        if num != 0: print 'Post #'+str(num)+' sent';

    def read_topic(self, id):
        res = self.get_full('http://waper.ru/forum/topic/%s'%id, 0)
        regex = re.compile(r'<div class="r.h?"?">.*?<a name="(.*?)">.*?<a href="/user/.*?">(.*?)</a>.*?<span class=".*?">(\d{2}.\d{2}.\d{4} \d{2}:\d{2})</span>.*?<div>(.*?)</div>', re.DOTALL);
        posts = regex.findall(res);
        return posts;
    def topic_info(self, id): 
        res = self.get('http://waper.ru/forum/topic/%s'%id)
        regex1 = re.compile(r'<div class="tp"><a href="/group/.*?">(.*?)</a></div>.*?<div class="tpanel"><small><a href="/forum/.*?">(.*?)</a>.*?\|(.*?)</small><br/></div>.*?<a href="/user/.*?">(.*?)</a>', re.DOTALL)
        #print regex1.findall(res)[0]
        #print len(regex1.findall(res)[0])
        (groupname, forumname, topicname, author) = regex1.findall(res)[0]
        pages = self.count_pages('http://waper.ru/forum/topic/%s'%id)
        return groupname, forumname, topicname, author, pages
