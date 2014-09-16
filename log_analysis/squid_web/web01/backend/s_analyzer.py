import json
import threading 
import redis_connector as redis
#import get_ip_source

def handle(fname):
	f = file(fname)
	hour_end_time = float(f.readline().split()[0]) + 3600 
	ip_hour_dic = { hour_end_time : {'total_pv': 0 }  }
	uv_dic = {}
	region_dic = {}
	cache_type_dic = {}
	for line in f.xreadlines():
		line = line.split()
 		access_time,raw_ip , cache_type, response_size,request_url,content_type,MIME_content_type= float(line[0]) ,line[2], line[3],line[4],line[6],line[9],line[11]
		if access_time < hour_end_time : # put this record into this time period 
			ip_hour_dic[hour_end_time]['total_pv'] +=1 
			
		else:
			hour_end_time +=3600 
			ip_hour_dic[hour_end_time] = {'total_pv': 1}
			print hour_end_time
		# handle uv 
		if uv_dic.has_key(raw_ip):
			uv_dic[raw_ip] +=1
		else: 
			uv_dic[raw_ip] = 1
		#handle region ranking 
		internet_ip, intranet_ip = raw_ip.split('/')
		region_ip = '.'.join(internet_ip.split('.')[:2])
		if region_dic.has_key(region_ip):
			region_dic[region_ip][0] += 1
		else :
			region_dic[region_ip] = [1, internet_ip]
		#handle squid request status
		cache_type = cache_type.split('/')[0] 
		if cache_type_dic.has_key(cache_type):
			cache_type_dic[cache_type] +=1
		else:
			cache_type_dic[cache_type] = 1


	print ip_hour_dic
	print len(uv_dic)
	print 'InternetIP : ', len(region_dic)
	print 'Cache types:', cache_type_dic
	sorted_region_list = sorted(region_dic.items(), key=lambda x:x[1][0], reverse=True)[:100]
	"""for i in sorted_region_list:
		#get all regions
		url = 'http://ip.taobao.com/service/getIpInfo.php?ip=%s' % i[1][1] 
		print url
		p=threading.Thread(target=get_ip_source.get_region, args=(url,) )
		p.start()
	"""

	result_dic = {
		'ip_hour_dic' : ip_hour_dic,
		'cache_type_dic': cache_type_dic
	}

	return result_dic




if __name__ == '__main__':
	result = handle('log25w.log')			
	#result = handle('/usr/local/squid/var/logs/squid_access.log')			
	redis.r['SQUID_LOG'] =  json.dumps(result)
	#handle('../squid_access.log')			
