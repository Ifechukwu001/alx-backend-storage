#!/usr/bin/env python3
"""Display stats on Nginx logs on MongoDB.

"""
import pymongo


client = pymongo.MongoClient()
db = client.logs

log_count = db.nginx.count()
get_count = db.nginx.find({"method": "GET"}).count()
post_count = db.nginx.find({"method": "POST"}).count()
put_count = db.nginx.find({"method": "PUT"}).count()
patch_count = db.nginx.find({"method": "PATCH"}).count()
delete_count = db.nginx.find({"method": "DELETE"}).count()
getstatus_count = db.nginx.find({"method": "GET", "path": "/status"}).count()

print("{} logs".format(log_count))
print("Methods:")
print("    method GET: {}".format(get_count))
print("    method POST: {}".format(post_count))
print("    method PUT: {}".format(put_count))
print("    method PATCH: {}".format(patch_count))
print("    method DELETE: {}".format(delete_count))
print("{} status check".format(getstatus_count))
