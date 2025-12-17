import pyedflib
import qlelib
import time
import os
from decode_data import eegIsX8

qldata2edf = qlelib.qldata2edf
qle2edf = qlelib.qle2edf
repair = qlelib.qle_data_check
_get_lost_rate = qle2edf._get_lost_rate

def find_file(root, func, recursion = True):
    ret = []
    for f in os.listdir(root):
        full_name = root + '/' + f
        if(os.path.isfile(full_name)):
            if func(full_name):
                ret.append(full_name)
        elif recursion:
            ret += find_file(full_name, func)
    return ret  

def repair_err_data(data_p, force = True):
    if eegIsX8(data_p):
        with open(data_p, 'rb') as f:
            f.seek(41)
            data = f.read(8)
        end_ms = int.from_bytes(data, byteorder='little', signed=True)
        if force or end_ms == 0:
            dir_ = os.path.dirname(data_p)
            base_name = data_p[len(dir_) + 1:]
            repair_name = dir_ + '/repair_' + base_name
            data, err_list = repair.qle_data_check(data_p, repair_name, force_write=False)
            if len(err_list) > 0:
                data_p = repair_name
    return data_p

def data_translate_edf(data_p):
    data_p = repair_err_data(data_p, False)
    return qldata2edf.convert(data_p)


def edf_join(edf_list:list[str], out_put_name):
    import qlelib.data2edf as data2edf
    from pyedflib import EdfReader
    from datetime import datetime,timedelta

    if len(edf_list) == 0:
        return
    if os.path.exists(out_put_name + '.edf'):
        raise Exception('out name is exists %s' % out_put_name)
    edf_readers:list[EdfReader] = []
    anno_csvs = []
    headers = [data2edf._debug_parse_header(name) for name in edf_list]
    assert all([h['record_duration'] == headers[0]['record_duration'] for h in headers]), 'All files must have the same record duration'
    header = headers[0]
    durations = []
    for i in edf_list:
        csv_f = i + '.csv'
        if not os.path.exists(csv_f):
            csv_f = None
        anno_csvs.append(csv_f)
        edf_readers.append(EdfReader(i))
    for i in range(len(edf_readers)):
        sample_rate = edf_readers[i].getSampleFrequency(0)
        ori_duration = edf_readers[i].getFileDuration()
        last_data = edf_readers[i].readSignal(0, start=int((ori_duration - header['record_duration']) * sample_rate), n = int(sample_rate * header['record_duration']), digital=True)
        offset = 0
        for ii in range(int(sample_rate * header['record_duration'])):
            if last_data[-ii - 1] == 0:
                offset -= 1
            else:
                break
        time_d = offset/sample_rate
        durations.append(ori_duration + time_d)
        
    edf_writer = data2edf.EdfHandle(header['record_duration'])
    edf_writer.from_reader(edf_readers[0], anno_csvs[0])
    edf_end_time = edf_readers[0].getStartdatetime().timestamp() + durations[0]
    for i in range(1, len(edf_readers)):
        edf_start_time = edf_readers[i].getStartdatetime().timestamp()
        dif = edf_start_time - edf_end_time
        assert abs(dif) < 60*20, 'edf not conutiue'
        edf_end_time = edf_start_time + durations[i]
        edf_writer.append_reader(edf_readers[i], anno_csvs[0])

    handle = edf_writer.get_edf_handle(out_put_name)
    handle.setEquipment(edf_readers[0].getEquipment().replace(' ', '_'))
    start_time = edf_readers[0].getStartdatetime()
    edf_writer._export(handle, start_time)

