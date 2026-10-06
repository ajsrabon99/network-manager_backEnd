from django.db import models

class NetworkDevice(models.Model):
    ip_address = models.GenericIPAddressField()
    mac_address = models.CharField(max_length=20)
    hostname = models.CharField(max_length=255, blank=True)
    device_type = models.CharField(max_length=50, default="Unknown")
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.hostname or self.ip_address
    

class TrustedDevice(models.Model):
    name = models.CharField(max_length=100)
    mac_address = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name