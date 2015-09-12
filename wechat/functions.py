#encoding:utf-8
from wechat.config import *

from xml.etree.ElementTree import Element
from xml.etree.ElementTree import tostring
from datetime import datetime
from lxml import etree
import httplib2
import time
import random
import string
import hashlib
import json

# xml格式的字符串 ==》 字典
def parse_Xml2Dict(raw_xml):
    xmlstr = etree.fromstring(raw_xml)
    dict_xml = {}
    for child in xmlstr:
        dict_xml[child.tag] = child.text.encode(u'UTF-8')
    return dict_xml

# 字典 ==》 xml格式的字符串
def parse_Dict2Xml(tag, d):
    elem = Element(tag)
    for key, val in d.items():
        child = Element(key)
        child.text=str(val)
        elem.append(child)
    my_str = tostring(elem, encoding=u'UTF-8')
    return my_str

# json样式的str ==> dict
def parse_Json2Dict(my_json):
    my_dict = json.loads(my_json)
    return my_dict

# dict ==> json样式的str
def parse_Dict2Json(my_dict):
    my_json = json.dumps(my_dict, ensure_ascii=False)
    return my_json
	
def my_get(url):
    h = httplib2.Http()
    resp, content = h.request(url, 'GET')
    return resp, content

def my_post(url, data):
    h = httplib2.Http()
    resp, content = h.request(url, 'POST', data)
    return resp, content
	
def get_access_token():
	global WEIXIN_ACCESS_TOKEN
	global WEIXIN_ACCESS_TOKEN_LASTTIME
	global WEIXIN_ACCESS_TOKEN_EXPIRES_IN

	if WEIXIN_ACCESS_TOKEN_LASTTIME == 0 or (int(time.time()) - WEIXIN_ACCESS_TOKEN_LASTTIME > WEIXIN_ACCESS_TOKEN_EXPIRES_IN - 300):
	
		resp, result = my_get(WEIXIN_ACCESS_TOKEN_URL)
		decodejson = parse_Json2Dict(result)
		
		WEIXIN_ACCESS_TOKEN = str(decodejson[u'access_token'])
		WEIXIN_ACCESS_TOKEN_LASTTIME = int(time.time())
		WEIXIN_ACCESS_TOKEN_EXPIRES_IN = decodejson['expires_in']
		
		print "new access_token ->>" + WEIXIN_ACCESS_TOKEN + "---" + str(WEIXIN_ACCESS_TOKEN_LASTTIME) + "---" + str(WEIXIN_ACCESS_TOKEN_EXPIRES_IN)
		return WEIXIN_ACCESS_TOKEN
	else:
		print "old access_token ->>" + WEIXIN_ACCESS_TOKEN + "---" + str(WEIXIN_ACCESS_TOKEN_LASTTIME) + "---" + str(WEIXIN_ACCESS_TOKEN_EXPIRES_IN)
		
		
		return WEIXIN_ACCESS_TOKEN

	'''
	if (WEIXIN_ACCESS_TOKEN == '' and WEIXIN_ACCESS_TOKEN_LASTTIME == '') or (datetime.now() - WEIXIN_ACCESS_TOKEN_LASTTIME > 7200 - 300):
		resp, result = my_get(WEIXIN_ACCESS_TOKEN_URL)
        decodejson = parse_Json2Dict(result)
		global WEIXIN_ACCESS_TOKEN
		WEIXIN_ACCESS_TOKEN = str(decodejson['access_token'])
		WEIXIN_ACCESS_TOKEN_LASTTIME = datetime.now()
        return WEIXIN_ACCESS_TOKEN
	else:
		return WEIXIN_ACCESS_TOKEN
	
    try:
        token = Access_Token.objects.get(id = 1)
    except Access_Token.DoesNotExist:
        resp, result = my_get(WEIXIN_ACCESS_TOKEN_URL)
        decodejson = parse_Json2Dict(result)
		
		WEIXIN_ACCESS_TOKEN = str(decodejson['access_token'])	# 全局变量保存获取的 access_token
		WEIXIN_ACCESS_TOKEN_LASTTIME = datetime.now()			# 记录本次保存的时间
		
        #at = Access_Token(token=decodejson['access_token'],expires_in=decodejson['expires_in'],date=datetime.now())
        #at.save()
        return WEIXIN_ACCESS_TOKEN
    else:
        if (datetime.now() - token.date ).seconds > (token.expires_in-300):
            resp, result = my_get(WEIXIN_ACCESS_TOKEN_URL)
            decodejson = parse_Json2Dict(result)
            Access_Token.objects.filter(id = 1).update(token = decodejson['access_token'],expires_in=decodejson['expires_in'],date=datetime.now())
            return str(decodejson['access_token'])
        else:
            return str(token.token)
	'''