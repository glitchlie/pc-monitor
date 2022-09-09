import redis


class Redis():
    def __init__(self, host="localhost", port=6379,
                 db=0, password=None, socket_timeout=None):
        self.client = redis.Redis(host=host, port=port,
                                  db=db, password=password, socket_timeout=socket_timeout)


    def add_record(self, list_name, ts, val):
        self.client.zadd(list_name, {str(ts) + ":" + str(val): ts})


    def fetch_records(self, list_name, start_idx, end_idx):
        data = self.client.zrange(list_name, start_idx, end_idx)
        return [[int(el.decode().split(":")[0]) * 1000, 
                float(el.decode().split(":")[1])] for el in data]


    def fetch_increment(self, list_name, start_score, end_score="+inf"):
        data = self.client.zrangebyscore(list_name, start_score, end_score)
        return [[int(el.decode().split(":")[0]) * 1000,
                float(el.decode().split(":")[1])] for el in data]
