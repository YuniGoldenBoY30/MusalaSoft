import logging

import requests

logging.basicConfig(filename='logs/battery.log', level=logging.DEBUG, format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()

logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


def get_data():
    try:
        logger.info("Accessing to api data drone")
        data_list = requests.get('http://localhost:8000/drone/list/?skip=0&limit=100').json()
        return data_list
    except Exception as e:
        logger.critical(str(e.__str__()))
        print("No access to api")


if get_data():
    logging.info(f"Check total of: {len(get_data())} drones")
    logging.info(f"-------------------------------------------")
    for data in get_data():
        battery = data['battery_capacity']
        drone_id = data['id']
        logging.info(f"Checking: {drone_id} drone")
        if battery > 25:
            logging.info(f"State: BATTERY GOOD: {battery} %")
        elif 15 < battery <= 25:
            logging.warning(f"State: WARNING, LOW BATTERY!: {battery} %")
        elif 10 < battery <= 15:
            logging.error(f"State: CAUTION!, BATTERY BELOW 15%: {battery} %")
        else:
            logging.critical(f"State: CRITICAL, DRONE WILL BE SHUTDOWN!: {battery} %")
