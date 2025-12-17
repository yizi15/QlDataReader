import glob
import os

from DataReader_Utils2 import *


path_of_data_batch='E:\QuanLanProject\RSC\X7\DOCUMENT\临床\CE3_CLaudio_QuanLan_V3\Day19_20230317\package (17)'


def DataloaderX7(path, signed=False):  # for ACC-36727, the sign is False
    DataTotal = []
    PackageIDs = []
    with open(path, 'rb') as f:
        TotalLen = len(f.read())
        f.seek(0, 0)
        DataType = f.read(3)
        f.seek(12, 0)
        PackageCount = int.from_bytes(f.read(4), byteorder='little', signed=False)
        f.seek(16, 0)
        Resolution = int.from_bytes(f.read(1), byteorder='little', signed=False)

        f.seek(21, 0)
        SampleRate = int.from_bytes(f.read(4), byteorder='little', signed=False)
        f.seek(81, 0)
        ChannelDataLenth = int.from_bytes(f.read(4), byteorder='little', signed=False)

        f.seek(30, 0)
        ST_Y = int.from_bytes(f.read(2), byteorder='little', signed=False)
        ST_M = int.from_bytes(f.read(1), byteorder='little', signed=False)
        ST_D = int.from_bytes(f.read(1), byteorder='little', signed=False)
        ST_H = int.from_bytes(f.read(1), byteorder='little', signed=False)
        ST_Min = int.from_bytes(f.read(1), byteorder='little', signed=False)
        ST_S = int.from_bytes(f.read(1), byteorder='little', signed=False)
        ST_ms = int.from_bytes(f.read(2), byteorder='little', signed=False)

        f.seek(40, 0)
        ET_Y = int.from_bytes(f.read(2), byteorder='little', signed=False)
        ET_M = int.from_bytes(f.read(1), byteorder='little', signed=False)
        ET_D = int.from_bytes(f.read(1), byteorder='little', signed=False)
        ET_H = int.from_bytes(f.read(1), byteorder='little', signed=False)
        ET_Min = int.from_bytes(f.read(1), byteorder='little', signed=False)
        ET_S = int.from_bytes(f.read(1), byteorder='little', signed=False)
        ET_ms = int.from_bytes(f.read(2), byteorder='little', signed=False)

        ST = np.array([ST_Y, ST_M, ST_D, ST_H, ST_Min, ST_S, ST_ms])
        ET = np.array([ET_Y, ET_M, ET_D, ET_H, ET_Min, ET_S, ET_ms])
        # package_sent= (ET - ST)*np.array([365*24*60*60*1000,30*24*60*60*1000,24*60*60*1000,60*60*1000,60*1000,1000,0])/100 # 100 means package send frequency
        # package_loss = PacketCount/sum(package_sent)*100

        f.seek(90, 0)
        DataOffSet = int.from_bytes(f.read(4), byteorder='little', signed=signed)
        PackageOffSet = 8

        if DataType == b'EEG':
            PackageDataLength = 208

        elif DataType == b'ACC':
            PackageDataLength = 38

        elif DataType == b'sti':
            PackageDataLength = 12

        elif DataType == b'EMG':
            PackageDataLength = 248

        if not PackageCount:
            PackageCount = int((TotalLen - DataOffSet) / PackageDataLength)
        else:
            PackageDataLength = int((TotalLen - DataOffSet) / PackageCount)

        f.seek(DataOffSet, 0)
        for i in range(PackageCount):
            PackageT = f.read(PackageDataLength)

            PackageID = int.from_bytes(PackageT[0:8], byteorder='little', signed=signed)
            PackageT = PackageT[8:]
            for j in range(int(len(PackageT) // Resolution)):
                # print(int(len(PackageT) // 2))
                DataT = int.from_bytes(PackageT[j * Resolution:j * Resolution + Resolution], byteorder='little',
                                       signed=signed)
                DataTotal.append(DataT)
                # print(j)
            PackageIDs.append(PackageID)
        PackageIDs = np.array(PackageIDs)

        if str(DataType, encoding="utf-8") == 'EEG':
            DataTotal = np.array(DataTotal)
            A = DataTotal
            DataTotal = DataTotal[0:len(DataTotal) // 2 * 2]
            DataTotal_T = DataTotal.reshape(-1, 2)
            DataTotal = []
            DataTotal.append(DataTotal_T[:, 0])
            DataTotal.append(DataTotal_T[:, 1])

        elif str(DataType, encoding="utf-8") == 'ACC':
            DataTotal = np.array(DataTotal)
            A = DataTotal
            DataTotal = DataTotal[0:len(DataTotal) // 3 * 3]
            DataTotal_T = DataTotal.reshape(-1, 3)
            DataTotal = []
            DataTotal.append(DataTotal_T[:, 0])
            DataTotal.append(DataTotal_T[:, 1])
            DataTotal.append(DataTotal_T[:, 2])

        elif str(DataType, encoding="utf-8") == 'EMG':
            DataTotal = np.array(DataTotal)
            DataTotal = DataTotal[0:len(DataTotal) // 8 * 8]
            DataTotal_T = DataTotal.reshape(-1, 8)
            DataTotal = []
            DataTotal.append(DataTotal_T[:, 0])
            DataTotal.append(DataTotal_T[:, 1])
            DataTotal.append(DataTotal_T[:, 2])
            DataTotal.append(DataTotal_T[:, 3])
            DataTotal.append(DataTotal_T[:, 4])
            DataTotal.append(DataTotal_T[:, 5])
            DataTotal.append(DataTotal_T[:, 6])
            DataTotal.append(DataTotal_T[:, 7])

        # package_loss = (sum(PackageIDs[2:-1] - PackageIDs[1:-2] - 100) / 100) / (
        #             sum(PackageIDs[2:-1] - PackageIDs[1:-2] - 100) / 100 + PackageCount)

        # package_loss = (sum(PackageIDs[2:-1] - PackageIDs[1:-2] - 100) / 100) / (sum(PackageIDs[2:-1] - PackageIDs[1:-2] - 100) / 100 + PackageCount)

        package_loss =[]

    return DataTotal, PackageIDs, SampleRate, ST, ET, package_loss



def data_translate_mat(data_p):

    # def no_path_warning(self):
    #
    #     no_path_warning = QMessageBox.information(None, "提示", "请选择导出路径")
    #
    #     return no_path_warning
    # try:
    #     path_of_data
    # except NameError:
    #     A = no_path_warning(self)
    #     return
    # else:
    #     data_p = path_of_data[0]
    #     print(data_p[-3::])

    EEG_p = data_p

    if EEG_p[-3::] == 'eeg':
        EEG, PackageIDs, SampleRate, ST, ET, package_loss = np.array(DataloaderX7(EEG_p, signed=False))

        scio.savemat(EEG_p[:-3] + "mat", {'EEG': EEG, 'PackageIDs': PackageIDs, 'SampleRate': SampleRate,
                                          'StartTime': ST, 'EndTime': ET, 'package_loss': package_loss})
    elif EEG_p[-3::] == 'acc':
        ACC_p = EEG_p
        ACC_T, PackageIDs, SampleRate, ST, ET, package_loss = DataloaderX7(ACC_p, signed=False)
        # plt.plot(ACC_T)
        ACC_T = ACC_T
        ACCx_raw = ACC_T[0]- 32767
        ACCy_raw = ACC_T[1]- 32767
        ACCz_raw = ACC_T[2]- 32767

        ACCx = ACC_T[0][1:-2] - ACC_T[0][2:-1]
        ACCy = ACC_T[1][1:-2] - ACC_T[1][2:-1]
        ACCz = ACC_T[2][1:-2] - ACC_T[2][2:-1]
        ACC = np.abs(ACCx) + np.abs(ACCy) + np.abs(ACCz)

        scio.savemat(EEG_p[:-3] + "mat",
                     {'ACC': ACC, 'ACCT': ACC_T, 'ACCx_raw': ACCx_raw, 'ACCy_raw': ACCy_raw, 'ACCz_raw': ACCz_raw,
                      'ACCx': ACCx, 'ACCy': ACCy, 'ACCz': ACCz, 'PackageIDs': PackageIDs, 'SampleRate': SampleRate,
                      'StartTime': ST, 'EndTime': ET, 'package_loss': package_loss})


    elif EEG_p[-3::] == 'emg':
        EMG_p = EEG_p
        EMG, PackageIDs, SampleRate, ST, ET, package_loss = DataloaderX7(EMG_p, signed=False)
        scio.savemat(EEG_p[:-3] + "mat", {'EMG': EMG, 'PackageIDs': PackageIDs, 'SampleRate': SampleRate,
                                          'StartTime': ST, 'EndTime': ET, 'package_loss': package_loss})

    elif EEG_p[-3::] == 'sti':
        Sti_p = EEG_p
        Sti_T, PackageIDs, SampleRate, ST, ET, package_loss = DataloaderX7(Sti_p, signed=False)
        # plt.plot(ACC_T)
        # ACCx=ACC_T[0][1:-2] - ACC_T[0][2:-1]
        # ACCy = ACC_T[1][1:-2] - ACC_T[1][2:-1]
        # ACCz = ACC_T[2][1:-2] - ACC_T[2][2:-1]
        # ACC = np.abs(ACCx) + np.abs(ACCy) + np.abs(ACCz)

        scio.savemat(EEG_p[:-3] + "mat", {'StiIdx': Sti_T})



def data_batch_translate_mat(data_p):
    file_name_datas = []
    file_name_datas_user=[]
    roots = []

    for root,_,_ in os.walk(path_of_data_batch):
        # print(root)
        roots.append(root)


    for root in roots[1:]:
        pth = root+'\\'
        for _,_,data_names in os.walk(pth):
            for file_name_data in data_names:
                file_name_datas_user.append(pth+file_name_data)
            file_name_datas.append(file_name_datas_user)
            file_name_datas_user = []

    file_name_datas_user = []

    for file_name_datas_user in  file_name_datas:
        for data_path_abs in  file_name_datas_user:
            if data_path_abs[-4:-1] != 'log' and ~os.path.exists('eeg.eeg') and ~os.path.exists('acc.acc') and ~os.path.exists('sti.sti'):
                # DataloaderX7(data_path_abs)
                data_translate_mat(data_path_abs)
            print(data_path_abs)
    print(roots)
    print(file_name_datas)






