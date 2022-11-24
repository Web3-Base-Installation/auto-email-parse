#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/23 下午2:24
# @Author  : Xsu
# @File    : main.py

import pyzmail
import imapclient
import re
from typing import List

OUTLOOK = "outlook"
GOOGLE = "google"
OAUTH_MAPPING  = {
    OUTLOOK:{"host":"outlook.office365.com","port":993}
}
QUERY_FIELDS = ["Inbox","Junk","Archive","Deleted","Drafts","Notes","Outbox","Sent"]

class MailParse:

    def __init__(self,parsetype:str):
        if parsetype not in OAUTH_MAPPING.keys():
            raise ValueError(f"parseType should be set in \f{list(OAUTH_MAPPING.keys())}")
        self.host = OAUTH_MAPPING.get(parsetype).get('host')
        self.port = OAUTH_MAPPING.get(parsetype).get('port')
        self.imapObj = imapclient.IMAPClient(self.host, port=self.port)

    def login(self,email:str,password:str):
        try:
            self.imapObj.login(email,password)
            return True
        except:
            return False

    def parse_batch(self,filed:List,from_user:str,email_objs:List,email_subject:str,re_content:str,re_idx:int):
        response = []
        for email_obj in email_objs:
           result = self.parse(filed,from_user,email_obj.get("username"),email_obj.get("password"),email_subject,re_content,re_idx)
           if result:
               response.append({"email":email_obj,"parse_result":result})
        return response

    def parse(self,filed:List,from_user:str,email:str,password:str,email_subject:str,re_content:str,re_idx:int):
        if not set(filed).issubset(QUERY_FIELDS):
            raise ValueError(f"filed should be set in \f{QUERY_FIELDS}")
        if not self.login(email,password):
            raise ValueError(f"LOGIN failed \f{email}")
        try:
            for box in filed:
                self.imapObj.select_folder(box, readonly=False)
                uids = self.imapObj.search(['FROM', from_user])  # UNSEEN
                if len(uids) < 1:
                    continue
                for uid in uids:
                    Rawmessages = self.imapObj.fetch(uid, [b'BODY[]'])
                    messages = pyzmail.PyzMessage.factory(Rawmessages[uid][b'BODY[]'])
                    emailtitle = messages.get_subject()
                    if emailtitle != email_subject:
                        continue
                    content = messages.html_part.get_payload().decode('utf-8')
                    return re.findall(re_content,content)[re_idx]
        except Exception as e:
            raise ValueError(f"parse failed {email}:{e}")
