import os, pickle
from server import server

class alliance(object):

  index = 0
  api_keys = []
  total_keys = int(os.environ["api_keys"],10)
  baseurl = "https://politicsandwar.com/api/"
  pnw_id=server.pnw_id

  for x in range(total_keys):
    api_keys.append(os.environ["api_key_%d" % x])
  
  def __init__(self):
    pass

  def serialize_wars(self):
    f =  open('wars.pickle','wb')
    pickle.dump(self.wars, f)
    f.close()

  def deserialize_wars(self):
    f = open('wars.pickle','rb')
    self.wars = pickle.load(f)
    f.close()

  @classmethod
  def get_api_key(cls):
    key = cls.api_keys[cls.index]
    cls.index = (cls.index + 1) % cls.total_keys
    return key


alliance = alliance()
alliance.wars = dict()
try:
  alliance.deserialize_wars()
except:
  pass