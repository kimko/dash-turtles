from requests import get
from os import getenv
import json

import pandas as pd

class Turtle_Manager():
    def __init__(self, test=False):
        self.turtle_service_url = getenv('turtle_service_url')
        assert(self.turtle_service_url)
        #  TODO error handling
        res = get(self.turtle_service_url + '/turtles')
        data = json.loads(res.content)
        self.df = pd.read_json(data['data']['turtles'])

    def get_count_per_period_and_year(self, period, locations):
        # TODO error handling
        res = get(f'{self.turtle_service_url}/turtlesPeriodYear?period={period}&locations={locations}')
        data = json.loads(res.content)
        df = pd.read_json(data['data']['turtles'])
        return df

    def filter_from_periodStart_to_endDate(self, endDate, frequency):
        # TODO error handling
        res = get(f'{self.turtle_service_url}/turtlesPeriodStartToEnd?period={frequency}&endDate={endDate}')
        data = json.loads(res.content)
        df = pd.read_json(data['data']['turtles'])
        return df

    def get_df(self):
        return self.df

if __name__ == '__main__':
    df = Turtle_Manager().get_df()
