import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import cv2
import numpy as np
import os

# ===========================
# 🔧 Setup folders
# ===========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "images")

if not os.path.exists(IMG_DIR):
    os.makedirs(IMG_DIR)

# ===========================
# 🔒 IMAGE ENCRYPTION FUNCTIONS
# ===========================
def encrypt_image():
    file_path = filedialog.askopenfilename(title="Select Image to Encrypt", filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
    if not file_path:
        return

    img = cv2.imread(file_path)
    if img is None:
        messagebox.showerror("Error", "Could not read the image!")
        return

    key = np.random.randint(0, 256, size=img.shape, dtype=np.uint8)
    encrypted = cv2.bitwise_xor(img, key)

    enc_path = os.path.join(IMG_DIR, "encrypted.png")
    key_path = os.path.join(IMG_DIR, "key.npy")

    cv2.imwrite(enc_path, encrypted)
    np.save(key_path, key)

    messagebox.showinfo("Success", f"✅ Image Encrypted!\nEncrypted file: {enc_path}\nKey saved: {key_path}")

def decrypt_image():
    enc_path = os.path.join(IMG_DIR, "encrypted.png")
    key_path = os.path.join(IMG_DIR, "key.npy")

    if not os.path.exists(enc_path) or not os.path.exists(key_path):
        messagebox.showerror("Error", "Missing encrypted image or key file!")
        return

    encrypted = cv2.imread(enc_path)
    key = np.load(key_path)
    decrypted = cv2.bitwise_xor(encrypted, key)

    dec_path = os.path.join(IMG_DIR, "decrypted.png")
    cv2.imwrite(dec_path, decrypted)

    messagebox.showinfo("Success", f"✅ Image Decrypted!\nSaved at: {dec_path}")

def show_images():
    enc_path = os.path.join(IMG_DIR, "encrypted.png")
    dec_path = os.path.join(IMG_DIR, "decrypted.png")

    if not os.path.exists(enc_path) or not os.path.exists(dec_path):
        messagebox.showwarning("Warning", "Please encrypt and decrypt an image first.")
        return

    enc = cv2.imread(enc_path)
    dec = cv2.imread(dec_path)

    cv2.imshow("🔒 Encrypted Image", enc)
    cv2.imshow("🔓 Decrypted Image", dec)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# ===========================
# ✉️ TEXT ENCRYPTION FUNCTIONS
# ===========================
def encrypt_text():
    text = text_input.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Warning", "Please enter some text first.")
        return

    # Convert text to bytes
    data = np.frombuffer(text.encode('utf-8'), dtype=np.uint8)

    # Generate random key of same length
    key = np.random.randint(0, 256, size=data.shape, dtype=np.uint8)

    # XOR encrypt
    encrypted = np.bitwise_xor(data, key)

    # Save encrypted text & key
    np.save(os.path.join(BASE_DIR, "text_key.npy"), key)
    with open(os.path.join(BASE_DIR, "text_encrypted.txt"), "wb") as f:
        f.write(encrypted.tobytes())

    messagebox.showinfo("Success", "✅ Text Encrypted Successfully!\nSaved as text_encrypted.txt")

def decrypt_text():
    key_path = os.path.join(BASE_DIR, "text_key.npy")
    enc_path = os.path.join(BASE_DIR, "text_encrypted.txt")

    if not os.path.exists(key_path) or not os.path.exists(enc_path):
        messagebox.showerror("Error", "Missing encrypted text or key file!")
        return

    key = np.load(key_path)
    with open(enc_path, "rb") as f:
        encrypted = np.frombuffer(f.read(), dtype=np.uint8)

    decrypted = np.bitwise_xor(encrypted, key)
    text = decrypted.tobytes().decode('utf-8', errors='ignore')

    text_input.delete("1.0", tk.END)
    text_input.insert(tk.END, text)
    messagebox.showinfo("Success", "✅ Text Decrypted Successfully!")

# ===========================
# 🖥️ GUI SETUP
# ===========================
root = tk.Tk()
root.title("🧠 Image + Text Encryption App")
root.geometry("500x650")
root.config(bg="#1e1e2e")

# Title
tk.Label(root, text="🔐 Encryption & Decryption App", font=("Arial", 16, "bold"), fg="white", bg="#1e1e2e").pack(pady=10)

# ---------- Image Section ----------
tk.Label(root, text="🖼 Image Encryption", font=("Arial", 14, "bold"), fg="#2ecc71", bg="#1e1e2e").pack(pady=10)

tk.Button(root, text="Encrypt Image", command=encrypt_image, width=20, bg="#2ecc71", fg="white", font=("Arial", 12, "bold")).pack(pady=5)
tk.Button(root, text="Decrypt Image", command=decrypt_image, width=20, bg="#e67e22", fg="white", font=("Arial", 12, "bold")).pack(pady=5)
tk.Button(root, text="Show Images", command=show_images, width=20, bg="#3498db", fg="white", font=("Arial", 12, "bold")).pack(pady=5)

# ---------- Text Section ----------
tk.Label(root, text="✉️ Text Encryption", font=("Arial", 14, "bold"), fg="#f1c40f", bg="#1e1e2e").pack(pady=10)

text_input = scrolledtext.ScrolledText(root, width=50, height=10, font=("Arial", 11))
text_input.pack(pady=10)

tk.Button(root, text="Encrypt Text", command=encrypt_text, width=15, bg="#9b59b6", fg="white", font=("Arial", 11, "bold")).pack(pady=5)
tk.Button(root, text="Decrypt Text", command=decrypt_text, width=15, bg="#e84393", fg="white", font=("Arial", 11, "bold")).pack(pady=5)

# Exit
tk.Button(root, text="Exit", command=root.quit, width=10, bg="#c0392b", fg="white", font=("Arial", 10, "bold")).pack(pady=20)

root.mainloop()
