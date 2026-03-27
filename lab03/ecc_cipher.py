import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.ecc import Ui_MainWindow
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Kết nối Event
        self.ui.btnGenerate.clicked.connect(self.call_api_gen_keys)
        self.ui.btnSig.clicked.connect(self.call_api_sign)
        self.ui.btnVerify.clicked.connect(self.call_api_verify)

    def call_api_gen_keys(self):
        url = "http://127.0.0.1:5000/api/ecc/generate_keys"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Thông báo")
                msg.setText(data.get("message", "Keys generated!"))
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    def call_api_sign(self):
        url = "http://127.0.0.1:5000/api/ecc/sign"
        # Sửa thành txtinfo theo hình
        payload = {
            "message": self.ui.txtinfo.toPlainText(), 
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                # Sửa thành txtSig theo hình
                self.ui.txtSig.setPlainText(data["signature"]) 

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Signed Successfully")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    def call_api_verify(self):
        url = "http://127.0.0.1:5000/api/ecc/verify"
        # Sửa tên biến txtinfo và txtSig cho đúng với Object Inspector
        payload = {
            "message": self.ui.txtinfo.toPlainText(),
            "signature": self.ui.txtSig.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                if data.get("is_verified"):
                    msg.setText("Verified Successfully")
                else:
                    msg.setText("Verified Fail")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())