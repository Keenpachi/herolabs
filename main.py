from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
import requests
import json
import time

app = FastAPI()


@app.get("/parking/{parking_id}")
def fetch_data(parking_id: str):
    current_data = json.load(open('parking_data.json', 'r'))

    if parking_id in current_data.keys():
        parking_data = current_data.get(parking_id)
        response = {'total_places': parking_data[0], 'taken_places': parking_data[1]}
    else:
        response = {"parking data don't exist"}

    return response


@app.put("/crawl/{parking_id}/{refresh_period}")
def update_scheduler(parking_id: str, refresh_period: int):

    scheduler_data = json.load(open('scheduler.json', 'r'))
    scheduler_data[parking_id] = [refresh_period, time.time()]

    with open('scheduler.json', 'w') as fp:
        json.dump(scheduler_data, fp)

    return {'scheduler updated'}


def run_scheduler():
    current_time = time.time()
    scheduler_data = json.load(open('scheduler.json', 'r'))
    current_data = json.load(open('parking_data.json', 'r'))

    # update scheduled parking data
    for key, value in scheduler_data.items():
        if (current_time - value[1])/60 > value[0]:
            url = f'http://private-b2c96-mojeprahaapi.apiary-mock.com/pr-parkings/{key}'
            response_data = requests.get(url).json()
            current_data[key] = [response_data['properties']['total_num_of_places'], response_data['properties']['num_of_taken_places']]
            # update scheduler time
            scheduler_data[key] = [scheduler_data.get(key)[0], current_time]

    # save data
    with open('scheduler.json', 'w') as f:
        json.dump(scheduler_data, f)

    with open('parking_data.json', 'w') as f:
        json.dump(current_data, f)


@app.on_event('startup')
def init_data():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_scheduler, 'cron', second='*/5')
    scheduler.start()
