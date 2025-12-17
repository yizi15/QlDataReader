# -*- coding: utf-8 -*-


# Created by: GariXi 20220330  garyxi@foxmail.com



import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QWidget
from PyQt5.QtGui import QIcon
import numpy as np
import scipy.io as scio


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 540)
        MainWindow.setMinimumSize(QtCore.QSize(900, 560))
        MainWindow.setMaximumSize(QtCore.QSize(900, 560))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(140, 20, 640, 30))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.DeviceConnection = QtWidgets.QPushButton(self.centralwidget)
        self.DeviceConnection.setGeometry(QtCore.QRect(40, 90, 101, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(16)
        self.DeviceConnection.setFont(font)
        self.DeviceConnection.setObjectName("DeviceConnection")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(150, 90, 251, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("textBrowser")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(250, 70, 48, 16))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.Vcheck = QtWidgets.QPushButton(self.centralwidget)
        self.Vcheck.setGeometry(QtCore.QRect(40, 180, 101, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(16)
        self.Vcheck.setFont(font)
        self.Vcheck.setObjectName("Vcheck")
        self.VtotalBox = QtWidgets.QTextBrowser(self.centralwidget)
        self.VtotalBox.setGeometry(QtCore.QRect(180, 180, 81, 31))
        self.VtotalBox.setObjectName("VtotalBox")
        self.Vtotal = QtWidgets.QLabel(self.centralwidget)
        self.Vtotal.setGeometry(QtCore.QRect(200, 160, 48, 16))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(12)
        self.Vtotal.setFont(font)
        self.Vtotal.setAlignment(QtCore.Qt.AlignCenter)
        self.Vtotal.setObjectName("Vtotal")
        self.VremainBox = QtWidgets.QTextBrowser(self.centralwidget)
        self.VremainBox.setGeometry(QtCore.QRect(320, 180, 81, 31))
        self.VremainBox.setObjectName("VremainBox")
        self.Vremain = QtWidgets.QLabel(self.centralwidget)
        self.Vremain.setGeometry(QtCore.QRect(320, 160, 81, 16))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(12)
        self.Vremain.setFont(font)
        self.Vremain.setAlignment(QtCore.Qt.AlignCenter)
        self.Vremain.setObjectName("Vremain")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(460, 90, 391, 341))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.textBrowser_2.setFont(font)
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.DeviceConnection_3 = QtWidgets.QPushButton(self.centralwidget)
        self.DeviceConnection_3.setGeometry(QtCore.QRect(490, 450, 331, 41))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(16)
        self.DeviceConnection_3.setFont(font)
        self.DeviceConnection_3.setObjectName("DeviceConnection_3")
        self.Vremain_2 = QtWidgets.QLabel(self.centralwidget)
        self.Vremain_2.setGeometry(QtCore.QRect(620, 70, 81, 16))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(12)
        self.Vremain_2.setFont(font)
        self.Vremain_2.setAlignment(QtCore.Qt.AlignCenter)
        self.Vremain_2.setObjectName("Vremain_2")
        self.datapath_label = QtWidgets.QLabel(self.centralwidget)
        self.datapath_label.setGeometry(QtCore.QRect(170, 250, 111, 20))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(12)
        self.datapath_label.setFont(font)
        self.datapath_label.setAlignment(QtCore.Qt.AlignCenter)
        self.datapath_label.setObjectName("datapath_label")
        self.data_export_button = QtWidgets.QPushButton(self.centralwidget)
        self.data_export_button.setGeometry(QtCore.QRect(40, 330, 101, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(16)
        self.data_export_button.setFont(font)
        self.data_export_button.setObjectName("data_export_button")
        self.data_clear_button = QtWidgets.QPushButton(self.centralwidget)
        self.data_clear_button.setGeometry(QtCore.QRect(300, 330, 101, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(16)
        self.data_clear_button.setFont(font)
        self.data_clear_button.setObjectName("data_clear_button")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(310, 510, 90, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(400, 510, 180, 40))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.path_button = QtWidgets.QPushButton(self.centralwidget)
        self.path_button.setGeometry(QtCore.QRect(360, 280, 41, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.path_button.setFont(font)
        self.path_button.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.path_button.setObjectName("path_button")
        self.data_path_box = QtWidgets.QTextBrowser(self.centralwidget)
        self.data_path_box.setGeometry(QtCore.QRect(40, 280, 361, 31))
        self.data_path_box.setObjectName("data_path_box")
        self.data_path_box_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.data_path_box_2.setGeometry(QtCore.QRect(40, 420, 361, 31))
        self.data_path_box_2.setObjectName("data_path_box_2")
        self.data_translate_button = QtWidgets.QPushButton(self.centralwidget)
        self.data_translate_button.setGeometry(QtCore.QRect(170, 460, 101, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(16)
        self.data_translate_button.setFont(font)
        self.data_translate_button.setObjectName("data_translate_button")
        self.data_path_data = QtWidgets.QPushButton(self.centralwidget)
        self.data_path_data.setGeometry(QtCore.QRect(360, 420, 41, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.data_path_data.setFont(font)
        self.data_path_data.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.data_path_data.setObjectName("data_path_data")
        self.datapath_label_2 = QtWidgets.QLabel(self.centralwidget)
        self.datapath_label_2.setGeometry(QtCore.QRect(130, 390, 181, 20))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(12)
        self.datapath_label_2.setFont(font)
        self.datapath_label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.datapath_label_2.setObjectName("datapath_label_2")
        self.label.raise_()
        self.DeviceConnection.raise_()
        self.textBrowser.raise_()
        self.label_2.raise_()
        self.Vcheck.raise_()
        self.VtotalBox.raise_()
        self.Vtotal.raise_()
        self.VremainBox.raise_()
        self.Vremain.raise_()
        self.textBrowser_2.raise_()
        self.DeviceConnection_3.raise_()
        self.Vremain_2.raise_()
        self.datapath_label.raise_()
        self.data_export_button.raise_()
        self.data_clear_button.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.data_path_box.raise_()
        self.path_button.raise_()
        self.data_path_box_2.raise_()
        self.data_translate_button.raise_()
        self.data_path_data.raise_()
        self.datapath_label_2.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.DeviceConnection.clicked.connect(self.device_connect)
        self.Vcheck.clicked.connect(self.Volume_Check)
        self.data_export_button.clicked.connect(self.data_export)
        self.data_clear_button.clicked.connect(self.data_clear)
        self.DeviceConnection_3.clicked.connect(self.data_check)
        self.path_button.clicked.connect(self.path_choose)
        self.data_path_data.clicked.connect(self.data_choose)
        self.data_translate_button.clicked.connect(self.data_translate)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DreamLand可穿戴式睡眠脑电记录设备数据管理软件"))
        MainWindow.setWindowIcon(QIcon(r'E:\QuanLanProject\RSC\X6\文档\软件\桌面软件\RSC_DataReader(3.0_develop)\QL_logo.jpg'))
        self.label.setText(_translate("MainWindow", "DreamLand可穿戴式睡眠脑电记录设备数据管理软件（X7）"))
        self.DeviceConnection.setText(_translate("MainWindow", "连接设备"))
        self.label_2.setText(_translate("MainWindow", "设备ID"))
        self.Vcheck.setText(_translate("MainWindow", "查询容量"))
        self.Vtotal.setText(_translate("MainWindow", "总容量"))
        self.Vremain.setText(_translate("MainWindow", "剩余容量"))
        self.DeviceConnection_3.setText(_translate("MainWindow", "查询数据"))
        self.Vremain_2.setText(_translate("MainWindow", "数据列表"))
        self.datapath_label.setText(_translate("MainWindow", "数据导出地址"))
        self.data_export_button.setText(_translate("MainWindow", "数据导出"))
        self.data_clear_button.setText(_translate("MainWindow", "清除数据"))
        self.label_3.setText(_translate("MainWindow", "copyright©"))
        self.label_4.setText(_translate("MainWindow", "全澜科技有限公司出品"))
        self.path_button.setText(_translate("MainWindow", "..."))
        self.data_translate_button.setText(_translate("MainWindow", "转换"))
        self.data_path_data.setText(_translate("MainWindow", "..."))
        self.datapath_label_2.setText(_translate("MainWindow", "选择数据转换为MAT格式"))

    def device_connect(self):
        cmd = 'adb devices'  # list devices
        d = os.popen(cmd)
        f = d.read()
        begin = f.find('\n')
        end = f.rfind('\t')
        global device
        device = f[begin + 1:end]  # get device ID
        self.textBrowser.setText(device)

    def Volume_Check(self):
        cmd = 'adb shell df -h'
        d = os.popen(cmd)
        f = d.read()
        # tot = f.find('3.0G')
        tot = 202
        # ava = f.find('261M')
        ava = 213
        comp_tot = f[tot:tot + 5]
        comp_ava = f[ava:ava + 5]
        self.VtotalBox.setText(comp_tot)
        self.VremainBox.setText(comp_ava)

    def data_check(self):
        cmd = 'adb -s ' + str(device) + ' shell "ls -a /userdata/box/data"'
        d = os.popen(cmd)
        f = d.read()
        self.textBrowser_2.setText(f)

    def path_choose(self):
        global path
        path = QFileDialog.getExistingDirectory(None,
                  "选取指定文件夹",
                  r"C:\Users\Administrator\Desktop")
        self.data_path_box.setText(str(path))


    def data_choose(self):
        global path_of_data
        path_of_data = QFileDialog.getOpenFileName(None,
                  "选取指定文件",
                  r"C:\Users\Administrator\Desktop")
        self.data_path_box_2.setText(str(path_of_data))


    def DataloaderX7(self,FilePth,signed=False):#for ACC, the sign is Ture

        self.DataTotal = []
        self.PackageIDs = []
        with open(FilePth, 'rb') as f:
            self.TotalLen = len(f.read())
            f.seek(0, 0)
            self.DataType = f.read(3)
            f.seek(12, 0)
            self.PacketCount = int.from_bytes(f.read(4), byteorder='little', signed=False)
            f.seek(23, 0)
            self.SampleRate = f.read(4)

            f.seek(30, 0)
            self.ST_Y = int.from_bytes(f.read(2), byteorder='little', signed=False)
            self.ST_M = int.from_bytes(f.read(1), byteorder='little', signed=False)
            self.ST_D = int.from_bytes(f.read(1), byteorder='little', signed=False)
            self.ST_H = int.from_bytes(f.read(1), byteorder='little', signed=False)
            self.ST_Min = int.from_bytes(f.read(1), byteorder='little', signed=False)
            self.ST_S = int.from_bytes(f.read(1), byteorder='little', signed=False)
            self.ST_ms = int.from_bytes(f.read(2), byteorder='little', signed=False)

            f.seek(40, 0)
            self.ET_Y = int.from_bytes(f.read(2), byteorder='little', signed=False)
            self.ET_M = int.from_bytes(f.read(1), byteorder='little', signed=False)
            self.ET_D = int.from_bytes(f.read(1), byteorder='little', signed=False)
            self.ET_H = int.from_bytes(f.read(1), byteorder='little', signed=False)
            self.ET_Min = int.from_bytes(f.read(1), byteorder='little', signed=False)
            self.ET_S = int.from_bytes(f.read(1), byteorder='little', signed=False)
            self.ET_ms = int.from_bytes(f.read(2), byteorder='little', signed=False)

            self.ST = np.array([self.ST_Y,self.ST_M,self.ST_D,self.ST_H,self.ST_Min,self.ST_S,self.ST_ms])
            self.ET = np.array([self.ET_Y, self.ET_M, self.ET_D, self.ET_H, self.ET_Min, self.ET_S, self.ET_ms])
            # package_sent= (ET - ST)*np.array([365*24*60*60*1000,30*24*60*60*1000,24*60*60*1000,60*60*1000,60*1000,1000,0])/100 # 100 means package send frequency
            # package_loss = PacketCount/sum(package_sent)*100

            f.seek(90, 0)
            self.DataOffSet = int.from_bytes(f.read(4), byteorder='little', signed=False)
            self.PackageOffSet = 8
            self.PackageDataLength = int((self.TotalLen - self.DataOffSet) / self.PacketCount)
            self.f.seek(self.DataOffSet, 0)
            for i in range(self.PacketCount):
                self.PackageT = f.read(self.PackageDataLength)
                self.PackageID = int.from_bytes(self.PackageT[0:8], byteorder='little', signed=False)
                self.PackageT = self.PackageT[8:]
                for j in range(int(len(self.PackageT) // 2)):
                    # print(int(len(PackageT) // 2))
                    self.DataT = int.from_bytes(self.PackageT[j * 2:j * 2 + 2], byteorder='little', signed=False)
                    self.DataTotal.append(self.DataT)
                    # print(j)
                self.PackageIDs.append(self.PackageID)
            self.PackageIDs=np.array(self.PackageIDs)
            if self.DataType=='EEG':
                self.DataTotal_T=np.array(self.DataTotal).reshape(2,-1)
                self.DataTotal = []
                self.DataTotal.append(self.DataTotal_T[0])
                self.DataTotal.append(self.DataTotal_T[1])
            elif self.DataType=='ACC':
                self.DataTotal_T=np.array(self.DataTotal).reshape(3,-1)
                self.DataTotal = []
                self.DataTotal.append(self.DataTotal_T[0])
                self.DataTotal.append(self.DataTotal_T[1])
                self.DataTotal.append(self.DataTotal_T[2])

            self.package_loss = (sum(self.PackageIDs[2:-1]-self.PackageIDs[1:-2]-100)/100)/(sum(self.PackageIDs[2:-1]-self.PackageIDs[1:-2]-100)/100+self.PacketCount)



        return self.DataTotal, self.PackageIDs,self.SampleRate,self.ST,self.ET,self.package_loss


    def data_translate(self):
        EEG_p =path_of_data[0]
        print(EEG_p[-3::])
        if EEG_p[-3::] == 'eeg':
            EEG = np.array(self.DataloaderX7(EEG_p, signed=False))
            scio.savemat(EEG_p[:-3] + "EEG.mat", {'EEG': EEG})
        elif EEG_p[-3::] == 'acc':
            ACC_p=EEG_p
            ACC=self.DataloaderX7(ACC_p, signed=True)
            ACCx=ACC[0]

            ACCx = np.array(self.DataloaderX7(ACC_p, signed=True)).reshape(-1, 3)[1:, 0] - np.array(
                self.DataloaderX7(ACC_p, signed=True)).reshape(-1, 3)[0:-1, 0]
            ACCy = np.array(self.DataloaderX7(ACC_p, signed=True)).reshape(-1, 3)[1:, 1] - np.array(
                self.DataloaderX7(ACC_p, signed=True)).reshape(-1, 3)[0:-1, 1]
            ACCz = np.array(self.DataloaderX7(ACC_p, signed=True)).reshape(-1, 3)[1:, 2] - np.array(
                self.DataloaderX7(ACC_p, signed=True)).reshape(-1, 3)[0:-1, 2]
            ACC = np.abs(ACCx) + np.abs(ACCy) + np.abs(ACCz)
            scio.savemat(EEG_p[:-3] + "ACC.mat", {'ACC': ACC})


    def data_export(self):
        cmd = 'adb -s ' + str(device) + ' pull /userdata/box/data ' + path
        os.popen(cmd)
        cmd = 'adb -s ' + str(device) + ' pull /userdata/box/head.log ' + path
        os.popen(cmd)
        cmd = 'adb -s ' + str(device) + ' pull /userdata/box/box.log ' + path
        os.popen(cmd)


    def data_clear(self):
        cmd = f'adb -s {str(device)} shell rm -rf /userdata/box/data/*'
        os.popen(cmd)