def data_translate_edf_path(data_p:str):    

    def func(path:str):
        return path.endswith('.eeg') or path.endswith('eeg.qle')
    eeg_p = find_file(data_p, func, recursion=False)
    if len(eeg_p) == 1:
        eeg_p = eeg_p[0]
        if eegIsX8(eeg_p):
            acc_p = find_file(data_p, lambda _: _.endswith('.acc') or _.endswith('acc.qle'), recursion=False)
            tri_p = find_file(data_p, lambda _: _.endswith('tri.tri') or _.endswith('tri.dat'), recursion=False)
            sw_p = find_file(data_p, lambda _: _.endswith('sti.log'), recursion=False)
            dir_info = {'EEG':eeg_p}
            if len(acc_p) == 1:
                dir_info['ACC'] = acc_p[0]
            if len(tri_p) == 1:
                dir_info['TRI'] = tri_p[0]
            if len(sw_p) == 1:
                dir_info['SW'] = sw_p[0]
            return qle2edf.convert_dir(dir_info, os.path.join(data_p, os.path.basename(data_p)))
            
    def func(path:str):
        return path.endswith('.eeg') or path.endswith('.acc') or path.endswith('.qle')
    all_file = find_file(data_p, func, recursion=False)
    for f in all_file:
        qldata2edf.convert(f)


def data_translate_edf_path_repiar(data_p:str):    

    def func(path:str):
        return path.endswith('.eeg') or path.endswith('eeg.qle')
    eeg_p = find_file(data_p, func, recursion=False)
    if len(eeg_p) == 1:
        eeg_p = eeg_p[0]
        if eegIsX8(eeg_p):
            acc_p = find_file(data_p, lambda _: _.endswith('.acc') or _.endswith('acc.qle'), recursion=False)
            tri_p = find_file(data_p, lambda _: _.endswith('tri.tri') or _.endswith('tri.dat'), recursion=False)
            sw_p = find_file(data_p, lambda _: _.endswith('sti.log'), recursion=False)
            dir_info = {'EEG':eeg_p}
            if len(acc_p) == 1:
                dir_info['ACC'] = acc_p[0]
            if len(tri_p) == 1:
                dir_info['TRI'] = tri_p[0]
            if len(sw_p) == 1:
                dir_info['SW'] = sw_p[0]
            try:
                lost_rate = qle2edf.convert_dir(dir_info, os.path.join(data_p, os.path.basename(data_p)))
            except Exception as e:
                acc_path = acc_p[0]
                eeg_path = eeg_p
                id,ms = repair.qle_data_get_right(acc_path)
                repair_name  = "%s/repair_eeg.qle" % (os.path.dirname(acc_path))
                repair_name1 = "%s/repair_acc.qle" % (os.path.dirname(acc_path))
                repair.qle_data_check_0(eeg_path, id, ms, repair_name, True)
                repair.qle_data_check_0(acc_path, id, ms, repair_name1, True)
                dir_info['EEG'] = repair_name
                dir_info['ACC'] = repair_name1
                lost_rate = qle2edf.convert_dir(dir_info, os.path.join(data_p, os.path.basename(data_p)))

            return lost_rate
        
def repair_sd_err_data(record_id):
    root_path = r'C:\Users\fengxinan\Downloads'
    acc_path = root_path + r'\%s\%s_acc.acc' % (record_id, record_id)
    eeg_path = root_path + r'\%s\%s_eeg.eeg' % (record_id, record_id)
    
    print(record_id)
    if not os.path.exists(root_path + f'/{record_id}'):
        if os.path.exists(root_path + f'/{record_id}_acc.acc') and os.path.exists(root_path + f'/{record_id}_eeg.eeg'):
            os.mkdir(root_path + r'\%s' % (record_id) )
            os.rename(root_path + f'/{record_id}_acc.acc', acc_path)
            os.rename(root_path + f'/{record_id}_eeg.eeg', eeg_path)
    try:
        os.mkdir(root_path + r'\%s\%s' % (record_id, record_id) )
    except :
        pass

    acc_path = repair_err_data(acc_path)
    eeg_path = repair_err_data(eeg_path)
    
    id,ms = repair.qle_data_get_right(acc_path)
    repair_name  = "%s/%s/eeg.qle" % (os.path.dirname(acc_path), record_id)
    repair_name1 = "%s/%s/acc.qle" % (os.path.dirname(acc_path), record_id)
    repair.qle_data_check_0(eeg_path, id, ms, repair_name, True)
    repair.qle_data_check_0(acc_path, id, ms, repair_name1, True)
    data_translate_edf_path(root_path + r'\%s\%s'  % (record_id, record_id))

