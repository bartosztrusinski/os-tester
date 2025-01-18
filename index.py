import sys
import os
import platform
import socket
import psutil
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton
from PyQt5.QtCore import QProcess

def get_ipv4_info():
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                return f"Interface: {interface}, IP: {addr.address}"
    return "No IPv4 address found."

def get_proxy_info():
    proxy_env = os.environ.get('http_proxy') or os.environ.get('https_proxy')
    if proxy_env:
        return f"Proxy enabled: {proxy_env}"
    return "No proxy configured."

def get_system_info():
    try:
        uname = platform.uname()
        cores = psutil.cpu_count(logical=True)
        ram = round(psutil.virtual_memory().total / (1024 ** 3), 2)
        
        if uname.system == "Windows":
            version = platform.win32_ver()
            os_version = f"{uname.system} {version[0]} (Build {version[1]})"
        else:
            os_version = f"{uname.system} {uname.release} {uname.version}"
        
        return f"System: {os_version}, {uname.machine}\nCores: {cores}\nRAM: {ram} GB"
    except Exception as e:
        return f"System information could not be determined: {e}"


def get_bios_version():
    try:
        result = subprocess.check_output(
            ['powershell', '-Command', '(Get-WmiObject Win32_BIOS).SMBIOSBIOSVersion'],
            universal_newlines=True
        )
        return f"BIOS version: {result.strip()}"
    except Exception as e:
        return f"BIOS version could not be determined: {e}"


def get_host_name():
    return f"Host Name: {socket.gethostname()}"

class MyTestApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MyTest - System Info")
        self.resize(600, 400)

        self.layout = QVBoxLayout()
        self.text_view = QTextEdit()
        self.text_view.setReadOnly(True)
        self.layout.addWidget(self.text_view)

        # Buttons
        self.add_button("Get IPv4 Info", get_ipv4_info)
        self.add_button("Check Proxy", get_proxy_info)
        self.add_button("System Info", get_system_info)
        self.add_button("BIOS Version", get_bios_version)
        self.add_button("Host Name", get_host_name)

        self.setLayout(self.layout)

    def add_button(self, label, action):
        button = QPushButton(label)
        button.clicked.connect(lambda: self.run_action(action))
        self.layout.addWidget(button)

    def run_action(self, action):
        result = action()
        self.text_view.append(result + '\n')

def main():
    if len(sys.argv) > 1:
        command = sys.argv[1]
        commands = {
            "button1": get_ipv4_info,
            "button2": get_proxy_info,
            "button3": get_system_info,
            "button4": get_bios_version,
            "button5": get_host_name,
            "help": lambda: "\n".join(["button1: Get IPv4 Info", "button2: Check Proxy", "button3: System Info", "button4: BIOS Version", "button5: Host Name"]),
        }

        if command in commands:
            print(commands[command]())
        else:
            print("Invalid command. Use 'help' for a list of commands.")
        sys.exit()

    app = QApplication(sys.argv)
    window = MyTestApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
