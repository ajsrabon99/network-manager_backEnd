from django.shortcuts import render
from .utils import get_network_info, get_bandwidth, scan_devices
from .models import NetworkDevice, TrustedDevice


def dashboard(request):
    context = get_network_info()

    bandwidth = get_bandwidth()

    scanned_devices = scan_devices()

    for d in scanned_devices:
        NetworkDevice.objects.update_or_create(
            mac_address=d["mac"],
            defaults={
                "ip_address": d["ip"],
                "hostname": d["hostname"],
                "device_type": d["device_type"],
            }
        )

    devices = NetworkDevice.objects.all().order_by("-last_seen")

    trusted_macs = TrustedDevice.objects.values_list(
        "mac_address",
        flat=True
    )

    unknown_devices = [
        d for d in devices
        if d.mac_address not in trusted_macs
    ]

    context.update({
        "devices": devices,
        "unknown_devices": unknown_devices,
        "download": bandwidth["download"],
        "upload": bandwidth["upload"],
    })

    return render(request, "exmp_frontend.html", context)