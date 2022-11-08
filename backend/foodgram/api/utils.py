from django.conf import settings
from django.http import HttpResponse


def create_shopping_cart_txt(ingredients):
    purchases = [f'{item[settings.INGREDIENT]} - {item[settings.AMOUNT]} '
                 f'{item[settings.MEASUREMENT_UNIT]}\n'
                 for item in ingredients]
    response = HttpResponse(content_type=settings.CONTENT_TYPE)
    response['Content-Disposition'] = settings.CONTENT_DISPOSITION
    response.writelines(purchases)
    return response
