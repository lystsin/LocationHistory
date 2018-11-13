# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 13:12:39 2018

@author: lystsin
"""

import os
import json
import logging
import datetime

import const

# loggerの設定
logging.config.fileConfig(const.LOGGER_CONF)
logger = logging.getLogger()

def main():
    logger.info('start main')
    
    # locationsファイルの読み込み
    locations = load_locations()
    
    # locationsを日ごとにマージ
    location_day = dict(make_location_day(locations))
    
    # 一日ずつ処理
    for k, v in sorted(location_day.items(), key=lambda x: x[0]):
        #月ごとのディレクトリ作成（存在しない場合のみ）
        dir_path = const.DATA_DIR + '/' + k[:6]
        os.makedirs(dir_path, exist_ok=True)
        
        #日ごとにJsonファイルに出力
        write_file_name = dir_path + '/' + k + '.json'
        with open(write_file_name, 'w') as wf:
            wf.write(json.dumps(v, ensure_ascii=False, indent=4, 
                                sort_keys=False, separators=(',', ': ')))
    
    logger.info('end main')
    

def load_locations():
    logger.info('start load_locations')
    
    with open(const.DATA_DIR + '/' + const.READ_FILE_NAME, 'r') as rf:
        dct = json.load(rf)
    return dct['locations']

    logger.info('end load_locations')


def make_location_day(locations):
    logger.info('start make_location_day')
    
    location_day = {}
    for location in locations:
        timestamp = timestampms_to_timestamp(location['timestampMs'])
        
        # 年月日のキーが含まれていなければ、年月日をキーに辞書追加
        if(timestamp[:8] not in location_day):
            location_day[timestamp[:8]] = {}
        
        # 年月日の辞書にタイムスタンプをキーに位置情報をセット
        location_day[timestamp[:8]][timestamp] = location
        
    logger.info('end make_location_day')
    
    return location_day


def timestampms_to_timestamp(timestampMs):
    timestamp = datetime.fromtimestamp(int(timestampMs[:10])).strftime('%Y%m%d%H%M%S')
    return timestamp
    

if __name__ == '__main__':
    main()
    
    