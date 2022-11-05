from django.conf import settings
from django.http import HttpResponse


def create_shopping_cart_txt(ingredients):
    purchases = [f'{item[settings.INGREDIENT]} - {item[settings.AMOUNT]} '
                 f'{item[settings.MEASUREMENT_UNIT]}\n'
                 for item in ingredients]
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=Purchases.txt'
    response.writelines(purchases)
    return response
