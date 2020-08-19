#!/usr/bin/python
# coding:utf8
"""
@author: Cong Yu
@time: 2020-08-17 21:07
"""
import os
import re
import time
import json

import difflib
import sys

file1 = open('files/file1.txt').readlines()
file2 = open('files/file2.txt').readlines()

file1 = [_.strip() for _ in file1]
file2 = [_.strip() for _ in file2]

b = list(difflib.Differ().compare(file1, file2))
a = '\n'.join(b)
print(a)


d = difflib.HtmlDiff()
htmlContent = d.make_file(file1, file2)

with open('diff.html', 'w') as f:
    f.write(htmlContent)

