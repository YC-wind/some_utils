#!/usr/bin/python
# coding:utf8
"""
@author: Cong Yu
@time: 2020-08-04 20:41
"""
import os
import re
import time
import json
import faiss
import pickle
import numpy as np

index_data = []  # data_len * dim (纬度)
d = 200  # dimension

# 以下必须 转为 float32
index_data = np.array(index_data).astype('float32')
print(index_data.shape)
index = faiss.IndexFlatL2(d)  # build the index
print(index.is_trained)
index.add(index_data)
print(index.ntotal)
pickle.dumps(index, open("faiss_index_demo.bin", "wb"))
k = 4  # we want to see 4 nearest neighbors
# 离线服务的话，序列化 index 对象，提起来作为服务即可
D, I = index.search(index_data[:5], k)  # actual search

print(I[:5])  # neighbors of the 5 first queries
print(I[-5:])
