import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.rsa import Ui_MainWindow
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Kết nối Event cho các nút bấm (Tên đã khớp với file UI)
        self.ui.btnGenerateKeys.clicked.connect(self.call_api_gen_keys)
        self.ui.btnEncrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btnDecrypt.clicked.connect(self.call_api_decrypt)
        self.ui.btnSign.clicked.connect(self.call_api_sign)
        self.ui.btnVerify.clicked.connect(self.call_api_verify)

    def call_api_gen_keys(self):
        url = "http://127.0.0.1:5000/api/rsa/generate_keys"
        try:
            # Nếu bạn đã sửa API sang POST thì đổi .get thành .post ở đây
            response = requests.get(url) 
            if response.status_code == 200:
                data = response.json()
                QMessageBox.information(self, "Thông báo", data["message"])
            else:
                print("Error while calling API")
        except Exception as e:
            print(f"Error: {e}")

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/encrypt"
        payload = {
            "message": self.ui.txtplaintext.toPlainText(),
            "key_type": "public"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txtciphertext.setPlainText(data["encrypted_message"])
                QMessageBox.information(self, "Thông báo", "Encrypted Successfully")
        except Exception as e:
            print(f"Error: {e}")

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/decrypt"
        payload = {
            "ciphertext": self.ui.txtciphertext.toPlainText(),
            "key_type": "private" # Đã sửa lỗi chính tả 'privale'
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txtplaintext.setPlainText(data["decrypted_message"])
                QMessageBox.information(self, "Thông báo", "Decrypted Successfully")
        except Exception as e:
            print(f"Error: {e}")

    def call_api_sign(self):
        url = "http://127.0.0.1:5000/api/rsa/sign"
        payload = {
            "message": self.ui.txtinformatic.toPlainText(),
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                # ĐÃ SỬA: txtsign thành txtsignature (khớp với UI)
                self.ui.txtsignature.setPlainText(data["signature"])
                QMessageBox.information(self, "Thông báo", "Signed Successfully")
        except Exception as e:
            print(f"Error: {e}")

    def call_api_verify(self):
        url = "http://127.0.0.1:5000/api/rsa/verify"
        payload = {
            "message": self.ui.txtinformatic.toPlainText(),
            "signature": self.ui.txtsignature.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                if data.get("is_verified"):
                    QMessageBox.information(self, "Kết quả", "Verified Successfully")
                else:
                    QMessageBox.warning(self, "Kết quả", "Verified Fail")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())