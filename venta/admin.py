from django.contrib import admin
from .models import Client,Vendor,Category,Product,Invoice,Offer

admin.site.register(Client)
admin.site.register(Vendor)
admin.site.register(Category)
admin.site.register(Invoice)
admin.site.register(Offer)
admin.site.register(Product)
# Register your models here.
