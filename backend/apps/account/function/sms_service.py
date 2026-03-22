import requests
from django.conf import settings


def send_otp_sms(phone,otp):
    url ="https://www.fast2sms.com/dev/bulkV2"
    
    payload = {
        "message":f"Your otp is {otp}",
        "route":"q",
        "numbers":phone
    }
    
    headerS = {
        
        "authorization":settings.FAST2SMS_API_KEY,
        "Content-Type":"application/json"
    }
    
    response = requests.post(url=url,json=payload,headers=headerS)
    
    print("SMS RESPONSE :",response.json())
    
    return response.json()