import firebase_admin 
from firebase_admin import credentials ,messaging 
import os




cred = credentials.Certificate("backend\serviceAccountKey.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

def send_push_notification(token,title,body, data=None):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data=data or {},token=token,
        
    )
    response = messaging.send(message)
    return response

