import binascii  # hex encoding
import ctypes
import json as jsond  # json
import platform
import subprocess
import time  # sleep before exit
from time import gmtime, strftime
from uuid import uuid4  # gen random guid

# https requests

start = strftime("%H:%M:%S", gmtime())
import sys
import os
import colorama
colorama.init(autoreset=False)
from colorama import Fore
import requests


def slow_type(text, speed, newLine=True):
    for i in text:
        print(i, end="", flush=True)
        time.sleep(speed)
    if newLine:
        print()
try:
    from Crypto.Cipher import AES
    from Crypto.Hash import SHA256
    from Crypto.Util.Padding import pad, unpad
except ModuleNotFoundError:
    print("Exception when importing modules")
    print("installing necessary modules....")
    os.system("pip install pycryptodome")
    print("Modules installed!")
    time.sleep(1.5)
    exit(0)


class api:
    name = ownerid = secret = version = hash_to_check = ""

    def __init__(self, name, ownerid, secret, version, hash_to_check):
        self.name = name

        self.ownerid = ownerid

        self.secret = secret

        self.version = version
        self.hash_to_check = hash_to_check
        self.init()

    sessionid = enckey = ""
    initialized = False

    def init(self):

        if self.sessionid != "":
            print("You've already initialized!")
            time.sleep(2)
            exit(0)
        init_iv = SHA256.new(str(uuid4())[:8].encode()).hexdigest()

        self.enckey = SHA256.new(str(uuid4())[:8].encode()).hexdigest()

        post_data = {
            "type": binascii.hexlify(("init").encode()),
            "ver": encryption.encrypt(self.version, self.secret, init_iv),
            "hash": self.hash_to_check,
            "enckey": encryption.encrypt(self.enckey, self.secret, init_iv),
            "name": binascii.hexlify(self.name.encode()),
            "ownerid": binascii.hexlify(self.ownerid.encode()),
            "init_iv": init_iv
        }

        response = self.__do_request(post_data)

        if response == "KeyAuth_Invalid":
            print("The application doesn't exist")
            ctypes.windll.kernel32.SetConsoleTitleW("NLD v1.1 Captcha Token Generator")
            time.sleep(3)
            sys.exit()

        response = encryption.decrypt(response, self.secret, init_iv)
        json = jsond.loads(response)

        if json["message"] == "invalidver":
            print("Invalid Version!")
            ctypes.windll.kernel32.SetConsoleTitleW("NLD v1.1 Captcha Token Generator")
            time.sleep(4)
            sys.exit()

        if not json["success"]:
            print(json["message"])
            ctypes.windll.kernel32.SetConsoleTitleW("NLD v1.1 Captcha Token Generator")
            time.sleep(3)
            sys.exit()

        self.sessionid = json["sessionid"]
        self.initialized = True
        self.__load_app_data(json["appinfo"])

    def register(self, user, password, license, hwid=None):
        self.checkinit()
        if hwid is None:
            hwid = others.get_hwid()

        init_iv = SHA256.new(str(uuid4())[:8].encode()).hexdigest()

        post_data = {
            "type": binascii.hexlify(("register").encode()),
            "username": encryption.encrypt(user, self.enckey, init_iv),
            "pass": encryption.encrypt(password, self.enckey, init_iv),
            "key": encryption.encrypt(license, self.enckey, init_iv),
            "hwid": encryption.encrypt(hwid, self.enckey, init_iv),
            "sessionid": binascii.hexlify(self.sessionid.encode()),
            "name": binascii.hexlify(self.name.encode()),
            "ownerid": binascii.hexlify(self.ownerid.encode()),
            "init_iv": init_iv
        }

        response = self.__do_request(post_data)

        response = encryption.decrypt(response, self.enckey, init_iv)

        json = jsond.loads(response)

        if json["success"]:
            print("successfully registered")
        else:
            print(json["message"])
            sys.exit()

    def upgrade(self, user, license):
        self.checkinit()
        init_iv = SHA256.new(str(uuid4())[:8].encode()).hexdigest()

        post_data = {
            "type": binascii.hexlify(("upgrade").encode()),
            "username": encryption.encrypt(user, self.enckey, init_iv),
            "key": encryption.encrypt(license, self.enckey, init_iv),
            "sessionid": binascii.hexlify(self.sessionid.encode()),
            "name": binascii.hexlify(self.name.encode()),
            "ownerid": binascii.hexlify(self.ownerid.encode()),
            "init_iv": init_iv
        }

        response = self.__do_request(post_data)

        response = encryption.decrypt(response, self.enckey, init_iv)

        json = jsond.loads(response)

        if json["success"]:
            print("successfully upgraded user")
        else:
            print(json["message"])
            sys.exit()

    def login(self, user, password, hwid=None):
        self.checkinit()
        if hwid is None:
            hwid = others.get_hwid()

        init_iv = SHA256.new(str(uuid4())[:8].encode()).hexdigest()

        post_data = {
            "type": binascii.hexlify(("login").encode()),
            "username": encryption.encrypt(user, self.enckey, init_iv),
            "pass": encryption.encrypt(password, self.enckey, init_iv),
            "hwid": encryption.encrypt(hwid, self.enckey, init_iv),
            "sessionid": binascii.hexlify(self.sessionid.encode()),
            "name": binascii.hexlify(self.name.encode()),
            "ownerid": binascii.hexlify(self.ownerid.encode()),
            "init_iv": init_iv
        }

        response = self.__do_request(post_data)

        response = encryption.decrypt(response, self.enckey, init_iv)

        json = jsond.loads(response)

        if json["success"]:
            self.__load_user_data(json["info"])
            print("successfully logged in")
        else:
            print(json["message"])
            sys.exit()

    def license(self, key, hwid=None):
        self.checkinit()
        if hwid is None:
            hwid = others.get_hwid()

        init_iv = SHA256.new(str(uuid4())[:8].encode()).hexdigest()

        post_data = {
            "type": binascii.hexlify(("license").encode()),
            "key": encryption.encrypt(key, self.enckey, init_iv),
            "hwid": encryption.encrypt(hwid, self.enckey, init_iv),
            "sessionid": binascii.hexlify(self.sessionid.encode()),
            "name": binascii.hexlify(self.name.encode()),
            "ownerid": binascii.hexlify(self.ownerid.encode()),
            "init_iv": init_iv
        }

        response = self.__do_request(post_data)
        response = encryption.decrypt(response, self.enckey, init_iv)

        json = jsond.loads(response)

        if json["success"]:
            self.__load_user_data(json["info"])
            print()
            ctypes.windll.kernel32.SetConsoleTitleW("NLD v1.1 Captcha Token Generator")
            slow_type(f"{Fore.LIGHTCYAN_EX}[INFO]{Fore.RESET}{Fore.LIGHTGREEN_EX} Valid License Key!{Fore.RESET}", 0.03)
            slow_type(f"{Fore.LIGHTCYAN_EX}[INFO]{Fore.RESET} Made by{Fore.LIGHTYELLOW_EX} 67 {Fore.RESET}", 0.03)
        else:
            from readsettings import ReadSettings
            #print(json["message"])
            config = ReadSettings("settings.json")
            key = config["LicenseKey"]
            print()
            if json["message"] == "HWID Doesn't match. Ask for key reset.":
                ctypes.windll.kernel32.SetConsoleTitleW("NLD v1.1 Captcha Token Generator")

                slow_type(f"{Fore.LIGHTCYAN_EX}[INFO]{Fore.RESET}{Fore.LIGHTRED_EX} HWID Doesn't Match!{Fore.RESET} [License Key: {key}]", 0.03)
                slow_type(f"{Fore.LIGHTCYAN_EX}[INFO]{Fore.RESET} You can reset HWID in{Fore.LIGHTYELLOW_EX} "
                f"Settings!"
                f"{Fore.RESET}", 0.03)
                time.sleep(3)
                slow_type(f"{Fore.LIGHTCYAN_EX}[INFO]{Fore.RESET} Closing...", 0.03)
                # print(Fore.LIGHTCYAN_EX + "[INFO]" + Fore.RESET + " Closing...")
                time.sleep(1)
                sys.exit()
            if json["message"] == "Key Not Found.":
                ctypes.windll.kernel32.SetConsoleTitleW("NLD v1.1 Captcha Token Generator")
                slow_type(f"{Fore.LIGHTCYAN_EX}[INFO]{Fore.RESET}{Fore.LIGHTRED_EX} License Key Not Found"
                f"!{Fore.RESET} ["
                f"Lice"
                f"nse Key: {key}]", 0.03)
                time.sleep(3)
                slow_type(f"{Fore.LIGHTCYAN_EX}[INFO]{Fore.RESET} Closing...", 0.03)
                # print(Fore.LIGHTCYAN_EX + "[INFO]" + Fore.RESET + " Closing...")
                time.sleep(1)
                sys.exit()
            else:
                ErrorMessage = json["message"]
                ctypes.windll.kernel32.SetConsoleTitleW("NLD v1.1 Captcha Token Generator")

                slow_type(f"{Fore.LIGHTCYAN_EX}[INFO]{Fore.RESET}{Fore.LIGHTRED_EX} "
                f"{ErrorMessage}{Fore.RESET} [License Key: {key}]", 0.03)
                time.sleep(3)
                slow_type(f"{Fore.LIGHTCYAN_EX}[INFO]{Fore.RESET} Closing...", 0.03)
                # print(Fore.LIGHTCYAN_EX + "[INFO]" + Fore.RESET + " Closing...")
                time.sleep(1)
                sys.exit()

    def var(self, name):
        self.checkinit()
        init_iv = SHA256.new(str(uuid4())[:8].encode()).hexdigest()

        post_data = {
            "type": binascii.hexlify(("var").encode()),
            "varid": encryption.encrypt(name, self.enckey, init_iv),
            "sessionid": binascii.hexlify(self.sessionid.encode()),
            "name": binascii.hexlify(self.name.encode()),
            "ownerid": binascii.hexlify(self.ownerid.encode()),
            "init_iv": init_iv
        }

        response = self.__do_request(post_data)

        response = encryption.decrypt(response, self.enckey, init_iv)

        json = jsond.loads(response)

        if json["success"]:
            return json["message"]
        else:
            print(json["message"])
            time.sleep(5)
            sys.exit()

    def getvar(self, var_name):
        self.checkinit()
        init_iv = SHA256.new(str(uuid4())[:8].encode()).hexdigest()

        post_data = {
            "type": binascii.hexlify(("getvar").encode()),
            "var": encryption.encrypt(var_name, self.enckey, init_iv),
            "sessionid": binascii.hexlify(self.sessionid.encode()),
            "name": binascii.hexlify(self.name.encode()),
            "ownerid": binascii.hexlify(self.ownerid.encode()),
            "init_iv": init_iv
        }
        response = self.__do_request(post_data)
        response = encryption.decrypt(response, self.enckey, init_iv)
        json = jsond.loads(response)

        if json["success"]:
            return json["response"]
        else:
            print(json["message"])
            time.sleep(5)
            sys.exit()

    def setvar(self, var_name, var_data):
        self.checkinit()
        init_iv = SHA256.new(str(uuid4())[:8].encode()).hexdigest()
        post_data = {
            "type": binascii.hexlify(("setvar").encode()),
            "var": encryption.encrypt(var_name, self.enckey, init_iv),
            "data": encryption.encrypt(var_data, self.enckey, init_iv),
            "sessionid": binascii.hexlify(self.sessionid.encode()),
            "name": binascii.hexlify(self.name.encode()),
            "ownerid": binascii.hexlify(self.ownerid.encode()),
            "init_iv": init_iv
        }
        response = self.__do_request(post_data)
        response = encryption.decrypt(response, self.enckey, init_iv)
        json = jsond.loads(response)

        if json["success"]:
            return True
        else:
            print(json["message"])
            time.sleep(5)
            sys.exit()

    def ban(self):
        self.checkinit()
        init_iv = SHA256.new(str(uuid4())[:8].encode()).hexdigest()
        post_data = {
            "type": binascii.hexlify(("ban").encode()),
            "sessionid": binascii.hexlify(self.sessionid.encode()),
            "name": binascii.hexlify(self.name.encode()),
            "ownerid": binascii.hexlify(self.ownerid.encode()),
            "init_iv": init_iv
        }
        response = self.__do_request(post_data)
        response = encryption.decrypt(response, self.enckey, init_iv)
        json = jsond.loads(response)

        if json["success"]:
            return True
        else:
            print(json["message"])
            time.sleep(5)
            sys.exit()

    def file(self, fileid):
        self.checkinit()
        init_iv = SHA256.new(str(uuid4())[:8].encode()).hexdigest()

        post_data = {
            "type": binascii.hexlify(("file").encode()),
            "fileid": encryption.encrypt(fileid, self.enckey, init_iv),
            "sessionid": binascii.hexlify(self.sessionid.encode()),
            "name": binascii.hexlify(self.name.encode()),
            "ownerid": binascii.hexlify(self.ownerid.encode()),
            "init_iv": init_iv
        }

        response = self.__do_request(post_data)

        response = encryption.decrypt(response, self.enckey, init_iv)

        json = jsond.loads(response)

        if not json["success"]:
            print(json["message"])
            time.sleep(5)
            sys.exit()
        return binascii.unhexlify(json["contents"])

    def webhook(self, webid, param):
        self.checkinit()
        init_iv = SHA256.new(str(uuid4())[:8].encode()).hexdigest()

        post_data = {
            "type": binascii.hexlify(("webhook").encode()),
            "webid": encryption.encrypt(webid, self.enckey, init_iv),
            "params": encryption.encrypt(param, self.enckey, init_iv),
            "sessionid": binascii.hexlify(self.sessionid.encode()),
            "name": binascii.hexlify(self.name.encode()),
            "ownerid": binascii.hexlify(self.ownerid.encode()),
            "init_iv": init_iv
        }

        response = self.__do_request(post_data)

        response = encryption.decrypt(response, self.enckey, init_iv)
        json = jsond.loads(response)

        if json["success"]:
            return json["message"]
        else:
            print(json["message"])
            time.sleep(5)
            sys.exit()

    def check(self):
        self.checkinit()
        init_iv = SHA256.new(str(uuid4())[:8].encode()).hexdigest()
        post_data = {
            "type": binascii.hexlify(("check").encode()),
            "sessionid": binascii.hexlify(self.sessionid.encode()),
            "name": binascii.hexlify(self.name.encode()),
            "ownerid": binascii.hexlify(self.ownerid.encode()),
            "init_iv": init_iv
        }
        response = self.__do_request(post_data)

        response = encryption.decrypt(response, self.enckey, init_iv)
        json = jsond.loads(response)
        if json["success"]:
            return True
        else:
            return False

    def checkblacklist(self):
        self.checkinit()
        hwid = others.get_hwid()
        init_iv = SHA256.new(str(uuid4())[:8].encode()).hexdigest()
        post_data = {
            "type": binascii.hexlify(("checkblacklist").encode()),
            "hwid": encryption.encrypt(hwid, self.enckey, init_iv),
            "sessionid": binascii.hexlify(self.sessionid.encode()),
            "name": binascii.hexlify(self.name.encode()),
            "ownerid": binascii.hexlify(self.ownerid.encode()),
            "init_iv": init_iv
        }
        response = self.__do_request(post_data)

        response = encryption.decrypt(response, self.enckey, init_iv)
        json = jsond.loads(response)
        if json["success"]:
            return True
        else:
            return False

    def log(self, message):
        self.checkinit()
        init_iv = SHA256.new(str(uuid4())[:8].encode()).hexdigest()

        post_data = {
            "type": binascii.hexlify(("log").encode()),
            "pcuser": encryption.encrypt(os.getenv('username'), self.enckey, init_iv),
            "message": encryption.encrypt(message, self.enckey, init_iv),
            "sessionid": binascii.hexlify(self.sessionid.encode()),
            "name": binascii.hexlify(self.name.encode()),
            "ownerid": binascii.hexlify(self.ownerid.encode()),
            "init_iv": init_iv
        }

        self.__do_request(post_data)

    def checkinit(self):
        if not self.initialized:
            print("Initialize first, in order to use the functions")
            sys.exit()

    def __do_request(self, post_data):

        rq_out = requests.post(
            "https://keyauth.win/api/1.0/", data=post_data
        )

        return rq_out.text

    class application_data_class:
        numUsers = numKeys = app_ver = customer_panel = onlineUsers = ""

    # region user_data
    class user_data_class:
        username = ip = hwid = expires = createdate = lastlogin = subscription = ""

    user_data = user_data_class()
    app_data = application_data_class()

    def __load_app_data(self, data):
        self.app_data.numUsers = data["numUsers"]
        self.app_data.numKeys = data["numKeys"]
        self.app_data.app_ver = data["version"]
        self.app_data.customer_panel = data["customerPanelLink"]
        self.app_data.onlineUsers = data["numOnlineUsers"]

    def __load_user_data(self, data):
        self.user_data.username = data["username"]
        self.user_data.ip = data["ip"]
        self.user_data.hwid = data["hwid"]
        self.user_data.expires = data["subscriptions"][0]["expiry"]
        self.user_data.createdate = data["createdate"]
        self.user_data.lastlogin = data["lastlogin"]
        self.user_data.subcription = data["subscriptions"][0]["subscription"]


