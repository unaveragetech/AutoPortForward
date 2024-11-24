import logging
import time
import psutil
import socket
import subprocess
import os

# Configuration
BLOCKED_IPS_FILE = 'blocked_ips.txt'
MAX_BLOCK_THRESHOLD = 5  # Max number of failed connection attempts to block an IP
LOG_FILE = 'connections.log'

# Set up logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

# Load Blocked IPs
def load_blocked_ips():
    if os.path.exists(BLOCKED_IPS_FILE):
        with open(BLOCKED_IPS_FILE, 'r') as f:
            return set(f.read().splitlines())
    return set()

# Save Blocked IPs
def save_blocked_ips(blocked_ips):
    with open(BLOCKED_IPS_FILE, 'w') as f:
        for ip in blocked_ips:
            f.write(f"{ip}\n")

# Block IP using firewall (platform-specific)
def block_ip(ip):
    if platform.system() == "Windows":
        subprocess.run(f"netsh advfirewall firewall add rule name=\"Block {ip}\" dir=in action=block remoteip={ip}")
    elif platform.system() == "Linux":
        subprocess.run(f"sudo iptables -A INPUT -s {ip} -j DROP")
    logging.info(f"Blocked IP: {ip}")

# Monitor network connections and sanitize them
def monitor_connections():
    failed_attempts = {}
    blocked_ips = load_blocked_ips()

    while True:
        for conn in psutil.net_connections(kind='inet'):
            ip = conn.raddr.ip
            if ip:
                # Skip IPs already blocked
                if ip in blocked_ips:
                    continue
                
                # Increment failed attempt count
                failed_attempts[ip] = failed_attempts.get(ip, 0) + 1
                log_connection(ip, failed_attempts[ip])

                # If failed attempts exceed threshold, block the IP
                if failed_attempts[ip] >= MAX_BLOCK_THRESHOLD:
                    block_ip(ip)
                    blocked_ips.add(ip)
                    save_blocked_ips(blocked_ips)
                    failed_attempts[ip] = 0

        time.sleep(10)  # Check every 10 seconds

# Log each connection attempt
def log_connection(ip, attempt_count):
    logging.info(f"Connection attempt from IP: {ip} - Attempt #{attempt_count}")

def main():
    print("Starting connection monitor and sanitizer...")
    monitor_connections()

if __name__ == "__main__":
    main()
