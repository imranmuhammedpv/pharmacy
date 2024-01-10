from django.contrib import admin
from .models import Pharmacy
from.models import user,product,booking,cart,Login
# Register your models here.
admin.site.register(Pharmacy)
admin.site.register(user)
admin.site.register(product)
admin.site.register(booking)
admin.site.register(cart)
admin.site.register(Login)


