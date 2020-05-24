#!/usr/bin/python
# coding:utf8
"""
@author: Cong Yu
@time: 2020-05-24 23:19
"""
import os
import re
import time
import json
import xmind
from termcolor import *
from xmind.core.const import TOPIC_DETACHED
from xmind.core.markerref import MarkerId
from xmind.core.topic import TopicElement


def xmind_to_json(file="./files/demo.xmind"):
    """
    （1）加载x-mind，转化为json
    """
    workbook = xmind.load(file)
    json_ = workbook.getPrimarySheet().getData()
    print(json.dumps(json_, ensure_ascii=False, indent=2))


def write_xmind():
    """
    （2）写xmind
    """
    # 1、如果指定的XMind文件存在，则加载，否则创建一个新的
    workbook = xmind.load("./files/my.xmind")
    # 2、获取第一个画布（Sheet），默认新建一个XMind文件时，自动创建一个空白的画布
    sheet1 = workbook.getPrimarySheet()

    # ***** 第一个画布 *****
    sheet1.setTitle("first sheet")  # 设置画布名称

    # 获取画布的中心主题，默认创建画布时会新建一个空白中心主题
    root_topic1 = sheet1.getRootTopic()
    root_topic1.setTitle("root node")  # 设置主题名称

    # 创建一个子主题，并设置其名称
    sub_topic1 = root_topic1.addSubTopic()
    sub_topic1.setTitle("first sub topic")

    sub_topic2 = root_topic1.addSubTopic()
    sub_topic2.setTitle("second sub topic")

    sub_topic3 = root_topic1.addSubTopic()
    sub_topic3.setTitle("third sub topic")

    sub_topic4 = root_topic1.addSubTopic()
    sub_topic4.setTitle("fourth sub topic")

    # 除了新建子主题，还可以创建自由主题(注意:只有中心主题支持创建自由主题)
    detached_topic1 = root_topic1.addSubTopic(topics_type=TOPIC_DETACHED)
    detached_topic1.setTitle("detached topic")
    detached_topic1.setPosition(0, 30)

    # 创建一个子主题的子主题
    sub_topic1_1 = sub_topic1.addSubTopic()
    sub_topic1_1.setTitle("I'm a sub topic too")

    # ***** 设计第二个画布 *****
    sheet2 = workbook.createSheet()
    sheet2.setTitle("second sheet")

    # 获取画布的中心主题
    root_topic2 = sheet2.getRootTopic()
    root_topic2.setTitle("root node")

    # 使用另外一种方法创建子主题
    topic1 = TopicElement(ownerWorkbook=workbook)
    # 给子主题添加一个主题间超链接，通过指定目标主题ID即可，这里链接到第一个画布
    topic1.setTopicHyperlink(sheet1.getID())
    topic1.setTitle("redirection to the first sheet")

    topic2 = TopicElement(ownerWorkbook=workbook)
    topic2.setTitle("topic with an url hyperlink")
    # 给子主题添加一个URL超链接
    topic2.setURLHyperlink("https://github.com/zhuifengshen/xmind")

    topic3 = TopicElement(ownerWorkbook=workbook)
    topic3.setTitle("third node")
    # 给子主题添加一个备注（快捷键F4)
    topic3.setPlainNotes("notes for this topic")
    topic3.setTitle("topic with \n notes")

    topic4 = TopicElement(ownerWorkbook=workbook)
    # 给子主题添加一个文件超链接
    topic4.setFileHyperlink("logo.png")
    topic4.setTitle("topic with a file")

    topic1_1 = TopicElement(ownerWorkbook=workbook)
    topic1_1.setTitle("sub topic")
    # 给子主题添加一个标签（目前XMind软件仅支持添加一个，快捷键）
    topic1_1.addLabel("a label")

    topic1_1_1 = TopicElement(ownerWorkbook=workbook)
    topic1_1_1.setTitle("topic can add multiple markers")
    # 给子主题添加两个图标
    topic1_1_1.addMarker(MarkerId.starBlue)
    topic1_1_1.addMarker(MarkerId.flagGreen)

    topic2_1 = TopicElement(ownerWorkbook=workbook)
    topic2_1.setTitle("topic can add multiple comments")
    # 给子主题添加一个批注（评论）
    topic2_1.addComment("I'm a comment!")
    topic2_1.addComment(content="Hello comment!", author='devin')

    # 将创建好的子主题添加到其父主题下
    root_topic2.addSubTopic(topic1)
    root_topic2.addSubTopic(topic2)
    root_topic2.addSubTopic(topic3)
    root_topic2.addSubTopic(topic4)
    topic1.addSubTopic(topic1_1)
    topic2.addSubTopic(topic2_1)
    topic1_1.addSubTopic(topic1_1_1)

    # 给中心主题下的每个子主题添加一个优先级图标
    topics = root_topic2.getSubTopics()
    for index, topic in enumerate(topics):
        topic.addMarker("priority-" + str(index + 1))

    # 添加一个主题与主题之间的联系
    sheet2.createRelationship(topic1.getID(), topic2.getID(), "relationship test")

    # 4、保存（如果指定path参数，另存为该文件名）
    xmind.save(workbook, path='./files/my.xmind')


