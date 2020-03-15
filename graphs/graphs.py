import pandas as pd
import os
import calendar


class Graphs:
    def __init__(self,app):
        csv_filename = os.path.join(app.root_path, 'graphs\\data', 'DECCC.csv')
        self.df = pd.read_csv(csv_filename)
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp']).apply(lambda x: x.date())
        #This is still WIP
        self.year_count = {}

    def get_daily_metrics(self):
        day_count = {}
        for row in self.df['timestamp']:
            if str(row) not in day_count.keys():
                day_count[str(row)] = 1
            else:
                day_count[str(row)] = day_count[str(row)] + 1
        return day_count

    def get_monthly_metrics(self):
        month_count = {}
        for row in self.df['timestamp']:
            month = calendar.month_name[row.month]
            if month not in month_count.keys():
                month_count[month] = 1
            else:
                month_count[month] = month_count[month] + 1
        return  month_count

    def get_yearly_metrics(self):
        return None