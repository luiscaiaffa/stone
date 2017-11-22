from django.contrib import admin
from .models import CreditCard, Wallet, Invoice

admin.site.register(CreditCard)
admin.site.register(Wallet)
admin.site.register(Invoice)