def repair_sd_err_data_tst(record_id):
    print(record_id)
    record_dir = r'I:\record_tst\%s' % record_id
    out_dir = r'F:\x8_log\%s' % record_id
    try:
        os.mkdir(out_dir)
    except :
        pass
    acc_path = fr'{record_dir}/acc.qle' 
    eeg_path = fr'{record_dir}/eeg.qle' 
    # acc_path = repair_err_data(acc_path)
    # eeg_path = repair_err_data(eeg_path)
    
    id,ms = repair.qle_data_get_right(acc_path)
    repair_name  = "%s/eeg.qle" % out_dir
    repair_name1 = "%s/acc.qle" % out_dir
    repair.qle_data_check_0(eeg_path, id, ms, repair_name, True)
    repair.qle_data_check_0(acc_path, id, ms, repair_name1, True)
    data_translate_edf_path(out_dir)
    
        
def edf_reshape_day(sorted_edf_path_list, hour_start:int):
    assert hour_start % 1 == 0
    import numpy as np
    from scipy import interpolate
    from qlelib.data2edf import EdfHandle
    import copy
    def qle_clip(arr: np.ndarray, min, max):
        arr = np.round(arr)
        arr = np.clip(arr, min, max)
        return arr
    from datetime import datetime, timedelta
    
    last_chs = None
    split_res = []
    def resample(i_datas, rate:float, max = None):
        for i in range(len(i_datas)):
            d = i_datas[i]
            f = interpolate.interp1d(range(len(d)), d, kind='quadratic')
            tnew = np.linspace(0, len(d) - 1, round(len(d) * rate))
            xnew = f(tnew)
            if max is not None:
                xnew = qle_clip(xnew, max[i][1], max[i][0])
            i_datas[i] = xnew.astype(np.int16)
        return i_datas
    
    def app_res(edf_reader:pyedflib.EdfReader, flag, timestamp, res, sp):
        def export_edf(start_date_time:datetime, i_datas):
            handle = EdfHandle()
            n_channel = len(edf_reader.getSampleFrequencies())
            for i in range(n_channel):
                edf_header = edf_reader.getSignalHeader(i)
                edf_header = copy.deepcopy(edf_header)
                edf_header['sample_rate'] = 500
                ch_info = handle.EdfOriChannel(edf_header)
                handle.chennel_list.append(ch_info)
                ch_info.set_data(i_datas[i])
            handle.export_edf(start_date_time.strftime('%Y%m%d%H%M%S'), start_date_time)
            
        if (flag == 'e' or timestamp is None) and len(split_res) > 0:
            s_endtime = split_res[0][1]
            sub_arr = []
            edf_export_start_time = split_res[0][1]
            for s in split_res:
                s_starttime = s[1]
                delta = abs(s_starttime - s_endtime)
                if  delta > timedelta(seconds=60*2):
                    edf_data = np.concatenate(sub_arr, dtype=np.int16)
                    export_edf(edf_export_start_time, edf_data)
                    sub_arr = []
                    edf_export_start_time = s[1]
                sub_arr.append(s[3])
                s_endtime = s[2]
            export_edf(edf_export_start_time, edf_data)
        if timestamp is None:
            return     
        edf_header = edf_reader.getSignalHeader(0)
        max = [ [edf_reader.getSignalHeader(i)['digital_max'],edf_reader.getSignalHeader(i)['digital_min']] for i in range(len(res))]
        res = resample(res, 500/sp, max=max)
        split_res.append([flag, timestamp, timestamp + timedelta(seconds=len(res[0])/500), res])

            
            
    for edf_path in sorted_edf_path_list:
        edf_reader = pyedflib.EdfReader(edf_path)
        start_time = edf_reader.getStartdatetime()

        n_channel = len(edf_reader.getSampleFrequencies())
        assert last_chs is None or last_chs == n_channel
        last_chs = n_channel
        read_datas = [edf_reader.readSignal(i, digital=True) for i in range(n_channel)]
        edf_ori_sps = len(read_datas[0])
        for i in range(edf_ori_sps, edf_ori_sps - 500, -1):
            if not all([read_datas[j][i - 1] == 0 for j in range(n_channel)]):
                break
        for j in range(n_channel):
            read_datas[j] = read_datas[j][:min(i + 1, edf_ori_sps)]
        edf_ori_sps = len(read_datas[0])
        sample_rate = edf_reader.readAnnotations()[2][0]
        sample_rate = float(sample_rate.split(':')[-1])
        duration_s = edf_ori_sps/sample_rate
        
        end_time = start_time + timedelta(seconds=duration_s)
        duration_hour = duration_s//360
        in_hour = [start_time.hour + i for i in range(int(duration_hour))]
        indices = [index for index, value in enumerate(in_hour) if value == hour_start]
        if start_time.hour == hour_start and (start_time.minute > 0 or start_time.second > 0 or start_time.microsecond > 0):
            del indices[0]
            
        to_split_data = read_datas
        offset_s = 0
        flag = None
        for index in indices:
            flag = 'e'
            s_stamp = start_time + timedelta(hours=index)
            utc_s = s_stamp.timestamp()
            utc_s = utc_s - (utc_s % 3600)
            s_stamp = datetime.fromtimestamp(utc_s)
            duration_s_1 = (s_stamp - start_time).total_seconds() - (s_stamp.microsecond/1000000)
            data1, to_split_data = np.split(to_split_data, [round((duration_s_1 - offset_s) * sample_rate)], 1)
            app_res(edf_reader, flag, start_time + timedelta(seconds=offset_s), data1, sample_rate)
            offset_s += duration_s_1
            flag = 's'
        app_res(edf_reader, flag, start_time + timedelta(seconds=offset_s), to_split_data, sample_rate)
        
    app_res(edf_reader, None, None, None, None)


