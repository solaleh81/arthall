from celery import shared_task
from kavenegar import KavenegarAPI
from config import settings
from orders.models import Order


@shared_task
def send_order_sms(order_id):
    try:
        order = Order.objects.get(id=order_id)
        api = KavenegarAPI(settings.KAVENEGAR_API_KEY)

        params = {
            'receptor': order.phone,
            'token': order.full_name,
            'token10': order.order_number,
            'template': 'send-sms-for-create-order'
        }

        response = api.verify_lookup(params)
        return response
    except:
        print("error")
