import numpy as np
import pyedflib

# signal label/waveform  amplitude    f       sf
# ---------------------------------------------------
#    1    squarewave        100 uV    0.1Hz   200 Hz
#    2    ramp              100 uV    1 Hz    200 Hz
#    3    pulse 1           100 uV    1 Hz    200 Hz
#    4    pulse 2           100 uV    1 Hz    256 Hz
#    5    pulse 3           100 uV    1 Hz    217 Hz
#    6    noise             100 uV    - Hz    200 Hz
#    7    sine 1 Hz         100 uV    1 Hz    200 Hz
#    8    sine 8 Hz         100 uV    8 Hz    200 Hz
#    9    sine 8.1777 Hz    100 uV    8.25 Hz 200 Hz
#    10    sine 8.5 Hz       100 uV    8.5Hz   200 Hz
#    11    sine 15 Hz        100 uV   15 Hz    200 Hz
#    12    sine 17 Hz        100 uV   17 Hz    200 Hz
#    13    sine 50 Hz        100 uV   50 Hz    200 Hz


class DataParser:
    @staticmethod
    def parse_points(in_file, split_char = ','):
        with open(in_file, 'r') as f:
            temp = f.read().split(split_char)

            if temp[-1] == '':
                temp.pop(-1)
        return [int(v) for v in temp]

    @staticmethod
    def parse_dat(in_file, byte_len, start_offset, byteorder = 'little', signed = False):
        with open(in_file, 'rb') as f:
            temp = f.read()[start_offset:]
        data_list = []
        for i in range(0, len(temp), byte_len):
            v = int.from_bytes(temp[i: i + byte_len], byteorder = byteorder, signed = signed)
            data_list.append(v)
        return data_list

class EdfHandle:
    class ChannelInfo:
        def __init__(self, label:str, dimension:str, sample_rate:int, physical_max:int, physical_min:int, digital_max:int, digital_min:int, transducer :str= '', prefilter:str = '') -> None:
            self.ch_dict = {
                'label': label,
                'dimension': dimension,
                'sample_rate': sample_rate,
                'physical_max': physical_max,
                'physical_min': physical_min,
                'digital_max': digital_max,
                'digital_min': digital_min,
                'transducer': transducer,
                'prefilter': prefilter
                }
            self.__data_list = []
    
        def add_data(self, in_data):
            self.__data_list += in_data
        
        def get_data(self):
            data = np.array(self.__data_list)
            return data

    def __init__(self) -> None:
        self.chennel_list = []
        pass

    def add_channel(self, label:str, dimension:str, sample_rate:int, physical_max:int, physical_min:int, digital_max:int, digital_min:int, transducer :str= '', prefilter:str = ''):
        ch_info = self.ChannelInfo(label, dimension, sample_rate, physical_max, physical_min, digital_max, digital_min, transducer, prefilter)
        self.chennel_list.append(ch_info)
        return ch_info
    
    def export(self, filename):
        handle = pyedflib.EdfWriter(filename,
                           len(self.chennel_list),
                           file_type=pyedflib.FILETYPE_EDFPLUS)
        channel_info_list = [info.ch_dict for info in self.chennel_list]
        data_list = [info.get_data() for info in self.chennel_list]
        handle.setSignalHeaders(channel_info_list)
        handle.writeSamples(data_list)
        # handle.writeAnnotation(0, -1, "Recording starts")
        # handle.writeAnnotation(298, -1, "Test 1")
        # handle.writeAnnotation(294.99, -1, "pulse 1")
        # handle.writeAnnotation(295.9921875, -1, "pulse 2")
        # handle.writeAnnotation(296.99078341013825, -1, "pulse 3")
        # handle.writeAnnotation(600, -1, "Recording ends")
        handle.close()

