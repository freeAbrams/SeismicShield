import requests
import os
import time
import logging
from config import API_URL, SCALE_THRESHOLD, CHECK_INTERVAL, LOG_FILE, TARGET_AREA_NAME, HARD_DRIVE_PATH

# logの設定
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def check_earthquake():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        #print(f"Data retrieved: {data}")  # 打印获取的数据到控制台
        #logging.info(f"Data retrieved: {data}")  # 记录获取的数据到日志

        for event in data:
            if not event['cancelled']:
                earthquake_id = event['id']
                magnitude = event['earthquake']['hypocenter']['magnitude']
                origin_time = event['earthquake']['originTime']
                for area in event['areas']:
                    if area['name'] == TARGET_AREA_NAME and area['scaleFrom'] >= SCALE_THRESHOLD:
                        logging.info(f"Earthquake detected: ID={earthquake_id}, Magnitude={magnitude}, OriginTime={origin_time}. Would stop hard drive.")
                        print(f"Earthquake detected: ID={earthquake_id}, Magnitude={magnitude}, OriginTime={origin_time}. Would stop hard drive.")  # 地震情報をコンソールに出力
                        # stop_hard_drive()  # HDD停止
                        print(f"Hard drive {HARD_DRIVE_PATH} would be stopped.")  # HDDの停止情報をコンソールに出力
                        logging.info(f"Hard drive {HARD_DRIVE_PATH} would be stopped.")  # HDDの停止情報をログに出力
                        break
    except requests.RequestException as e:
        logging.error(f"Error fetching earthquake data: {e}")
        print(f"Error fetching earthquake data: {e}")  # エラー情報をコンソールに出力

if __name__ == "__main__":
    while True:
        print("Running earthquake check loop...")  # コンソールに地震チェックループを出力
        logging.info("Running earthquake check loop...")
        check_earthquake()
        time.sleep(CHECK_INTERVAL)