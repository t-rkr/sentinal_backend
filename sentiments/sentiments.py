import pandas as pd
import os
from datetime import datetime

class Sentiments:
    def __init__(self,app):
        csv_filename = os.path.join(app.root_path, 'sentiments\\data', 'sentis.csv')
        self.df = pd.read_csv(csv_filename)
        self.df['timestamp'] = self.df['timestamp'].apply(lambda x: datetime.fromtimestamp(x))

    def get_polarity(self):
        return {"positive":len(self.df[(self.df['target_new']==1)]),"negative":len(self.df[(self.df['target_new']==0)])}