from flask import Flask, request, jsonify
import os
# Đảm bảo đường dẫn import chính xác với cấu trúc lab03/cipher/rsa/rsa_cipher.py
from cipher.rsa.rsa_cipher import RSACipher

app = Flask(__name__)

# Khởi tạo đối tượng RSA
rsa_cipher = RSACipher()

@app.route('/api/rsa/generate_keys', methods=['GET'])
def rsa_generate_keys():
    try:
        rsa_cipher.generate_keys()
        return jsonify({'message': 'Keys generated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/rsa/encrypt", methods=["POST"])
def rsa_encrypt():
    data = request.json
    message = data.get('message', '')
    key_type = data.get('key_type', 'public')
    
    try:
        # Load keys trả về (private, public)
        keys = rsa_cipher.load_keys()
        private_key, public_key = keys
        
        key = public_key if key_type == 'public' else private_key
        
        encrypted_message = rsa_cipher.encrypt(message, key)
        return jsonify({'encrypted_message': encrypted_message.hex()})
    except FileNotFoundError:
        return jsonify({'error': 'Key files not found. Please generate keys first!'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/api/rsa/decrypt", methods=["POST"])
def rsa_decrypt():
    data = request.json
    ciphertext_hex = data.get('ciphertext', '')
    key_type = data.get('key_type', 'private')
    
    try:
        keys = rsa_cipher.load_keys()
        private_key, public_key = keys
        
        key = private_key if key_type == 'private' else public_key
        
        ciphertext = bytes.fromhex(ciphertext_hex)
        decrypted_message = rsa_cipher.decrypt(ciphertext, key)
        
        if decrypted_message is False:
            return jsonify({'error': 'Decryption failed'}), 400
            
        return jsonify({'decrypted_message': decrypted_message})
    except FileNotFoundError:
        return jsonify({'error': 'Key files not found.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/rsa/sign', methods=['POST'])
def rsa_sign_message():
    data = request.json
    message = data.get('message', '')
    
    try:
        private_key, _ = rsa_cipher.load_keys()
        signature = rsa_cipher.sign(message, private_key)
        return jsonify({'signature': signature.hex()})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/rsa/verify', methods=['POST'])
def rsa_verify_signature():
    data = request.json
    message = data.get('message', '')
    signature_hex = data.get('signature', '')
    
    try:
        _, public_key = rsa_cipher.load_keys()
        signature = bytes.fromhex(signature_hex)
        is_verified = rsa_cipher.verify(message, signature, public_key)
        return jsonify({'is_verified': is_verified})
    except Exception as e:
        return jsonify({'is_verified': False, 'error': str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)