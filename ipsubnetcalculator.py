import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QFormLayout, QLineEdit, QPushButton,
                             QLabel, QGroupBox, QMessageBox)
import ipaddress

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IP Subnet Calculator")
        self.setGeometry(100, 100, 600, 400)

        # Central Widget and Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Input Group
        input_group = QGroupBox("Network Information")
        input_layout = QFormLayout()
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("e.g., 192.168.1.1")
        self.subnet_input = QLineEdit()
        self.subnet_input.setPlaceholderText("e.g., 255.255.255.0 or 24")
        input_layout.addRow("IP Address:", self.ip_input)
        input_layout.addRow("Subnet Mask:", self.subnet_input)
        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)

        # Buttons
        button_layout = QHBoxLayout()
        self.calculate_btn = QPushButton("Calculate")
        self.calculate_btn.clicked.connect(self.calculate)
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear)
        button_layout.addWidget(self.calculate_btn)
        button_layout.addWidget(self.clear_btn)
        main_layout.addLayout(button_layout)

        # Results Group
        result_group = QGroupBox("Results")
        result_layout = QFormLayout()
        
        # Create result labels
        self.network_address_label = QLabel()
        self.broadcast_address_label = QLabel()
        self.subnet_mask_label = QLabel()
        self.cidr_label = QLabel()
        self.total_hosts_label = QLabel()
        self.usable_hosts_label = QLabel()
        self.host_range_label = QLabel()
        self.ip_binary_label = QLabel()
        self.subnet_binary_label = QLabel()

        # Add rows to result layout
        result_layout.addRow("Network Address:", self.network_address_label)
        result_layout.addRow("Broadcast Address:", self.broadcast_address_label)
        result_layout.addRow("Subnet Mask:", self.subnet_mask_label)
        result_layout.addRow("CIDR Notation:", self.cidr_label)
        result_layout.addRow("Total Hosts:", self.total_hosts_label)
        result_layout.addRow("Usable Hosts:", self.usable_hosts_label)
        result_layout.addRow("Host Range:", self.host_range_label)
        result_layout.addRow("IP Address (Binary):", self.ip_binary_label)
        result_layout.addRow("Subnet Mask (Binary):", self.subnet_binary_label)
        
        result_group.setLayout(result_layout)
        main_layout.addWidget(result_group)

    def calculate(self):
        ip_str = self.ip_input.text().strip()
        subnet_str = self.subnet_input.text().strip()

        if not ip_str or not subnet_str:
            QMessageBox.warning(self, "Error", "Please enter both IP address and subnet mask.")
            return

        try:
            interface = ipaddress.IPv4Interface(f"{ip_str}/{subnet_str}")
        except ValueError as e:
            QMessageBox.warning(self, "Error", f"Invalid IP or subnet mask: {e}")
            return

        network = interface.network

        # Network details
        net_addr = network.network_address
        broadcast_addr = network.broadcast_address
        subnet_mask = interface.netmask
        cidr = network.prefixlen
        total_hosts = network.num_addresses
        usable_hosts = max(0, total_hosts - 2)

        # Host range calculation
        if usable_hosts > 0:
            first_host = net_addr + 1
            last_host = broadcast_addr - 1
            host_range = f"{first_host} - {last_host}"
        else:
            host_range = "No usable hosts"

        # Convert to binary
        ip_binary = self.to_binary(str(interface.ip))
        subnet_binary = self.to_binary(str(subnet_mask))

        # Update labels
        self.network_address_label.setText(str(net_addr))
        self.broadcast_address_label.setText(str(broadcast_addr))
        self.subnet_mask_label.setText(str(subnet_mask))
        self.cidr_label.setText(f"/{cidr}")
        self.total_hosts_label.setText(str(total_hosts))
        self.usable_hosts_label.setText(str(usable_hosts))
        self.host_range_label.setText(host_range)
        self.ip_binary_label.setText(ip_binary)
        self.subnet_binary_label.setText(subnet_binary)

    def to_binary(self, address):
        octets = address.split('.')
        binary_octets = []
        for octet in octets:
            binary_octet = bin(int(octet))[2:].zfill(8)
            binary_octets.append(binary_octet)
        return '.'.join(binary_octets)

    def clear(self):
        self.ip_input.clear()
        self.subnet_input.clear()
        self.network_address_label.clear()
        self.broadcast_address_label.clear()
        self.subnet_mask_label.clear()
        self.cidr_label.clear()
        self.total_hosts_label.clear()
        self.usable_hosts_label.clear()
        self.host_range_label.clear()
        self.ip_binary_label.clear()
        self.subnet_binary_label.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())