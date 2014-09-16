#!/usr/bin/env python

import tab
import redis_connector as redis
import json

def handle(fname):
	f = file(fname)
	hour_end_time = float(f.readline().split()[0]) + 3600
	ip_hour_dic = {hour_end_time:{'total_pv':0}}
	uv_dic = {}
	cache_type_dic = {}
	http_code_dic = {}
	url_dic = {}
	for line in f.xreadlines():
		line = line.split()
		access_time,raw_ip,cache_type,response_size,url = float(line[0]),line[2],line[3],line[4],line[10]
		#handle pv	
		if access_time < hour_end_time:
			ip_hour_dic[hour_end_time]['total_pv'] += 1
		else:
			hour_end_time += 3600
			ip_hour_dic[hour_end_time] = {'total_pv':1}
			

		#handle uv
		if uv_dic.has_key(raw_ip):
			uv_dic[raw_ip] += 1
		else:
			uv_dic[raw_ip] = 1	
	
		
		#handle cache_type
		cache_type = line[3].split('/')[0]
		if cache_type_dic.has_key(cache_type):
			cache_type_dic[cache_type] += 1
		else:
			cache_type_dic[cache_type] = 1

		
		#handle http code
		http_code = line[3].split('/')[1]
		if http_code_dic.has_key(http_code):
			http_code_dic[http_code] += 1
		else:
			http_code_dic[http_code] = 1


		#handle response_size
		response_size_sum = int((response_size + response_size))/1024/1024

		#handle url
		if url_dic.has_key(url):
			url_dic[url] += 1
		else:
			url_dic[url] =1

	sorted_url_list = sorted(url_dic.items(), key=lambda x:x[1], reverse=True)[:30]


	result_dic = {
		'ip_hour_dic':ip_hour_dic,
		'uv':len(uv_dic),
		'cache_type_dic':cache_type_dic,
		'http_code_dic':http_code_dic,
		'response_size_sum':response_size_sum,
		'request_url_list':sorted_url_list
	}

	return result_dic

if __name__ == '__main__':
	result=handle('log25w.log')
	redis.conn['log'] = json.dumps(result)
	print result
