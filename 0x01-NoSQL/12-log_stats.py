#!/usr/bin/env python3
"""Display stats on Nginx logs on MongoDB.

Counts the documents that are in the database
"""
import pymongo


if __name__ == '__main__':
    client = pymongo.MongoClient()
    db = client.logs

    log_count = db.nginx.count_documents({})
    get_count = db.nginx.count_documents({"method": "GET"})
    post_count = db.nginx.count_documents({"method": "POST"})
    put_count = db.nginx.count_documents({"method": "PUT"})
    patch_count = db.nginx.count_documents({"method": "PATCH"})
    delete_count = db.nginx.count_documents({"method": "DELETE"})
    stats_cnt = db.nginx.count_documents({"method": "GET", "path": "/status"})

    print("{} logs".format(log_count))
    print("Methods:")
    print("method GET: {}".format(get_count))
    print("method POST: {}".format(post_count))
    print("method PUT: {}".format(put_count))
    print("method PATCH: {}".format(patch_count))
    print("method DELETE: {}".format(delete_count))
    print("{} status check".format(stats_cnt))
