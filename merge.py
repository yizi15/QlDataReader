import os

def edf_join(edf_list:list[str], out_put_name):
    import data2edf
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
    
    
if __name__ == '__main__':
    edf_join([r'C:\Users\fengxinan\Desktop\R\53032_53032.edf', r'C:\Users\fengxinan\Desktop\R2\53225_53225.edf'], r'C:\Users\fengxinan\Desktop\R\5.edf')