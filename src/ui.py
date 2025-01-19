from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt

from modules.system_info import get_system_info
from modules.host_info import get_host_name
from modules.bios_info import get_bios_version
from modules.network_info import get_ipv4_info
from modules.proxy_info import get_proxy_info


class MyTestApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Operating System Info")
        self.resize(500, 600)

        self.layout = QVBoxLayout()
        self.text_view = QTextEdit()
        self.text_view.setReadOnly(True)
        self.text_view.setStyleSheet("""
          font-size: 16px;
        """)
        self.layout.addWidget(self.text_view)

        self.add_button("Network Info", get_ipv4_info)
        self.add_button("Proxy Info", get_proxy_info)
        self.add_button("System Info", get_system_info)
        self.add_button("BIOS Version", get_bios_version)
        self.add_button("Host Name", get_host_name)

        self.setLayout(self.layout)

    def add_button(self, label, action):
        button = QPushButton(label)
        button.setStyleSheet("""
          font-size: 16px;
          font-weight: bold;
          color: #fafafa;
          background-color: #136095;
          border-radius: 4px;
          padding: 10px;
          margin-top: 5px;
        """)
        button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        button.clicked.connect(lambda: self.run_action(action))
        self.layout.addWidget(button)

    def run_action(self, action):
        result = action()
        self.text_view.append(result + '\n')