def write_edf(file, channel):
    file_duration = 600
    f = pyedflib.EdfWriter(file,
                           channel,
                           file_type=pyedflib.FILETYPE_EDFPLUS)
    channel_info = []
    data_list = []

    ch_dict = {
        'label': 'squarewave',
        'dimension': 'uV',
        'sample_rate': 200,
        'physical_max': 100,
        'physical_min': -100,
        'digital_max': 0,
        'digital_min': 65535,
        'transducer': '',
        'prefilter': ''
    }
    channel_info.append(ch_dict)
    data_list.append(np.random.normal(size=file_duration * 200))

    ch_dict = {
        'label': 'ramp',
        'dimension': 'uV',
        'sample_rate': 200,
        'physical_max': 100,
        'physical_min': -100,
        'digital_max': 32767,
        'digital_min': -32768,
        'transducer': '',
        'prefilter': ''
    }
    channel_info.append(ch_dict)
    data_list.append(np.random.normal(size=file_duration * 200))

    ch_dict = {
        'label': 'pulse 1',
        'dimension': 'uV',
        'sample_rate': 200,
        'physical_max': 100,
        'physical_min': -100,
        'digital_max': 32767,
        'digital_min': -32768,
        'transducer': '',
        'prefilter': ''
    }
    channel_info.append(ch_dict)
    data_list.append(np.random.normal(size=file_duration * 200))

    ch_dict = {
        'label': 'pulse 2',
        'dimension': 'uV',
        'sample_rate': 256,
        'physical_max': 100,
        'physical_min': -100,
        'digital_max': 32767,
        'digital_min': -32768,
        'transducer': '',
        'prefilter': ''
    }
    channel_info.append(ch_dict)
    data_list.append(np.random.normal(size=file_duration * 200))

    ch_dict = {
        'label': 'pulse 3',
        'dimension': 'uV',
        'sample_rate': 217,
        'physical_max': 100,
        'physical_min': -100,
        'digital_max': 32767,
        'digital_min': -32768,
        'transducer': '',
        'prefilter': ''
    }
    channel_info.append(ch_dict)
    data_list.append(np.random.normal(size=file_duration * 200))

    ch_dict = {
        'label': 'noise',
        'dimension': 'uV',
        'sample_rate': 200,
        'physical_max': 100,
        'physical_min': -100,
        'digital_max': 32767,
        'digital_min': -32768,
        'transducer': '',
        'prefilter': ''
    }
    channel_info.append(ch_dict)
    data_list.append(np.random.normal(size=file_duration * 200))

    ch_dict = {
        'label': 'sine 1 Hz',
        'dimension': 'uV',
        'sample_rate': 200,
        'physical_max': 100,
        'physical_min': -100,
        'digital_max': 32767,
        'digital_min': -32768,
        'transducer': '',
        'prefilter': ''
    }
    channel_info.append(ch_dict)
    data_list.append(np.random.normal(size=file_duration * 200))

    ch_dict = {
        'label': 'sine 8 Hz',
        'dimension': 'uV',
        'sample_rate': 200,
        'physical_max': 100,
        'physical_min': -100,
        'digital_max': 32767,
        'digital_min': -32768,
        'transducer': '',
        'prefilter': ''
    }
    channel_info.append(ch_dict)
    data_list.append(np.random.normal(size=file_duration * 200))

    ch_dict = {
        'label': 'sine 8.1777 Hz',
        'dimension': 'uV',
        'sample_rate': 200,
        'physical_max': 100,
        'physical_min': -100,
        'digital_max': 32767,
        'digital_min': -32768,
        'transducer': '',
        'prefilter': ''
    }
    channel_info.append(ch_dict)
    data_list.append(np.random.normal(size=file_duration * 200))

    ch_dict = {
        'label': 'sine 8.5 Hz',
        'dimension': 'uV',
        'sample_rate': 200,
        'physical_max': 100,
        'physical_min': -100,
        'digital_max': 32767,
        'digital_min': -32768,
        'transducer': '',
        'prefilter': ''
    }
    channel_info.append(ch_dict)
    data_list.append(np.random.normal(size=file_duration * 200))

    ch_dict = {
        'label': 'sine 15 Hz',
        'dimension': 'uV',
        'sample_rate': 200,
        'physical_max': 100,
        'physical_min': -100,
        'digital_max': 32767,
        'digital_min': -32768,
        'transducer': '',
        'prefilter': ''
    }
    channel_info.append(ch_dict)
    data_list.append(np.random.normal(size=file_duration * 200))

    ch_dict = {
        'label': 'sine 17 Hz',
        'dimension': 'uV',
        'sample_rate': 200,
        'physical_max': 100,
        'physical_min': -100,
        'digital_max': 32767,
        'digital_min': -32768,
        'transducer': '',
        'prefilter': ''
    }
    channel_info.append(ch_dict)
    data_list.append(np.random.normal(size=file_duration * 200))

    ch_dict = {
        'label': 'sine 50 Hz',
        'dimension': 'uV',
        'sample_rate': 200,
        'physical_max': 100,
        'physical_min': -100,
        'digital_max': 32767,
        'digital_min': -32768,
        'transducer': '',
        'prefilter': ''
    }
    channel_info.append(ch_dict)
    data_list.append(np.random.normal(size=file_duration * 200))

    f.setSignalHeaders(channel_info)
    f.writeSamples(data_list)
    f.writeAnnotation(0, -1, "Recording starts")
    f.writeAnnotation(298, -1, "Test 1")
    f.writeAnnotation(294.99, -1, "pulse 1")
    f.writeAnnotation(295.9921875, -1, "pulse 2")
    f.writeAnnotation(296.99078341013825, -1, "pulse 3")
    f.writeAnnotation(600, -1, "Recording ends")
    f.close()
    del f


if __name__ == "__main__":
    root_dir = r'F:\data-0.01mv-7HZ-20210614'
    name_list = [root_dir + '/channel0', root_dir + "/channel1", 
root_dir + "/channel2", root_dir + "/channel3"]

    edf = EdfHandle()
    channel_list = [
                edf.add_channel("channel0", 'uV', 600, 9000, -2000, 4096, 0),
                edf.add_channel("channel1", 'uV', 600, 9000, -2000, 4096, 0),
                edf.add_channel("channel2", 'uV', 200, 9000, -2000, 4096, 0),
                edf.add_channel("channel3", 'uV', 200, 9000, -2000, 4096, 0)
                ]
    assert len(name_list) == len(channel_list)

    for i in range(len(name_list)):
        data = DataParser.parse_points(name_list[i])
        channel_list[i].add_data(data)

    edf.export("data-0.01mv-7HZ-202106142.edf")

