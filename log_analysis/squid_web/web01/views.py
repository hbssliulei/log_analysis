import datetime
from django.shortcuts import render, render_to_response
from web01.backend import redis_connector as redis
import json
from django.http import HttpResponse


# Create your views here.


def index(request):
	

	return render_to_response('index.html')


def get_squid_log(request):
	squid_data = json.loads(redis.r.get('SQUID_LOG'))
	ip_hour_list = sorted(squid_data['ip_hour_dic'].items(), key=lambda x: x[0])
	print ip_hour_list
	time_list, data_list = [],[]
	
	for i in ip_hour_list:
		time_list.append(i[0])
		data_list.append(i[1]['total_pv'])
	time_list = map(lambda x: datetime.datetime.fromtimestamp(float(x)).strftime('%H:%M')  , time_list   )
	#hand pie 
	pie_list = []	
	for k,v in squid_data['cache_type_dic'].items():
		pie_list.append([k,v])
	data_dic = {
		'column_g':{
			'time_list': time_list,
			'data_list': data_list},
		'pie_g': pie_list
	}		
	
	return HttpResponse(  json.dumps(data_dic)  )

 
