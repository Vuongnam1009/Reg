import os
import random
from subprocess import CREATE_NO_WINDOW
import threading
import time
import pandas as pd
import requests
# import undetected_chromedriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import re
from re import L
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from PyQt5.QtGui import QBrush, QColor
from selenium.common.exceptions import WebDriverException
import threading,string,random,os,time
from PyQt5 import QtCore, QtGui, QtWidgets
import ipaddress
from PyQt5.QtCore import QThread, pyqtSignal
from selenium.webdriver.support.select import Select
import json
from datetime import datetime, timedelta
import io
import base64
from selenium import webdriver
import logging
from faker import Faker
logging.basicConfig(level=10)
import undetected_chromedriver as uc
from unidecode import unidecode
import uuid
from PIL import Image
import pathlib
import pyotp
from PyQt5.QtCore import Qt
import subprocess
from PyQt5.QtWidgets import QApplication, QMessageBox
from selenium_stealth import stealth
import itertools
class Reg(QThread):
    show = pyqtSignal(int, int, str)
    check = pyqtSignal(bool)
    def __init__(self, ref, x, y, selected_name_type, state, state1, thread_count, selected_proxy, selected_solver, selected_name_type1) -> None:
        super().__init__()
        self.ref = ref
        self.x = x
        self.y = y
        self.userid = []
        self.cookiepd = []
        self.selected_name_type = selected_name_type
        self.state = state
        self.state1 = state1
        self.fileproxy = []
        self.current_proxy_index = 0
        self.thread_count = thread_count
        self.selected_proxy = selected_proxy
        self.selected_solver = selected_solver
        self.selected_indexes = getattr(self, 'selected_indexes', set())
        self.proxy = None
        self.circular_buffer = []
        self.selected_name_type1 = selected_name_type1
    def getproxy(self, api_key):
        js = {
            "api_key": api_key,
            "sign": "string",
            "id_location": 0
        }
        while True:
            a = requests.post('https://tmproxy.com/api/proxy/get-new-proxy', json=js).json()
            if a['code'] == 0:
                print(a['data']['https'])
                return a['data']['https']
            elif a['code'] == 5:
                b = requests.post('https://tmproxy.com/api/proxy/get-current-proxy', json={'api_key': api_key}).json()
                if b['data']['timeout'] >= 300:
                    return b['data']['https']
                else:
                    giay = str(a['message']).split('after ')[1].split(' sec')[0]
                    for x in range(int(giay) + 2, 0, -1):
                        time.sleep(1)
            else:
                return 'no'
    def initialize_circular_buffer(self, length):
        self.circular_buffer = list(range(length))
        random.shuffle(self.circular_buffer)
    def is_ipv6(self,address):
        try:
            ipaddress.IPv6Address(address)
            return True
        except ipaddress.AddressValueError:
            return False
    def set_proxy(self,options, proxy_address):
        options.add_argument(f'--proxy-server={proxy_address}')
    def getDriver(self):
        try:
            time.sleep(3)
            options = webdriver.ChromeOptions()
            if self.selected_proxy == "TM Proxy":
                file_path = 'config/apiproxy.txt'
                with open(file_path, mode='r') as file:
                    fileproxy = file.read().split('\n')
                proxies = list(filter(None, fileproxy))
                if not self.circular_buffer:
                    self.initialize_circular_buffer(len(proxies))
                index = self.circular_buffer.pop(0)
                self.selected_indexes.add(index)
                apiproxy = proxies[index]
                self.proxy = self.getproxy(apiproxy)
                self.show.emit(self.row, 5, 'Thiết lập proxy cho Chrome')
                self.show.emit(self.row, 5, f'Proxy của bạn là {self.proxy}')
                self.show.emit(self.row, 4, self.proxy)
                options.add_argument(f'--proxy-server=http://{self.proxy}')
            elif self.selected_proxy == "tinsoft":
                file_path = "config/apitinsoft.txt"
                with open(file_path, "r") as file:
                    lines = file.readlines()
                num_lines = len(lines)
                if num_lines > 0:
                    random_line = random.choice(lines)
                apikey = random_line
                response_change_proxy = requests.get(f'http://proxy.tinsoftsv.com/api/changeProxy.php?key={apikey}&location=0')
                if response_change_proxy.status_code == 200:
                    try:
                        data_change_proxy = response_change_proxy.json()
                        if data_change_proxy["success"]:
                            self.proxy1 = data_change_proxy["proxy"]
                            self.show.emit(self.row, 5, 'Thiết lập proxy cho Chrome')
                            self.show.emit(self.row, 5, f'Proxy của bạn là {self.proxy1}')
                            self.show.emit(self.row, 4, self.proxy1)
                            options.add_argument(f'--proxy-server=http://{self.proxy1}')
                        else:
                            description_change_proxy = data_change_proxy.get("description", "")
                            if "wait" in description_change_proxy.lower():
                                response_get_proxy = requests.get(f'http://proxy.tinsoftsv.com/api/getProxy.php?key={apikey}')
                                try:
                                    data_get_proxy = response_get_proxy.json()
                                    if data_get_proxy["success"]:
                                        self.previous_proxy = data_get_proxy["proxy"]
                                        self.show.emit(self.row, 5, 'Thiết lập proxy cho Chrome')
                                        self.show.emit(self.row, 5, f'Proxy của bạn là {self.previous_proxy}')
                                        self.show.emit(self.row, 4, self.previous_proxy)
                                        options.add_argument(f'--proxy-server=http://{self.previous_proxy}')
                                    else:
                                        self.show.emit(self.row, 5,f"key sai vui lòng kiểm tra lại key: {data_get_proxy.get('description', '')}")
                                except ValueError as e:
                                   self.show.emit(self.row, 5,f"Không thể phân tích cú pháp phản hồi JSON để nhận proxy trước đó. Lỗi: {e}")
                            else:
                                self.show.emit(self.row, 5,f"Yêu cầu API không thành công. Sự miêu tả: {description_change_proxy}")
                    except ValueError as e:
                        self.show.emit(self.row, 5,f"Không phân tích được phản hồi JSON. Lỗi: {e}")
                else:
                    self.show.emit(self.row, 5,f"Yêu cầu thay đổi proxy không thành công với mã trạng thái: {response_change_proxy.status_code}")
            elif self.selected_proxy == "ip:port:user:pass":
                sleep_time = random.uniform(3, 6)
                time.sleep(sleep_time)
                self.show.emit(self.row, 5, f'Đang delay mở cài proxy, vui lòng đợi {sleep_time:.2f}')

                input_file_path = "config/proxyip.txt"
                output_folder = 'proxyport'
                os.makedirs(output_folder, exist_ok=True)
                output_file_path = os.path.join(output_folder, 'background.js')

                with open(output_file_path, 'w') as output_file:
                    with open(input_file_path, 'r') as input_file:
                        lines = input_file.readlines()

                        for line in random.sample(lines, min(7, len(lines))):  # Lấy ngẫu nhiên 5 dòng từ file
                            ip, port, username, password = line.strip().split(':')
                            js_code = f'''
                var config = {{
                    mode: "fixed_servers",
                    rules: {{
                        singleProxy: {{
                            scheme: "http",
                            host: "{ip}",
                            port: parseInt({port})
                        }},
                        bypassList: ["localhost"]
                    }}
                }};
                chrome.proxy.settings.set({{
                    value: config,
                    scope: "regular"
                }}, function() {{}});

                function callbackFn(details) {{
                    return {{
                        authCredentials: {{
                            username: "{username}",
                            password: "{password}"
                        }}
                    }};
                }}
                chrome.webRequest.onAuthRequired.addListener(callbackFn, {{
                    urls: ["<all_urls>"]
                }}, ['blocking']);
                '''

                            output_file.write(js_code + '\n\n')
                self.show.emit(self.row, 4, ip)
            else:
                self.show.emit(self.row, 5, 'Bạn không sử dụng proxy')
                self.show.emit(self.row, 4, 'no proxy')
                time.sleep(1)
            options.headless = False
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
            if self.selected_proxy == "TM Proxy":
                background_js_content = """
                // Your JavaScript code for background.js goes here
                console.log("daoanhCODER!");
                """

                output_folder = 'proxyport'

                os.makedirs(output_folder, exist_ok=True)

                output_file_path = os.path.join(output_folder, 'background.js')

                with open(output_file_path, 'w') as output_file:
                    output_file.write(background_js_content)
            elif self.selected_proxy == "tinsoft":
                background_js_content = """
                // Your JavaScript code for background.js goes here
                console.log("daoanhCODER!");
                """

                output_folder = 'proxyport'

                os.makedirs(output_folder, exist_ok=True)

                output_file_path = os.path.join(output_folder, 'background.js')

                with open(output_file_path, 'w') as output_file:
                    output_file.write(background_js_content)
            elif self.selected_proxy == "không đổi ip":
                background_js_content = """
                // Your JavaScript code for background.js goes here
                console.log("daoanhCODER!");
                """

                output_folder = 'proxyport'

                os.makedirs(output_folder, exist_ok=True)

                output_file_path = os.path.join(output_folder, 'background.js')
                with open(output_file_path, 'w') as output_file:
                    output_file.write(background_js_content)

            if self.selected_solver == "Captcha69.com":
                options.add_argument(f"--load-extension=" + ",".join([
                    str(pathlib.Path("./funcaptcha").absolute()),
                    str(pathlib.Path("./webgl").absolute()),
                    str(pathlib.Path("./webgl1").absolute()),
                    str(pathlib.Path("./webgl2").absolute()),
                    str(pathlib.Path("./webgl4").absolute()),
                    str(pathlib.Path("./fingerprintspoofing").absolute()),
                    str(pathlib.Path("./proxyport").absolute()),

                ]))
            elif self.selected_solver == "AntiCaptcha.top":
                options.add_argument(f"--load-extension=" + ",".join([
                    str(pathlib.Path("./webgl").absolute()),
                    str(pathlib.Path("./webgl1").absolute()),
                    str(pathlib.Path("./webgl2").absolute()),
                    str(pathlib.Path("./webgl4").absolute()),
                    str(pathlib.Path("./fingerprintspoofing").absolute()),
                    str(pathlib.Path("./proxyport").absolute()),
                ]))
            elif self.selected_solver == "Capsolver.com":
                options.add_argument(f"--load-extension=" + ",".join([
                    str(pathlib.Path("./capsolver").absolute()),
                    str(pathlib.Path("./webgl").absolute()),
                    str(pathlib.Path("./webgl1").absolute()),
                    str(pathlib.Path("./webgl2").absolute()),
                    str(pathlib.Path("./webgl4").absolute()),
                    str(pathlib.Path("./fingerprintspoofing").absolute()),
                    str(pathlib.Path("./proxyport").absolute()),
                ]))
            print(f'extension: {self.selected_solver}')
            options.add_argument('--lang=vi')
            version_list = ["21H2", "22H1", "22H2"]
            version = random.choice(version_list)
            options.add_argument("--version=" + version)
            browser_list = ["Chrome", "Firefox", "Edge"]
            browser = random.choice(browser_list)
            options.add_argument("--browser=" + browser)
            hardware_list = ["Intel", "AMD", "NVIDIA"]
            hardware = random.choice(hardware_list)
            options.add_argument("--hardware=" + hardware)
            device_scale_factor = round((0.5), 2)
            options.add_argument('--ignore-gpu-blacklist')
            options.add_argument("--disable-application-cache")
            options.add_argument(f"--force-device-scale-factor={device_scale_factor}")
            options.add_argument('--window-position=%s,%s' % (self.x, self.y))
            options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
            manufacturers = ["Samsung", "Google", "Nokia", "Sony", "LG", "HTC", "Motorola"]
            models = ["Xperia", "Galaxy", "Pixel", "One", "G"]
            versions = ["1", "II", "III", "Pro", "Max", "Lite"]
            while True:
                win = random.randint(7, 11)
                if win != 9:
                    break
            random_manufacturer = random.choice(manufacturers)
            random_model = random.choice(models)
            random_version = random.choice(versions)
            fake1 = Faker()
            user_agent = f'Mozilla/5.0 (Linux; Android {win}.9.9; {random_manufacturer} {random_model} {random_version}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(78, 100)}.0.4515.159 Mobile Safari/537.36'
            options.add_argument(f'--user-agent={user_agent}')
            options.add_argument('--log-level=3')
            options.add_argument('--disable-infobars')
            options.add_argument('--disable-save-password-bubble')
            options.add_argument("--mute-audio")
            options.add_argument('--disable-gpu')
            options.add_argument("--disable-web-security")
            options.add_argument("--disable-site-isolation-trials")
            options.add_argument("--disable-application-cache")
            options.add_argument('--disable-blink-features=AutomationControlled')
            prefs = {"credentials_enable_service":False,
                     "profile.password_manager_enabled":False}
            options.add_experimental_option("prefs",prefs)
            #options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument('--app=https://giapdaoanh28122005coder.000webhostapp.com/checkserverip/ip.html')
            s = Service("chromedriver.exe")
            s.creation_flags = CREATE_NO_WINDOW
            self.driver = webdriver.Chrome(service=s, options=options)
            stealth(self.driver,
                        languages=["vi-VN", "vi"],
                        vendor="Google Inc.",
                        platform="Win32",
                        webgl_vendor="Intel Inc.",
                        renderer=random.choice(['ANGLE (NVIDIA Quadro 2000M Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA Quadro K420 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA Quadro 2000M Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA Quadro K2000M Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (Intel(R) HD Graphics Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) HD Graphics Family Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (ATI Radeon HD 3800 Series Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) HD Graphics 4000 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (Intel(R) HD Graphics 4000 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (AMD Radeon R9 200 Series Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (Intel(R) HD Graphics Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) HD Graphics Family Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) HD Graphics Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) HD Graphics Family Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) HD Graphics 4000 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) HD Graphics 3000 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Mobile Intel(R) 4 Series Express Chipset Family Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) G33/G31 Express Chipset Family Direct3D9Ex vs_0_0 ps_2_0)', 'ANGLE (Intel(R) Graphics Media Accelerator 3150 Direct3D9Ex vs_0_0 ps_2_0)', 'ANGLE (Intel(R) G41 Express Chipset Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce 6150SE nForce 430 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) HD Graphics 4000)', 'ANGLE (Mobile Intel(R) 965 Express Chipset Family Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) HD Graphics Family)', 'ANGLE (NVIDIA GeForce GTX 760 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 760 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 760 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (AMD Radeon HD 6310 Graphics Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) Graphics Media Accelerator 3600 Series Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) G33/G31 Express Chipset Family Direct3D9 vs_0_0 ps_2_0)', 'ANGLE (AMD Radeon HD 6320 Graphics Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) G33/G31 Express Chipset Family (Microsoft Corporation - WDDM 1.0) Direct3D9Ex vs_0_0 ps_2_0)', 'ANGLE (Intel(R) G41 Express Chipset)', 'ANGLE (ATI Mobility Radeon HD 5470 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) Q45/Q43 Express Chipset Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce 310M Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) G41 Express Chipset Direct3D9 vs_3_0 ps_3_0)', 'ANGLE (Mobile Intel(R) 45 Express Chipset Family (Microsoft Corporation - WDDM 1.1) Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GT 440 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (ATI Radeon HD 4300/4500 Series Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (AMD Radeon HD 7310 Graphics Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) HD Graphics)', 'ANGLE (Intel(R) 4 Series Internal Chipset Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (AMD Radeon(TM) HD 6480G Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (ATI Radeon HD 3200 Graphics Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (AMD Radeon HD 7800 Series Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) G41 Express Chipset (Microsoft Corporation - WDDM 1.1) Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce 210 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GT 630 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (AMD Radeon HD 7340 Graphics Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) 82945G Express Chipset Family Direct3D9 vs_0_0 ps_2_0)', 'ANGLE (NVIDIA GeForce GT 430 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce 7025 / NVIDIA nForce 630a Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) Q35 Express Chipset Family Direct3D9Ex vs_0_0 ps_2_0)', 'ANGLE (Intel(R) HD Graphics 4600 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (AMD Radeon HD 7520G Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (AMD 760G (Microsoft Corporation WDDM 1.1) Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GT 220 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce 9500 GT Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) HD Graphics Family Direct3D9 vs_3_0 ps_3_0)', 'ANGLE (Intel(R) Graphics Media Accelerator HD Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce 9800 GT Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) Q965/Q963 Express Chipset Family (Microsoft Corporation - WDDM 1.0) Direct3D9Ex vs_0_0 ps_2_0)', 'ANGLE (NVIDIA GeForce GTX 550 Ti Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) Q965/Q963 Express Chipset Family Direct3D9Ex vs_0_0 ps_2_0)', 'ANGLE (AMD M880G with ATI Mobility Radeon HD 4250 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GTX 650 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (ATI Mobility Radeon HD 5650 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (ATI Radeon HD 4200 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (AMD Radeon HD 7700 Series Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) G33/G31 Express Chipset Family)', 'ANGLE (Intel(R) 82945G Express Chipset Family Direct3D9Ex vs_0_0 ps_2_0)', 'ANGLE (SiS Mirage 3 Graphics Direct3D9Ex vs_2_0 ps_2_0)', 'ANGLE (NVIDIA GeForce GT 430)', 'ANGLE (AMD RADEON HD 6450 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (ATI Radeon 3000 Graphics Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) 4 Series Internal Chipset Direct3D9 vs_3_0 ps_3_0)', 'ANGLE (Intel(R) Q35 Express Chipset Family (Microsoft Corporation - WDDM 1.0) Direct3D9Ex vs_0_0 ps_2_0)', 'ANGLE (NVIDIA GeForce GT 220 Direct3D9 vs_3_0 ps_3_0)', 'ANGLE (AMD Radeon HD 7640G Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (AMD 760G Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (AMD Radeon HD 6450 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GT 640 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce 9200 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GT 610 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (AMD Radeon HD 6290 Graphics Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (ATI Mobility Radeon HD 4250 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce 8600 GT Direct3D9 vs_3_0 ps_3_0)', 'ANGLE (ATI Radeon HD 5570 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (AMD Radeon HD 6800 Series Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) G45/G43 Express Chipset Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (ATI Radeon HD 4600 Series Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA Quadro NVS 160M Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) HD Graphics 3000)', 'ANGLE (NVIDIA GeForce G100)', 'ANGLE (AMD Radeon HD 8610G + 8500M Dual Graphics Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Mobile Intel(R) 4 Series Express Chipset Family Direct3D9 vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce 7025 / NVIDIA nForce 630a (Microsoft Corporation - WDDM) Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) Q965/Q963 Express Chipset Family Direct3D9 vs_0_0 ps_2_0)', 'ANGLE (AMD RADEON HD 6350 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (ATI Radeon HD 5450 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce 9500 GT)', 'ANGLE (AMD Radeon HD 6500M/5600/5700 Series Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Mobile Intel(R) 965 Express Chipset Family)', 'ANGLE (NVIDIA GeForce 8400 GS Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) HD Graphics Direct3D9 vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GTX 560 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GT 620 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GTX 660 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (AMD Radeon(TM) HD 6520G Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GT 240 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (AMD Radeon HD 8240 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA Quadro NVS 140M)', 'ANGLE (Intel(R) Q35 Express Chipset Family Direct3D9 vs_0_0 ps_2_0)']),
                        fix_hairline=True,
                    )
            self.driver.set_window_size(800, 800)
        except WebDriverException as e:
            if 'This version of ChromeDriver only supports' in str(e):
                self.show.emit(self.row, 5, 'Vui lòng cài đúng version!')
                return 'version_error'
            self.show.emit(self.row, 5, 'Đang mở lại chrome...')
            try:
                self.driver.close()
            except:
                pass
            return self.getDriver()
    def GetTMmail(self):
        mail = ""
        user = ["a", "b", "c", "d", "e", "f", "g", "h", "u", "i", "o", "y", "m", "n", "l", "h", "q", "x", "s", "k", "p", "t", "w", "v", "j", "z"]
        for i in range(4):
            num = str(random.randint(1, 100))
            mail += random.choice(user)
            mail += num
        domain = requests.get("https://api.mail.tm/domains?page=1", headers={"content-type": "application/json"}).json()["hydra:member"][0]["domain"]
        mail += "@" + domain
        data = '{"address":"' + mail + '","password":"28122005"}'
        try:
            acc = requests.post("https://api.mail.tm/accounts", data=data, headers={"content-type": "application/json"}).json()
            token = requests.post("https://api.mail.tm/token", data=data, headers={"content-type": "application/json"}).json()["token"]
        except Exception as e:
            print(e)
            acc, token = GetTMmail(self)
        return mail, token
    def GetCodeTMmail(self, token):
        messages = requests.get("https://api.mail.tm/messages", headers={"authorization": "Bearer " + token}).text
        c = re.findall(r'\b\d{6}\b', messages)
        if c == []:
            return ""
        return re.findall(r"\d{6}", c[0])[0]
    def reg(self, mail:str, token:str, password1:str):
        driver = self.getDriver()
        if driver == "version_error":
            return 'stopall'
        driver = self.driver
        time.sleep(2)
        # driver.get('chrome-extension://bhjdkfocbikffppofmidkkooancpglko/setting.html')
        # time.sleep(2)
        # accept_cookies_button0 = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.ID, "16"))
        # )
        # accept_cookies_button0.click()
        # accept_cookies_button = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.ID, "32"))
        # )
        # accept_cookies_button.click()
        # # accept_cookies_button1 = WebDriverWait(driver, 10).until(
        # #     EC.element_to_be_clickable((By.ID, "64"))
        # # )
        # # accept_cookies_button1.click()
        # accept_cookies_button2 = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.ID, "128"))
        # )
        # accept_cookies_button2.click()
        # accept_cookies_button3 = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.ID, "512"))
        # )
        # accept_cookies_button3.click()
        # accept_cookies_button4 = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.ID, "256"))
        # )
        # accept_cookies_button4.click()
        if self.selected_proxy == "ip:port:user:pass":
            time.sleep(2)
            driver.get('https://giapdaoanh28122005coder.000webhostapp.com/checkserverip/ip.html')
            time.sleep(4)
        self.show.emit(self.row, 5, 'Tiến hành reg acc')
        driver.get("https://twitter.com/")
        time.sleep(2)
        if self.selected_proxy == "freeproxy":
            try:
                accept_cookies_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[text()='Accept all cookies']"))
                )
                accept_cookies_button.click()
            except:
                pass
        element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Tạo tài khoản')]"))
        )
        element.click()
        time.sleep(3)
        if self.selected_name_type == "Tên Việt":
            self.show.emit(self.row, 5, 'Tiến hành reg accc bằng name Việt')
            gender = random.choice(['male', 'female'])
            self.name9 = requests.get(f'https://story-shack-cdn-v2.glitch.me/generators/vietnamese-name-generator/{gender}').json()['data']['name']
            self.show.emit(self.row, 5, self.name9)
            for x in self.name9:
                try:
                    element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.NAME, 'name'))
                    )
                    element.send_keys(x)
                except:
                    driver.close()
        elif self.selected_name_type == "Tên US":
            try:
                self.show.emit(self.row, 5, 'Tiến hành reg accc bằng name Ngoại')
                fake = Faker()
                self.random_name = fake.name()
                self.show.emit(self.row, 5, self.random_name)
                for x in self.random_name:
                    element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.NAME, 'name'))
                    )
                    element.send_keys(x)
            except:
                driver.close()
        time.sleep(2)
        try:
            text_to_click = "Sử dụng email"
            element = driver.find_element(By.XPATH, f'//div[@role="button" and .//span[text()="{text_to_click}"]]')
            element.click()
        except:
            pass
        time.sleep(1.2)
        try:
            for x in mail:
                driver.find_element(By.NAME, 'email').send_keys(x)
        except:
            driver.close()
        time.sleep(2)
        try:
            start_date = datetime(1977, 1, 1)
            end_date = datetime(2004, 12, 31)
            time_between_dates = end_date - start_date
            days_between_dates = time_between_dates.days
            random_number_of_days = random.randrange(days_between_dates)
            random_date = start_date + timedelta(days=random_number_of_days)
            formatted_random_date = random_date.strftime("%d-%m-%Y")
            self.show.emit(self.row, 5, 'điền ngày tháng năm sinh')
            date_input = driver.find_element(By.NAME, "Ngày sinh")
            date_input.send_keys(formatted_random_date)
        except:
            driver.close()
        time.sleep(1.3)
        try:
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Tiếp theo']")))
            element.click()
        except:
            driver.close()
        time.sleep(2)
        try:
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Tiếp theo']")))
            element.click()
            self.show.emit(self.row, 5, 'click')
        except:
            driver.close()
        time.sleep(3)
        try:
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Đăng ký']")))
            element.click()
            self.show.emit(self.row, 5, 'click')
        except:
            driver.close()
        time.sleep(5)
        try:
            driver.find_element(By.NAME, 'verfication_code').click()
            self.show.emit(self.row, 5, f"Vui lòng đợi 8 giây để đợi code")
            random_sleep_time = random.uniform(8, 11)
            self.show.emit(self.row, 5, f"vui lòng đợi  {random_sleep_time:.2f} giây để nhận code")
            time.sleep(random_sleep_time)
            if self.selected_name_type1 == "Hotmail":
                mail = mail
                passmail = password1
                a = requests.get(f'https://tools.dongvanfb.net/api/get_code?mail={mail}&pass={passmail}&type=twitter')
                print(a.text)
                if a.status_code == 200:
                    result = json.loads(a.text)
                    verification_code = result.get('content', 'N/A')
                    match = re.search(r'\b\d{6}\b', verification_code)
                    if match:
                        verification_code = match.group()
                        self.show.emit(self.row, 5, f'mã của bạn là: {verification_code}')
                        driver.find_element(By.NAME, 'verfication_code').send_keys(verification_code)
                        print(f"Verification Code: {verification_code}")
                    else:
                        print("Could not find a 6-digit verification code.")
                else:
                    print(f"Error: {a.status_code}")
            elif self.selected_name_type1 == "Mail.tm":
                code = self.GetCodeTMmail(token)
                self.show.emit(self.row, 5, f'mã của bạn là: {code}')
                driver.find_element(By.NAME, 'verfication_code').send_keys(code)
        except:
            self.show.emit(self.row, 5, 'Đang giải captcha, Vui lòng chờ đợi')
            if self.selected_solver == "Captcha69.com":
                        try:
                            self.show.emit(self.row, 5, 'Check song')
                            wait = WebDriverWait(driver, 300)
                            xpath_expression = 'verfication_code'
                            submit_button = wait.until(EC.element_to_be_clickable((By.NAME, xpath_expression)))
                            submit_button.click()
                            print("Clicked on verfication_code")
                            random_sleep_time = random.uniform(8, 11)
                            self.show.emit(self.row, 5, f"vui lòng đợi  {random_sleep_time:.2f} giây để nhận code")
                            time.sleep(random_sleep_time)
                            if self.selected_name_type1 == "Hotmail":
                                mail = mail
                                passmail = password1
                                a = requests.get(f'https://tools.dongvanfb.net/api/get_code?mail={mail}&pass={passmail}')
                                print(a.text)
                                if a.status_code == 200:
                                    result = json.loads(a.text)
                                    verification_code = result.get('content', 'N/A')
                                    match = re.search(r'\b\d{6}\b', verification_code)
                                    if match:
                                        verification_code = match.group()
                                        self.show.emit(self.row, 5, f'mã của bạn là: {verification_code}')
                                        submit_button.send_keys(verification_code)
                                        print(f"Verification Code: {verification_code}")
                            elif self.selected_name_type1 == "Mail.tm":
                                code = self.GetCodeTMmail(token)
                                self.show.emit(self.row, 5, f'mã của bạn là: {code}')
                                submit_button.send_keys(code)
                        except Exception as e:
                            print(f"Error clicking on verfication_code: {e}")
            elif self.selected_solver == "AntiCaptcha.top":
                with open('captcha/keyAntiCaptcha.txt', 'r') as file:
                        api_key = file.read().strip()
                url = "https://anticaptcha.top/api/captcha"
                headers = {
                    "Content-Type": "application/json"
                }
                data = {
                    "apikey": api_key,
                    "type": 16,
                    "websitekey": "2CB16598-CB82-4CF7-B332-5990DB66F3AB",
                    "pageurl": "https://twitter.com"
                }
                captchaToken = None
                while captchaToken is None:
                    response = requests.post(url, headers=headers, data=json.dumps(data))
                    if response.status_code == 200:
                        result = response.json()
                        if result.get("success"):
                            captchaToken = result.get("captcha")
                            driver.execute_script(f"parent.postMessage(JSON.stringify({{eventId:'challenge-complete',payload:{{sessionToken:'{captchaToken}'}}}}),'*')")
                            try:
                                wait = WebDriverWait(driver, 5)
                                xpath_expression = 'verfication_code'
                                submit_button = wait.until(EC.element_to_be_clickable((By.NAME, xpath_expression)))
                                submit_button.click()
                                print("Clicked on verfication_code")
                                random_sleep_time = random.uniform(8, 11)
                                self.show.emit(self.row, 5, f"vui lòng đợi  {random_sleep_time:.2f} giây để nhận code")
                                time.sleep(random_sleep_time)
                                if self.selected_name_type1 == "Hotmail":
                                    mail = mail
                                    passmail = password1
                                    a = requests.get(f'https://tools.dongvanfb.net/api/get_code?mail={mail}&pass={passmail}')
                                    print(a.text)
                                    if a.status_code == 200:
                                        result = json.loads(a.text)
                                        verification_code = result.get('content', 'N/A')
                                        match = re.search(r'\b\d{6}\b', verification_code)
                                        if match:
                                            verification_code = match.group()
                                            self.show.emit(self.row, 5, f'mã của bạn là: {verification_code}')
                                            submit_button.send_keys(verification_code)
                                            print(f"Verification Code: {verification_code}")
                                elif self.selected_name_type1 == "Mail.tm":
                                    code = self.GetCodeTMmail(token)
                                    self.show.emit(self.row, 5, f'mã của bạn là: {code}')
                                    submit_button.send_keys(code)
                            except Exception as e:
                                print(f"Error clicking on verfication_code: {e}")
                                captchaToken = None
            else:
                self.show.emit(self.row, 5, 'đang giải captcha')
                max_retries = 10
                retry = 0
                while retry < max_retries:
                    try:
                        wait = WebDriverWait(driver, 20)
                        xpath_expression = 'verfication_code'
                        submit_button = wait.until(EC.element_to_be_clickable((By.NAME, xpath_expression)))
                        submit_button.click()
                        self.show.emit(self.row, 5, f"Vui lòng đợi 8 giây để đợi code")
                        time.sleep(8)
                        code = self.GetCodeTMmail(token)
                        self.show.emit(self.row, 5, f'mã của bạn là: {code}')
                        try:
                            submit_button.send_keys(code)
                        except:
                            self.show.emit(self.row, 5,'mã code không được gửi về')
                            driver.close()
                        break
                    except Exception as e:
                        retry += 1
                if retry == max_retries:
                    self.show.emit(self.row, 5, f"Số lần thử lại tối đa ({max_retries}) đạt. Không thể bấm vào nút.")
                    driver.close()
        time.sleep(2)
        try:
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Tiếp theo']")))
            element.click()
        except:
            pass
        time.sleep(2)
        text_to_check = "Không thể hoàn tất đăng ký của bạn ngay bây giờ."
        if text_to_check in driver.page_source:
            print("Văn bản được hiển thị trên trang web.")
            self.show.emit(self.row, 5, "Văn bản được hiển thị trên trang web.")
            time.sleep(2)
            self.show.emit(self.row, 5, "tiến hành reg lại")
            self.show.emit(self.row, 5, 'Tiến hành reg lại acc')
            driver.get("https://twitter.com/")
            time.sleep(2)
            if self.selected_proxy == "freeproxy":
                try:
                    accept_cookies_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//span[text()='Accept all cookies']"))
                    )
                    accept_cookies_button.click()
                except:
                    pass
            element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Tạo tài khoản')]"))
            )
            element.click()
            time.sleep(3)
            if self.selected_name_type == "Tên Việt":
                self.show.emit(self.row, 5, 'Tiến hành reg accc bằng name Việt')
                gender = random.choice(['male', 'female'])
                self.name9 = requests.get(f'https://story-shack-cdn-v2.glitch.me/generators/vietnamese-name-generator/{gender}').json()['data']['name']
                self.show.emit(self.row, 5, self.name9)
                for x in self.name9:
                    try:
                        element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.NAME, 'name'))
                        )
                        element.send_keys(x)
                    except:
                        driver.close()
            elif self.selected_name_type == "Tên US":
                try:
                    self.show.emit(self.row, 5, 'Tiến hành reg accc bằng name Ngoại')
                    fake = Faker()
                    self.random_name = fake.name()
                    self.show.emit(self.row, 5, self.random_name)
                    for x in self.random_name:
                        element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.NAME, 'name'))
                        )
                        element.send_keys(x)
                except:
                    driver.close()
            time.sleep(2)
            try:
                text_to_click = "Sử dụng email"
                element = driver.find_element(By.XPATH, f'//div[@role="button" and .//span[text()="{text_to_click}"]]')
                element.click()
            except:
                pass
            time.sleep(1.2)
            try:
                for x in mail:
                    driver.find_element(By.NAME, 'email').send_keys(x)
            except:
                driver.close()
            time.sleep(2)
            try:
                start_date = datetime(1977, 1, 1)
                end_date = datetime(2004, 12, 31)
                time_between_dates = end_date - start_date
                days_between_dates = time_between_dates.days
                random_number_of_days = random.randrange(days_between_dates)
                random_date = start_date + timedelta(days=random_number_of_days)
                formatted_random_date = random_date.strftime("%d-%m-%Y")
                self.show.emit(self.row, 5, 'điền ngày tháng năm sinh')
                date_input = driver.find_element(By.NAME, "Ngày sinh")
                date_input.send_keys(formatted_random_date)
            except:
                driver.close()
            time.sleep(1.3)
            try:
                wait = WebDriverWait(driver, 10)
                element = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Tiếp theo']")))
                element.click()
            except:
                driver.close()
            time.sleep(2)
            try:
                wait = WebDriverWait(driver, 10)
                element = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Tiếp theo']")))
                element.click()
                self.show.emit(self.row, 5, 'click')
            except:
                driver.close()
            time.sleep(3)
            try:
                wait = WebDriverWait(driver, 10)
                element = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Đăng ký']")))
                element.click()
                self.show.emit(self.row, 5, 'click')
            except:
                driver.close()
            if self.selected_proxy == "freeproxy":
                self.show.emit(self.row, 5, f"đối với freeproxy phải đợi 10 giây để check captcha")
                time.sleep(10)
            time.sleep(5)
            try:
                driver.find_element(By.NAME, 'verfication_code').click()
                self.show.emit(self.row, 5, f"Vui lòng đợi 8 giây để đợi code")
                random_sleep_time = random.uniform(8, 11)
                self.show.emit(self.row, 5, f"vui lòng đợi  {random_sleep_time:.2f} giây để nhận code")
                time.sleep(random_sleep_time)
                if self.selected_name_type1 == "Hotmail":
                    mail = mail
                    passmail = password1
                    a = requests.get(f'https://tools.dongvanfb.net/api/get_code?mail={mail}&pass={passmail}&type=twitter')
                    print(a.text)
                    if a.status_code == 200:
                        result = json.loads(a.text)
                        verification_code = result.get('content', 'N/A')
                        match = re.search(r'\b\d{6}\b', verification_code)
                        if match:
                            verification_code = match.group()
                            self.show.emit(self.row, 5, f'mã của bạn là: {verification_code}')
                            driver.find_element(By.NAME, 'verfication_code').send_keys(verification_code)
                            print(f"Verification Code: {verification_code}")
                        else:
                            print("Could not find a 6-digit verification code.")
                    else:
                        print(f"Error: {a.status_code}")
                elif self.selected_name_type1 == "Mail.tm":
                    code = self.GetCodeTMmail(token)
                    self.show.emit(self.row, 5, f'mã của bạn là: {code}')
                    driver.find_element(By.NAME, 'verfication_code').send_keys(code)
            except:
                self.show.emit(self.row, 5, 'Đang giải captcha, Vui lòng chờ đợi')
                if self.selected_solver == "Captcha69.com":
                            try:
                                wait = WebDriverWait(driver, 300)
                                xpath_expression = 'verfication_code'
                                submit_button = wait.until(EC.element_to_be_clickable((By.NAME, xpath_expression)))
                                submit_button.click()
                                print("Clicked on verfication_code")
                                random_sleep_time = random.uniform(8, 11)
                                self.show.emit(self.row, 5, f"vui lòng đợi  {random_sleep_time:.2f} giây để nhận code")
                                time.sleep(random_sleep_time)
                                if self.selected_name_type1 == "Hotmail":
                                    mail = mail
                                    passmail = password1
                                    a = requests.get(f'https://tools.dongvanfb.net/api/get_code?mail={mail}&pass={passmail}&type=twitter')
                                    print(a.text)
                                    if a.status_code == 200:
                                        result = json.loads(a.text)
                                        verification_code = result.get('content', 'N/A')
                                        match = re.search(r'\b\d{6}\b', verification_code)
                                        if match:
                                            verification_code = match.group()
                                            self.show.emit(self.row, 5, f'mã của bạn là: {verification_code}')
                                            submit_button.send_keys(verification_code)
                                            print(f"Verification Code: {verification_code}")
                                elif self.selected_name_type1 == "Mail.tm":
                                    code = self.GetCodeTMmail(token)
                                    self.show.emit(self.row, 5, f'mã của bạn là: {code}')
                                    submit_button.send_keys(code)
                            except Exception as e:
                                print(f"Error clicking on verfication_code: {e}")
                elif self.selected_solver == "Capsolver.com":
                    try:
                        wait = WebDriverWait(driver, 300)
                        xpath_expression = 'verfication_code'
                        submit_button = wait.until(EC.element_to_be_clickable((By.NAME, xpath_expression)))
                        submit_button.click()
                        print("Clicked on verfication_code")
                        random_sleep_time = random.uniform(8, 11)
                        self.show.emit(self.row, 5, f"vui lòng đợi  {random_sleep_time:.2f} giây để nhận code")
                        time.sleep(random_sleep_time)
                        if self.selected_name_type1 == "Hotmail":
                            mail = mail
                            passmail = password1
                            a = requests.get(f'https://tools.dongvanfb.net/api/get_code?mail={mail}&pass={passmail}&type=twitter')
                            print(a.text)
                            if a.status_code == 200:
                                result = json.loads(a.text)
                                verification_code = result.get('content', 'N/A')
                                match = re.search(r'\b\d{6}\b', verification_code)
                                if match:
                                    verification_code = match.group()
                                    self.show.emit(self.row, 5, f'mã của bạn là: {verification_code}')
                                    submit_button.send_keys(verification_code)
                                    print(f"Verification Code: {verification_code}")
                        elif self.selected_name_type1 == "Mail.tm":
                            code = self.GetCodeTMmail(token)
                            self.show.emit(self.row, 5, f'mã của bạn là: {code}')
                            submit_button.send_keys(code)
                    except Exception as e:
                        print(f"Error clicking on verfication_code: {e}")
                elif self.selected_solver == "AntiCaptcha.top":
                    with open('captcha/keyAntiCaptcha.txt', 'r') as file:
                            api_key = file.read().strip()
                    url = "https://anticaptcha.top/api/captcha"
                    headers = {
                        "Content-Type": "application/json"
                    }
                    data = {
                        "apikey": api_key,
                        "type": 16,
                        "websitekey": "2CB16598-CB82-4CF7-B332-5990DB66F3AB",
                        "pageurl": "https://twitter.com"
                    }
                    captchaToken = None
                    while captchaToken is None:
                        response = requests.post(url, headers=headers, data=json.dumps(data))
                        if response.status_code == 200:
                            result = response.json()
                            if result.get("success"):
                                captchaToken = result.get("captcha")
                                driver.execute_script(f"parent.postMessage(JSON.stringify({{eventId:'challenge-complete',payload:{{sessionToken:'{captchaToken}'}}}}),'*')")
                                try:
                                    wait = WebDriverWait(driver, 5)
                                    xpath_expression = 'verfication_code'
                                    submit_button = wait.until(EC.element_to_be_clickable((By.NAME, xpath_expression)))
                                    submit_button.click()
                                    print("Clicked on verfication_code")
                                    random_sleep_time = random.uniform(8, 11)
                                    self.show.emit(self.row, 5, f"vui lòng đợi  {random_sleep_time:.2f} giây để nhận code")
                                    time.sleep(random_sleep_time)
                                    if self.selected_name_type1 == "Hotmail":
                                        mail = mail
                                        passmail = password1
                                        a = requests.get(f'https://tools.dongvanfb.net/api/get_code?mail={mail}&pass={passmail}&type=twitter')
                                        print(a.text)
                                        if a.status_code == 200:
                                            result = json.loads(a.text)
                                            verification_code = result.get('content', 'N/A')
                                            match = re.search(r'\b\d{6}\b', verification_code)
                                            if match:
                                                verification_code = match.group()
                                                self.show.emit(self.row, 5, f'mã của bạn là: {verification_code}')
                                                submit_button.send_keys(verification_code)
                                                print(f"Verification Code: {verification_code}")
                                    elif self.selected_name_type1 == "Mail.tm":
                                        code = self.GetCodeTMmail(token)
                                        self.show.emit(self.row, 5, f'mã của bạn là: {code}')
                                        submit_button.send_keys(code)
                                except Exception as e:
                                    print(f"Error clicking on verfication_code: {e}")
                                    captchaToken = None
                else:
                    self.show.emit(self.row, 5, 'đang giải captcha')
                    max_retries = 10
                    retry = 0
                    while retry < max_retries:
                        try:
                            wait = WebDriverWait(driver, 20)
                            xpath_expression = 'verfication_code'
                            submit_button = wait.until(EC.element_to_be_clickable((By.NAME, xpath_expression)))
                            submit_button.click()
                            self.show.emit(self.row, 5, f"Vui lòng đợi 8 giây để đợi code")
                            time.sleep(8)
                            code = self.GetCodeTMmail(token)
                            self.show.emit(self.row, 5, f'mã của bạn là: {code}')
                            try:
                                submit_button.send_keys(code)
                            except:
                                self.show.emit(self.row, 5,'mã code không được gửi về')
                                driver.close()
                            break
                        except Exception as e:
                            retry += 1
                    if retry == max_retries:
                        self.show.emit(self.row, 5, f"Số lần thử lại tối đa ({max_retries}) đạt. Không thể bấm vào nút.")
                        driver.close()
            time.sleep(2)
            try:
                wait = WebDriverWait(driver, 10)
                element = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Tiếp theo']")))
                element.click()
            except:
                driver.close()
            time.sleep(3)
            try:
                password_length = 12
                characters = string.ascii_letters + string.digits
                random_password = ''.join(random.choice(characters) for _ in range(password_length))
                self.show.emit(self.row, 3, random_password)
                driver.find_element(By.NAME, 'password').send_keys(random_password)
            except:
                driver.close()
            time.sleep(2)
            try:
                alert = driver.switch_to.alert
                alert.dismiss()
            except:
                pass
            try:
                wait = WebDriverWait(driver, 10)
                element = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Tiếp theo']")))
                element.click()
            except:
                driver.close()
            self.show.emit(self.row, 5, 'check xem acc có bị khóa không')
            time.sleep(5)
            try:
                time.sleep(5)
                start_element_appeared = False
                try:
                    element = driver.find_element(By.CSS_SELECTOR, "input.Button.EdgeButton.EdgeButton--primary[value='Start']")
                    element.click()
                    start_element_appeared = True
                except Exception as e:
                    pass
                if start_element_appeared:
                    self.show.emit(self.row, 5 ,'Tài khoản bị khóa, đang mở khóa nick...')
                    driver.refresh()
                    if self.selected_solver == "Captcha69.com":
                                try:
                                    button = WebDriverWait(driver, 400).until(
                                        EC.element_to_be_clickable((By.XPATH, "//input[@value='Continue to X']"))
                                    )
                                    button.click()
                                except Exception as e:
                                    print(f"Error clicking on verfication_code: {e}")
                    elif self.selected_solver == "Capsolver.com":
                        try:
                            button = WebDriverWait(driver, 400).until(
                                EC.element_to_be_clickable((By.XPATH, "//input[@value='Continue to X']"))
                            )
                            button.click()
                        except Exception as e:
                            print(f"Error clicking on verfication_code: {e}")
                    elif self.selected_solver == "AntiCaptcha.top":
                        with open('captcha/keyAntiCaptcha.txt', 'r') as file:
                            api_key = file.read().strip()
                        url = "https://anticaptcha.top/api/captcha"
                        headers = {
                            "Content-Type": "application/json"
                        }
                        data = {
                            "apikey": api_key,
                            "type": 16,
                            "websitekey": "0152B4EB-D2DC-460A-89A1-629838B529C9",
                            "pageurl": "https://twitter.com"
                        }
                        captchaToken = None

                        while captchaToken is None:
                            response = requests.post(url, headers=headers, data=json.dumps(data))

                            if response.status_code == 200:
                                result = response.json()
                                if result.get("success"):
                                    captchaToken = result.get("captcha")
                                    driver.execute_script(f"parent.postMessage(JSON.stringify({{eventId:'challenge-complete',payload:{{sessionToken:'{captchaToken}'}}}}),'*')")
                        time.sleep(2)
                        url = "https://anticaptcha.top/api/captcha"
                        headers = {
                            "Content-Type": "application/json"
                        }

                        data = {
                            "apikey": api_key,
                            "type": 16,
                            "websitekey": "0152B4EB-D2DC-460A-89A1-629838B529C9",
                            "pageurl": "https://twitter.com"
                        }
                        captchaToken = None
                        while captchaToken is None:
                            response = requests.post(url, headers=headers, data=json.dumps(data))

                            if response.status_code == 200:
                                result = response.json()
                                if result.get("success"):
                                    captchaToken = result.get("captcha")
                                    driver.execute_script(f"parent.postMessage(JSON.stringify({{eventId:'challenge-complete',payload:{{sessionToken:'{captchaToken}'}}}}),'*')")
                                    try:
                                        button = WebDriverWait(driver, 10).until(
                                            EC.element_to_be_clickable((By.XPATH, "//input[@value='Continue to X']"))
                                        )
                                        button.click()
                                    except Exception as e:
                                        print(f"Error clicking on verfication_code: {e}")
                                        captchaToken = None
                    time.sleep(2)
                    for i in range(2):
                        driver.get('https://twitter.com/home')
                    self.show.emit(self.row, 5 ,'Giải thành công đang sử lý công việc tiếp')
                    time.sleep(3)
                    driver.set_window_size(2000,2000)
                    element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Profile')]"))
                    )
                    element.click()
                    driver.set_window_size(700,700)
                    time.sleep(4)
                    current_url = driver.current_url
                    parts = current_url.split('/')
                    username = parts[-1]
                    print('Username:', username)
                    self.show.emit(self.row, 2, username)

                    self.show.emit(self.row, 5, 'setup profile')
                    time.sleep(2)
                    try:
                        element = driver.find_element(By.XPATH, "//*[text()='Set up profile']")
                        element.click()
                        time.sleep(2)
                        file = random.choice(os.listdir(self.ref.pathFolder))
                        img = os.path.join(self.ref.pathFolder, file)
                        xpath="//input[@type='file']"
                        upanh = driver.find_element(By.XPATH,xpath)
                        upanh.send_keys(img)
                        time.sleep(2)
                        element = driver.find_element(By.CSS_SELECTOR, 'div[role="button"][data-testid="applyButton"]')
                        element.click()
                        time.sleep(1)
                        try:
                            element = driver.find_element(By.XPATH, "//*[text()='Next']")
                            element.click()
                        except:
                            element = driver.find_element(By.XPATH, "//span[contains(text(), 'Tiếp theo')]")
                            element.click()
                    except:
                        pass
                    time.sleep(2)
                    try:
                        file = random.choice(os.listdir(self.ref.pathFolder))
                        img = os.path.join(self.ref.pathFolder, file)
                        xpath="//input[@type='file']"
                        upanh = driver.find_element(By.XPATH,xpath)
                        upanh.send_keys(img)
                        time.sleep(2)
                        element = driver.find_element(By.CSS_SELECTOR, 'div[role="button"][data-testid="applyButton"]')
                        element.click()
                        time.sleep(1)
                        try:
                            element = driver.find_element(By.XPATH, "//*[text()='Next']")
                            element.click()
                        except:
                            element = driver.find_element(By.XPATH, "//span[contains(text(), 'Tiếp theo')]")
                            element.click()
                    except:
                        pass
                    time.sleep(2)
                    try:
                        with open('data/bio.txt', 'r', encoding='utf-8') as file:
                            lyrics = file.readlines()
                        random_lyric = random.choice(lyrics)
                        driver.find_element(By.NAME, 'text').send_keys(random_lyric)
                        time.sleep(1)
                        try:
                            element = driver.find_element(By.XPATH, "//*[text()='Next']")
                            element.click()
                        except:
                            element = driver.find_element(By.XPATH, "//span[contains(text(), 'Tiếp theo')]")
                            element.click()
                    except:
                        pass
                    time.sleep(2)
                    try:
                        with open('data/bio.txt', 'r', encoding='utf-8') as file:
                            lyrics = file.readlines()
                        random_lyric = random.choice(lyrics)
                        driver.find_element(By.NAME, 'text').send_keys(random_lyric)
                        time.sleep(1)
                        try:
                            element = driver.find_element(By.XPATH, "//*[text()='Next']")
                            element.click()
                        except:
                            element = driver.find_element(By.XPATH, "//span[contains(text(), 'Tiếp theo')]")
                            element.click()
                    except:
                        pass
                    time.sleep(2)
                    element = driver.find_element(By.XPATH, "//*[text()='Save']")
                    element.click()
                    time.sleep(2)
                    driver.get(f'https://twitter.com/{username}')
                    time.sleep(2)
                    try:
                        self.show.emit(self.row, 5, f'tiến hành đi follow nick theo yêu cầu')
                        with open('data/linkfl.txt', 'r', encoding='utf-8') as file:
                            songs = file.readlines()
                        driver.get(songs)
                        time.sleep(2)
                        wait = WebDriverWait(driver, 5)
                        follow = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(.,"Follow")]')))
                        follow.click()
                    except:
                        pass
                    time.sleep(2)
                    if self.state == Qt.Checked:
                        self.show.emit(self.row, 5, 'Tiến hành đi bật 2FA bạn đã chọn')
                        driver.set_window_size(700, 700)
                        driver.get('https://twitter.com/i/flow/two-factor-auth-app-enrollment')
                        time.sleep(2)

                        text_to_click = "Get started"
                        wait = WebDriverWait(driver, 10)
                        element = wait.until(EC.presence_of_element_located((By.XPATH, f"//span[text()='{text_to_click}']")))
                        element.click()

                        text_to_click = "Can’t scan the QR code?"
                        wait = WebDriverWait(driver, 10)
                        element = wait.until(EC.presence_of_element_located((By.XPATH, f"//span[text()='{text_to_click}']")))
                        element.click()

                        time.sleep(5)
                        all_text = driver.page_source
                        match = re.search(r'\b[A-Z0-9]{16}\b', all_text)

                        if match:
                            key = match.group(0)
                            totp = pyotp.TOTP(key)
                            a = totp.now()
                            self.show.emit(self.row, 5, 'Match: ' + a)
                            time.sleep(2)
                            element = driver.find_element(By.XPATH, "//*[contains(text(), 'Next')]")
                            element.click()
                            time.sleep(2)
                            element = driver.find_element(By.NAME, "text")
                            element.send_keys(a)
                            time.sleep(2)
                            element = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, "//span[text()='Confirm']"))
                            )

                            # Click on the element
                            element.click()
                            if self.state1 == Qt.Checked:
                                self.show.emit(self.row, 5, 'đang lấy cookie')
                                cookie = ""
                                cookies = driver.get_cookies()
                                for ck in cookies:
                                    cookie += "%s=%s;" % (ck["name"], ck["value"])
                                print(f'cookie của bạn ;{cookie}')
                                open('ouput/fileacctw2fa.txt', mode='a').write(username + '|' + random_password + '|' + key + '|' + cookie + '|' + mail + '|'+ password1 + '\n')
                            else:
                                self.show.emit(self.row, 5, 'không lấy cookie')
                                open('ouput/fileacctw2fa.txt', mode='a').write(username + '|' + random_password + '|' + key + '|' + mail + '|'+ password1 + '\n')
                            time.sleep(3)
                        else:
                            self.show.emit(self.row, 5, 'Không tìm thấy mã')
                    else:
                        self.show.emit(self.row, 5, 'Bạn không chọn bật 2FA, bỏ qua')
                        if self.state1 == Qt.Checked:
                            self.show.emit(self.row, 5, 'đang lấy cookie')
                            time.sleep(2)
                            driver.get(f'https://twitter.com/{username}')
                            time.sleep(2)
                            cookie = ""
                            cookies = driver.get_cookies()
                            for ck in cookies:
                                cookie += "%s=%s;" % (ck["name"], ck["value"])
                            self.show.emit(self.row, 5, cookie)
                            open('ouput/fileacctw.txt', mode='a').write(username + '|' + random_password + '|' + cookie + '|' + mail + '|'+ password1 + '\n')
                        else:
                            self.show.emit(self.row, 5, 'không lấy cookie')
                            open('ouput/fileacctw.txt', mode='a').write(username + '|' + random_password + '|' + mail + '|'+ password1 + '\n')

                    time.sleep(2)

                else:
                    self.show.emit(self.row, 5, 'nick không bị khóa làm bước tiếp theo')
                    try:
                        self.show.emit(self.row, 5, f'tiến hành đi follow nick theo yêu cầu')
                        with open('data/linkfl.txt', 'r', encoding='utf-8') as file:
                            songs = file.readlines()
                        driver.get(songs)
                        time.sleep(2)
                        wait = WebDriverWait(driver, 5)
                        follow = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(.,"Follow")]')))
                        follow.click()
                    except:
                        pass
                    self.show.emit(self.row, 5, 'đi setup profile')
                    for i in range(2):
                            driver.get('https://twitter.com/home')
                    time.sleep(3)
                    driver.set_window_size(2000,2000)
                    element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Profile')]"))
                    )
                    element.click()
                    driver.set_window_size(700,700)
                    time.sleep(4)
                    current_url = driver.current_url
                    parts = current_url.split('/')
                    username = parts[-1]
                    print('Username:', username)
                    self.show.emit(self.row, 2, username)
                    #open('ouput/fileacctw.txt', mode='a').write(username + '|' + random_password + '|' + mail + '|' + '28122005' + '\n')
                    self.show.emit(self.row, 5, 'setup profile')
                    time.sleep(2)
                    try:
                        element = driver.find_element(By.XPATH, "//*[text()='Set up profile']")
                        element.click()
                        time.sleep(2)
                        file = random.choice(os.listdir(self.ref.pathFolder))
                        img = os.path.join(self.ref.pathFolder, file)
                        xpath="//input[@type='file']"
                        upanh = driver.find_element(By.XPATH,xpath)
                        upanh.send_keys(img)
                    except:
                        pass
                    time.sleep(2)
                    element = driver.find_element(By.CSS_SELECTOR, 'div[role="button"][data-testid="applyButton"]')
                    element.click()
                    time.sleep(1)
                    try:
                        element = driver.find_element(By.XPATH, "//*[text()='Next']")
                        element.click()
                    except:
                        element = driver.find_element(By.XPATH, "//span[contains(text(), 'Tiếp theo')]")
                        element.click()
                    time.sleep(2)
                    try:
                        file = random.choice(os.listdir(self.ref.pathFolder))
                        img = os.path.join(self.ref.pathFolder, file)
                        xpath="//input[@type='file']"
                        upanh = driver.find_element(By.XPATH,xpath)
                        upanh.send_keys(img)
                        time.sleep(2)
                        element = driver.find_element(By.CSS_SELECTOR, 'div[role="button"][data-testid="applyButton"]')
                        element.click()
                        time.sleep(1)
                        try:
                            element = driver.find_element(By.XPATH, "//*[text()='Next']")
                            element.click()
                        except:
                            element = driver.find_element(By.XPATH, "//span[contains(text(), 'Tiếp theo')]")
                            element.click()
                    except:
                        pass
                    time.sleep(2)
                    try:
                        with open('data/bio.txt', 'r', encoding='utf-8') as file:
                            lyrics = file.readlines()
                        random_lyric = random.choice(lyrics)
                        driver.find_element(By.NAME, 'text').send_keys(random_lyric)
                        time.sleep(1)
                        try:
                            element = driver.find_element(By.XPATH, "//*[text()='Next']")
                            element.click()
                        except:
                            element = driver.find_element(By.XPATH, "//span[contains(text(), 'Tiếp theo')]")
                            element.click()
                    except:
                        pass
                    time.sleep(2)
                    try:
                        with open('data/bio.txt', 'r', encoding='utf-8') as file:
                            lyrics = file.readlines()
                        random_lyric = random.choice(lyrics)
                        driver.find_element(By.NAME, 'text').send_keys(random_lyric)
                        time.sleep(1)
                        try:
                            element = driver.find_element(By.XPATH, "//*[text()='Next']")
                            element.click()
                        except:
                            element = driver.find_element(By.XPATH, "//span[contains(text(), 'Tiếp theo')]")
                            element.click()
                    except:
                        pass
                    time.sleep(2)
                    element = driver.find_element(By.XPATH, "//*[text()='Save']")
                    element.click()
                    time.sleep(2)
                    driver.get(f'https://twitter.com/{username}')
                    time.sleep(2)
                    if self.state == Qt.Checked:
                        self.show.emit(self.row, 5, 'Tiến hành đi bật 2FA bạn đã chọn')
                        driver.set_window_size(700, 700)
                        driver.get('https://twitter.com/i/flow/two-factor-auth-app-enrollment')
                        time.sleep(2)
                        text_to_click = "Get started"
                        wait = WebDriverWait(driver, 10)
                        element = wait.until(EC.presence_of_element_located((By.XPATH, f"//span[text()='{text_to_click}']")))
                        element.click()
                        text_to_click = "Can’t scan the QR code?"
                        wait = WebDriverWait(driver, 10)
                        element = wait.until(EC.presence_of_element_located((By.XPATH, f"//span[text()='{text_to_click}']")))
                        element.click()
                        time.sleep(5)
                        all_text = driver.page_source
                        match = re.search(r'\b[A-Z0-9]{16}\b', all_text)
                        if match:
                            key = match.group(0)
                            totp = pyotp.TOTP(key)
                            a = totp.now()
                            self.show.emit(self.row, 5, 'Match: ' + a)
                            time.sleep(2)
                            element = driver.find_element(By.XPATH, "//*[contains(text(), 'Next')]")
                            element.click()
                            time.sleep(2)

                            element = driver.find_element(By.NAME, "text")
                            element.send_keys(a)
                            time.sleep(2)
                            element = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, "//span[text()='Confirm']"))
                            )
                            element.click()
                            if self.state1 == Qt.Checked:
                                self.show.emit(self.row, 5, 'đang lấy cookie')
                                time.sleep(2)
                                driver.get(f'https://twitter.com/{username}')
                                time.sleep(2)
                                cookie = ""
                                cookies = driver.get_cookies()
                                for ck in cookies:
                                    cookie += "%s=%s;" % (ck["name"], ck["value"])
                                self.show.emit(self.row, 5, cookie)
                                open('ouput/fileacctw2fa.txt', mode='a').write(username + '|' + random_password + '|' + key + '|' + cookie + '|' + mail + '|'+ password1 + '\n')
                            else:
                                self.show.emit(self.row, 5, 'không lấy cookie')
                                open('ouput/fileacctw2fa.txt', mode='a').write(username + '|' + random_password + '|' + key + '|' + mail + '|'+ password1 + '\n')
                            time.sleep(3)
                        else:
                            self.show.emit(self.row, 5, 'Không tìm thấy mã')
                    else:
                        self.show.emit(self.row, 5, 'Bạn không chọn bật 2FA, bỏ qua')
                        if self.state1 == Qt.Checked:
                            self.show.emit(self.row, 5, 'đang lấy cookie')
                            cookie = ""
                            cookies = driver.get_cookies()
                            for ck in cookies:
                                cookie += "%s=%s;" % (ck["name"], ck["value"])
                            print(cookie)
                            open('ouput/fileacctw.txt', mode='a').write(username + '|' + random_password + '|' + cookie + '|' + mail + '|'+ password1 + '\n')
                        else:
                            self.show.emit(self.row, 5, 'không lấy cookie')
                            open('ouput/fileacctw.txt', mode='a').write(username + '|' + random_password + '|' + mail + '|'+ password1 + '\n')
                    self.show.emit(self.row, 5, "Thành công!")
            except Exception as e:
                    self.show.emit(self.row, 5, "Không thể thực hiện bước tiếp theo: ")
                    driver.close()
            self.show.emit(self.row, 5, "Thành công!")
        else:
            self.show.emit(self.row, 5, "Văn bản không được hiển thị trên trang web.")
            try:
                password_length = 12
                characters = string.ascii_letters + string.digits
                random_password = ''.join(random.choice(characters) for _ in range(password_length))
                self.show.emit(self.row, 3, random_password)
                driver.find_element(By.NAME, 'password').send_keys(random_password)
            except:
                driver.close()
            time.sleep(2)
            try:
                alert = driver.switch_to.alert
                alert.dismiss()
            except:
                pass
            try:
                wait = WebDriverWait(driver, 10)
                element = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Tiếp theo']")))
                element.click()
            except:
                driver.close()
            self.show.emit(self.row, 5, 'check xem acc có bị khóa không')
            time.sleep(5)
            try:
                time.sleep(5)
                start_element_appeared = False
                try:
                    element = driver.find_element(By.CSS_SELECTOR, "input.Button.EdgeButton.EdgeButton--primary[value='Start']")
                    element.click()
                    start_element_appeared = True
                except Exception as e:
                    pass
                if start_element_appeared:
                    self.show.emit(self.row, 5 ,'Tài khoản bị khóa, đang mở khóa nick...')
                    driver.refresh()
                    if self.selected_solver == "Captcha69.com":
                                try:
                                    button = WebDriverWait(driver, 400).until(
                                        EC.element_to_be_clickable((By.XPATH, "//input[@value='Continue to X']"))
                                    )
                                    button.click()
                                except Exception as e:
                                    print(f"Error clicking on verfication_code: {e}")
                    elif self.selected_solver == "Capsolver.com":
                        try:
                            button = WebDriverWait(driver, 400).until(
                                EC.element_to_be_clickable((By.XPATH, "//input[@value='Continue to X']"))
                            )
                            button.click()
                        except Exception as e:
                            print(f"Error clicking on verfication_code: {e}")
                    elif self.selected_solver == "AntiCaptcha.top":
                        with open('captcha/keyAntiCaptcha.txt', 'r') as file:
                            api_key = file.read().strip()
                        url = "https://anticaptcha.top/api/captcha"
                        headers = {
                            "Content-Type": "application/json"
                        }
                        data = {
                            "apikey": api_key,
                            "type": 16,
                            "websitekey": "0152B4EB-D2DC-460A-89A1-629838B529C9",
                            "pageurl": "https://twitter.com"
                        }
                        captchaToken = None

                        while captchaToken is None:
                            response = requests.post(url, headers=headers, data=json.dumps(data))

                            if response.status_code == 200:
                                result = response.json()
                                if result.get("success"):
                                    captchaToken = result.get("captcha")
                                    driver.execute_script(f"parent.postMessage(JSON.stringify({{eventId:'challenge-complete',payload:{{sessionToken:'{captchaToken}'}}}}),'*')")
                        time.sleep(2)
                        url = "https://anticaptcha.top/api/captcha"
                        headers = {
                            "Content-Type": "application/json"
                        }

                        data = {
                            "apikey": api_key,
                            "type": 16,
                            "websitekey": "0152B4EB-D2DC-460A-89A1-629838B529C9",
                            "pageurl": "https://twitter.com"
                        }
                        captchaToken = None
                        while captchaToken is None:
                            response = requests.post(url, headers=headers, data=json.dumps(data))

                            if response.status_code == 200:
                                result = response.json()
                                if result.get("success"):
                                    captchaToken = result.get("captcha")
                                    driver.execute_script(f"parent.postMessage(JSON.stringify({{eventId:'challenge-complete',payload:{{sessionToken:'{captchaToken}'}}}}),'*')")
                                    try:
                                        button = WebDriverWait(driver, 10).until(
                                            EC.element_to_be_clickable((By.XPATH, "//input[@value='Continue to X']"))
                                        )
                                        button.click()
                                    except Exception as e:
                                        print(f"Error clicking on verfication_code: {e}")
                                        captchaToken = None
                    time.sleep(2)
                    for i in range(2):
                        driver.get('https://twitter.com/home')
                    self.show.emit(self.row, 5 ,'Giải thành công đang sử lý công việc tiếp')
                    time.sleep(3)
                    driver.set_window_size(2000,2000)
                    element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Profile')]"))
                    )
                    element.click()
                    driver.set_window_size(700,700)
                    time.sleep(4)
                    current_url = driver.current_url
                    parts = current_url.split('/')
                    username = parts[-1]
                    print('Username:', username)
                    self.show.emit(self.row, 2, username)

                    self.show.emit(self.row, 5, 'setup profile')
                    time.sleep(2)
                    try:
                        element = driver.find_element(By.XPATH, "//*[text()='Set up profile']")
                        element.click()
                        time.sleep(2)
                        file = random.choice(os.listdir(self.ref.pathFolder))
                        img = os.path.join(self.ref.pathFolder, file)
                        xpath="//input[@type='file']"
                        upanh = driver.find_element(By.XPATH,xpath)
                        upanh.send_keys(img)
                        time.sleep(2)
                        element = driver.find_element(By.CSS_SELECTOR, 'div[role="button"][data-testid="applyButton"]')
                        element.click()
                        time.sleep(1)
                        try:
                            element = driver.find_element(By.XPATH, "//*[text()='Next']")
                            element.click()
                        except:
                            element = driver.find_element(By.XPATH, "//span[contains(text(), 'Tiếp theo')]")
                            element.click()
                    except:
                        pass
                    time.sleep(2)
                    try:
                        file = random.choice(os.listdir(self.ref.pathFolder))
                        img = os.path.join(self.ref.pathFolder, file)
                        xpath="//input[@type='file']"
                        upanh = driver.find_element(By.XPATH,xpath)
                        upanh.send_keys(img)
                        time.sleep(2)
                        element = driver.find_element(By.CSS_SELECTOR, 'div[role="button"][data-testid="applyButton"]')
                        element.click()
                        time.sleep(1)
                        try:
                            element = driver.find_element(By.XPATH, "//*[text()='Next']")
                            element.click()
                        except:
                            element = driver.find_element(By.XPATH, "//span[contains(text(), 'Tiếp theo')]")
                            element.click()
                    except:
                        pass
                    time.sleep(2)
                    try:
                        with open('data/bio.txt', 'r', encoding='utf-8') as file:
                            lyrics = file.readlines()
                        random_lyric = random.choice(lyrics)
                        driver.find_element(By.NAME, 'text').send_keys(random_lyric)
                        time.sleep(1)
                        try:
                            element = driver.find_element(By.XPATH, "//*[text()='Next']")
                            element.click()
                        except:
                            element = driver.find_element(By.XPATH, "//span[contains(text(), 'Tiếp theo')]")
                            element.click()
                    except:
                        pass
                    time.sleep(2)
                    try:
                        with open('data/bio.txt', 'r', encoding='utf-8') as file:
                            lyrics = file.readlines()
                        random_lyric = random.choice(lyrics)
                        driver.find_element(By.NAME, 'text').send_keys(random_lyric)
                        time.sleep(1)
                        try:
                            element = driver.find_element(By.XPATH, "//*[text()='Next']")
                            element.click()
                        except:
                            element = driver.find_element(By.XPATH, "//span[contains(text(), 'Tiếp theo')]")
                            element.click()
                    except:
                        pass
                    time.sleep(2)
                    element = driver.find_element(By.XPATH, "//*[text()='Save']")
                    element.click()
                    time.sleep(2)
                    driver.get(f'https://twitter.com/{username}')
                    time.sleep(2)
                    try:
                        self.show.emit(self.row, 5, f'tiến hành đi follow nick theo yêu cầu')
                        with open('data/linkfl.txt', 'r', encoding='utf-8') as file:
                            songs = file.readlines()
                        driver.get(songs)
                        time.sleep(2)
                        wait = WebDriverWait(driver, 5)
                        follow = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(.,"Follow")]')))
                        follow.click()
                    except:
                        pass
                    time.sleep(2)
                    if self.state == Qt.Checked:
                        self.show.emit(self.row, 5, 'Tiến hành đi bật 2FA bạn đã chọn')
                        driver.set_window_size(700, 700)
                        driver.get('https://twitter.com/i/flow/two-factor-auth-app-enrollment')
                        time.sleep(2)

                        text_to_click = "Get started"
                        wait = WebDriverWait(driver, 10)
                        element = wait.until(EC.presence_of_element_located((By.XPATH, f"//span[text()='{text_to_click}']")))
                        element.click()

                        text_to_click = "Can’t scan the QR code?"
                        wait = WebDriverWait(driver, 10)
                        element = wait.until(EC.presence_of_element_located((By.XPATH, f"//span[text()='{text_to_click}']")))
                        element.click()

                        time.sleep(5)
                        all_text = driver.page_source
                        match = re.search(r'\b[A-Z0-9]{16}\b', all_text)

                        if match:
                            key = match.group(0)
                            totp = pyotp.TOTP(key)
                            a = totp.now()
                            self.show.emit(self.row, 5, 'Match: ' + a)
                            time.sleep(2)
                            element = driver.find_element(By.XPATH, "//*[contains(text(), 'Next')]")
                            element.click()
                            time.sleep(2)
                            element = driver.find_element(By.NAME, "text")
                            element.send_keys(a)
                            time.sleep(2)
                            element = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, "//span[text()='Confirm']"))
                            )

                            # Click on the element
                            element.click()
                            if self.state1 == Qt.Checked:
                                self.show.emit(self.row, 5, 'đang lấy cookie')
                                cookie = ""
                                cookies = driver.get_cookies()
                                for ck in cookies:
                                    cookie += "%s=%s;" % (ck["name"], ck["value"])
                                print(f'cookie của bạn ;{cookie}')
                                open('ouput/fileacctw2fa.txt', mode='a').write(username + '|' + random_password + '|' + key + '|' + cookie + '|' + mail + '|'+ password1 + '\n')
                            else:
                                self.show.emit(self.row, 5, 'không lấy cookie')
                                open('ouput/fileacctw2fa.txt', mode='a').write(username + '|' + random_password + '|' + key + '|' + mail + '|'+ password1 + '\n')
                            time.sleep(3)
                        else:
                            self.show.emit(self.row, 5, 'Không tìm thấy mã')
                    else:
                        self.show.emit(self.row, 5, 'Bạn không chọn bật 2FA, bỏ qua')
                        if self.state1 == Qt.Checked:
                            self.show.emit(self.row, 5, 'đang lấy cookie')
                            time.sleep(2)
                            driver.get(f'https://twitter.com/{username}')
                            time.sleep(2)
                            cookie = ""
                            cookies = driver.get_cookies()
                            for ck in cookies:
                                cookie += "%s=%s;" % (ck["name"], ck["value"])
                            self.show.emit(self.row, 5, cookie)
                            open('ouput/fileacctw.txt', mode='a').write(username + '|' + random_password + '|' + cookie + '|' + mail + '|'+ password1 + '\n')
                        else:
                            self.show.emit(self.row, 5, 'không lấy cookie')
                            open('ouput/fileacctw.txt', mode='a').write(username + '|' + random_password + '|' + mail + '|'+ password1 + '\n')

                    time.sleep(2)

                else:
                    self.show.emit(self.row, 5, 'nick không bị khóa làm bước tiếp theo')
                    try:
                        self.show.emit(self.row, 5, f'tiến hành đi follow nick theo yêu cầu')
                        with open('data/linkfl.txt', 'r', encoding='utf-8') as file:
                            songs = file.readlines()
                        driver.get(songs)
                        time.sleep(2)
                        wait = WebDriverWait(driver, 5)
                        follow = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(.,"Follow")]')))
                        follow.click()
                    except:
                        pass
                    self.show.emit(self.row, 5, 'đi setup profile')
                    for i in range(2):
                            driver.get('https://twitter.com/home')
                    time.sleep(3)
                    driver.set_window_size(2000,2000)
                    element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Profile')]"))
                    )
                    element.click()
                    driver.set_window_size(700,700)
                    time.sleep(4)
                    current_url = driver.current_url
                    parts = current_url.split('/')
                    username = parts[-1]
                    print('Username:', username)
                    self.show.emit(self.row, 2, username)
                    #open('ouput/fileacctw.txt', mode='a').write(username + '|' + random_password + '|' + mail + '|' + '28122005' + '\n')
                    self.show.emit(self.row, 5, 'setup profile')
                    time.sleep(2)
                    try:
                        element = driver.find_element(By.XPATH, "//*[text()='Set up profile']")
                        element.click()
                        time.sleep(2)
                        file = random.choice(os.listdir(self.ref.pathFolder))
                        img = os.path.join(self.ref.pathFolder, file)
                        xpath="//input[@type='file']"
                        upanh = driver.find_element(By.XPATH,xpath)
                        upanh.send_keys(img)
                    except:
                        pass
                    time.sleep(2)
                    element = driver.find_element(By.CSS_SELECTOR, 'div[role="button"][data-testid="applyButton"]')
                    element.click()
                    time.sleep(1)
                    try:
                        element = driver.find_element(By.XPATH, "//*[text()='Next']")
                        element.click()
                    except:
                        element = driver.find_element(By.XPATH, "//span[contains(text(), 'Tiếp theo')]")
                        element.click()
                    time.sleep(2)
                    try:
                        file = random.choice(os.listdir(self.ref.pathFolder))
                        img = os.path.join(self.ref.pathFolder, file)
                        xpath="//input[@type='file']"
                        upanh = driver.find_element(By.XPATH,xpath)
                        upanh.send_keys(img)
                        time.sleep(2)
                        element = driver.find_element(By.CSS_SELECTOR, 'div[role="button"][data-testid="applyButton"]')
                        element.click()
                        time.sleep(1)
                        try:
                            element = driver.find_element(By.XPATH, "//*[text()='Next']")
                            element.click()
                        except:
                            element = driver.find_element(By.XPATH, "//span[contains(text(), 'Tiếp theo')]")
                            element.click()
                    except:
                        pass
                    time.sleep(2)
                    try:
                        with open('data/bio.txt', 'r', encoding='utf-8') as file:
                            lyrics = file.readlines()
                        random_lyric = random.choice(lyrics)
                        driver.find_element(By.NAME, 'text').send_keys(random_lyric)
                        time.sleep(1)
                        try:
                            element = driver.find_element(By.XPATH, "//*[text()='Next']")
                            element.click()
                        except:
                            element = driver.find_element(By.XPATH, "//span[contains(text(), 'Tiếp theo')]")
                            element.click()
                    except:
                        pass
                    time.sleep(2)
                    try:
                        with open('data/bio.txt', 'r', encoding='utf-8') as file:
                            lyrics = file.readlines()
                        random_lyric = random.choice(lyrics)
                        driver.find_element(By.NAME, 'text').send_keys(random_lyric)
                        time.sleep(1)
                        try:
                            element = driver.find_element(By.XPATH, "//*[text()='Next']")
                            element.click()
                        except:
                            element = driver.find_element(By.XPATH, "//span[contains(text(), 'Tiếp theo')]")
                            element.click()
                    except:
                        pass
                    time.sleep(2)
                    element = driver.find_element(By.XPATH, "//*[text()='Save']")
                    element.click()
                    time.sleep(2)
                    driver.get(f'https://twitter.com/{username}')
                    time.sleep(2)
                    if self.state == Qt.Checked:
                        self.show.emit(self.row, 5, 'Tiến hành đi bật 2FA bạn đã chọn')
                        driver.set_window_size(700, 700)
                        driver.get('https://twitter.com/i/flow/two-factor-auth-app-enrollment')
                        time.sleep(2)
                        text_to_click = "Get started"
                        wait = WebDriverWait(driver, 10)
                        element = wait.until(EC.presence_of_element_located((By.XPATH, f"//span[text()='{text_to_click}']")))
                        element.click()
                        text_to_click = "Can’t scan the QR code?"
                        wait = WebDriverWait(driver, 10)
                        element = wait.until(EC.presence_of_element_located((By.XPATH, f"//span[text()='{text_to_click}']")))
                        element.click()
                        time.sleep(5)
                        all_text = driver.page_source
                        match = re.search(r'\b[A-Z0-9]{16}\b', all_text)
                        if match:
                            key = match.group(0)
                            totp = pyotp.TOTP(key)
                            a = totp.now()
                            self.show.emit(self.row, 5, 'Match: ' + a)
                            time.sleep(2)
                            element = driver.find_element(By.XPATH, "//*[contains(text(), 'Next')]")
                            element.click()
                            time.sleep(2)

                            element = driver.find_element(By.NAME, "text")
                            element.send_keys(a)
                            time.sleep(2)
                            element = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, "//span[text()='Confirm']"))
                            )
                            element.click()
                            if self.state1 == Qt.Checked:
                                self.show.emit(self.row, 5, 'đang lấy cookie')
                                time.sleep(2)
                                driver.get(f'https://twitter.com/{username}')
                                time.sleep(2)
                                cookie = ""
                                cookies = driver.get_cookies()
                                for ck in cookies:
                                    cookie += "%s=%s;" % (ck["name"], ck["value"])
                                self.show.emit(self.row, 5, cookie)
                                open('ouput/fileacctw2fa.txt', mode='a').write(username + '|' + random_password + '|' + key + '|' + cookie + '|' + mail + '|'+ password1 + '\n')
                            else:
                                self.show.emit(self.row, 5, 'không lấy cookie')
                                open('ouput/fileacctw2fa.txt', mode='a').write(username + '|' + random_password + '|' + key + '|' + mail + '|'+ password1 + '\n')
                            time.sleep(3)
                        else:
                            self.show.emit(self.row, 5, 'Không tìm thấy mã')
                    else:
                        self.show.emit(self.row, 5, 'Bạn không chọn bật 2FA, bỏ qua')
                        if self.state1 == Qt.Checked:
                            self.show.emit(self.row, 5, 'đang lấy cookie')
                            cookie = ""
                            cookies = driver.get_cookies()
                            for ck in cookies:
                                cookie += "%s=%s;" % (ck["name"], ck["value"])
                            print(cookie)
                            open('ouput/fileacctw.txt', mode='a').write(username + '|' + random_password + '|' + cookie + '|' + mail + '|'+ password1 + '\n')
                        else:
                            self.show.emit(self.row, 5, 'không lấy cookie')
                            open('ouput/fileacctw.txt', mode='a').write(username + '|' + random_password + '|' + mail + '|'+ password1 + '\n')
                    self.show.emit(self.row, 5, "Thành công!")
            except Exception as e:
                self.show.emit(self.row, 5, "Không thể thực hiện bước tiếp theo: ")
                driver.close()
            self.show.emit(self.row, 5, "Thành công!")
    def Stop(self):
        self.show.emit(self.row, 5, "Đã dừng tạo!")
        try: threading.Thread(target=self.driver.quit).start()
        except: pass
        self.terminate()
    def run(self):
        while True:
            try:
                if self.selected_name_type1 == "Hotmail":
                    mail, password1 = str(next(self.ref.iterGmail)).split("|")
                    token = 'daoanhcoder'
                elif self.selected_name_type1 == "Mail.tm":
                    mail, token = self.GetTMmail()
                    password1 = "28122005"
            except:
                return
            self.row = self.ref.tableWidget.rowCount()
            self.ref.tableWidget.insertRow(self.row)
            yellow_brush = QBrush(QColor(255, 255, 200))
            for col in range(self.ref.tableWidget.columnCount()):
                item = self.ref.tableWidget.item(self.row, col)
                item = QtWidgets.QTableWidgetItem('')
                item.setBackground(yellow_brush)
                self.ref.tableWidget.setItem(self.row, col, item)
            try:
                self.show.emit(self.row, 0, mail)
                self.show.emit(self.row, 1, password1)
                self.show.emit(self.row, 5, "Đang bắt đầu reg...")
                check = self.reg(mail, token, password1)
                if check == "stopall":
                    return
                self.check.emit(True)
                self.driver.close()
                time.sleep(1)
                green_brush = QBrush(QColor(200, 255, 200))
                for col in range(self.ref.tableWidget.columnCount()):
                    item = self.ref.tableWidget.item(self.row, col)
                    if item is None:
                        item = QtWidgets.QTableWidgetItem('')
                        self.ref.tableWidget.setItem(self.row, col, item)
                    item.setBackground(green_brush)
            except Exception as e:
                try:
                    self.driver.close()
                except:
                    pass
                self.check.emit(False)
                print(f'lỗi ở đây: {e}')
                self.show.emit(self.row, 5, 'Đang mở lại chrome')
                try:
                    with open('nickloi.txt', 'a+', encoding="utf-8") as file:
                        file.write("%s|%s\n" % (mail, password1))
                except:
                    pass
                red_brush = QBrush(QColor(255, 200, 200))
                for col in range(self.ref.tableWidget.columnCount()):
                    item = self.ref.tableWidget.item(self.row, col)
                    if item is None:
                        item = QtWidgets.QTableWidgetItem('')
                        self.ref.tableWidget.setItem(self.row, col, item)
                    item.setBackground(red_brush)