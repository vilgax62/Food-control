from celery import shared_task
from .function.sms_service import send_otp_sms

@shared_task
def send_otp_task(phone,otp):
    send_otp_sms(phone,otp)
    
    
    
