#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/24 下午2:15
# @Author  : Xsu
# @File    : example.py

from email_parse import MailParse

# print(MailParse("outlook").login("",""))
print(MailParse("outlook").parse(["Inbox","Junk"],"community@minima.global","","",'Welcome to the Minima Incentive program',
                                     r"<a.+?href=\"(.+?)\".*>",re_idx=1))