import json,urllib2


def get_region(url):
	#res = urllib2.Request(url)
	result = urllib2.urlopen(url)
	region_dic = json.loads(result.read())

	print region_dic['data']['area']
	print region_dic['data']['region']
	print region_dic['data']['city']



get_region('http://ip.taobao.com/service/getIpInfo.php?ip=112.224.19.48')
