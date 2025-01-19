import sys
from PyQt6.QtWidgets import QApplication

from modules.system_info import get_system_info
from modules.host_info import get_host_name
from modules.bios_info import get_bios_version
from modules.network_info import get_ipv4_info
from modules.proxy_info import get_proxy_info
from ui import MyTestApp

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
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
