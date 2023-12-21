from django.contrib import admin
from .models import phar
from.models import user,product,booking,cart
# Register your models here.
admin.site.register(phar)
admin.site.register(user)
admin.site.register(product)
admin.site.register(booking)
admin.site.register(cart)

