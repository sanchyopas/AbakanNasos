from home.models import *
from shop.models import ShopSettings

def settings_shop(request):
    return {"settings_shop": ShopSettings.objects.get()}