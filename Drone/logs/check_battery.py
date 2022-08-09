import logging
from datetime import datetime

import requests

logging.basicConfig(filename='battery_log.log', level=logging.INFO, format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()


def get_data():
    try:
        print("espere....")
        URL = 'http://localhost:8000/drone/list/?skip=0&limit=100'  # configuramos la url
        data = requests.get(URL)

        data = data.json()
        return data
    except Exception as e:
        logger.critical(f"Accessed on {str(datetime.now())} " + str(e.__str__()))
        print("No access to api")


if get_data():
    logging.info(f"Check {len(get_data())} drones battery level")
    for data in get_data():
        battery = data['battery_capacity']
        drone_id = data['id']
        logging.info(f"Check {drone_id} drone battery level")
        if battery > 25:
            logging.info(f"Battery Good  ------ {battery}%")
        elif 15 < battery <= 25:
            logging.warning(f"Battery below 25% {str(datetime.now())} ------ {battery}%")
        elif 10 < battery <= 15:
            logging.error(f"Battery below 15% {str(datetime.now())} ------ {battery}%")
        else:
            logging.critical(f"Battery below 10% {str(datetime.now())} ------ {battery}%")
