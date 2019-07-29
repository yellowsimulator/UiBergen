#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import traceback
import argparse
import yaml
import datetime
import sys
import logging
import csv
from cognite import CogniteClient
from post_data import *

import pandas as pd

client = CogniteClient()
api_key = os.environ['COGNITE_KEY']#config["cognite"]["api_key"]
client = CogniteClient(api_key=api_key, timeout=300)

def post_data():
    url = "https://tcloud2.twave.io/cunb4h/rest/waves/Michaelkrohnsgate/Pos_4/Velocity/"
    username = "admin"
    password = "7ToC41Zc"
    ts_name="spectra_pos_1_accelerate"
    value, epoctime = get_raw_string_data(username,password,url)
    d = {"timestamp":[epoctime], ts_name:[value]}
    df = pd.DataFrame(d)
    try:
        client.datapoints.post_datapoints_frame(df)
        print(" OK")
    except Exception as error:
        print(error)
    
def get_data_point():
    res = client.datapoints.get_datapoints(name="spectra_pos_1_accelerate",start=1551954125615)
    print(res)
 


# Main function
if __name__ == "__main__":
    """ Parse arguments """
    
    get_data_point()