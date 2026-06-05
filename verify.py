import base64
from Crypto.Cipher import AES
from Crypto.Hash import MD5
import re

password = "wry"

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'const encryptedWry = "([^"]+)";', content)
encrypted_data = match.group(1)

def decrypt_cryptojs(encrypted, password):
    data = base64.b64decode(encrypted)
    salt = data[8:16]
    ciphertext = data[16:]
    
    key_iv = b''
    prev = b''
    while len(key_iv) < 48:
        md5_hash = MD5.new(prev + password.encode('utf-8') + salt)
        key_iv += md5_hash.digest()
        prev = md5_hash.digest()
    
    key = key_iv[:32]
    iv = key_iv[32:48]
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(ciphertext)
    pad_len = decrypted[-1]
    decrypted = decrypted[:-pad_len]
    return decrypted.decode('utf-8')

decrypted_text = decrypt_cryptojs(encrypted_data, password)

# Находим навигацию по неделям
nav_pattern = r'(<div class="sub-tab-nav">.*?</div>)'
nav_match = re.search(nav_pattern, decrypted_text, re.DOTALL)

if nav_match:
    nav_section = nav_match.group(1)
    print("=== Навигация по неделям в разделе Meditation ===")
    print(nav_section)
    print()
    
    week_buttons = re.findall(r'data-subtab="week(\d+)"', nav_section)
    if week_buttons:
        weeks = [int(w) for w in week_buttons]
        print(f"Всего недель: {len(weeks)}")
        print(f"Недели: {', '.join([f'Week {w}' for w in weeks])}")
        
        # Проверяем контент для каждой недели
        for week_num in weeks:
            panel_id = f'sub-panel-week{week_num}'
            if panel_id in decrypted_text:
                print(f"✓ Контент для {panel_id} найден")
            else:
                print(f"✗ Контент для {panel_id} НЕ найден")
