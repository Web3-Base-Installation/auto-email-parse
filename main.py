#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/23 下午2:24
# @Author  : Xsu
# @File    : main.py

import pyzmail
import imapclient
import re
from typing import List

class MailParse:

    def __init__(self,parsetype:str,emails:List):
        self.parseType = parsetype
        self.emails = emails
        self.mappingDic = {"outlook":{"host":"outlook.office365.com","port":993}}

    def login(self):
        if self.parseType not in self.mappingDic.keys():
            return False
        try:
            self.imapObj = imapclient.IMAPClient(self.mappingDic.get(self.parseType).get("host"), port=self.mappingDic.get(self.parseType).get("port"))
            return True
        except:
            return False

    def parse(self,filed:List,from_user:str,email_subject:str,re_content:str):
        parse_result = []
        for email_object in self.emails:
            try:
                if self.login() != True:
                    continue
                self.imapObj.login(email_object["username"], email_object["password"])
                for box in filed:
                    self.imapObj.select_folder(box, readonly=False)
                    uids = self.imapObj.search(['FROM', from_user])  # UNSEEN
                    if len(uids) < 1:
                        continue
                    for uid in uids:
                        Rawmessages = self.imapObj.fetch(uid, [b'BODY[]'])
                        messages = pyzmail.PyzMessage.factory(Rawmessages[uid][b'BODY[]'])
                        emailtitle = messages.get_subject()
                        if emailtitle == email_subject:
                            result = re.findall(re_content, messages.html_part.get_payload().decode('utf-8'))[1]
                            parse_result.append({"account":email_object["username"],"result":result})
            except Exception as e:
                print(f"error-{email_object['username']}-{e}")
        return parse_result


if __name__ == '__main__':
    print(MailParse("outlook",[{"username":"","password":""}]).parse(["Inbox","Junk"],'community@minima.global','Welcome to the Minima Incentive program',r"<a.+?href=\"(.+?)\".*>"))

