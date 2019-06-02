import pandas as pd


class Turtle_Manager():
    def __init__(self):
        self.df = pd.read_csv(
            'https://s3-us-west-2.amazonaws.com/cool-turtles/turtles.csv')

    def get_turtles(self):
        df = self.df
        df = df[df['Weight'] != 0]
        df = df[df['Carapace'] != 0]
        df = df[df['Plastron'] != 0]
        df = df[df['Species'] == 'Cpb']
        df.Date = pd.to_datetime(df.Date)
        df.Gravid = df.Gravid.map({True: 'Y', False: ''})
        fields = ['ID', 'Date', 'Capture Location', 'Gender', 'Annuli', 'Annuli_orig', 'Weight', 'Carapace', 'Plastron', 'Gravid']
        self.df = df[fields]
        return self.df