class others:
    @staticmethod
    def get_hwid():
        if platform.system() != "Windows":
            return subprocess.Popen('hal-get-property --udi /org/freedesktop/Hal/devices/computer --key system.hardware.uuid'.split())

        cmd = subprocess.Popen(
            "wmic useraccount where name='%username%' get sid", stdout=subprocess.PIPE, shell=True)

        (suppost_sid, error) = cmd.communicate()

        suppost_sid = suppost_sid.split(b'\n')[1].strip()

        return suppost_sid.decode()


class encryption:
    @staticmethod
    def encrypt_string(plain_text, key, iv):
        plain_text = pad(plain_text, 16)

        aes_instance = AES.new(key, AES.MODE_CBC, iv)

        raw_out = aes_instance.encrypt(plain_text)

        return binascii.hexlify(raw_out)

    @staticmethod
    def decrypt_string(cipher_text, key, iv):
        cipher_text = binascii.unhexlify(cipher_text)

        aes_instance = AES.new(key, AES.MODE_CBC, iv)

        cipher_text = aes_instance.decrypt(cipher_text)

        return unpad(cipher_text, 16)

    @staticmethod
    def encrypt(message, enc_key, iv):
        try:
            _key = SHA256.new(enc_key.encode()).hexdigest()[:32]

            _iv = SHA256.new(iv.encode()).hexdigest()[:16]

            return encryption.encrypt_string(message.encode(), _key.encode(), _iv.encode()).decode()
        except:
            print("Invalid Application Information. Long text is secret short text is ownerid. Name is supposed to be app name not username")
            sys.exit()

    @staticmethod
    def decrypt(message, enc_key, iv):
        try:
            _key = SHA256.new(enc_key.encode()).hexdigest()[:32]

            _iv = SHA256.new(iv.encode()).hexdigest()[:16]

            return encryption.decrypt_string(message.encode(), _key.encode(), _iv.encode()).decode()
        except:
            print("Invalid Application Information. Long text is secret short text is ownerid. Name is supposed to be app name not username")
            sys.exit()
