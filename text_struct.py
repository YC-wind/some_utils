#!/usr/bin/python
# coding:utf8
"""
@author: Cong Yu
@time: 2020-07-11 18:16
"""
import os
import re
import time
import json
import pandas as pd


def match(sentence, conditions):
    for condition in conditions:
        flag = True
        for condition_and in condition:
            if condition_and["operate"] == "Match":
                if re.search(condition_and["value"], sentence):
                    pass
                else:
                    flag = False
                    break

            elif condition_and["operate"] == "NotMatch":
                if not re.search(condition_and["value"], sentence):
                    pass
                else:
                    flag = False
                    break

            elif condition_and["operate"] == "TextLenLess":
                if len(sentence) < int(condition_and["value"]):
                    pass
                else:
                    flag = False
                    break

            elif condition_and["operate"] == "TextLenGreater":
                if len(sentence) > int(condition_and["value"]):
                    pass
                else:
                    flag = False
                    break
            else:
                print(f"operate [{condition_and['operate']}] is not allowed...")
                flag = False
                break
        if flag and len(condition):
            print(condition, sentence)
            return condition
    return None


class TextStructure:
    def __init__(self, config):
        self.chapter1 = config["chapter1"]
        self.chapter2 = config["chapter2"]
        self.chapter3 = config["chapter3"]
        self.chapter4 = config["chapter4"]
        self.chapter5 = config["chapter5"]
        self.clear = config["clear"]

        # 是否为 章节标题 （0-无 1-5 对应标题level）
        self.is_chapter_level = 0
        self.chapter_text = ""
        self.now_chapters = [""] * 5
        pass

    def match_chapter(self, sentence, level=1):
        if level == 1:
            has_chapter = match(sentence, self.chapter1["conditions"])
            if has_chapter:
                self.is_chapter_level = 1
                self.chapter_text = sentence
                self.now_chapters = [sentence] + [""] * 4
                return True
        elif level == 2:
            has_chapter = match(sentence, self.chapter2["conditions"])
            if has_chapter:
                self.is_chapter_level = 2
                self.chapter_text = sentence
                self.now_chapters = self.now_chapters[:1] + [sentence] + [""] * 3
                return True
        elif level == 3:
            has_chapter = match(sentence, self.chapter3["conditions"])
            if has_chapter:
                self.is_chapter_level = 3
                self.chapter_text = sentence
                self.now_chapters = self.now_chapters[:2] + [sentence] + [""] * 2
                return True
        elif level == 4:
            has_chapter = match(sentence, self.chapter4["conditions"])
            if has_chapter:
                self.is_chapter_level = 4
                self.chapter_text = sentence
                self.now_chapters = self.now_chapters[:3] + [sentence] + [""] * 1
                return True
        elif level == 5:
            has_chapter = match(sentence, self.chapter5["conditions"])
            if has_chapter:
                self.is_chapter_level = 5
                self.chapter_text = sentence
                self.now_chapters = self.now_chapters[:4] + [sentence]
                return True

        # self.is_chapter_level = 0
        # self.chapter_text = ""
        return False

    def parser(self, text):

        structure_data = []
        sentences = text.split("\n")

        for sentence in sentences:
            if len(sentence.strip()) < 1:
                continue
            for i in range(1, 6):
                flag = self.match_chapter(sentence, level=i)
                if flag:
                    # print(flag, sentence)
                    break
            # print(sentence, self.is_chapter_level)
            if match(sentence, self.clear["conditions"]):
                self.is_chapter_level = 0
                continue

            if self.is_chapter_level > 0:
                # print(self.is_chapter_level, self.chapter_text, sentence)
                # print(self.now_chapters, sentence)
                structure_data.append({
                    "chapter1": self.now_chapters[0],
                    "chapter2": self.now_chapters[1],
                    "chapter3": self.now_chapters[2],
                    "chapter4": self.now_chapters[3],
                    "chapter5": self.now_chapters[4],
                    "text": sentence
                })

        df = pd.DataFrame(structure_data)
        df.to_csv("demo.csv")
        # a = df.groupby(["chapter1", "chapter2"])
        # for k, v in a:
        #     print("group:", k)
        #     print("values:", v.values)
        pass


# conditions, 内圈与， 外圈或

# config_1 = {
#     "chapter1": {
#         "conditions": [[{"value": "^[一二三四五六七八九十]+、", "operate": "Match"},
#                         {"value": "50", "operate": "TextLenLess"},
#                         ]
#                        ]
#     },
#     "chapter2": {
#         "conditions": [[{"value": "^（[一二三四五六七八九十]+）", "operate": "Match"}
#                         ]
#                        ]
#     },
#     "chapter3": {
#         "conditions": [[
#         ]
#         ]
#     },
#     "chapter4": {
#         "conditions": [[
#         ]
#         ]
#     },
#     "chapter5": {
#         "conditions": [[
#         ]
#         ]
#     },
#     "clear": {
#         "conditions": [[{"value": "^(附件|附则)", "operate": "Match"},
#                         {"value": "50", "operate": "TextLenLess"},
#                         ],
#                        [{"value": "^.{0,6}年.{0,3}年.{0,3}日?", "operate": "Match"},
#                         {"value": "15", "operate": "TextLenLess"},
#                         ],
#                        [{"value": "(部|局)$", "operate": "Match"},
#                         {"value": "10", "operate": "TextLenLess"},
#                         ],
#                        ]
#     },
# }
#
config_ = {
    "chapter1": {
        "conditions": [
            [{"value": "^第[一二三四五六七八九十]+章", "operate": "Match"},
             {"value": "50", "operate": "TextLenLess"},
             ],
            [{"value": "^[一二三四五六七八九十]+、", "operate": "Match"},
             {"value": "50", "operate": "TextLenLess"},
             ],
        ]
    },
    "chapter2": {
        "conditions": [
            # [{"value": "^（[一二三四五六七八九十]+）", "operate": "Match"}
            #  ],
            [{"value": "^第[一二三四五六七八九十]+条", "operate": "Match"}
             ],
        ]
    },
    "chapter3": {
        "conditions": [[]]
    },
    "chapter4": {
        "conditions": [[]]
    },
    "chapter5": {
        "conditions": [[]]
    },
    "clear": {
        "conditions": [
            [{"value": "^(附件|附则)", "operate": "Match"},
             {"value": "50", "operate": "TextLenLess"},
             ],
            [{"value": "^.{0,6}年.{0,3}年.{0,3}日?", "operate": "Match"},
             {"value": "15", "operate": "TextLenLess"},
             ],
            [{"value": "(部|局)$", "operate": "Match"},
             {"value": "10", "operate": "TextLenLess"},
             ],
        ]
    },
}

text_ = "第一章总则"
print(match(text_, config_["chapter1"]["conditions"]))

ts = TextStructure(config_)

doc_ = """
xxxxx
xxxxxxx
xxxxx
第一章 1
第一条 11
第二条 12
第三条 13
第四条 14
第五条 15
第六条 16
第二章 2
第七条 21
第八条 22

"""

ts.parser(doc_)