if __name__ == '__main__':
    #data_translate_edf(r'F:\download\197970_acc.acc')
    # edf_join([r"C:\Users\fengxinan\Downloads\B04-04pre-120875_120875.edf", r"C:\Users\fengxinan\Downloads\B04-04pre-120874_120874.edf"], r"C:\Users\fengxinan\Downloads\45.edf")
    # data_translate_edf_path_repiar(r'C:\Users\fengxinan\Downloads\92648')
    data_translate_edf_path(r'I:\record_tst\1765879914628_0_0')
    # #88793
    # #88794
    # #89068
    # #88381, 89509
    #'1744881811498_0_1', '1744881811498_0_2', '1744881811498_0_3', '1744789750385_0_0', '1744618573530_0_0', '1744618573530_0_1', '1744354992627_0_1',
    # new_acc_data = bytearray()
    # with open(r'C:\Users\fengxinan\Downloads\160922\160922_eeg.eeg', 'rb') as f:
    #     new_acc_data += f.read(534)
    #     with open(r'C:\Users\fengxinan\Downloads\161603\161603_eeg.eeg', 'rb') as f:
    #         f.read(534)
    #         new_acc_data += f.read()
    # with open(r'C:\Users\fengxinan\Downloads\161603\161603_eeg.eeg', 'wb') as f:
    #     f.write(new_acc_data)
    # #164043
    # for r in [194856, 194108,194855,194886]:
    #     repair_sd_err_data(r)
        