def xmind_route(in_put_file):
    workbook = xmind.load(in_put_file)
    json_ = workbook.getPrimarySheet().getData()
    routes = []
    print(json_["title"], "\n\n")
    print(json_["topic"]["title"])
    routes.append(json_["topic"]["title"])
    try:
        conditions = [_["title"] for _ in json_["topic"]["topics"]]
    except KeyError:
        print("no next node!")
        return {"status": 1, "result": "流程结束啦!"}
    for index, condition in enumerate(conditions):
        print("index:%d\t condition:%s" % (index, condition))

    def goto(node):
        print(node["title"])
        routes.append(node["title"])
        try:
            conditions_ = [_["title"] for _ in node["topics"]]
            for index_, condition_ in enumerate(conditions_):
                print("index:%d\t condition:%s" % (index_, condition_))
            in_put_ = get_input(len(conditions_))
            return goto(node["topics"][in_put_])
        except KeyError:
            print("no next node!")
            return {"status": 1, "result": "流程结束啦!"}

    def get_input(max_len):
        try:
            in_temp = int(input("please choose one route:\n"))
            if in_temp in range(max_len):
                return in_temp
            else:
                print(colored("index should be less than %s ." % (colored(max_len, "magenta")), "yellow"))
                return get_input(max_len)
        except ValueError:
            print(colored("index should be integer, please input a integer.", "yellow"))
            return get_input(max_len)

    in_put = get_input(len(conditions))
    result = goto(json_["topic"]["topics"][in_put])
    print(result)
    print(routes)
    print("routes:\n", " --> ".join([colored(_, "red") for _ in routes]))


# 推理xmind
def load_xmind(in_put_file):
    """
        加载 xmind 文件
    :param in_put_file:
    :return:
    """
    workbook = xmind.load(in_put_file)
    return workbook.getPrimarySheet().getData()


def to_nodes(xmind_json):
    nodes = []
    global max_height
    max_height = 1

    def get_node(node, father, height):
        temp_node = {}
        global max_height
        temp_node["name"] = node["title"]
        temp_node["height"] = height
        temp_node["value"] = -1
        temp_node["father"] = father
        try:
            temp_node["operate"] = "and" if node["markers"][0] == "symbol-plus" else "or"
        except Exception as e:
            print(repr(e))
            temp_node["operate"] = ""
        try:
            temp_node["children"] = [_["title"] for _ in node["topics"]]
            for j in node["topics"]:
                get_node(j, temp_node["name"], height + 1)
        except KeyError:
            pass
        if height >= max_height:
            max_height = height
        nodes.append(temp_node)

    node_ = dict()
    node_["name"] = xmind_json["topic"]["title"]
    node_["height"] = max_height
    node_["value"] = -1
    node_["father"] = "-1"
    node_["operate"] = "and" if xmind_json["topic"]["markers"][0] == "symbol-plus" else "or"
    node_["children"] = [_["title"] for _ in xmind_json["topic"]["topics"]]
    nodes.append(node_)
    max_height += 1
    for i in xmind_json["topic"]["topics"]:
        get_node(i, node_["name"], 2)
    return nodes, max_height


def xmind_inference(in_put_file, activate_nodes):
    """
        根据已经激活的节点， 判断根节点是否 为 真（true/false）
    :param in_put_file:                 图谱文件
    :param activate_nodes:              已经激活的节点
    :return:
    """
    # 加载 xmind 图谱
    json_ = load_xmind(in_put_file)
    # 将图谱 中的节点， 转化为 node 格式
    nodes, height = to_nodes(json_)
    print(height)
    print(json.dumps(nodes, ensure_ascii=False, indent=2))
    # 保存为 json 文件
    # open("./files/operate_nodes.json", "w").write(json.dumps(nodes, ensure_ascii=False, indent=2))
    # list to dict
    new_nodes = {_["name"]: _ for _ in nodes}

    # 得出 推理路径
    inference_routes = []

    def inference(node):
        # 根据当前 节点，往上推理出上一层节点的值
        if node["operate"] == "and":
            # 只有子节点的值 都为 1 的时候，才为真
            flag = True
            for _ in node["children"]:
                if new_nodes[_]["value"] == 0:
                    flag = False
            if flag:
                temp = node["name"] if node["name"] in activate_nodes else colored(node["name"], "green")
                result = "all of (" + " 、 ".join(
                    [colored(_, "red") if _ in activate_nodes else colored(_, "green") for _ in
                     node["children"]]) + ")   -->  " + temp
                inference_routes.append(result)
                new_nodes[node["name"]]["value"] = 1
            else:
                new_nodes[node["name"]]["value"] = 0
        else:
            flag = False
            p = []
            for _ in node["children"]:
                if new_nodes[_]["value"] == 1:
                    p.append(_)
                    flag = True
            if flag:
                temp = node["name"] if node["name"] in activate_nodes else colored(node["name"], "green")
                result = "one of (" + " 、 ".join(
                    [colored(_, "red") if _ in activate_nodes else colored(_, "green") for _ in p]) + ")   -->  " + temp
                inference_routes.append(result)
                new_nodes[node["name"]]["value"] = 1
            else:
                new_nodes[node["name"]]["value"] = 0

    print("given nodes:\n", activate_nodes)
    for node_name in activate_nodes:
        new_nodes[node_name]["value"] = 1
    # 逐层 进行 推理（自底向上推理）
    for h in range(height - 1, 0, -1):
        for name, node_ in new_nodes.items():
            if node_["height"] == h and node_["operate"] != "":
                inference(node_)
    print("\ninference_routes:\n")
    for _ in inference_routes:
        print(_)
    print("\nnodes result:\n")
    for i, v in new_nodes.items():
        print(v)


# xmind_to_json()
# write_xmind()
# xmind_route("./files/demo.xmind")
# print(load_xmind("../xmind_files/operate.xmind"))
xmind_inference("./files/operate.xmind",
                ["condition312", "condition32", "condition22", "condition211", "condition11"])
