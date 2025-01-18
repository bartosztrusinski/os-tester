from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton
from modules.system_info import get_system_info
from modules.host_info import get_host_name
from modules.bios_info import get_bios_version
from modules.network_info import get_ipv4_info
from modules.proxy_info import get_proxy_info


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