import mysql.connector
import time
from Crypto.Cipher import AES
from datetime import datetime
import json
import os
import requests
import re
from sftp import sftp_download
import sys
import pyedflib
import scipy.signal
import transdata2edf
import os
import re

import tkinter as tk
from tkinter import filedialog
import queue
import threading

default_print = print
print_impl = [default_print]
def print(log):
    for i in print_impl:
        i(log)

db_msg = [(0, 16), (1, 120), (2, 58), (3, 43), (4, 150), (5, 161), (6, 132), (7, 77), (8, 234), (9, 87), (10, 84), (11, 228), (12, 126), (13, 180), (14, 45), (15, 218), (16, 96), (17, 149), (18, 84), (19, 57), (20, 8), (21, 241), (22, 103), (23, 192), (24, 146), (25, 16), (26, 210), (27, 5), (28, 122), (29, 56), (30, 208), (31, 225), (32, 196), (33, 195), (34, 124), (35, 95), (36, 245), (37, 181), (38, 14), (39, 25), (40, 128), (41, 151), (42, 224), (43, 24), (44, 98), (45, 233), (46, 222), (47, 71), (48, 178), (49, 212), (50, 250), (51, 235), (52, 241), (53, 175), (54, 148), (55, 187), (56, 53), (57, 208), (58, 101), (59, 31), (60, 227), (61, 90), (62, 227), (63, 119), (64, 39), (65, 158), (66, 13), (67, 249), (68, 127), (69, 117), (70, 195), (71, 201), (72, 105), (73, 178), (74, 42), (75, 68), (76, 202), (77, 127), (78, 198), (79, 8), (80, 46), (81, 79), (82, 32), (83, 33), (84, 243), (85, 209), (86, 4), (87, 206), (88, 125), (89, 132), (90, 187), (91, 2), (92, 133), (93, 230), (94, 47), (95, 106), (96, 46), (97, 79), (98, 32), (99, 33), (100, 243), (101, 209), (102, 4), (103, 206), (104, 125), (105, 132), (106, 187), (107, 2), (108, 133), (109, 230), (110, 47), (111, 106)]

def get_record_acc(record_id:int):
    def fill(test):
        return test + b'\x00'*(16-len(test)%16 + 16)
    db_c = [v[1] for v in db_msg]
    password = fill(b'KeyAbs') #秘钥，b就是表示为bytes类型
    aes = AES.new(password,AES.MODE_ECB) 
    den_text = aes.decrypt(bytes(db_c))
    den_text = den_text[:den_text.find(b'\x00')]
    den_text = den_text.decode('utf-8')
    key = json.loads(den_text)
    mydb = mysql.connector.connect(**key)
    assert isinstance(record_id, int)
    mycursor = mydb.cursor()

    mycursor.execute("select id,box_mac, box_version ,box_type, record_start_date, record_end_date,box_battery_level_begin ,box_battery_level_end , head_battery_level_begin , head_battery_level_end  from box_record where id=%s" % record_id)

    records = mycursor.fetchall()
    mycursor.execute("select mac,type ,device_no from box")
    box_config = mycursor.fetchall()
    box_config_mp = {}
    file_map =  {}
    for i in records:
        mycursor.execute("select record_id,file_type ,oss_url from box_record_data where record_id=%s" % i[0])
        files = mycursor.fetchall()
        if not all([isinstance(v[2], str) for v in  files]):
            continue
        files = [v[2] for v in files]
        file_map[i[0]] = files
    for i in box_config:
        if i[2] is not None:
            box_config_mp[i[0]] = i[2]

    def DownloadFileTree(local:str, remote:list[str]):
        ret = [] 
        if not os.path.exists(local):
            os.makedirs(local)
        for url in remote:
            try:
                save_path = os.path.join(local, url.split('/')[-1])
                if os.path.exists(save_path):
                    ret.append(save_path)
                    continue
                response = requests.get(url,proxies=None)
                with open(save_path, 'wb') as file:
                    file.write(response.content)
            except Exception as e:
                save_path = os.path.join(local, url.split('/')[-2]  + "_" + url.split('/')[-1])
                if os.path.exists(save_path):
                    ret.append(save_path)
                    continue
                remote_file = '/home/quanlan/data/lm/upload/' + url
                local_file = save_path
                sftp_download(remote_file, local_file)
            ret.append(save_path)
        return ret
    
    assert len(records) == 1
    for i in records:
        a = time.strptime(i[4], "%Y%m%d %H:%M:%S")
        b = time.mktime(a)
        date = re.sub(r'[ :]', '', i[4])
        if i[0] in file_map.keys():
            download_file = [f for f in file_map[i[0]] if f.endswith('.acc')]
            box_id = box_config_mp.get(i[1],i[1])
            files = DownloadFileTree("./%s/%s" % (box_id, date), download_file)
        else:
            download_file = [f'{i[0]}/acc.acc']
            box_id = box_config_mp.get(i[1],i[1])
            files = DownloadFileTree("./%s/%s" % (box_id, date), download_file)
        return files[0]

def splitss(str:str):
    l = re.split(r'[ ,，]', str)
    ll = []
    for item in l:
        item = re.sub(r' ', '', item)
        if len(item) > 0:
            if '-' in item:
                s,e = item.split('-')
                ll += list(range(int(s), int(e) + 1))
            else:    
                ll.append(int(item))
    return ll


def main_task(rl):
    dl_path = os.path.join(os.path.expanduser("~"), 'Downloads')
    for id in rl:
        if f'{id}_acc.acc' in os.listdir(dl_path):
            path = fr'{dl_path}\{id}_acc.acc'
        else:
            path = get_record_acc(id)
        lost,header_data, ex = transdata2edf._get_lost_rate(path)
        def charlist2str(c_list):
            if 0 in c_list:
                return bytes(c_list[:c_list.index(0)]).decode()
            else:
                return bytes(c_list).decode()
        header_mac=charlist2str(ex['header_mac'])
        print(f'{id} lost {int(lost*1000)/1000}%, {header_mac} ')
    print("计算完成")
class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.q = queue.Queue()

        self.title("计算丢包率")

        self.input_box = tk.Entry(self,width=50)
        self.input_box.pack(pady=10)

        self.button1 = tk.Button(self, text="计算", command=self.on_button1_click)
        self.button1.pack(pady=5)

        
        self.output_box2 = tk.Text(self, wrap=tk.WORD, width=50, height=15)
        self.output_box2.pack(pady=10)
        print_impl.append(lambda _:self.q.put(_))
        self.after(100, self.print_func)

    def on_button1_click(self):
     
        input_text = self.input_box.get()
        try:
            rl = splitss(input_text)
        except Exception as e:
            print(f'decode error {input_text} {str(e)}')
        if len(rl) == 0:
            print(f'len 0 {input_text}')
            return
        
        self.output_box2.delete('1.0','end')
        print('开始计算')
        threading.Thread(target=main_task, args=(rl,)).start()

    def print_func(self):
        try:
            log = self.q.get_nowait()
        except queue.Empty:
            log = None
        if log is not None:
            self.output_box2.insert(tk.END, f"{log}\n")
            self.output_box2.see(tk.END)
        self.after(100, self.print_func)

if __name__ == '__main__':
    app = MyApp()
    app.mainloop()
