import sys, socket, threading, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, QObject
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad

class ClientSignals(QObject):
    log = pyqtSignal(str)

class ClientUI(QWidget):
    def __init__(self):
        super().__init__()
        self.signals = ClientSignals()
        self.client_key = RSA.generate(2048) # Logic gốc: Client tạo RSA
        self.aes_key = None
        self.sock = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("HUTECH - AES-RSA Client UI")
        self.setFixedSize(500, 500)
        layout = QVBoxLayout()

        self.btn_connect = QPushButton("KẾT NỐI SERVER")
        self.btn_connect.setFixedHeight(40)
        self.btn_connect.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
        self.btn_connect.clicked.connect(self.start_connection)
        layout.addWidget(self.btn_connect)

        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet("background-color: #f4f4f4; color: #333;")
        self.signals.log.connect(lambda text: self.log_area.append(text))
        layout.addWidget(QLabel("<b>Nhật ký hoạt động:</b>"))
        layout.addWidget(self.log_area)

        self.msg_input = QLineEdit()
        self.msg_input.setPlaceholderText("Nhập tin nhắn...")
        layout.addWidget(self.msg_input)

        self.btn_send = QPushButton("GỬI TIN NHẮN MÃ HÓA")
        self.btn_send.setEnabled(False)
        self.btn_send.setFixedHeight(40)
        self.btn_send.setStyleSheet("background-color: #4CAF50; color: white;")
        self.btn_send.clicked.connect(self.send_message)
        layout.addWidget(self.btn_send)

        self.setLayout(layout)

    def decrypt_message(self, key, encrypted_message):
        iv = encrypted_message[:16]
        ciphertext = encrypted_message[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ciphertext), AES.block_size).decode()

    def encrypt_message(self, key, message):
        cipher = AES.new(key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
        return cipher.iv + ciphertext

    def start_connection(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(('localhost', 12345))
            threading.Thread(target=self.handshake_and_receive, daemon=True).start()
        except Exception as e:
            self.signals.log.emit(f"Lỗi kết nối: {e}")

    def handshake_and_receive(self):
        try:
            # 1. Nhận Server Public Key
            server_pub_key = RSA.import_key(self.sock.recv(2048))
            self.signals.log.emit("[+] Đã nhận Server Public Key.")

            # 2. Gửi Client Public Key
            self.sock.send(self.client_key.publickey().export_key(format='PEM'))
            self.signals.log.emit("[+] Đã gửi Client Public Key.")

            # 3. Nhận AES Key (mã hóa RSA)
            enc_aes_key = self.sock.recv(2048)
            cipher_rsa = PKCS1_OAEP.new(self.client_key)
            self.aes_key = cipher_rsa.decrypt(enc_aes_key)
            self.signals.log.emit(f"[OK] Đã nhận khóa AES: {self.aes_key.hex()}")

            self.btn_send.setEnabled(True)
            self.btn_connect.setEnabled(False)

            # 4. Luồng nhận tin nhắn liên tục
            while True:
                data = self.sock.recv(1024)
                if not data: break
                msg = self.decrypt_message(self.aes_key, data)
                self.signals.log.emit(f"<b>Server/Client khác:</b> {msg}")
        except Exception as e:
            self.signals.log.emit(f"Lỗi: {e}")

    def send_message(self):
        msg = self.msg_input.text()
        if msg:
            enc_msg = self.encrypt_message(self.aes_key, msg)
            self.sock.send(enc_msg)
            self.signals.log.emit(f"Bạn: {msg}")
            self.msg_input.clear()
            if msg == "exit": self.sock.close(); sys.exit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ClientUI(); win.show()
    sys.exit(app.exec_())