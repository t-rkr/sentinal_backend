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

    def get_user_metrics(self):
        df = self.df
        df['timestamp'] = self.df['timestamp'].apply(lambda x: pd.Timestamp(x).strftime('%Y-%m-%d'))
        df =  df.set_index('timestamp')
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

    def get_total_tweets(self):
        data = {"total":int(self.df['text'].count())}
        return data

    def get_yearly_metrics(self):
        return None