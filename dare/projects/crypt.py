from cryptography.fernet import Fernet
import json
# Generate and store this key securely
key = b'HqimpHwvpjigCgr10_megvwT1u1KBYR6LkzdaeYlUp4=' #Fernet.generate_key()
cipher = Fernet(key)


def decrypt_data(encrypted_string):
    decrypted_data = cipher.decrypt(encrypted_string).decode()  # Decrypt and convert back to string
    return json.loads(decrypted_data)  # Convert JSON string back to dictionary

# print(decrypt_data("gAAAAABn7ssZ9_qsBhcKReZli8Wwd3aMpH2nsj35qaORC_Uefp3ITd4QrJ3iIFNtwdF3dXYVWSIsSuczBmaq_SkwPo9rM8eFBX_IWYPWPF3ACVw6cgZ_jGc5Rbnshm0QzU_8EwcNNl3g"))