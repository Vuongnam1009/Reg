import hashlib
import requests
import hashlib
import requests
from datetime import datetime, timedelta
import uuid
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
import pyperclip 
import hashlib
import socket
import requests
import tkinter as tk
from pathlib import Path
import json
from tkinter import messagebox
import os
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QApplication, QDesktopWidget
from PyQt5.QtGui import QPixmap
import random
from subprocess import CREATE_NO_WINDOW
import threading
import time
from PyQt5.QtWidgets import QPushButton
import pandas as pd
import requests
from selenium.webdriver.chrome.service import Service
from PyQt5.QtWidgets import QCheckBox
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from PyQt5.QtGui import QPixmap
from selenium.webdriver.support.select import Select
from PyQt5.QtWidgets import QLabel
import base64
import logging
logging.basicConfig(level=10)
from unidecode import unidecode
from PIL import Image
from PyQt5.QtWidgets import QMessageBox
import time
import base64
import uuid
import sys 
# Hàm lưu key vào tệp key.txt
from PyQt5.QtCore import Qt
import os
from subprocess import CREATE_NO_WINDOW

import time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QComboBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QButtonGroup
class Ui_RegTikTokChrome(object):
    def setupUi(self, RegTikTokChrome):
        RegTikTokChrome.setObjectName("Phần mềm auto reg tiktok chrome")
        RegTikTokChrome.resize(1523, 646)
        RegTikTokChrome.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks | QtWidgets.QMainWindow.AnimatedDocks)
        RegTikTokChrome.setUnifiedTitleAndToolBarOnMac(False)
        RegTikTokChrome.setStyleSheet("background-color: #f0f0f0;")
        
        self.centralwidget = QtWidgets.QWidget(RegTikTokChrome)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_4 = QtWidgets.QFrame(self.frame_2)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.btnStart = QtWidgets.QPushButton(self.frame_4)
        self.btnStart.setMinimumSize(QtCore.QSize(0, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/icons8-play-100.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnStart.setIcon(icon)
        self.btnStart.setObjectName("btnStart")
        self.btnStart.setStyleSheet("background-color: #4CAF50; color: white; border: 1px solid #4CAF50; border-radius: 15px; padding: 5px 10px;")

        self.horizontalLayout_3.addWidget(self.btnStart)

        self.btnStop = QtWidgets.QPushButton(self.frame_4)
        self.btnStop.setEnabled(False)
        self.btnStop.setMinimumSize(QtCore.QSize(0, 30))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("img/icons8-stop-100.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnStop.setIcon(icon1)
        self.btnStop.setObjectName("btnStop")
        self.btnStop.setStyleSheet("background-color: #D9534F; color: white; border: 1px solid #D9534F; border-radius: 15px; padding: 5px 10px;")


        self.horizontalLayout_3.addWidget(self.btnStop)
        self.horizontalLayout_2.addWidget(self.frame_4)
                
        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.label = QtWidgets.QLabel(self.frame_3)
        self.label.setObjectName("label")
        self.label.setStyleSheet("color: #007bff;")
        self.horizontalLayout.addWidget(self.label)

        self.threadCount = QtWidgets.QSpinBox(self.frame_3)
        self.threadCount.setMaximum(20)
        self.threadCount.setProperty("value", 2)
        self.threadCount.setObjectName("threadCount")
        self.horizontalLayout.addWidget(self.threadCount)
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        self.label_3.setObjectName("label_3")
        self.label_3.setStyleSheet("color: #007bff;")
        self.horizontalLayout.addWidget(self.label_3)

        self.btnFolderAvatar = QtWidgets.QPushButton(self.frame_3)
        self.btnFolderAvatar.setMinimumSize(QtCore.QSize(0, 30))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("img/folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnFolderAvatar.setIcon(icon2)
        self.btnFolderAvatar.setObjectName("btnFolderAvatar")
        self.btnFolderAvatar.setStyleSheet("background-color: #FFC107; color: #000; border: 1px solid #FFC107; border-radius: 15px; padding: 5px 10px;")
        self.horizontalLayout.addWidget(self.btnFolderAvatar)

        self.pathAvatar = QtWidgets.QLineEdit(self.frame_3)
        self.pathAvatar.setReadOnly(True)
        self.pathAvatar.setObjectName("pathAvatar")
        self.pathAvatar.setStyleSheet("background-color: #fff; color: #000; border: 1px solid #ccc; border-radius: 5px;")
        self.horizontalLayout.addWidget(self.pathAvatar)

        self.btnFileGmail = QtWidgets.QPushButton(self.frame_3)
        self.btnFileGmail.setMinimumSize(QtCore.QSize(0, 30))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("img/icons8-txt-96.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnFileGmail.setIcon(icon3)
        self.btnFileGmail.setObjectName("btnFileGmail")
        self.btnFileGmail.setStyleSheet("background-color: #FFC107; color: #000; border: 1px solid #FFC107; border-radius: 15px; padding: 5px 10px;")
        self.horizontalLayout.addWidget(self.btnFileGmail)

        self.pathGmail = QtWidgets.QLineEdit(self.frame_3)
        self.pathGmail.setReadOnly(True)
        self.pathGmail.setObjectName("pathGmail")
        self.pathGmail.setStyleSheet("background-color: #fff; color: #000; border: 1px solid #ccc; border-radius: 5px;")
        self.horizontalLayout.addWidget(self.pathGmail)

        self.label_2 = QtWidgets.QLabel(self.frame_3)
        self.label_2.setObjectName("label_2")
        self.label_2.setStyleSheet("color: #007bff;")
        self.horizontalLayout.addWidget(self.label_2)

        self.horizontalLayout_2.addWidget(self.frame_3)
        self.verticalLayout.addWidget(self.frame_2)

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")

        self.tableWidget = QtWidgets.QTableWidget(self.frame)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(0)

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)

        self.tableWidget.horizontalHeader().setDefaultSectionSize(160)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)

        self.verticalLayout.addWidget(self.frame)

        RegTikTokChrome.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(RegTikTokChrome)
        self.statusbar.setObjectName("statusbar")
        RegTikTokChrome.setStatusBar(self.statusbar)
    
        
        self.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.show_context_menu)
        self.selected_rows = []
        self.retranslateUi(RegTikTokChrome)
        QtCore.QMetaObject.connectSlotsByName(RegTikTokChrome)
        self.colorizeErrorRows()
        
    def handleOutputClick2(self):
        folder_path = "ouput"
        file_name = "fileacctw2fa.txt"
        file_path = os.path.join(folder_path, file_name)

        if os.path.exists(file_path):
            os.startfile(file_path)
        else:
            messagebox.showinfo("Thông báo", f"Tệp '{file_name}' không tồn tại trong thư mục '{folder_path}'")
    def getDriver11(self):

                options = uc.ChromeOptions()
                options.headless = False
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--no-sandbox")
                path = os.path.join(os.getcwd(), "webgl")
                print(path)
                options.add_argument('-load-extension='+path)
                options.add_argument('--lang=vi')
                while(True):
                    win = random.randint(7,11)
                    if win != 9:
                        break
                prefs = {"credentials_enable_service":False,"profile.password_manager_enabled":False,"profile.default_content_setting_values.notifications" : 2}
                options.add_experimental_option("prefs", prefs)
                options.add_argument('--log-level=3')
                options.add_argument(f'--user-agent=Mozilla/5.0 (Windows NT {win}.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(78, 100)}.0.4844.82 Safari/537.36')
                # options.add_argument('--window-position=%s,%s' % (self.x, self.y))
                #options.add_argument('--app=https://httpbin.org/ip')
                options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
                options.add_argument('--disable-infobars')
                options.add_argument("--mute-audio")
                options.add_argument('--safebrowsing-disable-extension-blacklist')
                options.add_argument('--safebrowsing-disable-download-protection')
                options.add_argument('--disable-popup-blocking')
                #chromeoptions.add_argument('--safebrowsing-disable-extension-blacklist')
                options.add_argument("--disable-notifications")
                options.add_argument("--disable-ipc-flooding-protection")
                options.add_argument("--disable-plugins-discovery")
                options.add_argument("--safebrowsing-disable-auto-update")
                options.add_argument('--safebrowsing-disable-download-protection')
                options.add_argument('--disable-blink-features=AutomationControlled')
                options.add_argument('--ignore-certificate-errors')
                # options.add_argument('-window-size=516,726') 
                s = Service("chromedriver.exe")
                s.creation_flags = CREATE_NO_WINDOW
                driver = uc.Chrome(service=s, options=options , use_subprocess=True)
                driver.set_window_size(360,700)
                time.sleep(2)
                driver.get('https://iphey.com/')
                time.sleep(4)
                page_source = driver.page_source
                if "Trustworthy" in page_source:
                    messagebox.showinfo('kiểm tra chrome', "Chrome sạch: Trustworthy")
                else:
                    messagebox.showinfo('kiểm tra chrome', "Chrome không sạch")
    def show_context_menu(self, position):
        context_menu = QtWidgets.QMenu(self.tableWidget)
        action_select_all = context_menu.addAction(QIcon("img/tatca.jpg"), "Chọn tất cả")
        action_copy_selected = context_menu.addAction(QIcon("img/cppy.png"), "Sao chép dòng đã chọn")
        check_chrome = context_menu.addAction(QIcon("img/chrome.jpg"), "Kiểm tra Chrome") 
        action_reload_list1 = context_menu.addAction(QIcon("img/anti.png"), "kiểm tra tiền anticaptcha") 
        action = context_menu.exec_(self.tableWidget.mapToGlobal(position))
        if action == action_select_all:
            for row in range(self.tableWidget.rowCount()):
                self.tableWidget.selectRow(row)
                self.selected_rows.append(row)
        elif action == action_copy_selected:
            selected_rows_text = []
            for row in self.selected_rows:
                selected_row_items = [self.tableWidget.item(row, col).text() if self.tableWidget.item(row, col) else "" for col in range(5)]
                selected_rows_text.append('\t'.join(selected_row_items))
            clipboard = QtWidgets.QApplication.clipboard()
            clipboard.setText('\n'.join(selected_rows_text))
        elif action == check_chrome:
            self.getDriver11()
        elif action == action_reload_list1:
            self.anticpatcha()
    def check_box_changed(self, state):
        if state == QtCore.Qt.Checked:
            selected_items = self.tableWidget.selectedItems()
            for item in selected_items:
                row = item.row()
                if row not in self.selected_rows:
                    self.selected_rows.append(row)
        else:
            selected_items = self.tableWidget.selectedItems()
            for item in selected_items:
                row = item.row()
                if row in self.selected_rows:
                    self.selected_rows.remove(row)
    
    def colorizeErrorRows(self):
        for row in range(self.tableWidget.rowCount()):
            status_item = self.tableWidget.item(row, 4)
            if status_item and status_item.text().strip().lower() == "WinError":
                for col in range(self.tableWidget.columnCount()):
                    self.tableWidget.item(row, col).setBackground(QtGui.QColor(255, 0, 0))
    def handleOutputClick(self):
        folder_path = "ouput"
        file_name = "fileacctw.txt"
        file_path = os.path.join(folder_path, file_name)

        if os.path.exists(file_path):
            os.startfile(file_path)
        else:
            messagebox.showinfo("Thông báo", f"Tệp '{file_name}' không tồn tại trong thư mục '{folder_path}'")
    
    def proxy(self):
        folder_path = "config"
        file_name = "apiproxy.txt"
        file_path = os.path.join(folder_path, file_name)

        if os.path.exists(file_path):
            os.startfile(file_path)
        else:
            messagebox.showinfo("Thông báo", f"Tệp '{file_name}' không tồn tại trong thư mục '{folder_path}'")
    def CheckBalance(self):
            file_path = 'captcha/key1stcaptcha2.txt'
            with open(file_path, mode='r') as file:
                fileproxy = file.read().strip() 
            api_key = fileproxy.split('\n')[0]
            print(api_key)
            response = requests.get(f'https://api.1stcaptcha.com/user/balance?apikey={api_key}')
            if response.status_code == 200:
                json_response = response.json()
                if 'Balance' in json_response:
                    balance = json_response['Balance']
                    QMessageBox.information(None, "Tiền của bạn", f"Tiền của bạn ở 1stcaptcha còn: {balance}")
                else:
                    QMessageBox.information(None, "Tiền của bạn", "Vui lòng kiểm tra apikey ở file: key1stcaptcha2.txt")
    def anticpatcha(self):
            file_path = 'captcha/keyAntiCaptcha.txt'

            with open(file_path, mode='r') as file:
                fileproxy = file.read().strip() 
            api_key = fileproxy.split('\n')[0]
            print(api_key)
            response = requests.get(f'https://anticaptcha.top/api/getbalance?apikey={api_key}')
            if response.status_code == 200:
                json_response = response.json()
                if 'balance' in json_response:
                    balance = json_response['balance']
                    QMessageBox.information(None, "Tiền của bạn", f"Tiền của bạn ở anticaptcha còn: {balance}")
                else:
                   QMessageBox.information(None, "Tiền của bạn", "Vui lòng kiểm tra apikey ở file: keyAntiCaptcha.txt")
    def retranslateUi(self, RegTikTokChrome):
        _translate = QtCore.QCoreApplication.translate
        RegTikTokChrome.setWindowTitle(_translate("RegTikTokChrome", "Phần mềm auto reg Twitter chrome V30.1"))
        self.btnStart.setText(_translate("RegTikTokChrome", "Bắt đầu"))
        self.btnStop.setText(_translate("RegTikTokChrome", "Dừng"))
        self.label.setText(_translate("RegTikTokChrome", "Luồng:"))
        self.btnFolderAvatar.setText(_translate("RegTikTokChrome", "FolderAvatar"))
        self.btnFileGmail.setText(_translate("RegTikTokChrome", "File Hotmail"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("RegTikTokChrome", "MAIL"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("RegTikTokChrome", "MẬT KHẨU MAIL"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("RegTikTokChrome", "USERNAME"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("RegTikTokChrome", "MẬT KHẨU TWITTER"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("RegTikTokChrome", "PROXY"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("RegTikTokChrome", "TRẠNG THÁI"))
import resource_rc