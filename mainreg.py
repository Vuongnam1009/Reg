from datetime import datetime
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTableWidgetItem, QLabel, QMessageBox, QInputDialog
from PyQt5 import QtCore, QtGui
from Ui_reg import Ui_RegTikTokChrome
from main import Reg
import subprocess
from PyQt5 import QtCore, QtGui, QtWidgets
from win32api import GetSystemMetrics
# import requests
import sys
import configparser
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from faker import Faker
from PyQt5.Qt import QUrl
from PyQt5.QtWidgets import QApplication, QLabel
from io import BytesIO
from tkinter import Tk, Toplevel, Label, Entry, Button, messagebox
import hashlib
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton
import requests
import json
import uuid
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from tkinter import simpledialog
import time
can_close = False
import webbrowser
import hashlib
import uuid
import random
from datetime import datetime
import tkinter as tk
from tkinter import ttk, Toplevel, messagebox
from io import BytesIO
from PIL import Image, ImageTk
import requests
import webbrowser
can_close = False
from PyQt5.QtWidgets import QPushButton, QRadioButton, QFileDialog
import random
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QRadioButton, QPushButton, QInputDialog, QTextEdit
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QPlainTextEdit
import platform
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QVBoxLayout, QWidget, QPushButton, QInputDialog
class RegTikTok(Ui_RegTikTokChrome):
    def __init__(self) -> None:
        global days_left  
        days_left = None
        global hours_left  
        hours_left = None
        global minutes_left  
        minutes_left = None
        global seconds_left  
        seconds_left = None
        def generate_unique_key():
            machine_identifier = get_unique_identifier()  
            combined_str = f"daoanhcoder_{machine_identifier}"
            return combined_str
        def get_unique_identifier():
            identifier = platform.node()  # Using the machine name as an example, replace this with your method
            return identifier
        def authenticate_key():
            global can_close
            key = key_entry.get()
            print(key)
            loading_window = show_loading_window()
            loading_window.after(3000, loading_window.destroy) 
            key_list_url = "https://giapdaoanh28122005coder.000webhostapp.com/keykichtw/keytwetter"
            key_list = requests.get(key_list_url).text.splitlines()
            key_is_valid = False
            expiration = None
            for item in key_list:
                stored_key = item.split("|")[0]
                expiration_str = item.split("|")[1]
                expiration = datetime.strptime(expiration_str, "%d-%m-%Y")

                if key == stored_key:
                    key_is_valid = True
                    break
            if key_is_valid and datetime.now().date() < expiration.date():
                root.after(3000, lambda: finish_authentication(expiration))
            else:
                messagebox.showerror('Thông báo', 'Key không hợp lệ hoặc đã hết hạn.')

        def show_loading_window():
            loading_window = Toplevel(root)
            loading_window.title("Đang xác minh")
            loading_window.geometry("300x100")
            loading_window.transient(root)
            loading_window.focus_set()
            loading_window.grab_set()
            screen_width = loading_window.winfo_screenwidth()
            screen_height = loading_window.winfo_screenheight()
            window_width = 300
            window_height = 100
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            loading_window.geometry(f'{window_width}x{window_height}+{x}+{y}')
            progress_bar = ttk.Progressbar(loading_window, mode='indeterminate')
            progress_bar.pack(pady=20)
            progress_bar.start()
            return loading_window

        def finish_authentication(expiration):
            global can_close
            global days_left
            global hours_left
            global minutes_left
            global seconds_left
            time_left = (expiration - datetime.now()).total_seconds()
            days_left = int(time_left // (24 * 3600))
            hours_left = int((time_left % (24 * 3600)) // 3600)
            minutes_left = int((time_left % 3600) // 60)
            seconds_left = int(time_left % 60)
            messagebox.showinfo('Thông báo', f'Key hợp lệ. Sử dụng được {days_left} ngày {hours_left} giờ {minutes_left} phút {seconds_left} giây.')
            can_close = True
            root.destroy()
            return days_left, hours_left, minutes_left, seconds_left

        def on_closing():
            global can_close
            if can_close:
                root.destroy()
            else:
                messagebox.showinfo('Thông báo', 'Vui lòng đăng nhập trước khi thoát.')

        root = tk.Tk()
        root.title('Mã Máy')
        root.geometry('400x250')
        root.resizable(False, False)
        root.configure(bg='#f2f2f2')
        root.eval('tk::PlaceWindow . center')

        image_url = "https://i.imgur.com/PXMQoMf.png"
        response = requests.get(image_url)
        image_data = BytesIO(response.content)
        image = Image.open(image_data)
        icon = ImageTk.PhotoImage(image)

        admin_label = tk.Label(root, text="Admin: Giáp Đào Anh", font=("Arial", 12), fg='#eeaa22', bg='#f2f2f2')
        admin_label.pack()

        zalo_label = tk.Label(root, text="Liên hệ Zalo: 0565622060", fg="blue", cursor="hand2", font=("Arial", 12), bg='#f2f2f2')
        zalo_label.pack()

        def open_zalo_link(event):
            webbrowser.open_new("https://zalo.me/0565622060")

        zalo_label.bind("<Button-1>", open_zalo_link)

        key_label = tk.Label(root, text="MÃ MÁY:", font=("Arial", 12), bg='#f2f2f2', fg='black')
        key_label.pack()

        key_entry = tk.Entry(root, font=("Arial", 12))
        key_entry.pack()

        key_entry.insert(0, generate_unique_key())

        check_button = tk.Button(root, text='Đăng nhập', command=authenticate_key, font=("Arial", 12), fg='white', bg='#eeaa22')
        check_button.pack()

        # root.protocol("WM_DELETE_WINDOW", on_closing)
        root.tk.call('wm', 'iconphoto', root._w, icon)
        root.mainloop()
        super().__init__()
        self.setupUi(ui)
        response = requests.get('https://httpbin.org/ip')
        data = response.json()
        ip_address = data['origin']
        self.success = 0
        self.fail = 0
        self.lbTotal = QLabel(self.centralwidget)
        self.lbTotal.setText('<p><span style="font-size:9pt; color: black; font-weight:600;">Tổng: </span> <span style=" color:#ff0000;font-weight:600;">0</span></p>')
        self.lbSuccess = QLabel(self.centralwidget)
        self.lbSuccess.setText('<p><span style="font-size:9pt; color: black; font-weight:600;">Thành công: </span> <span style=" color:#ff0000;font-weight:600;">0</span></p>')
        self.lbFail = QLabel(self.centralwidget)
        self.lbFail.setText('<p><span style="font-size:9pt; color: black; font-weight:600;">Thất bại:</span> <span style=" color:#ff0000;font-weight:600;">0</span></p>')
        self.lbFail1 = QLabel(self.centralwidget)
        seconds = seconds_left
        display_text = f'<p><span style="font-size:9pt; color: black; font-weight:600;">Key máy của bạn còn:</span> <span style=" color:#ff0000;font-weight:600;">{days_left} ngày {hours_left} giờ {minutes_left} phút {seconds} giây</span></p>'
        self.lbFail1.setText(display_text)
        self.lbFai2 = QLabel(self.centralwidget)
        self.lbFai2.setText('<p><span style="font-size:9pt; color: black; font-weight:600;"></span> <span style=" color:#ff0000;font-weight:600;"></span></p>')
        self.lbFai3 = QLabel(self.centralwidget)
        self.lbFai3.setText('<p><span style="font-size:9pt; color: black; font-weight:600;"></span> <span style=" color:#ff0000;font-weight:600;"></span></p>')
        self.lbFai4 = QLabel(self.centralwidget)
        self.lbFai4.setText(f'<p><span style="font-size:9pt; color: black; font-weight:600;">Địa chỉ ip của bạn là:</span> <span style=" color:#ff0000;font-weight:600;">{ip_address}</span></p>')
        self.lbFai5 = QLabel(self.centralwidget)
        self.lbFai5.setText(
            '<p>'
            '<span style="font-size:9pt; color: black; font-weight:600;">Thông Báo:</span> '
            '<span style="color:#ff0000;font-weight:600;">chúng tôi đã update lại giải captcha và đã fix hết tất cả các lỗi </span>'
            '</p>'
        )
        self.statusbar.addWidget(self.lbTotal)
        self.statusbar.addWidget(self.lbSuccess)
        self.statusbar.addWidget(self.lbFail)
        self.statusbar.addWidget(self.lbFail1)
        self.statusbar.addWidget(self.lbFai2)
        self.statusbar.addWidget(self.lbFai3)
        self.statusbar.addWidget(self.lbFai4)
        self.statusbar.addWidget(self.lbFai5)
        self.btnStart.clicked.connect(self.StartReg)
        self.btnStop.clicked.connect(self.StopReg)
        self.btnFolderAvatar.clicked.connect(self.FolderAvatar)
        #self.btnFolderChrome.clicked.connect(self.FolderChrome)
        self.btnFileGmail.clicked.connect(self.FileDialogGmail)
        self.pathfileGmail = ""
        self.pathFolder = ""
        self.LoadData()
        self.threadCount.valueChanged.connect(self.SaveData)

        self.nameSelector1 = QComboBox(self.frame_3)
        self.nameSelector1.addItems(["Mail.tm", "Hotmail"])
        mail_icon = QIcon("img/mailtm.png")
        hotmail_icon = QIcon("img/hotmail.png")
        self.nameSelector1.setItemIcon(0, mail_icon)
        self.nameSelector1.setItemIcon(1, hotmail_icon)
        self.nameSelector1.setObjectName("mailaohotmail")
        self.nameSelector1.setStyleSheet("background-color: #fff; border: 1px solid #ccc; border-radius: 5px")
        self.horizontalLayout.addWidget(self.nameSelector1)
        self.nameSelector1.currentIndexChanged.connect(self.mailchon)
        self.selected_name_type1 = ""

        self.nameSelector = QComboBox(self.frame_3)
        self.nameSelector.addItems(["Tên Việt", "Tên US"])
        self.nameSelector.setObjectName("nameSelector")
        self.nameSelector.setStyleSheet("background-color: #fff; border: 1px solid #ccc; border-radius: 5px")
        self.horizontalLayout.addWidget(self.nameSelector)
        self.nameSelector.currentIndexChanged.connect(self.run_selected_name_type)
        self.selected_name_type = ""
        self.name9 = ""
        self.checkbox_2fa = QCheckBox("Bật 2FA")
        self.checkbox_2fa.setObjectName("checkbox_2fa")
        self.checkbox_2fa.setChecked(False)  
        self.checkbox_2fa.setStyleSheet("color: #007bff;")
        self.horizontalLayout.addWidget(self.checkbox_2fa)
        self.checkbox_2fa.stateChanged.connect(self.checkbox_2fa_changed)
        self.get_cookie = QCheckBox("Lấy cookie")
        self.get_cookie.setObjectName("get_cookie")
        self.get_cookie.setChecked(False)  
        self.get_cookie.setStyleSheet("color: #007bff;")
        self.horizontalLayout.addWidget(self.get_cookie)
        self.get_cookie.stateChanged.connect(self.cookie)
        radio_button_layout = QHBoxLayout()
        proxy_layout = QVBoxLayout()
        label_proxy = QLabel("cấu hình ip:  ", self.frame_3)
        self.horizontalLayout.addWidget(label_proxy)
        self.radioNone = QRadioButton("không đổi ip")
        self.radioNone.setObjectName("radioNone")
        self.radioNone.setChecked(True)  # Set it as default
        radio_button_layout.addWidget(self.radioNone)
        self.radioTMProxy = QRadioButton("TM Proxy")
        self.radioTMProxy.setObjectName("radioTMProxy")
        radio_button_layout.addWidget(self.radioTMProxy)
        self.ippord = QRadioButton("tinsoft")
        self.ippord.setObjectName("tinsoft")
        radio_button_layout.addWidget(self.ippord)
        self.ippord2 = QRadioButton("ip:port:user:pass")
        self.ippord2.setObjectName("ip:port:user:pass")
        radio_button_layout.addWidget(self.ippord2)

        self.horizontalLayout.addLayout(radio_button_layout)
        self.api_key_label = QLabel("NHẬP API KEY TM", self.frame_3)
        proxy_layout.addWidget(self.api_key_label)
        self.api_key_label.hide()
        self.proxy_input = QPlainTextEdit(self.frame_3)
        self.proxy_input.setPlaceholderText("API KEY TM")
        self.proxy_input.hide()
        proxy_layout.addWidget(self.proxy_input)
        self.save_proxy_button = QPushButton("Lưu API KEY", self.frame_3)
        self.save_proxy_button.clicked.connect(self.saveProxy)
        self.save_proxy_button.hide()
        proxy_layout.addWidget(self.save_proxy_button)

        self.horizontalLayout.addLayout(proxy_layout)
        self.api_key_label1 = QLabel("NHẬP key tinsoft", self.frame_3)
        proxy_layout.addWidget(self.api_key_label1)
        
        self.api_key_label1.hide()
        self.proxy_input1 = QPlainTextEdit(self.frame_3)
        self.proxy_input1.setPlaceholderText("tinsoft")
        self.proxy_input1.hide()
        proxy_layout.addWidget(self.proxy_input1)
        self.save_proxy_button1 = QPushButton("Lưu key", self.frame_3)
        self.save_proxy_button1.clicked.connect(self.saveProxy1)
        self.save_proxy_button1.hide()
        proxy_layout.addWidget(self.save_proxy_button1)

        self.horizontalLayout.addLayout(proxy_layout)
        self.api_key_label2 = QLabel("NHẬP ip:port:user:pass", self.frame_3)
        proxy_layout.addWidget(self.api_key_label2)

        self.api_key_label2.hide()
        self.proxy_input2 = QPlainTextEdit(self.frame_3)
        self.proxy_input2.setPlaceholderText("ip:port:user:pass")
        self.proxy_input2.hide()
        proxy_layout.addWidget(self.proxy_input2)
        self.save_proxy_button2 = QPushButton("Lưu ip:port:user:pass", self.frame_3)
        self.save_proxy_button2.clicked.connect(self.saveProxy2)
        self.save_proxy_button2.hide()
        proxy_layout.addWidget(self.save_proxy_button2)
        #self.horizontalLayout.addLayout(proxy_layout)

        self.radioNone.clicked.connect(self.handleProxySelection)
        self.radioTMProxy.clicked.connect(self.handleProxySelection)
        self.ippord.clicked.connect(self.handleProxySelection)
        self.ippord2.clicked.connect(self.handleProxySelection)
        self.comboCaptchaSolver = QComboBox(self.centralwidget)
        self.comboCaptchaSolver.addItems(["Captcha69.com", "AntiCaptcha.top", "Capsolver.com"])
        first_captcha_icon = QIcon(QPixmap('img/1st.png'))
        anti_captcha_icon = QIcon(QPixmap('img/anti.png'))
        anti_Capsolver_icon = QIcon(QPixmap('img/captsolever.png'))
        self.comboCaptchaSolver.setItemIcon(0, first_captcha_icon)
        self.comboCaptchaSolver.setItemIcon(1, anti_captcha_icon)
        self.comboCaptchaSolver.setItemIcon(2, anti_Capsolver_icon)
        self.comboCaptchaSolver.currentIndexChanged.connect(self.handle_combobox_selection)
        self.verticalLayout.addWidget(self.comboCaptchaSolver)
        self.selected_solver = ""

        
    def mailchon(self):
        self.selected_name_type1 = self.nameSelector1.currentText()
    def handle_combobox_selection(self):
        self.selected_solver = self.comboCaptchaSolver.currentText()
        
    def cookie(self, state1):
        self.state1 = state1
    def SaveData(self):
        try:
            self.pathFolder = self.pathAvatar.text()
            self.pathfileGmail = self.pathGmail.text()
            config["SETTINGS"]["pathAvatar"] = self.pathFolder
            config["SETTINGS"]["pathGmail"] = self.pathfileGmail
            config["SETTINGS"]["threadCount"] = str(self.threadCount.value())
            with open('settings.ini', 'w') as configfile:
                config.write(configfile)
        except Exception as e:
            print(f"Error while saving data: {e}")
    def LoadData(self):
        try:
            self.pathFolder = config["SETTINGS"]["pathAvatar"]
            self.pathAvatar.setText(self.pathFolder)
            self.pathfileGmail = config["SETTINGS"]["pathGmail"]
            self.pathGmail.setText(self.pathfileGmail)
            self.threadCount.setValue(int(config["SETTINGS"]["threadCount"]))
        except Exception as e:
            print(f"Error while loading data: {e}")
    def run_selected_name_type(self):
        self.selected_name_type = self.nameSelector.currentText()
    def checkbox_2fa_changed(self, state):
        self.state = state 
    def handleProxySelection(self):
        if self.radioNone.isChecked():
            self.selected_proxy = "không đổi ip"
            self.proxy_input.hide()
            self.save_proxy_button.hide()  
            self.api_key_label.hide()
            self.proxy_input1.hide()
            self.save_proxy_button1.hide()  
            self.api_key_label1.hide()
            self.proxy_input2.hide()
            self.save_proxy_button2.hide()  
            self.api_key_label2.hide()
        elif self.radioTMProxy.isChecked():
            self.selected_proxy = "TM Proxy"
            self.proxy_input.show()
            self.save_proxy_button.show()  
            self.api_key_label.show()
            self.api_key_label.hide()
            self.proxy_input1.hide()
            self.save_proxy_button1.hide()  
            self.api_key_label1.hide()
            self.proxy_input2.hide()
            self.save_proxy_button2.hide()  
            self.api_key_label2.hide()
        elif self.ippord.isChecked():
            self.selected_proxy = "tinsoft"
            self.proxy_input.hide()
            self.save_proxy_button.hide()  
            self.proxy_input1.show()
            self.save_proxy_button1.show()  
            self.api_key_label1.show()
            self.proxy_input2.hide()
            self.save_proxy_button2.hide()  
            self.api_key_label2.hide()
        elif self.ippord2.isChecked():
            self.selected_proxy = "ip:port:user:pass"
            self.proxy_input.hide()
            self.save_proxy_button.hide()  
            self.proxy_input1.hide()
            self.save_proxy_button1.hide()  
            self.api_key_label1.hide()
            self.proxy_input2.show()
            self.save_proxy_button2.show()  
            self.api_key_label2.show()
    def saveProxy(self):
        proxy = self.proxy_input.toPlainText()
        if proxy:
            with open("config/apiproxy.txt", "w") as file:
                file.write(proxy)
            self.proxy_input.clear()
            self.proxy_input.hide()
            self.api_key_label.hide()
            self.save_proxy_button.hide()
            print("Proxy đã được lưu vào apiproxy.txt")
    def saveProxy1(self):
        proxy = self.proxy_input1.toPlainText()
        if proxy:
            with open("config/apitinsoft.txt", "w") as file:
                file.write(proxy)
            self.proxy_input1.clear()
            self.proxy_input1.hide()
            self.api_key_label1.hide()
            self.save_proxy_button1.hide()
    def saveProxy2(self):
        proxy = self.proxy_input2.toPlainText()
        if proxy:
            with open("config/proxyip.txt", "w") as file:
                file.write(proxy)
            self.proxy_input2.clear()
            self.proxy_input2.hide()
            self.api_key_label2.hide()
            self.save_proxy_button2.hide()
    def StartReg(self):
        
        self.handleProxySelection()
        self.api_key_label.hide()
        self.proxy_input.hide()
        self.save_proxy_button.hide()
        self.proxy_input1.clear()
        self.proxy_input1.hide()
        self.api_key_label1.hide()
        self.save_proxy_button1.hide()
        self.proxy_input2.hide()
        self.api_key_label2.hide()
        self.save_proxy_button2.hide()
        print(f'extension: {self.selected_solver}')
        
        import win32api
        self.handle_combobox_selection()
        self.run_selected_name_type()
        self.mailchon()
        if not hasattr(self, 'state'):
            self.state = None
        if not hasattr(self, 'state1'):
            self.state1 = None
        width_scr = win32api.GetSystemMetrics(0)
        height_scr = win32api.GetSystemMetrics(1)
        if self.selected_name_type1 == "Hotmail":
            if not os.path.exists(self.pathfileGmail):
                self.MsgBox('Không tìm thấy file hotmail!')
                return
        if not os.path.exists(self.pathFolder):
            self.MsgBox('Không tìm thấy folder avatar!')
            return
        self.btnStart.setEnabled(False)
        self.btnStop.setEnabled(True)
        thread_count = self.threadCount.value()
        upper_threads = thread_count // 2 
        lower_threads = thread_count - upper_threads  
        x = 700
        y = 700
        width = 360
        height = 700

        self.threadReg = {}
        if self.selected_name_type1 == "Hotmail":
            with open(self.pathfileGmail, encoding='utf-8') as file:
                    file = file.read().splitlines()
                    countFile = len(file)
                    total_text = '<p><span style="font-size:9pt; color: black; font-weight:600;">Tổng: </span> <span style=" color:#ff0000;font-weight:600;">%s</span></p>' % countFile
                    self.lbTotal.setText(total_text)
                    self.iterGmail = iter(file)
        index = 0
        index2 = 0
        for i in range(upper_threads):
            if int(width_scr / width) == index:
                index = 0
                y = height
                index2 += 1
            if int(height_scr / height) == index2:
                index = 0
                index2 = 0

            self.threadReg[i] = Reg(
                self,
                index * x,
                index2 * y,
                self.selected_name_type,
                self.state,
                self.state1,
                thread_count,
                self.selected_proxy,
                self.selected_solver,
                self.selected_name_type1
            )

            self.threadReg[i].start()
            self.threadReg[i].show.connect(self.Show)
            self.threadReg[i].check.connect(self.SetLbStatus)
            self.threadReg[i].finished.connect(self.finishedReg)
            
            if self.selected_proxy == "ip:port:user:pass":
                sleep_time = random.uniform(3, 5)
                self.Delay(sleep_time) 
            index += 1
        index = 0
        index2 = 0
        y = height_scr // 2

        for i in range(upper_threads, thread_count):
            if int(width_scr / width) == index:
                index = 0
                y = height_scr // 2 + height 
                index2 += 1
            if int(height_scr / height) == index2:
                index = 0
                index2 = 0

            self.threadReg[i] = Reg(
                self,
                index * x,
                y + index2 * height,
                self.selected_name_type,
                self.state,
                self.state1,
                thread_count,
                self.selected_proxy,
                self.selected_solver,
                self.selected_name_type1
            )

            self.threadReg[i].start()
            self.threadReg[i].show.connect(self.Show)
            self.threadReg[i].check.connect(self.SetLbStatus)
            self.threadReg[i].finished.connect(self.finishedReg)
            if self.selected_proxy == "ip:port:user:pass":
                sleep_time = random.uniform(3, 5)
                self.Delay(sleep_time) 
            index += 1
    def finishedReg(self):
        self.btnStart.setEnabled(True)
        self.btnStop.setEnabled(False)
    def StopReg(self):
        self.finishedReg()
        try:
            for t in self.threadReg.values():
                t.Stop()
        except: return
    def FileDialogGmail(self):
        file , check = QFileDialog.getOpenFileName(None, "Open File Gmail", "", "Text Files (*.txt)")
        if check:
            self.pathGmail.setText(file)
            self.SaveData()
    def FolderAvatar(self):
        folder = QFileDialog.getExistingDirectory(None, "Open a folder avatar", "./", QFileDialog.ShowDirsOnly)
        if folder != "":
            self.pathAvatar.setText(folder)
            self.SaveData()
    def Delay(self, countdelay):
        loop = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(int(countdelay*1000), loop.quit)
        loop.exec()
    def Show(self, row: int, col: int, text: str):
        item = QTableWidgetItem(text)
        self.tableWidget.setItem(row, col, item)
        if col == 10 and text == "Failed": 
            item.setBackground(QtGui.QColor(255, 0, 0))
        else:
            item.setBackground(QtGui.QColor(255, 255, 255)) 
    def SetLbStatus(self, success: bool):
        self.mailchon()
        if success:
            self.success += 1
        else:
            self.fail += 1
        success_text = '<p><span style="font-size:9pt; color: black; font-weight:600;">Thành công: </span> <span style=" color:#ff0000;font-weight:600;">%s</span></p>' % self.success
        self.lbSuccess.setText(success_text)
        fail_text = '<p><span style="font-size:9pt; color: black; font-weight:600;">Thất bại:</span> <span style=" color:#ff0000;font-weight:600;">%s</span></p>' % self.fail
        self.lbFail.setText(fail_text)
        if self.selected_name_type1 == "Mail.tm":
            countFile = self.success + self.fail
            total_text = '<p><span style="font-size:9pt; color: black; font-weight:600;">Tổng: </span> <span style=" color:#ff0000;font-weight:600;">%s</span></p>' % countFile
            self.lbTotal.setText(total_text)
    def MsgBox(self, text="", icon=QMessageBox.Information):
        self.msg = QMessageBox()
        self.msg.setIcon(icon)
        self.msg.setWindowTitle("Thông báo")
        self.msg.setText(text)
        self.msg.setDefaultButton(QMessageBox.Ok)
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.exec_()
if __name__ == "__main__":
    import sys
    import configparser
    config = configparser.ConfigParser()
    try:
        config.read('settings.ini')
    except: pass
    try:
        config.add_section("SETTINGS")
    except: pass
    app = QApplication(sys.argv)
    image_url = "https://i.imgur.com/PXMQoMf.png"
    response = requests.get(image_url)
    if response.status_code == 200:
        image = QPixmap()
        image.loadFromData(response.content)
        app.setWindowIcon(QIcon(image))
    else:
        print("Không thể tải hình ảnh từ URL")
    ui = QMainWindow()
    cc = RegTikTok()
    ui.show()
    sys.exit(app.exec_())