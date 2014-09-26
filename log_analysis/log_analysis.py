#!/usr/bin/env python
import time
import sys
if len(sys.argv) < 4:
    print '''Use: %s log_file start_time end_time

<log_file> option: [www | bbs | pt | api | ssl]
      www  ---->wwwxd_access.log
      bbs  ---->bbsxd_access.log
      pt   --->ptxindong_access.log
      op   --->opxd_access.log
      api  --->apixd_access.log
      ssl  --->sslxd_access.log
<start_time> option: [0-23] and <end_time> option: [0-23] and end_time > start_time
    '''%sys.argv[0]
    sys.exit()
print 'loading....'
project=sys.argv[1]
log_file_dic={'www':'/md/log/web/wwwxd_access.log','bbs':'/md/log/web/bbsxd_access.log','pt':'/md/log/web/ptxidong_access.log','op':'/md/log/web/opxd_access.log','api':'/md/log/web/opxd_access.log','ssl':'/md/log/web/sslxd_access.log'}

if project in log_file_dic:
    log_file=log_file_dic[project]
else:
    print "%s does not exsit!"%project
    sys.exit()

def handle(fname):
    f=file(fname)
    first_line=f.readline()
    current_date=first_line.split()[7].split(':')[0].split('[')[1]
    start_time=''.join(current_date)+':'+sys.argv[2]
    end_time=''.join(current_date)+':'+sys.argv[3]
    u_start_time=time.mktime(time.strptime(start_time,'%d/%b/%Y:%H'))
    u_end_time=time.mktime(time.strptime(end_time,'%d/%b/%Y:%H'))

    time_pv_dic={u_start_time:0}
    http_code_dict={}
    for line in f.xreadlines():
        line=line.split('-')
        try:
            access_time=line[2].split()[0].split('[')[1]
            http_code=int(line[2].split()[5])
        except IndexError:pass
        u_access_time=time.mktime(time.strptime(access_time,'%d/%b/%Y:%H:%M:%S'))
        if u_start_time < u_access_time and u_access_time < u_end_time:
            time_pv_dic[u_start_time]+=1
        else:continue


        if http_code_dict.has_key(http_code):
            http_code_dict[http_code] += 1
        else:
            http_code_dict[http_code] = 1
    f.close()

    for i,j in time_pv_dic.items():
        hours=int(sys.argv[3])-int(sys.argv[2])
        qps=j/(3600*hours)
        print "qps:%d reqs/s" %qps

    for v,k in http_code_dict.items():
        print "%d:%d"%(v,k)
handle(log_file)
