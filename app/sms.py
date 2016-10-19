'''send sms message via bmob.'''
import json
import requests
import threading

class SMS_sender:
    def __init__(self,appid,appkey):
        self.headers={"X-Bmob-Application-ID":appid,
                      "X-Bmob-REST-API-Key":appkey,
                      "Content-Type":"application/json"}
    def send_sms(self,content,target):
        data={'mobilePhoneNumber':target,'content':content}
        request=requests.post("https://api.bmob.cn/1/requestSms",headers=self.headers,data=json.dumps(data))
        return request.json()

    def send_sms_code(self,template,target):
        data={'mobilePhoneNumber':target,'template':template}
        request=requests.post("https://api.bmob.cn/1/requestSmsCode",headers=self.headers,data=json.dumps(data))
        return request.json()

    def send_mass_sms_code(self,template,target):
        outputs=[]
        for target_item in target:
            outputs.append(self.send_sms_code(template,target_item))
        return outputs

    def async_send_mass_sms_code(self,template,*target):
        thr = threading.Thread(target=self.send_mass_sms_code, args=[template, target])
        thr.start()
        return thr
