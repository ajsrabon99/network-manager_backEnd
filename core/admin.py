from django.contrib import admin
from .models import NetworkDevice, TrustedDevice

admin.site.register(NetworkDevice)
admin.site.register(TrustedDevice)