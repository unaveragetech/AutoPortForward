import miniupnpc
import requests
import socket
import sys
import json
import os
import psutil
import time
import platform
import subprocess
from collections import deque

# Configuration File
CONFIG_FILE = 'config.json'

# Default Settings
DEFAULT_PORT = 25565
UPNP_SERVICE = 'TCP'  # TCP is usually used for most applications
BLOCKED_IPS_FILE = 'blocked_ips.txt'
MAX_BLOCK_THRESHOLD = 5  # Max number of failed connection attempts to block an IP
SETUP_COMPLETE_FILE = 'setup_complete.txt'  # The file that indicates setup completion

# Load Configuration or create if it doesn't exist
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    else:
        config = {
            "internal_ip": "",
            "external_ip": "",
            "gateways": [],
            "selected_gateway": 0,  # Index of selected gateway
            "blocked_ips": [],
            "auto_run": False,  # If set to True, auto start on system boot
            "port": DEFAULT_PORT
        }
        save_config(config)
        return config

# Save Configuration
def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

# Get Local (Internal) IP Address
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))  # Connect to Google's DNS
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip

# Get Public IP Address
def get_external_ip():
    try:
        response = requests.get('https://api.ipify.org')
        return response.text
    except requests.RequestException as e:
        print(f"Error getting external IP: {e}")
        return None

# Discover UPNP Gateways (Routers)
def discover_upnp():
    upnp = miniupnpc.UPnP()
    upnp.discover()  # Discover available UPNP devices
    gateways = []
    for idx in range(upnp.igdcount()):
        upnp.selectigd(idx)  # Select each device
        gateway = {
            'name': upnp.getdevicename(),
            'internal_ip': upnp.lanaddr,
            'external_ip': upnp.externalip(),
            'gateway': upnp.gateway(),
            'port': DEFAULT_PORT
        }
        gateways.append(gateway)
    return gateways

# Add Port Forwarding Rule
def add_port_forward(upnp, port, local_ip):
    try:
        upnp.addportmapping(port, UPNP_SERVICE, local_ip, port, 'AutoPortForward', '')
        print(f"Port {port} forwarded to local IP {local_ip}.")
    except Exception as e:
        print(f"Error adding port forward: {e}")

# Remove Port Forwarding Rule
def remove_port_forward(upnp, port):
    try:
        upnp.deleteportmapping(port, UPNP_SERVICE)
        print(f"Port {port} removed from forwarding.")
    except Exception as e:
        print(f"Error removing port forward: {e}")

# Block Malicious IPs
def block_malicious_ips():
    blocked_ips = load_config()['blocked_ips']
    if not blocked_ips:
        return
    print(f"Blocking the following IPs: {blocked_ips}")
    for ip in blocked_ips:
        # Use firewall or equivalent to block the IP (Platform specific)
        if platform.system() == "Windows":
            subprocess.run(f"netsh advfirewall firewall add rule name=\"Block {ip}\" dir=in action=block remoteip={ip}")
        elif platform.system() == "Linux":
            subprocess.run(f"sudo iptables -A INPUT -s {ip} -j DROP")
        print(f"Blocked IP: {ip}")

# Monitor Connections and Block Suspicious IPs
def monitor_and_block_connections():
    failed_attempts = {}
    while True:
        for conn in psutil.net_connections(kind='inet'):
            ip = conn.raddr.ip
            if ip:
                failed_attempts[ip] = failed_attempts.get(ip, 0) + 1
                if failed_attempts[ip] >= MAX_BLOCK_THRESHOLD:
                    print(f"Blocking suspicious IP: {ip}")
                    failed_attempts[ip] = 0
                    config = load_config()
                    config['blocked_ips'].append(ip)
                    save_config(config)
                    block_malicious_ips()
        time.sleep(10)  # Check every 10 seconds

# Auto-Run the Script on System Startup (Platform-Specific)
def setup_autorun():
    config = load_config()
    if config.get('auto_run'):
        if platform.system() == 'Windows':
            subprocess.run(['schtasks', '/create', '/tn', 'AutoPortForward', '/tr', 'pythonw.exe port_forward.py', '/sc', 'onstart', '/f'])
        elif platform.system() == 'Linux':
            subprocess.run(f'echo "@reboot python3 {os.path.abspath(__file__)}" | crontab -')
        print("Auto-run setup complete.")

# Check if setup has been completed
def check_setup():
    if not os.path.exists(SETUP_COMPLETE_FILE):
        print("Setup has not been completed. Running setup.bat to install dependencies...")
        subprocess.run([os.path.join(os.getcwd(), 'setup.bat')])  # Run setup.bat to install dependencies
        if not os.path.exists(SETUP_COMPLETE_FILE):
            print("Setup failed. Exiting...")
            sys.exit(1)

# Main function
def main():
    # Ensure setup is complete
    check_setup()

    config = load_config()
    action = sys.argv[1].lower() if len(sys.argv) > 1 else None

    if action not in ['enable', 'disable']:
        print("Usage: python3 port_forward.py [enable|disable]")
        return

    gateways = discover_upnp()
    if not gateways:
        print("No UPNP devices found.")
        return

    print("Available Gateways:")
    for idx, gateway in enumerate(gateways):
        print(f"{idx}: {gateway['name']} - {gateway['internal_ip']} (External: {gateway['external_ip']})")

    # Select gateway
    selected_gateway_idx = config.get('selected_gateway', 0)
    selected_gateway = gateways[selected_gateway_idx]
    print(f"Using Gateway: {selected_gateway['name']} - {selected_gateway['internal_ip']}")

    upnp = miniupnpc.UPnP()
    upnp.selectigd(selected_gateway_idx)

    # Get internal and external IPs
    internal_ip = get_local_ip()
    external_ip = get_external_ip()
    print(f"Local IP: {internal_ip}, External IP: {external_ip}")

    if action == 'enable':
        add_port_forward(upnp, config['port'], internal_ip)
    elif action == 'disable':
        remove_port_forward(upnp, config['port'])

    if config['auto_run']:
        setup_autorun()

    # Monitor network connections
    monitor_and_block_connections()

if __name__ == "__main__":
    main()
