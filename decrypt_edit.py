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

# Находим навигацию с неделями в meditation
med_panel_start = decrypted_text.find('id="panel-meditation"')
if med_panel_start != -1:
    # Ищем sub-tab-nav
    nav_start = decrypted_text.find('class="sub-tab-nav"', med_panel_start)
    if nav_start != -1:
        nav_end = decrypted_text.find('</div>', nav_start) + 6
        nav_section = decrypted_text[nav_start:nav_end]
        print("Навигация по неделям:")
        print(nav_section)
        print("\n")
        
        # Считаем кнопки week
        week_buttons = re.findall(r'data-subtab="week(\d+)"', nav_section)
        if week_buttons:
            max_week = max([int(w) for w in week_buttons])
            print(f"Всего недель: {len(week_buttons)}")
            print(f"Последняя неделя: Week {max_week}")
            
            # Ищем где заканчивается panel-meditation
            panel_end = decrypted_text.find('<!-- METAMORPHOSIS', med_panel_start)
            if panel_end == -1:
                panel_end = decrypted_text.find('<div class="tab-panel"', med_panel_start + 1000)
            
            meditation_full = decrypted_text[med_panel_start:panel_end]
            print(f"\nДлина раздела meditation: {len(meditation_full)} символов")
            
            # Проверяем последнюю неделю
            last_week_content = meditation_full[-2000:]
            print("\nКонец раздела meditation:")
            print(last_week_content[:1500])
