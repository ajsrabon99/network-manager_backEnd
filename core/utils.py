import socket
import psutil
import time
import subprocess
import re


def get_network_info():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)

    return {
        "ip": ip,
        "hostname": hostname,
        "gateway": "N/A",
    }


def get_bandwidth():
    start = psutil.net_io_counters()

    time.sleep(1)

    end = psutil.net_io_counters()

    download = (end.bytes_recv - start.bytes_recv) / 1024 / 1024
    upload = (end.bytes_sent - start.bytes_sent) / 1024 / 1024

    return {
        "download": round(download, 2),
        "upload": round(upload, 2),
    }


def scan_devices():
    output = subprocess.check_output(["arp", "-a"]).decode()

    devices = []

    for line in output.splitlines():
        match = re.search(
            r"(\d+\.\d+\.\d+\.\d+)\s+([0-9a-f:-]{17})", line, re.I
        )
        if match:
            ip = match.group(1)
            mac = match.group(2)

            hostname = get_hostname(ip)
            device_type = guess_device_type(hostname)

            devices.append({
                "ip": ip,
                "mac": mac,
                "hostname": hostname,
                "device_type": device_type
            })

    return devices


def get_hostname(ip):
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except:
        return "Unknown"

def guess_device_type(hostname):
    hostname = hostname.lower() if hostname else ""

    if any(x in hostname for x in ["iphone", "android", "galaxy", "redmi", "xiaomi", "phone"]):
        return "📱 Mobile"

    elif any(x in hostname for x in ["laptop", "desktop", "pc", "thinkpad", "dell", "hp", "lenovo"]):
        return "💻 Computer"

    elif any(x in hostname for x in ["tv", "androidtv", "smarttv"]):
        return "📺 Smart TV"

    elif any(x in hostname for x in ["printer"]):
        return "🖨️ Printer"

    return "❓ Unknown"