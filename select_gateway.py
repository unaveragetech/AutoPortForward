import miniupnpc
import json
import os

CONFIG_FILE = 'config.json'

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
            'port': 25565
        }
        gateways.append(gateway)
    return gateways

# Save selected gateway to config
def save_selected_gateway(gateway_idx):
    config = load_config()
    gateways = discover_upnp()
    if gateway_idx < len(gateways):
        selected_gateway = gateways[gateway_idx]
        config['gateways'] = gateways
        config['selected_gateway'] = gateway_idx
        save_config(config)
        print(f"Selected Gateway: {selected_gateway['name']} at {selected_gateway['internal_ip']}")
    else:
        print("Invalid gateway index")

# Load configuration or create if it doesn't exist
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    else:
        return {
            "internal_ip": "",
            "external_ip": "",
            "gateways": [],
            "selected_gateway": 0,
            "blocked_ips": [],
            "auto_run": False,
            "port": 25565
        }

# Save configuration
def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def main():
    print("Discovering available gateways...")
    gateways = discover_upnp()
    
    if not gateways:
        print("No UPNP devices found.")
        return

    print("Available Gateways:")
    for idx, gateway in enumerate(gateways):
        print(f"{idx}: {gateway['name']} - {gateway['internal_ip']} (External: {gateway['external_ip']})")

    try:
        selected_gateway_idx = int(input("Select the gateway to configure by entering its index: "))
        save_selected_gateway(selected_gateway_idx)
    except ValueError:
        print("Invalid input. Please enter a number corresponding to the gateway index.")

if __name__ == "__main__":
    main()
