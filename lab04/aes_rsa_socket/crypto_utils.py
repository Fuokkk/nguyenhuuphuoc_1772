from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

class CryptoManager:
    def __init__(self):
        self.key_pair = RSA.generate(2048)
        self.public_key = self.key_pair.public_key().export_key()
        self.aes_key = None

    def decrypt_aes_key(self, encrypted_aes_key):
        # Dùng Private Key RSA để giải mã khóa AES nhận từ Client
        cipher_rsa = PKCS1_OAEP.new(self.key_pair)
        self.aes_key = cipher_rsa.decrypt(encrypted_aes_key)
        return self.aes_key

    def encrypt_message(self, message):
        # Mã hóa tin nhắn bằng AES
        cipher_aes = AES.new(self.aes_key, AES.MODE_CBC)
        ct_bytes = cipher_aes.encrypt(pad(message.encode(), AES.block_size))
        # Trả về iv + ciphertext dưới dạng base64 để gửi qua socket
        return base64.b64encode(cipher_aes.iv + ct_bytes).decode()

    def decrypt_message(self, encoded_data):
        # Giải mã tin nhắn AES
        raw_data = base64.b64decode(encoded_data)
        iv = raw_data[:16]
        ct = raw_data[16:]
        cipher_aes = AES.new(self.aes_key, AES.MODE_CBC, iv)
        return unpad(cipher_aes.decrypt(ct), AES.block_size).decode()