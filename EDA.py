import re
import json
import random
import jieba.posseg as pos_tag
from itertools import permutations

delete_pos = ["t", "s", "f", "p", "c", "u", "e", "y", "o", "w"]
allow_pos = ["a", "n", "v", "d"]
synonyms_words = json.loads(open("files/synonyms_words.json").read())


def get_all_sentences(sentences):
    if len(sentences) == 1:
        return sentences[0]
    else:
        cc_s = []
        for _ in sentences[0]:
            cc_ = get_all_sentences(sentences[1:])
            for c in cc_:
                cc_s.append(_ + c)
        return cc_s


def random_delete_by_pos(text, pos=delete_pos, max_delete=6):
    """

    :param text:   输入文本
    :param pos:     可以随机删除的词性
    :param max_delete:  最大删除的个数，不然生产的太多，
    :return:
    """
    sentences = []
    c_ = 0
    for w, t in pos_tag.cut(text):
        # print(w, t)
        if t[0] in pos and c_ < max_delete:
            c_ += 1
            # print(w, t)
            sentences.append([w, ""])
        else:
            sentences.append([w])
    # 遍历所有 可选的删除
    ss = get_all_sentences(sentences)
    ss = list(set(ss))
    return ss


def random_replace_by_synonyms(text, max_replace=3, ):
    """

    :param text:   输入文本
    :param max_replace:  最大同义词替换的个数
    :return:
    """
    sentences = []
    c_ = 0
    for w, t in pos_tag.cut(text):
        # print(w, t)
        if c_ < max_replace:
            # 这里是 获取 同义词接口的
            synonyms_words_ = synonyms_words.get(w, "")
            synonyms_words_ = list(set([w] + [_ for _ in synonyms_words_.split("|") if _.strip()]))[:5]
            if len(synonyms_words_) > 1:
                # print(synonyms_words_)
                c_ += 1
            sentences.append(synonyms_words_)
        else:
            sentences.append([w])
    # 遍历所有 可选的删除
    ss = get_all_sentences(sentences)
    ss = list(set(ss))
    return ss


def random_swap_by_pos(text):
    sentences = re.split("，", text)
    if len(sentences) > 1:
        sentences = list(permutations(sentences, len(sentences)))
        sentences = ["，".join(_) for _ in sentences][:3]
    else:
        c = re.search("如何|怎么|有什么|在哪|哪个|那个", text)
        # print(c, c.start())
        if c:
            text_a = text[:c.start()] + text[c.start():]
            text_b = text[c.start():] + "，" + text[:c.start()]
            sentences = [text_a, text_b]
        else:
            sentences = [text]
    # print(sentences)
    return sentences


def random_generate(text, max_count=10):
    del_texts = random_delete_by_pos(text)
    syn_texts = random_replace_by_synonyms(text)
    new_texts = list(set(del_texts + syn_texts))
    if len(new_texts) > max_count:
        new_texts = random.sample(new_texts, max_count)
    swp_texts = random_swap_by_pos(text)
    new_texts = new_texts + swp_texts
    if len(new_texts) > max_count:
        new_texts = random.sample(new_texts, max_count)
    # 去重
    new_texts = list(set([_ for _ in new_texts if text != _]))
    return new_texts


text_ = "怎么查询天气情况"
a = random_generate(text_)
print("\n".join(a))
