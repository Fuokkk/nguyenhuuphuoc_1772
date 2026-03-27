import sys, socket, threading
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, QObject
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

class ServerSignals(QObject):
    log = pyqtSignal(str)

class ServerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.signals = ServerSignals()
        # LOGIC GỐC: Server tạo RSA key
        self.server_key = RSA.generate(2048)
        self.clients = [] 
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("HUTECH - AES-RSA Server UI (Fix IV Error)")
        self.setFixedSize(600, 500)
        layout = QVBoxLayout()

        layout.addWidget(QLabel("<b>RSA Public Key:</b>"))
        self.pub_key_display = QTextEdit(self.server_key.publickey().export_key().decode())
        self.pub_key_display.setFixedHeight(80)
        self.pub_key_display.setReadOnly(True)
        layout.addWidget(self.pub_key_display)

        layout.addWidget(QLabel("<b>Nhật ký Chat:</b>"))
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet("background-color: #1e1e1e; color: #00ff00; font-family: Consolas;")
        self.signals.log.connect(lambda text: self.log_area.append(text))
        layout.addWidget(self.log_area)

        self.setLayout(layout)
        threading.Thread(target=self.start_server, daemon=True).start()

    # --- HÀM LOGIC GỐC TỪ SERVER.PY CỦA BẠN ---
    def encrypt_message(self, key, message):
        cipher = AES.new(key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
        return cipher.iv + ciphertext # Trả về IV (16 bytes) + Ciphertext

    def decrypt_message(self, key, encrypted_message):
        if len(encrypted_message) < 16:
            return "[Lỗi] Dữ liệu nhận được quá ngắn"
        iv = encrypted_message[:16]
        ciphertext = encrypted_message[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return decrypted_message.decode()

    def handle_client(self, client_socket, client_address):
        self.signals.log.emit(f"Kết nối từ: {client_address}")
        try:
            # 1. Gửi Server Public Key
            client_socket.send(self.server_key.publickey().export_key(format='PEM'))
            
            # 2. Nhận Client Public Key
            data = client_socket.recv(2048)
            if not data: return
            client_received_key = RSA.import_key(data)
            
            # 3. Tạo AES Key và gửi cho Client (mã hóa RSA)
            aes_key = get_random_bytes(16)
            cipher_rsa = PKCS1_OAEP.new(client_received_key)
            encrypted_aes_key = cipher_rsa.encrypt(aes_key)
            client_socket.send(encrypted_aes_key)
            
            self.signals.log.emit(f"Trao đổi khóa thành công với {client_address}")
            self.clients.append((client_socket, aes_key))

            while True:
                encrypted_message = client_socket.recv(1024)
                if not encrypted_message: break
                
                # Giải mã và hiển thị lên UI
                decrypted_message = self.decrypt_message(aes_key, encrypted_message)
                self.signals.log.emit(f"<b>{client_address}:</b> {decrypted_message}")

                # Chuyển tiếp tin nhắn cho các Client khác (logic Chat Room)
                for client, key in self.clients:
                    if client != client_socket:
                        encrypted = self.encrypt_message(key, decrypted_message)
                        client.send(encrypted)
        except Exception as e:
            self.signals.log.emit(f"Lỗi client {client_address}: {str(e)}")
        finally:
            client_socket.close()

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', 12345))
        server_socket.listen(5)
        self.signals.log.emit("Server UI đang đợi kết nối...")
        while True:
            client_socket, addr = server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket, addr), daemon=True).start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ServerUI(); window.show()
    sys.exit(app.exec_())