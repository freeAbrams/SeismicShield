import requests
import os
import time
import logging
from config import API_URL, SCALE_THRESHOLD, CHECK_INTERVAL, LOG_FILE, TARGET_AREA_NAME, HARD_DRIVE_PATH

# 配置日志记录
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
                        print(f"Earthquake detected: ID={earthquake_id}, Magnitude={magnitude}, OriginTime={origin_time}. Would stop hard drive.")  # 打印检测到地震的信息到控制台
                        # stop_hard_drive()  # 注释掉实际停止硬盘的调用
                        print(f"Hard drive {HARD_DRIVE_PATH} would be stopped.")  # 打印停止硬盘信息到控制台
                        logging.info(f"Hard drive {HARD_DRIVE_PATH} would be stopped.")  # 记录停止硬盘信息到日志
                        break
    except requests.RequestException as e:
        logging.error(f"Error fetching earthquake data: {e}")
        print(f"Error fetching earthquake data: {e}")  # 打印错误信息到控制台

if __name__ == "__main__":
    while True:
        print("Running earthquake check loop...")  # 打印主循环运行信息到控制台
        logging.info("Running earthquake check loop...")
        check_earthquake()
        time.sleep(CHECK_INTERVAL)