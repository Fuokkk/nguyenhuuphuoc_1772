import sys
from PIL import Image

def decode_image(encoded_image_path):
    img = Image.open(encoded_image_path)
    width, height = img.size
    binary_message = ""

    # Bước 1: Trích xuất các bit cuối cùng (LSB) từ mỗi kênh màu của từng pixel
    for row in range(height):
        for col in range(width):
            pixel = img.getpixel((col, row))
            for color_channel in range(3): # Duyệt qua R, G, B
                # Lấy bit cuối cùng và nối vào chuỗi nhị phân
                binary_message += format(pixel[color_channel], '08b')[-1]

    # Bước 2: Chuyển đổi chuỗi nhị phân thành ký tự văn bản
    message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        char = chr(int(byte, 2))
        
        # Kiểm tra ký tự kết thúc thông điệp
        # LƯU Ý: Trong ảnh bạn gửi là '\0', nhưng file mã hóa trước đó dùng '1111111111111110'
        if char == '\0': 
            break
        message += char

    return message

def main():
    if len(sys.argv) != 2:
        print("Usage: python decrypt.py <encoded_image_path>")
        return

    encoded_image_path = sys.argv[1]
    decoded_message = decode_image(encoded_image_path)
    print("Decoded message:", decoded_message)

if __name__ == "__main__":
    main()