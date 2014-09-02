#coding = utf-8

'''

@author: adrian
'''
from api.keystone import client

from newproject.settings import AUTH_URL


aus = client.Client(auth_url=AUTH_URL)

# for user in aus.users.findall():
#     print user

for role in aus.roles.findall():
    print role.name