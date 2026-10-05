# 🌐 Network Manager

A lightweight, Django-based web dashboard for monitoring your local network. It shows your machine's network details, live bandwidth usage, and discovers devices connected to your LAN, flagging any device you haven't marked as trusted.

---

## ✨ Features

- **Live network info**: hostname and local IP address of the host machine
- **Real-time bandwidth monitor**: download and upload speed in MB/s (sampled with `psutil`)
- **Device discovery**: scans the ARP table to find devices on the local network (IP + MAC address)
- **Hostname resolution**: reverse DNS lookup for each discovered device
- **Device type detection**: guesses the type from the hostname (📱 Mobile, 💻 Computer, 📺 Smart TV, 🖨️ Printer, ❓ Unknown)
- **Unknown device alerts**: highlights devices whose MAC address isn't in your trusted list
- **Trusted device list**: manage trusted devices through the Django admin
- **Persistent device history**: devices and their "last seen" time are stored in SQLite
- **Auto-refreshing UI**: Bootstrap 5 dashboard that reloads every 10 seconds

---

## 🧰 Tech Stack

| Layer      | Technology                              |
|------------|-----------------------------------------|
| Backend    | Python, Django 5.2                      |
| Database   | SQLite                                  |
| Networking | `psutil`, `socket`, `arp -a`, `scapy`   |
| Frontend   | Django templates, Bootstrap 5.3 (CDN)   |

---

## 📁 Project Structure

```
network-manager/
├── manage.py
├── requirements.txt
├── db.sqlite3                  # SQLite database
├── network_manager/            # Django project config
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── core/                       # Main app
    ├── models.py               # NetworkDevice, TrustedDevice
    ├── views.py                # Dashboard view
    ├── utils.py                # Network scanning & bandwidth helpers
    ├── admin.py                # Admin registration
    ├── urls.py
    ├── migrations/
    └── templates/
        └── dashboard.html      # Dashboard UI
```

---

## 🗄️ Data Models

**`NetworkDevice`**

| Field         | Type                 | Description                       |
|---------------|----------------------|-----------------------------------|
| `ip_address`  | GenericIPAddressField | Device IP                         |
| `mac_address` | CharField(20)        | Device MAC address                |
| `hostname`    | CharField(255)       | Resolved hostname (optional)      |
| `device_type` | CharField(50)        | Guessed type, default `"Unknown"` |
| `last_seen`   | DateTimeField        | Auto-updated on every scan        |

**`TrustedDevice`**

| Field         | Type                      | Description                  |
|---------------|---------------------------|------------------------------|
| `name`        | CharField(100)            | Friendly name                |
| `mac_address` | CharField(20, unique)     | MAC address you trust        |

---

## ⚙️ How It Works

1. When you open the dashboard, `get_network_info()` reads the host's hostname and IP.
2. `get_bandwidth()` samples `psutil.net_io_counters()` twice, one second apart, and converts the difference to MB/s.
3. `scan_devices()` runs `arp -a`, parses IP/MAC pairs with a regex, resolves hostnames, and guesses device types.
4. Each device is saved with `update_or_create` keyed on MAC address, so `last_seen` stays current.
5. Any device whose MAC isn't in `TrustedDevice` is shown as **unknown** in the alert banner.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+ (Django 5.2 requires it)
- `arp` available on your system (included on Windows, macOS, and most Linux distros; on minimal Linux install `net-tools`)
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/ajsrabon99/network-manager.git
cd network-manager

# 2. Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py migrate

# 5. Create an admin user (to manage trusted devices)
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```

Open **http://127.0.0.1:8000/** to see the dashboard, and **http://127.0.0.1:8000/admin/** to manage devices.

### Accessing from another device on your network

```bash
python manage.py runserver 0.0.0.0:8000
```

Then add your machine's IP to `ALLOWED_HOSTS` in `network_manager/settings.py`.

---

## 🛡️ Managing Trusted Devices

1. Go to `/admin/` and log in.
2. Open **Trusted devices** → **Add**.
3. Enter a name and the device's MAC address (use the same format shown on the dashboard, e.g. `aa-bb-cc-dd-ee-ff` on Windows or `aa:bb:cc:dd:ee:ff` on Linux/macOS).
4. Save. The device will no longer appear in the unknown devices alert.

---

## 📦 Dependencies

```
asgiref==3.11.1
Django==5.2.15
psutil==7.2.2
scapy==2.7.0
sqlparse==0.5.5
tzdata==2026.2
```

---

## ⚠️ Known Limitations

- **ARP-based discovery** only finds devices your machine has recently communicated with, so a quiet device may not show up until it generates traffic. A proactive ping/ARP sweep would improve this.
- **Gateway** is currently shown as `N/A`.
- **Device type detection** is a simple hostname keyword match, so it will often return "Unknown".
- **MAC format** differs between operating systems (`-` vs `:`), so trusted MACs must match the format your OS reports.
- **Bandwidth sampling** blocks for ~1 second per page load.
- **Auto-refresh** reloads the whole page rather than updating via AJAX.
- Intended for **local/development use**. Not hardened for production.

---

## 🔒 Security Notes

Before deploying or sharing publicly:

- Move `SECRET_KEY` out of `settings.py` into an environment variable.
- Set `DEBUG = False` and configure `ALLOWED_HOSTS`.
- Add the dashboard behind authentication, since it exposes network details.
- Only scan networks you own or have permission to monitor.

---

## 🗺️ Roadmap Ideas

- [ ] Active network scanning with Scapy (ARP sweep)
- [ ] Gateway and DNS detection
- [ ] MAC vendor lookup (OUI database)
- [ ] One-click "Trust this device" button on the dashboard
- [ ] Bandwidth history charts
- [ ] Email / Telegram alerts for new unknown devices
- [ ] Per-device bandwidth tracking
- [ ] REST API and AJAX live updates
- [ ] Docker support

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

No license has been specified yet. Consider adding one (for example [MIT](https://choosealicense.com/licenses/mit/)) to let others know how they can use this project.

---

## 👤 Author

**ajsrabon99**: [GitHub](https://github.com/ajsrabon99)
