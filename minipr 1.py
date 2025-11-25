def encrypt_text(text, key):
    encrypted = ''.join(chr((ord(ch) + key) % 256) for ch in text)
    return encrypted

def decrypt_text(encrypted_text, key):
    decrypted = ''.join(chr((ord(ch) - key) % 256) for ch in encrypted_text)
    return decrypted

# Example use:
key = 4
data = "Hello Krushna!"
enc = encrypt_text(data, key)
print("Encrypted:", enc)
print("Decrypted:", decrypt_text(enc, key))
