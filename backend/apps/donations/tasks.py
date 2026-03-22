from celery import shared_task
from django.utils import timezone
from .models import Donation
from django.db import transaction
import logging
from backend.utils.notification import send_ws_notification
from backend.utils.fcm import  send_push_notification



logger = logging.getLogger(__name__)

@shared_task
def check_and_update_donations():
    donations = Donation.objects.filter(
        is_active = True,
        status = "PENDING",
        expiry_time__lt = timezone.now()
        ).only("id","search_radius","max_radius","radius_increment","expiry_time","accepted_by","donated_by")
    
    for donation in donations:
        with transaction.atomic():
            try:
                donation = Donation.objects.select_for_update().get(id=donation.id)
            except Donation.DoesNotExist:
                continue
            result = donation.extend_radius()
            if result=="extended":
                logger.info(f"Extended donation id = {donation:id}")
            else:
                logger.info(f"Expired donation id = {donation:id}")

#expiry notification:
            send_ws_notification(donation.donated_by.user.id,"Your donation expired",{"donation_id":donation.id})
            if donation.accepted_by:
                send_ws_notification(donation.accepted_by.user.id,"Donation expired before pickup",{"donation_id":donation.id})
            
            if donation.donated_by.user.fcm_token:
                send_push_notification(donation.donated_by.user.fcm_token,"Donation expired before pickup","NO Ngo picked your donation ",{"donation_id":str(donation.id)})