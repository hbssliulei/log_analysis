#!/usr/bin/env python

import redis

conn=redis.Redis(host='localhost',port=6379,db=0)

def get_redis(host='localhost',port=6379,db=0):
	return redis.Redis(host=host,port=port,db=db)
