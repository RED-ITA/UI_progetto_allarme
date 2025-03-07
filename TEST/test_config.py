import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QLabel, QPushButton, QWidget
import requests

class WiFiConfigApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configurazione Wi-Fi ESP32")

        layout = QVBoxLayout()

        # Campo per SSID
        self.ssid_input = QLineEdit()
        self.ssid_input.setPlaceholderText("Inserisci SSID Wi-Fi")
        layout.addWidget(QLabel("SSID:"))
        layout.addWidget(self.ssid_input)

        # Campo per Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Inserisci Password Wi-Fi")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)

        # Pulsante di invio
        send_button = QPushButton("Invia Configurazione")
        send_button.clicked.connect(self.send_wifi_config)
        layout.addWidget(send_button)

        # Widget centrale
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def send_wifi_config(self):
        ssid = self.ssid_input.text()
        password = self.password_input.text()
        
        # IP locale dell’ESP32 in modalità AP
        esp32_ip = "192.168.4.1"  # L'ESP32 usa tipicamente questo IP come AP
        
        # Invio delle credenziali al server ESP32
        try:
            response = requests.post(f"http://{esp32_ip}/wifi_config", json={"ssid": ssid, "password": password})
            if response.status_code == 200:
                print("Configurazione Wi-Fi inviata con successo!")
            else:
                print("Errore nella configurazione:", response.status_code)
        except Exception as e:
            print("Errore nella connessione all'ESP32:", e)

app = QApplication(sys.argv)
window = WiFiConfigApp()
window.show()
app.exec()
