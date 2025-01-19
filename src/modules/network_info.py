import platform
import socket
import psutil
import subprocess

def get_ipv4_info():
    system = platform.system()

    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                ip_address = addr.address

                if system == "Linux":
                    try:
                        with open('/etc/network/interfaces', 'r') as file:
                            file_content = file.read()
                            if f"iface {interface} inet static" in file_content:
                                ip_type = "Static"
                            else:
                                ip_type = "Dynamic"
                    except FileNotFoundError:
                        ip_type = "Dynamic"
                elif system == "Windows":
                    ip_type = "Dynamic" if addr.netmask != "255.255.255.255" else "Static"
                elif system == "Darwin":
                    try:
                        result = subprocess.check_output(['ifconfig', interface], universal_newlines=True)
                        if "inet " in result:
                            ip_type = "Static"
                        else:
                            ip_type = "Dynamic"
                    except subprocess.CalledProcessError:
                        ip_type = "Unknown (error checking IP)"
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