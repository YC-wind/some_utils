#!/usr/bin/python
# coding:utf8
"""
@author: Cong Yu
@time: 2020-05-24 23:12
"""
import time


class LocalCache:

    def __init__(self):
        self.dict = {}

    @staticmethod
    def now_time():
        return int(time.time())

    def get(self, key):
        # 这里面采用查询时，删除过期key 的策略： 查询，根据设置的时间，定时
        value = self.dict.get(key, None)
        if value:
            # 判断 当前 key 是否过期
            expire_time = value.get("expire", None)
            if expire_time is not None:
                if self.now_time() - value["time"] < expire_time:
                    return value["value"]
                else:
                    self.dict.pop(key)
                    return None
            else:
                return value["value"]
        else:
            return None

    def expire(self, key, t):
        value = self.dict.get(key, None)
        if value:
            # 判断 当前 key 是否过期
            self.dict[key]["expire"] = t
            return True
        else:
            return False

    def set(self, key, value):
        try:
            # 记录下 key 创建的时间
            self.dict[key] = {"value": value, "time": self.now_time()}
            return True
        except Exception as e:
            print(repr(e))
            return False


if __name__ == "__main__":
    # 测试下 自己实现的 模拟 本地redis
    """
    核心逻辑基本完成
    """
    redis = LocalCache()

    a = redis.get("1")
    print("初始情况：", a)

    a = redis.set("1", 1233124124)
    print("设置key", a)

    a = redis.get("1")
    print("获取key", a)

    time.sleep(3)

    a = redis.get("1")
    print("3s获取key", a)

    a = redis.expire("1", 5)
    print("设置时间3s", a)

    a = redis.get("1")
    print("3s", a)

    time.sleep(1)

    a = redis.get("1")
    print("1s", a)

    time.sleep(1)

    a = redis.get("1")
    print("1s", a)

    time.sleep(1)

    a = redis.get("1")
    print("1s", a)
