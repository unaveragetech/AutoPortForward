
### Project Structure
```
AutoPortForward/
│
├── port_forward.py        # Main Python script
├── config.json            # Configuration file (auto-generated if not found)
├── blocked_ips.txt        # File to store blocked IPs (auto-generated)
└── README.md              # Project documentation
```

### `README.md`

```markdown
# AutoPortForward

AutoPortForward is a Python script that automatically manages port forwarding on your router using UPNP (Universal Plug and Play). It allows you to easily forward a port for a specific application, monitor network connections, and block malicious IPs dynamically. Additionally, it provides a way to automatically run the script when your system starts.

## Features

- **Automatic Port Forwarding**: Open ports on your router based on the configuration.
- **Multiple Gateway Support**: Discover and select which router or gateway device to use for port forwarding.
- **Auto-Run on Startup**: The script can automatically run on system boot (Windows and Linux support).
- **Malicious IP Blocking**: Monitors incoming network connections and blocks suspicious IP addresses after a defined number of failed connection attempts.
- **Configurable**: Customize the port, gateway selection, and other settings via a JSON configuration file.
- **Cross-Platform**: Works on Windows and Linux.

## Prerequisites

- Python 3.7 or later.
- Required Python libraries:
  - `miniupnpc` (for UPNP functionality)
  - `psutil` (for network connection monitoring)
  - `requests` (for fetching the external IP)

You can install these dependencies using pip:

```bash
pip install miniupnpc psutil requests
```

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/AutoPortForward.git
   cd AutoPortForward
   ```

2. Install the required dependencies (if you haven't already):

   ```bash
   pip install miniupnpc psutil requests
   ```

3. Configure the script by running it once, which will generate the configuration file (`config.json`). You can edit this file to customize your settings.

## Usage

### Manual Port Forwarding

To enable port forwarding for the specified port (default is 25565), run the script with the `enable` argument:

```bash
python3 port_forward.py enable
```

To disable port forwarding, run the script with the `disable` argument:

```bash
python3 port_forward.py disable
```

The script will discover available UPNP gateways on your network, and you can select which one to use.

### Auto-Run on Startup

If you want the script to automatically run when your system starts, set the `"auto_run"` field to `true` in the `config.json` file:

```json
{
    "auto_run": true
}
```

On Windows, this will add the script to Task Scheduler. On Linux, it will add a cron job to run the script at startup.

### Configuration

The script uses a JSON configuration file (`config.json`) to store settings such as the internal and external IP addresses, gateways, and port to forward. The script will automatically create this file if it doesn't exist.

You can manually edit `config.json` to change the following options:

- `port`: The port to forward (default is 25565).
- `auto_run`: Set to `true` to make the script run at startup.
- `selected_gateway`: The index of the gateway to use (default is 0).
- `blocked_ips`: List of IP addresses that are blocked due to suspicious activity.

Example `config.json`:

```json
{
    "internal_ip": "192.168.1.100",
    "external_ip": "203.0.113.1",
    "gateways": [
        {
            "name": "Gateway 1",
            "internal_ip": "192.168.1.1",
            "external_ip": "203.0.113.1",
            "gateway": "192.168.1.1",
            "port": 25565
        },
        {
            "name": "Gateway 2",
            "internal_ip": "192.168.1.2",
            "external_ip": "203.0.113.2",
            "gateway": "192.168.1.2",
            "port": 25565
        }
    ],
    "selected_gateway": 0,
    "blocked_ips": [],
    "auto_run": false,
    "port": 25565
}
```

### Monitoring and Blocking Malicious IPs

The script will monitor network connections and count failed attempts from specific IP addresses. Once an IP exceeds a threshold (`MAX_BLOCK_THRESHOLD`), it will be added to the `blocked_ips` list and blocked using your system's firewall.

You can modify the threshold for blocking by changing the `MAX_BLOCK_THRESHOLD` variable in the script.

## Troubleshooting

- **No UPNP Devices Found**: Make sure your router supports UPNP and is properly configured to allow automatic port forwarding.
- **Firewall Issues**: On some systems, you might need to run the script as an administrator or with elevated privileges to modify firewall rules (blocking IPs or adding port forwards).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [miniupnpc](https://github.com/miniupnp/miniupnp) for UPNP functionality.
- [psutil](https://github.com/giampaolo/psutil) for network connection monitoring.
- [requests](https://docs.python-requests.org/en/latest/) for fetching the public IP.

```

### Additional Files

1. **`config.json`** (Auto-generated, structure explained in the README above).

```json
{
    "internal_ip": "",
    "external_ip": "",
    "gateways": [],
    "selected_gateway": 0,
    "blocked_ips": [],
    "auto_run": false,
    "port": 25565
}
```

2. **`blocked_ips.txt`** (This file will be auto-generated if malicious IP blocking is enabled and used).

This file will contain a list of IPs that have been blocked due to suspicious or failed connection attempts.

```txt
192.168.1.100
203.0.113.5
```

### Notes:

- **Firewall Rules**: The script uses system-specific commands (Windows' `netsh` and Linux' `iptables`) to block IPs. This means you will need administrative privileges to run the script or modify firewall rules.
- **Platform-Specific Setup**: The auto-run feature for Windows uses Task Scheduler, and for Linux, it adds a cron job. This ensures the script runs automatically when the system starts.

### Conclusion

This project allows for automatic port forwarding, network monitoring, and IP blocking, as well as the ability to run the script on system startup. You can customize the settings via the configuration file and monitor network activity for malicious behavior.
