import redis
import json

conn = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)
# conn = redis.Redis(host="127.0.0.1", port=6379, decode_responses=False)# 对于pickle二进制数据，不要解码，不然报错


def callback_1(data):
    print(data)


def callback_2(data):
    print(data)


# 第一步 生成一个订阅者对象
redis_sub = conn.pubsub()
redis_sub.subscribe(**{
    "test_1": callback_1,  # 原始视频
    "test_2": callback_2,  # 原始视频
})
redis_sub.run_in_thread(daemon=False)
# redis_sub.run_in_thread(daemon=True)

# 发布
conn.publish("test_1", json.dumps({"1": 2}))
conn.publish("test_2", json.dumps({"1": 3}))
