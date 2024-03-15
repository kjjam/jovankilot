from django.conf import settings
from ippanel import Client
from ippanel import HTTPError, Error, ResponseCode

from installation.models import SMSPanelPattern

sms = Client(settings.SMS_PANEL_KEY)


def send_welcoming_pattern_sms(customer_code, phone):
    pattern = SMSPanelPattern.objects.get(stage="WE")
    pattern_code = pattern.pattern_code
    panel_number = pattern.panel_number
    try:
        message_id = sms.send_pattern(pattern_code, panel_number, phone, [str(customer_code)])
        # todo logging
    except Error as e:
        print(f"Error handled => code: {e.code}, message: {e.message}")
        if e.code == ResponseCode.ErrUnprocessableEntity.value:
            for field in e.message:
                print(f"Field: {field} , Errors: {e.message[field]}")
    except HTTPError as e:
        print(f"Error handled => code: {e}")


def send_work_pattern_sms(request_web_id, phone):
    pattern = SMSPanelPattern.objects.get(stage="WO")
    pattern_code = pattern.pattern_code
    panel_number = pattern.panel_number
    try:
        message_id = sms.send_pattern(pattern_code, panel_number, phone, [request_web_id])
        # todo logging
    except Error as e:
        print(f"Error handled => code: {e.code}, message: {e.message}")
        if e.code == ResponseCode.ErrUnprocessableEntity.value:
            for field in e.message:
                print(f"Field: {field} , Errors: {e.message[field]}")
    except HTTPError as e:
        print(f"Error handled => code: {e}")
