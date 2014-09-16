from django.shortcuts import render,render_to_response

from web01.backend import redis_connector as redis

import json,datetime

from django.http import HttpResponse

# Create your views here.


def index(request):
	return render_to_response('index.html')


def login(request):
	return render_to_response('login.html')


def get_log_data(request):
	log_data = json.loads(redis.conn.get('log'))
	ip_hour_list = sorted(log_data['ip_hour_dic'].items(),key=lambda x:x[0])
	time_list,data_list = [],[]
	for i in ip_hour_list:
		time_list.append(i[0])
		data_list.append(i[1]['total_pv'])
	time_list = map(lambda x: datetime.datetime.fromtimestamp(float(x)).strftime('%H:%M')  , time_list   )
	#uv
	uv = []
	uv.append(log_data['uv'])

	#cache_type
	cache_type_list,cache_data_list = [],[]
	for k in log_data['cache_type_dic'].keys():
		cache_type_list.append(k)
	for v in log_data['cache_type_dic'].values():
		cache_data_list.append(v)

	#http code
	http_code_list,http_data_list = [],[]
	for k in log_data['http_code_dic'].keys():
		http_code_list.append(k)
	for v in log_data['http_code_dic'].values():
		http_data_list.append(v)

	#response_size_sum
	response_size_sum = []
	response_size_sum.append(log_data['response_size_sum'])

	#top url
#	url_title,url_data = [],[]
#	for i in log_data['request_url_list']:
#		for j in i:
#			url_title.append(i)
#			url_data.append(j)

	data_dic = {
		'ip_hour_dic':{
			'time_list':time_list,
			'data_list':data_list
		},
		'uv':uv,
		'cache_type_list':cache_type_list,
		'cache_data_list':cache_data_list,
		'http_type_list':http_code_list,
		'http_data_list':http_data_list,
		'response_size_sum':response_size_sum,
	}

	return HttpResponse(json.dumps(data_dic))

