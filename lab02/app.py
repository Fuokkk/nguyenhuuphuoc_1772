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


@app.route("/caesar")
def caesar():
    return render_template('caesar.html')

@app.route("/encrypt", methods=['POST'])
def caesar_encrypt():
    text = request.form.get('inputPlainText', '')
    key = int(request.form.get('inputKeyPlain', 0))
    Caesar = CaesarCipher()
    encrypted_text = Caesar.encrypt_text(text, key)
    
    return render_template('caesar.html', res_en=encrypted_text, old_txt_en=text, old_key_en=key)

@app.route("/decrypt", methods=['POST'])
def caesar_decrypt():
    text = request.form.get('inputCipherText', '')
    key = int(request.form.get('inputKeyCipher', 0))
    Caesar = CaesarCipher()
    decrypted_text = Caesar.decrypt_text(text, key)
    
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
    
    decrypted_text = vigenere_obj.vigenere_decrypt(text, key)
    return render_template('vigenere.html', 
                           res_de=decrypted_text, 
                           old_txt_de=text, 
                           old_key_de=key)
# --- 3. RAIL FENCE CIPHER ---
@app.route("/railfence")
def railfence_home():
    return render_template('railfence.html')

@app.route("/railfence_encrypt", methods=['POST'])
def railfence_encrypt_route():
    text = request.form.get('inputPlainText', '')
    key_raw = request.form.get('inputKeyPlain', '2')
    key = int(key_raw) if key_raw.isdigit() else 2
    
    railfence_obj = RailFenceCipher()
    res = railfence_obj.rail_fence_encrypt(text, key)
    return render_template('railfence.html', res_en=res, old_txt_en=text, old_key_en=key)

@app.route("/railfence_decrypt", methods=['POST'])
def railfence_decrypt_route():
    text = request.form.get('inputCipherText', '')
    key_raw = request.form.get('inputKeyCipher', '2')
    key = int(key_raw) if key_raw.isdigit() else 2
    
    railfence_obj = RailFenceCipher()
    res = railfence_obj.rail_fence_decrypt(text, key)
    return render_template('railfence.html', res_de=res, old_txt_de=text, old_key_de=key)

#playfair
@app.route("/playfair")
def playfair_home(): 
    return render_template('playfair.html')

@app.route("/playfair_matrix", methods=['POST'])
def playfair_matrix_gen(): 
    key = request.form.get('inputKeyPlain', '').upper().replace(" ", "")
    if not key: key = "KEY"
    playfair_obj = PlayFairCipher()
    matrix = playfair_obj.create_playfair_matrix(key)
    return render_template('playfair.html', matrix=matrix, old_key_en=key)

@app.route("/playfair_encrypt", methods=['POST'])
def playfair_encrypt_process(): 
    text = request.form.get('inputPlainText', '').upper().replace(" ", "")
    key = request.form.get('inputKeyPlain', '').upper().replace(" ", "")
    
    playfair_obj = PlayFairCipher()
    matrix = playfair_obj.create_playfair_matrix(key)
    res = playfair_obj.playfair_encrypt(text, matrix)
    
    return render_template('playfair.html', res_en=res, old_txt_en=text, old_key_en=key, matrix=matrix)

@app.route("/playfair_decrypt", methods=['POST'])
def playfair_decrypt_process(): 
    text = request.form.get('inputCipherText', '').upper().replace(" ", "")
    key = request.form.get('inputKeyCipher', '').upper().replace(" ", "")
    
    playfair_obj = PlayFairCipher()
    matrix = playfair_obj.create_playfair_matrix(key)
    res = playfair_obj.playfair_decrypt(text, matrix)
    
    return render_template('playfair.html', res_de=res, old_txt_de=text, old_key_de=key, matrix=matrix)
# --- 5. TRANSPOSITION CIPHER ---
@app.route("/transposition")
def transposition_home(): 
    return render_template('transposition.html')

@app.route("/trans_encrypt", methods=['POST'])
def trans_encrypt_route():
    text = request.form.get('inputPlainText', '')
    key_raw = request.form.get('inputKeyPlain', '2')
    
    key = int(key_raw) if key_raw.isdigit() else 2
    
    trans_obj = TranspositionCipher()
    res = trans_obj.encrypt(text, key)
    return render_template('transposition.html', res_en=res, old_txt_en=text, old_key_en=key)

@app.route("/trans_decrypt", methods=['POST'])
def trans_decrypt_route():
    text = request.form.get('inputCipherText', '')
    key_raw = request.form.get('inputKeyCipher', '2')
    key = int(key_raw) if key_raw.isdigit() else 2
    
    trans_obj = TranspositionCipher()
    res = trans_obj.decrypt(text, key)
    return render_template('transposition.html', res_de=res, old_txt_de=text, old_key_de=key)

# Chạy Server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)