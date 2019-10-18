import numpy
import pandas
from natsort import natsorted


def iterable(x):
    if isinstance(x, str): return False
    try:
        for t in x:
            break
        return True
    except:
        return False


class Logger:
    def __init__(self):
        self.data = {}

    @property
    def keys(self):
        return self.data.keys()

    @property
    def time(self):
        if 'time' in self.keys:
            time = self.data['time']
            time = numpy.array(time, dtype='f')
            return time
        else:
            return None

    def __getitem__(self, field):
        return self.get(field)

    def get(self, field):
        data = self.data[field]
        return data

    def __setitem__(self, field, data):
        if not iterable(field): field = [field]
        if not iterable(data): data = [data]
        for field_i, data_i in zip(field, data):
            keys = self.keys
            if field_i in keys:
                series = self.data[field_i]
                series.append(data_i)
                self.data[field_i] = series
            if field_i not in keys:
                self.data[field_i] = [data_i]

    def export(self):
        keys = self.keys
        keys = natsorted(keys)
        d = {}
        for k in keys: d[k] = self.get(k)
        df = pandas.DataFrame(d)
        return df
