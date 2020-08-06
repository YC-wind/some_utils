#!/usr/bin/python
# coding:utf8
"""
@author: Cong Yu
@time: 2020-08-06 19:45
"""
import os
import re
import time
import json

from py2neo import Graph, Node

g = Graph(host="127.0.0.1", http_port=7474, user="neo4j", password="neo4j")

# 创建节点 # label 表示节点类型，后面为节点参数
label = "people"
node = Node(label, name="张三", age=18)
g.create(node)
node = Node(label, name="李四", age=19)
g.create(node)

# 创建节点之间的关系 （下面是创建，  张三与历史的 朋友关系节点）
query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]-(q)" % (
    "people", "people", "张三", "李四", "friend", "朋友")
g.run(query)
