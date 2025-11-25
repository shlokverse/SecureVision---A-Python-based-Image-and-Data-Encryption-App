import cv2
import numpy as np
import os

# ✅ Step 1: Always work with absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))          # Folder where this .py file lives
IMG_DIR = os.path.join(BASE_DIR, "images")                     # Create images/ folder path

# ✅ Step 2: Make sure the folder exists
if not os.path.exists(IMG_DIR):
    os.makedirs(IMG_DIR)

# ✅ Step 3: Encrypt function
def encrypt_image(img_path):
    # Read the image
    img = cv2.imread(img_path)
    if img is None:
        print("❌ Error: Could not read the image. Check your path.")
        return

    # Generate a random key same size as the image
    key = np.random.randint(0, 256, size=img.shape, dtype=np.uint8)

    # Encrypt using XOR
    encrypted = cv2.bitwise_xor(img, key)

    # Save encrypted image and key
    enc_path = os.path.join(IMG_DIR, "encrypted.png")
    key_path = os.path.join(IMG_DIR, "key.npy")

    cv2.imwrite(enc_path, encrypted)
    np.save(key_path, key)

    print("✅ Image encrypted successfully.")
    print("🔑 Key saved at:", key_path)
    print("🗂 Encrypted image saved at:", enc_path)

# ✅ Step 4: Decrypt function
def decrypt_image():
    enc_path = os.path.join(IMG_DIR, "encrypted.png")
    key_path = os.path.join(IMG_DIR, "key.npy")

    # Load encrypted image and key
    if not os.path.exists(enc_path):
        print("❌ Encrypted image not found!")
        return
    if not os.path.exists(key_path):
        print("❌ Key file not found!")
        return

    encrypted = cv2.imread(enc_path)
    key = np.load(key_path)

    # Decrypt using XOR again
    decrypted = cv2.bitwise_xor(encrypted, key)

    # Save decrypted image
    dec_path = os.path.join(IMG_DIR, "decrypted.png")
    cv2.imwrite(dec_path, decrypted)

    print("✅ Image decrypted successfully.")
    print("🗂 Decrypted image saved at:", dec_path)

# ✅ Step 5: Optional — show results visually
def show_images():
    enc = cv2.imread(os.path.join(IMG_DIR, "encrypted.png"))
    dec = cv2.imread(os.path.join(IMG_DIR, "decrypted.png"))
    if enc is None or dec is None:
        print("⚠️ Could not display images. Encrypt/Decrypt first.")
        return
    cv2.imshow("🔒 Encrypted Image", enc)
    cv2.imshow("🔓 Decrypted Image", dec)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# ✅ Step 6: Example usage
if __name__ == "__main__":
    # Make sure you have 'input.jpg' or any image inside the images folder
    encrypt_image(os.path.join(IMG_DIR, "input.jpg"))
    decrypt_image()
    show_images()
