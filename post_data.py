import requests
import json
import os
import numpy as np
from datetime import datetime
from zlib import decompress
from base64 import decodestring
from struct import unpack
from requests.auth import HTTPBasicAuth,HTTPDigestAuth


def get_fault_frequency(data,fault_freq):
    spectrum = np.linspace(0,1000,len(data))
    print("length of data ",len(data))
    print("length of spectrum ",len(spectrum))

    #print(fault_freq)
    mx = max(data)
    idx = list(data).index(mx)
    #print("maximum index {}".format(idx))
    #fault_index = (np.abs(spectrum-fault_freq)).argmin()
    faults = list(filter(lambda f: round(f,0) == round(fault_freq,0) ,spectrum))
    #print(faults)
    fault = min(faults,key=lambda x:abs(x-fault_freq))
    index_of_fault = list(spectrum).index(fault)
    magnitude = data[index_of_fault]
    #print(fault)
    #print("fault {}".format(magnitude))
    exit()
    amplitude = data[fault_index]
    if amplitude:
        return amplitude
    else:
        return None


def get_date(linux_time):
    date = datetime.fromtimestamp(linux_time).strftime('%Y-%m-%d %H:%M:%S')
    return date




def get_data(username, password, url):

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
    'Accept-Encoding': 'gzip, deflate'}
    response = requests.get(url,auth=HTTPBasicAuth('{}'.format(username),
                            '{}'.format(password)),headers=headers)
    if response.status_code == 200:
        json_data = json.loads(response.text)
        return json_data
    else:
        print("Error: status code {}".format(response.status_code))

def decode_data(string_data,key):
    byte_object = decodestring(str.encode(string_data))
    data = decompress(byte_object)
    data_in_num = []
    if key in ["lower_env","upper_env"]:
        data_in_num = np.array([unpack('f', data[i * 4:(i + 1) * 4])[0]\
                            for i in range(len(data) // 4)], dtype='float32')
    elif key == "rms":
        data_in_num = np.fromstring(data, dtype='float32')
    else :
        #wave
        data_in_num = np.array([unpack('h', data[i * 2:(i + 1) * 2])[0]\
                            for i in range(len(data) // 2)], dtype='float32')
    return data_in_num


#import matplotlib.pyplot as plt
def get_twave_spectra(username,password,url):
    raw_data0 = get_data(username, password, url)
    try:
        last_url = raw_data0["_items"][-2]["_links"]["self"]
    except:
        last_url = raw_data0["_items"][-1]["_links"]["self"]
    raw_data = get_data(username, password, last_url)
    string_data = raw_data["data"]
    factor = float(raw_data["factor"])
    min_freq = raw_data["min_freq"]
    max_freq = raw_data["max_freq"]
    date = get_date(raw_data["t"])
    float_data = decode_data(string_data," ")*factor
    return date,min_freq, max_freq, float_data


def get_twave_waves(username,password,url):
    raw_data0 = get_data(username, password, url)
    try:
        last_url = raw_data0["_items"][-2]["_links"]["self"]
    except:
        last_url = raw_data0["_items"][-1]["_links"]["self"]
    #last_url = "http://tcloud2.twave.io/cunb4h/rest/waves/Michaelkrohnsgate/Pos_1/Velocity/1551106865"
    raw_data = get_data(username, password, last_url)
    string_data = raw_data["data"]
    factor = float(raw_data["factor"])
    date = get_date(raw_data["t"])
    float_data = decode_data(string_data,"wave")*factor
    print("data for position 4 {}".format(date))
    return date, float_data


def get_raw_string_data(username,password,url):
    raw_data0 = get_data(username, password, url)
    try:
        last_url = raw_data0["_items"][-2]["_links"]["self"]
    except:
        last_url = raw_data0["_items"][-1]["_links"]["self"]
    raw_data = get_data(username, password, last_url)
    string_data = raw_data["data"]
    time_stamp = int(round(raw_data["t"]*1000,0))
    return string_data, time_stamp
    






if __name__ == '__main__':
    key = os.environ['COGNITE_KEY']
    project = os.environ['COGNITE_PROJECT']
    print(project)
    url = "https://tcloud2.twave.io/cunb4h/rest/waves/Michaelkrohnsgate/Pos_4/Velocity/"
    username = "admin"
    password = "7ToC41Zc"
    #data = get_raw_string_data(username,password,url)
    #print(data)

