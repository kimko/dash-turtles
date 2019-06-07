from dateutil.relativedelta import relativedelta
from datetime import datetime

import pandas as pd


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


class Turtle_Manager():
    def __init__(self):
        df = pd.read_csv(
            'https://s3-us-west-2.amazonaws.com/cool-turtles/turtles.csv')
        df = df[df['Weight'] != 0]
        df = df[df['Carapace'] != 0]
        df = df[df['Plastron'] != 0]
        df = df[df['Species'] == 'Cpb']
        df.Gravid = df.Gravid.map({True: 'Y', False: ''})
        df.Date = pd.to_datetime(df.Date)
        self.df = df

    def get_df(self):
        return self.df
