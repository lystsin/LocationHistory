# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 13:12:39 2018

@author: lystsin
"""

import os
import json
import logging
import logging.config
from datetime import datetime

import geo
import const

# loggerの設定
logging.config.fileConfig(const.LOGGER_CONF)
logger = logging.getLogger()


def main():
    """Summary line.

    GoogleタイムラインJsonを読み込んで、処理しやすい形に整形と軽量化を行い再度ファイル出力を行う。

    1.GoogleタイムラインJson(以降locationsと呼ぶ)読み込み
    2.locationsのtimestampMsから、日ごとにJsonの形を変更
    　また、不要パラメータを削ぎ落として軽量化を図る
    3.月ごとのディレクトリに日ごとのJsonを出力する。

    """
    logger.info('start main')

    # locationsファイルの読み込み
    locations = load_locations()

    # locationsを日ごとにマージ
    location_day = dict(make_location_day(locations))

    # 一日ずつ処理
    for k, v in sorted(location_day.items(), key=lambda x: x[0]):
        # 月ごとのディレクトリ作成（存在しない場合のみ）
        dir_path = const.OUTPUT_DATA_DIR + '/' + k[:6]
        os.makedirs(dir_path, exist_ok=True)

        # 日ごとにJsonファイルに出力
        write_file_name = dir_path + '/' + k + '.json'
        with open(write_file_name, 'w') as wf:
            wf.write(json.dumps(v, ensure_ascii=False, sort_keys=False,
                                separators=(',', ': ')))

    distance = total_distance(location_day)

    logger.info('総移動距離 = {0}km'.format(str(distance)))

    logger.info('end main')


def load_locations():
    """Summary line.

    locationsを読み込む

    Returns:
        dct['locations'](dct) : locationsの中身だけ返却

    """
    logger.info('start load_locations')

    with open(const.INPUT_DATA_DIR + '/' + const.READ_FILE_NAME, 'r') as rf:
        dct = json.load(rf)

    logger.info('end load_locations')

    return dct['locations']


def make_location_day(locations):
    """Summary line.

    locationsを日ごとのJsonに整形、不要パラメータを削ぎ落として軽量化を行う。

    Args:
        locations(dict) : Googleタイムライン情報（全体）

    Returns:
        locations_day : 整形したlocations

    """
    logger.info('start make_location_day')

    locations_day = {}
    for location in locations:
        # 年月日のキーが含まれていなければ、年月日をキーに辞書追加
        timestamp = timestampms_to_timestamp(location['timestampMs'])
        if(timestamp[:8] not in locations_day):
            locations_day[timestamp[:8]] = {}

        # パラメータ削ぎ落とし
        location = select_parameter(location)

        # E7の値を実数に変換
        location = e7_to_float(location)

        # 年月日の辞書にタイムスタンプをキーに位置情報をセット
        locations_day[timestamp[:8]][timestamp] = location

    logger.info('end make_location_day')

    return locations_day


def select_parameter(location):
    """Summary line.

    定数SELECT_PARAMETESに定義したキーのみにlocation情報を削ぎ落とす

    Args:
        location(dict) : Googleタイムライン情報（単体）

    Returns:
        location : 削ぎ落としたlocation

    """
    ret_location = {}
    for param_name in const.SELECT_PARAMETERS:
        if param_name in location:
            ret_location[param_name] = location[param_name]
    return ret_location


def timestampms_to_timestamp(timestampMs):
    """Summary line.

    timestampMsをtimestampに変換する

    Args:
        timestampMs(str) : timestampMs

    Returns:
        timestamp : タイムスタンプ(%Y%m%d%H%M%S)

    """
    timestamp = datetime.fromtimestamp(int(timestampMs[:10]))
    return timestamp.strftime('%Y%m%d%H%M%S')


def e7_to_float(location):
    """Summary line.

    latitudeE7, longitudeE7を実数に変換する

    Args:
        location(dict) : Googleタイムライン情報

    Returns:
        location(dict) : latitude, longitude変換後のGoogleタイムライン情報

    """
    if 'latitudeE7' in location:
        location['latitude'] = location['latitudeE7'] / 10000000
        location.pop('latitudeE7')

    if 'longitudeE7' in location:
        location['longitude'] = location['longitudeE7'] / 10000000
        location.pop('longitudeE7')

    return location


def total_distance(location_day):
    """Summary line.

    latitudeE7, longitudeE7を実数に変換する

    Args:
        location(dict) : Googleタイムライン情報

    Returns:
        location(dict) : latitude, longitude変換後のGoogleタイムライン情報

    """
    logger.info('start total_distance')

    current_data = {}
    distance_total = 0
    for day, location in sorted(location_day.items(), key=lambda x: x[0]):
        distance_day = 0
        for timestamp, data in sorted(location.items(), key=lambda x: x[0]):
            # 初回処理
            if not current_data:
                current_data = data
            else:
                distance = geo.cal_rho(current_data['latitude'],
                                       current_data['longitude'],
                                       data['latitude'],
                                       data['longitude'])
                logger.debug('{0}の移動距離: {1}km'
                             .format(timestamp, str(distance)))
                current_data = data
                distance_day += distance

        distance_total += distance_day
        logger.debug('{0}の移動距離: {1}km'.format(day, str(distance_day)))

    logger.info('end total_distance')
    return distance_total


if __name__ == '__main__':
    main()
