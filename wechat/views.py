#encoding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from wechat.config import *
from wechat.functions import *
import hashlib

# Create your views here.
def index(request):
	# 微信接入参考 http://mp.weixin.qq.com/wiki/17/2d4265491f12608cd170a95559800f2d.html
	if request.method == "GET":
		signature	= request.GET.get("signature")
		timestamp	= request.GET.get("timestamp")
		nonce		= request.GET.get("nonce")
		echostr		= request.GET.get("echostr")
		# 放到数组中按字典序排序
		token		= WEIXIN_TOKEN
		tmp_list 	= [token, timestamp, nonce]
		tmp_list.sort()
		# 把三个字符串拼接在一起进行sha1加密
		tmp_str 		= "%s%s%s" % tuple(tmp_list)
		tmp_str		= hashlib.sha1(tmp_str).hexdigest()
		# 判断与传递进来的 signature 是否一致
		if tmp_str == signature:
			return HttpResponse(echostr)
		else:
			return render(request,'index.html')
	else:
		pass
		
def create_menu(request):
	CREATE_MENU_URL = 'http://www.itcastcpp.cn/user_info/'
	menu_data = {}
	button1 = {}
	button1['name'] = '我的传智历程'
	button1['type'] = 'view'
	button1['url'] = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=' + WEIXIN_APPID + '&redirect_uri=' + CREATE_MENU_URL + '&response_type=code&scope=snsapi_userinfo&state=snsapi_userinfo#wechat_redirect'

	menu_data['button'] = [button1]
	
	post_url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=' + WEIXIN_ACCESS_TOKEN
	post_data = parse_Dict2Json(menu_data)
	resp, content = my_post(post_url, post_data)
	response = parse_Json2Dict(content)
	
	if response['errcode'] == 0:
		return HttpResponse('create menu OK.')
	else:
		return HttpResponse('create menu err:' + response['errmsg'])


def user_info(request):
	get_access_token()
	return render(request, 'index.html')