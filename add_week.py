import base64
from Crypto.Cipher import AES
from Crypto.Hash import MD5
import re
from datetime import datetime, timedelta

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

def encrypt_cryptojs(data_text, password):
    data_bytes = data_text.encode('utf-8')
    import os
    salt = os.urandom(8)
    
    key_iv = b''
    prev = b''
    while len(key_iv) < 48:
        md5_hash = MD5.new(prev + password.encode('utf-8') + salt)
        key_iv += md5_hash.digest()
        prev = md5_hash.digest()
    
    key = key_iv[:32]
    iv = key_iv[32:48]
    
    block_size = 16
    padding = block_size - (len(data_bytes) % block_size)
    padded_data = data_bytes + bytes([padding]) * padding
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(padded_data)
    
    result = b'Salted__' + salt + encrypted
    return base64.b64encode(result).decode('utf-8')

decrypted_text = decrypt_cryptojs(encrypted_data, password)

# Находим навигацию по неделям
nav_pattern = r'(<div class="sub-tab-nav">.*?</div>)'
nav_match = re.search(nav_pattern, decrypted_text, re.DOTALL)

if nav_match:
    nav_section = nav_match.group(1)
    print("Текущая навигация:")
    print(nav_section)
    
    # Находим последнюю неделю
    week_buttons = re.findall(r'data-subtab="week(\d+)"', nav_section)
    if week_buttons:
        max_week = max([int(w) for w in week_buttons])
        new_week_num = max_week + 1
        print(f"\nДобавляем Week {new_week_num}")
        
        # Определяем даты для новой недели (начиная с June 1)
        start_date = datetime(2025, 6, 1)
        
        # Создаем кнопку для новой недели
        moon_icons = ['🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘', '🌑', '🌒']
        moon_icon = moon_icons[(new_week_num - 1) % len(moon_icons)]
        
        new_button = f'<button class="sub-tab-btn" data-subtab="week{new_week_num}"><span class="sub-tab-icon">{moon_icon}</span> Week {new_week_num}</button>'
        
        # Вставляем новую кнопку перед закрывающим тегом
        new_nav = nav_section.replace('</div>', f'{new_button}</div>')
        print(f"\nНовая навигация:")
        print(new_nav)
        
        # Заменяем навигацию в тексте
        decrypted_text = decrypted_text.replace(nav_section, new_nav)
        
        # Теперь находим конец panel-meditation и добавляем контент для новой недели
        panel_end_marker = '<!-- METAMORPHOSIS'
        panel_end_pos = decrypted_text.find(panel_end_marker)
        
        if panel_end_pos != -1:
            # Генерируем контент для новой недели
            week_content = f'''
                <div class="sub-panel" id="sub-panel-week{new_week_num}">
                    <article class="day-entry">
                        <div class="day-header"><span class="day-date">June 1</span><span class="day-status status-not">meditation not done</span><span class="day-divider"></span></div>
                        <div class="day-text">
                            <p>Week {new_week_num} — Day 1. Starting fresh with deeper focus.</p>
                        </div>
                    </article>
                    <article class="day-entry">
                        <div class="day-header"><span class="day-date">June 2</span><span class="day-status status-not">meditation not done</span><span class="day-divider"></span></div>
                        <div class="day-text">
                            <p>Week {new_week_num} — Day 2. Building momentum.</p>
                        </div>
                    </article>
                    <article class="day-entry">
                        <div class="day-header"><span class="day-date">June 3</span><span class="day-status status-not">meditation not done</span><span class="day-divider"></span></div>
                        <div class="day-text">
                            <p>Week {new_week_num} — Day 3. Finding stillness.</p>
                        </div>
                    </article>
                    <article class="day-entry">
                        <div class="day-header"><span class="day-date">June 4</span><span class="day-status status-not">meditation not done</span><span class="day-divider"></span></div>
                        <div class="day-text">
                            <p>Week {new_week_num} — Day 4. Deepening practice.</p>
                        </div>
                    </article>
                    <article class="day-entry">
                        <div class="day-header"><span class="day-date">June 5</span><span class="day-status status-not">meditation not done</span><span class="day-divider"></span></div>
                        <div class="day-text">
                            <p>Week {new_week_num} — Day 5. Observing thoughts.</p>
                        </div>
                    </article>
                    <article class="day-entry">
                        <div class="day-header"><span class="day-date">June 6</span><span class="day-status status-not">meditation not done</span><span class="day-divider"></span></div>
                        <div class="day-text">
                            <p>Week {new_week_num} — Day 6. Cultivating awareness.</p>
                        </div>
                    </article>
                    <article class="day-entry">
                        <div class="day-header"><span class="day-date">June 7</span><span class="day-status status-not">meditation not done</span><span class="day-divider"></span></div>
                        <div class="day-text">
                            <p>Week {new_week_num} — Day 7. Integration and reflection.</p>
                        </div>
                    </article>
                </div>
            '''
            
            # Вставляем перед маркером METAMORPHOSIS
            decrypted_text = decrypted_text[:panel_end_pos] + week_content + '\n\n' + decrypted_text[panel_end_pos:]
            
            print(f"\n✓ Добавлена Week {new_week_num} (June 1-7)")
            
            # Шифруем обратно
            encrypted_result = encrypt_cryptojs(decrypted_text, password)
            
            # Заменяем в файле
            new_content = content.replace(match.group(0), f'const encryptedWry = "{encrypted_result}";')
            
            with open('index.html', 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✓ Файл index.html успешно обновлен!")
        else:
            print("Не найден маркер METAMORPHOSIS")
    else:
        print("Не найдено кнопок недель")
else:
    print("Не найдена навигация sub-tab-nav")
