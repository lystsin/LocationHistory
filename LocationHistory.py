# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 13:12:39 2018

@author: lystsin
"""

import os
import json
import logging
from datetime import datetime


DATA_DIR = 'data'
READ_FILE_NAME = 'locations.json'


def main():
    # loggerの設定
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger()
    
    # locationsファイルの読み込み
    locations = load_locations()
    
    # locationsを日ごとにマージ
    location_day = dict(make_location_day(locations))
    
    # 一日ずつ処理
    for k, v in sorted(location_day.items(), key=lambda x: x[0]):
        dir_path = DATA_DIR + '/' + k[:6]
        os.makedirs(dir_path, exist_ok=True)
        write_file_name = dir_path + '/' + k + '.json'
        with open(write_file_name, 'w') as wf:
            wf.write(json.dumps(v, ensure_ascii=False, indent=4, 
                                sort_keys=False, separators=(',', ': ')))
    

def load_locations():
    with open(DATA_DIR + '/' + READ_FILE_NAME, 'r') as rf:
        dct = json.load(rf)
    return dct['locations']


def make_location_day(locations):
    location_day = {}
    for location in locations:
        timestamp = timestampms_to_timestamp(location['timestampMs'])
        
        # 年月日のキーが含まれていなければ、年月日をキーに辞書追加
        if(timestamp[:8] not in location_day):
            location_day[timestamp[:8]] = {}
        
        # 年月日の辞書にタイムスタンプをキーに位置情報をセット
        location_day[timestamp[:8]][timestamp] = location
        
    return location_day


def timestampms_to_timestamp(timestampMs):
    timestamp = datetime.fromtimestamp(int(timestampMs[:10])).strftime('%Y%m%d%H%M%S')
    return timestamp
    

if __name__ == '__main__':
    main()
    
    