import pandas as pd
import os
import calendar
import datetime


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
            print(row)
            month = calendar.month_name[row.month] if isinstance(row, datetime.date) else calendar.month_name[
                int(row.split("-")[1])]
            if str(month) not in month_count.keys():
                month_count[str(month)] = 1
            else:
                month_count[str(month)] = month_count[str(month)] + 1
        return month_count

    def get_user_metrics(self):
        df = self.df
        df['timestamp'] = df['timestamp'].apply(lambda x: pd.Timestamp(x).strftime('%Y-%m-%d'))
        df = df.set_index('timestamp')
        daily_users = {}
        daily_users_metrics = {}
        for row in df.itertuples():
            ind = str(row.Index)
            if not (ind in daily_users.keys()):
                daily_users[ind] = [row.user_id]
                daily_users_metrics[ind] = 1
            else:
                if row.user_id in daily_users[ind]:
                    pass
                else:
                    daily_users_metrics[ind] = daily_users_metrics[ind] + 1
                daily_users[ind].append(row.user_id)
        return daily_users_metrics

    def get_user_metrics_monthly(self,daily):
        ld = pd.DataFrame(daily.items(), columns=['time', 'count'])
        ld['time'] = pd.to_datetime(ld['time'])
        ld = ld.set_index('time')
        ld.index = pd.to_datetime(ld.index)
        ld['month'] = ld.index.month
        x = list(ld['count'].values)
        y = list(ld['month'].values)
        z = list(zip(x, y))
        a = {}
        for val in z:
            if calendar.month_name[val[1]] in a.keys():
                a[calendar.month_name[val[1]]] = a[calendar.month_name[val[1]]] +int( val[0])
            else:
                a[calendar.month_name[val[1]]] = int(val[0])
        return a

    def get_total_tweets(self):
        data = {"total":int(self.df['text'].count())}
        return data

    def get_yearly_metrics(self):
        return None