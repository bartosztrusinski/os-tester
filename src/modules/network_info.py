import platform
import socket
import psutil

def get_ipv4_info():
    system = platform.system()

    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                ip_address = addr.address

                if system == "Linux":
                    try:
                        with open('/etc/network/interfaces', 'r') as file:
                            if ip_address in file.read():
                                ip_type = "Static"
                            else:
                                ip_type = "Dynamic"
                    except FileNotFoundError:
                        ip_type = "Unknown (file not found)"
                elif system == "Windows":
                    ip_type = "Dynamic" if addr.netmask != "255.255.255.255" else "Static"
                else:
                    ip_type = "Unknown (platform not supported)"

                if "wlan" in interface.lower() or "wifi" in interface.lower():
                    connection_type = "Wi-Fi"
                elif "eth" in interface.lower() or "en" in interface.lower():
                    connection_type = "Ethernet"
                else:
                    connection_type = "Unknown"

                return f"Interface: {interface}, IP: {ip_address}, Type: {ip_type}, Connection: {connection_type}"

    return "No IPv4 address found."