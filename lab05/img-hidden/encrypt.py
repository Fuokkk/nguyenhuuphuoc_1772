import sys
from PIL import Image

def encode_image(image_path, message):
    try:
        # Open the image and ensure it's in RGB mode
        img = Image.open(image_path).convert("RGB")
    except Exception as e:
        print(f"Error opening image: {e}")
        return

    pixels = list(img.getdata())
    width, height = img.size
    
    # 1. Convert message to binary (8-bit) + delimiter (16-bit)
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    binary_message += '1111111111111110'  # End of message marker
    
    # 2. Check if the image is large enough
    # Each pixel has 3 channels (R, G, B), so capacity is width * height * 3
    if len(binary_message) > len(pixels) * 3:
        print("Error: Message is too large for this image.")
        return

    new_pixels = []
    data_index = 0
    
    # 3. Iterate through pixels and modify LSB
    for pixel in pixels:
        pixel_list = list(pixel) # Convert tuple to list to modify
        
        for color_channel in range(3):
            if data_index < len(binary_message):
                # Clear the last bit (& ~1) and OR it with the message bit
                current_bit = int(binary_message[data_index])
                pixel_list[color_channel] = (pixel_list[color_channel] & ~1) | current_bit
                data_index += 1
        
        new_pixels.append(tuple(pixel_list))

    # 4. Save the new image
    new_img = Image.new(img.mode, img.size)
    new_img.putdata(new_pixels)
    
    encoded_image_path = 'encoded_image.png'
    new_img.save(encoded_image_path)
    print(f"Steganography complete. Encoded image saved as: {encoded_image_path}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python encrypt.py <image_path> \"Your message here\"")
        return

    image_path = sys.argv[1]
    # Join all arguments after the path to allow messages with spaces
    message = " ".join(sys.argv[2:])
    encode_image(image_path, message)

if __name__ == "__main__":
    main()