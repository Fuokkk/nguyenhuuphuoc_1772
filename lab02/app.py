from flask import Flask, render_template, request
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayFairCipher
from cipher.transposition import TranspositionCipher

app = Flask(__name__)

# --- TRANG CHỦ ---
@app.route("/")
def home():
    return render_template('index.html')

# Đường dẫn /caesar khớp với href trong index.html
@app.route("/caesar")
def caesar():
    return render_template('caesar.html')

@app.route("/encrypt", methods=['POST'])
def caesar_encrypt():
    text = request.form.get('inputPlainText', '')
    key = int(request.form.get('inputKeyPlain', 0))
    Caesar = CaesarCipher()
    encrypted_text = Caesar.encrypt_text(text, key)
    # Trả về trang caesar.html kèm kết quả mã hóa
    return render_template('caesar.html', res_en=encrypted_text, old_txt_en=text, old_key_en=key)

@app.route("/decrypt", methods=['POST'])
def caesar_decrypt():
    text = request.form.get('inputCipherText', '')
    key = int(request.form.get('inputKeyCipher', 0))
    Caesar = CaesarCipher()
    decrypted_text = Caesar.decrypt_text(text, key)
    # Trả về trang caesar.html kèm kết quả giải mã
    return render_template('caesar.html', res_de=decrypted_text, old_txt_de=text, old_key_de=key)

# --- 2. VIGENERE CIPHER ---
@app.route("/vigenere")
def vigenere():
    return render_template('vigenere.html')

@app.route("/vigenere_encrypt", methods=['POST'])
def vigenere_encrypt_route():
    text = request.form.get('inputPlainText', '')
    key = request.form.get('inputKeyPlain', '')
    vigenere_obj = VigenereCipher()
    # Gọi hàm vigenere_encrypt từ class của bạn
    encrypted_text = vigenere_obj.vigenere_encrypt(text, key)
    return render_template('vigenere.html', 
                           res_en=encrypted_text, 
                           old_txt_en=text, 
                           old_key_en=key)

@app.route("/vigenere_decrypt", methods=['POST'])
def vigenere_decrypt_route():
    text = request.form.get('inputCipherText', '')
    key = request.form.get('inputKeyCipher', '')
    vigenere_obj = VigenereCipher()
    # Gọi hàm vigenere_decrypt từ class của bạn
    decrypted_text = vigenere_obj.vigenere_decrypt(text, key)
    return render_template('vigenere.html', 
                           res_de=decrypted_text, 
                           old_txt_de=text, 
                           old_key_de=key)

# --- 3. RAIL FENCE CIPHER ---
@app.route("/railfence")
def railfence(): 
    return render_template('railfence.html')

@app.route("/railfence_encrypt", methods=['POST'])
def railfence_encrypt():
    text = request.form.get('inputPlainText', '')
    key = int(request.form.get('inputKeyPlain', 2))
    railfence_obj = RailFenceCipher()
    res = railfence_obj.encrypt(text, key)
    return render_template('railfence.html', res_en=res, old_txt_en=text, old_key_en=key)

# --- 4. PLAYFAIR CIPHER ---
@app.route("/playfair")
def playfair(): 
    return render_template('playfair.html')

@app.route("/playfair_encrypt", methods=['POST'])
def playfair_encrypt():
    text = request.form.get('inputPlainText', '')
    key = request.form.get('inputKeyPlain', '')
    playfair_obj = PlayFairCipher()
    res = playfair_obj.encrypt(text, key)
    return render_template('playfair.html', res_en=res, old_txt_en=text, old_key_en=key)

# --- 5. TRANSPOSITION CIPHER ---
@app.route("/transposition")
def transposition(): 
    return render_template('transposition.html')

@app.route("/trans_encrypt", methods=['POST'])
def trans_encrypt():
    text = request.form.get('inputPlainText', '')
    key = request.form.get('inputKeyPlain', '')
    trans_obj = TranspositionCipher()
    res = trans_obj.encrypt(text, key)
    return render_template('transposition.html', res_en=res, old_txt_en=text, old_key_en=key)

# Chạy Server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)