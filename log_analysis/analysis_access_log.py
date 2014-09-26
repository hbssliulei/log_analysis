#!/usr/bin/env python
import time
import sys
import argparse

def handle(fname):
    f=file(fname)
    first_line=f.readline()
    current_date=first_line.split()[7].split(':')[0].split('[')[1]
    first_line_datetime=first_line.split()[7].split('[')[1]
    start_time=''.join(current_date)+':'+args.start_time
    end_time=''.join(current_date)+':'+args.end_time
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
    for i,j in time_pv_dic.items():
        hours=int(args.end_time)-int(args.start_time)
        qps=float(j)/(3600*hours)
        if qps == 0:
            print "qps:%d reqs/s,The date of the first line is [%s]"%(qps,first_line_datetime)
        else:
            print "qps:%d reqs/s" %qps

    for v,k in http_code_dict.items():
        print "%d:%d"%(v,k)
    f.close()

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument("project",type=str,help="value==>[ www | bbs | pt | op | api | ssl ]")
    parser.add_argument("start_time",type=str,help="value==>[0-23],recommend start_time<=3")
    parser.add_argument("end_time",type=str,help="value==>[0-23]")
    args=parser.parse_args()
    print 'loading....'
    project=args.project
    log_file_dic={'www':'/md/log/web/wwwxd_access.log','bbs':'/md/log/web/bbsxd_access.log','pt':'/md/log/web/ptxindong_access.log','op':'/md/log/web/opxd_access.log','api':'/md/log/web/opxd_access.log','ssl':'/md/log/web/sslxd_access.log'}
    if project in log_file_dic:
        log_file=log_file_dic[project]
    else:
        print "%s does not exsit!"%project
        sys.exit()
    handle(log_file)
