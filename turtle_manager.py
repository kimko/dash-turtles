from requests import get
from os import getenv
import json

from dateutil.relativedelta import relativedelta
from datetime import datetime

from apps.utils import helper_print_caller as print_caller
import pandas as pd

CHUNKSIZE = 1000
URL = 'https://s3-us-west-2.amazonaws.com/cool-turtles/turtles.csv'

def filter_from_periodStart_to_endDate(df, endDate, period):
    endDate = datetime.strptime(endDate, '%Y-%m-%d')
    startDate = str(endDate - relativedelta(months=4))
    if period == 'D':
        startDate = str(endDate - relativedelta(days=1))
    if period == 'W':
        startDate = str(endDate - relativedelta(weeks=1))
    if period == 'M':
        startDate = str(endDate - relativedelta(months=1))
    if period == 'Q':
        startDate = str(endDate - relativedelta(months=4))
    if period == 'A':
        startDate = str(endDate - relativedelta(years=1))
    return (df['Date'] > startDate) & (df['Date'] <= endDate)


def get_count_per_period_and_year(df, period='M'):
    if period == 'M':
        df['Period'] = df.Date.map(lambda x: x.month_name())
    elif period == 'Q':
        df['Period'] = df.Date.map(lambda x: 'Q' + str(x.quarter))
    df = df[['Period', 'Year', 'ID']].sort_values('Period').copy()
    df = df.groupby(['Period', 'Year']).count().reset_index()
    df.columns = ['Period', 'Year', 'Count']
    return df


class Turtle_Manager():
    def __init__(self, test=False):
        turtle_service_url = getenv('turtle_service_url')
        if turtle_service_url:
            #  TODO error handling
            res = get(turtle_service_url + '/turtles')
            data = json.loads(res.content)
            self.df = pd.read_json(data['data']['turtles'])
        else:
            self.df = self.load_from_csv(test)


    def load_from_csv(self, test=False):
        location = getenv('csv_location', URL)
        # TODO logging
        print_caller()
        print("(Deprecated) Reading from", location)
        if test:
            reader = pd.read_csv(location, chunksize=CHUNKSIZE, iterator=True, nrows=10)
        else:
            reader = pd.read_csv(location, chunksize=CHUNKSIZE, iterator=True)
        df = pd.concat(reader, ignore_index=True)
        print(df.shape[0])
        df = df[df['Weight'] != 0]
        df = df[df['Carapace'] != 0]
        df = df[df['Plastron'] != 0]
        df = df[df['Species'] == 'Cpb']
        # df['Month'] = df.Date.map(lambda x: x.strftime('%B'))
        df.Date = pd.to_datetime(df.Date)
        df['Month'] = df.Date.map(lambda x: x.month)
        df['Year'] = df.Date.map(lambda x: x.year)
        df.Gravid = df.Gravid.map({True: 'Y', False: ''})
        latLong = {
            'Mason Flats': ('45.520933', '-122.674101'),
            'Whitaker Ponds': ('45.573749', '-122.613542'),
            'Gresham': ('45.507347', '-122.433480'),
        }
        df['lat'] = df['Capture Location'].map(lambda x: latLong[x][0]).astype('float32')
        df['long'] = df['Capture Location'].map(lambda x: latLong[x][1]).astype('float32')
        return df

    def get_df(self):
        return self.df


if __name__ == '__main__':
    df = Turtle_Manager().get_df()
