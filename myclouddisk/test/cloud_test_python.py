# -*- coding: utf-8 -*-
'''
Created on 2013年11月26日

@author: adrian
'''

# curl   -i -H "X-Auth-Key: abc"  -H "X-Auth-User: abc"  http://localhost:8080/scloud_domain/lb  -X GET

import httplib, urllib

# params = urllib.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
params = urllib.urlencode({})

headers = {"Authorization": "20141001:123456",
           "Content-Type": "scloud-object",
           "X-CDMI-Specification-Version":"v1",
           "Host":"fasdfa",
           "Date":"fasdfasd"
           } 
conn = httplib.HTTPConnection("172.20.46.160:8080")

# urls = ["/scloud_object/admin/haha/helloadrianxxx.html","/scloud_container/admin/haha/","/scloud_domain/admin/"]
# 
# if sys.argv[1] == 'object':
#     test_url = urls[0]
# if sys.argv[1] == 'container':
#     test_url = urls[1]
# if sys.argv[1] == 'domain':
#     test_url = urls[2]
#     
test_url = "/scloud_object/hello/testData.sql"
           
conn.request("GET", test_url, params, headers)
response = conn.getresponse()
       
data = response.read()
resheader=response.getheaders()
# print str(resheader).encode("UTF-8")
# print resheader
# print data
# if test_url.startswith('/scloud_object'):
# savedBinFile = open('/Users/adrian/desktop/testDatahahahaha.sql', "wb"); # open a file, if not exist, create it
# savedBinFile.write(data);
# savedBinFile.close();
conn.close()

# test_put_url = urllib.quote("/scloud_object/hello/你好啊啊啊啊.docx")
# print test_put_url
# x = open('/Users/adrian/desktop/你好.docx','rb')
# data = x.read()
# params = {'body':data}
# params = str(params)
# conn.request("PUT", test_put_url, params, headers)
# conn.close()
