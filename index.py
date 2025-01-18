import sys
import os
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
    uname = os.uname()
    cores = psutil.cpu_count(logical=True)
    ram = round(psutil.virtual_memory().total / (1024 ** 3), 2)
    return f"System: {uname.sysname} {uname.release}, {uname.machine}\nCores: {cores}\nRAM: {ram} GB"

def get_bios_version():
    try:
        result = subprocess.check_output(['wmic', 'bios', 'get', 'SMBIOSBIOSVersion'], universal_newlines=True)
        return result.strip().split('\n')[1]
    except Exception:
        return "BIOS version could not be determined."

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
