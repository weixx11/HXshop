#!/usr/bin/env python
#coding=utf-8

import  requests
import json
class YunPian(object):

    def __init__(self,api_key):
        self.api_key=api_key
        self.single_send_url="https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self,code,mobile):
        parmas={
            "apikey":self.api_key,
            "mobile":mobile,
            "text":"【慕雪生鲜超市】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code),
        }

        response = requests.post(self.single_send_url, data=parmas)
        re_dict = json.loads(response.text)
        return re_dict

if __name__=="__main__":
    #云片网的APIKEY值
    yun_pian = YunPian("cd49448b6377b288eab75d8d99dd880f")
    yun_pian.send_sms("2018","mobile")