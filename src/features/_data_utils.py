import numpy as np
from datetime import datetime
from collections import OrderedDict
from os import walk

str2date = lambda x: datetime.strptime(x.decode("utf-8"), '"%Y-%m-%d %H:%M:%S"')

PATH_TO_DATA = '../../data/raw/'

def read_datafile(file_name):
    return np.genfromtxt(file_name, 
                         dtype=None, 
                         delimiter=';', 
                         names=True, 
                         converters={3: str2date})

def init_data(fileName, numOfDays, sinceDayId):
    #global dictDaysAndIds, day_id, x_time, x_time_float, y_grid, y_cons, y_prod
    data = read_datafile(PATH_TO_DATA + fileName)
    
    #date = data['date']
    day_id = data['dayId']
    since_day = np.searchsorted(day_id, sinceDayId)

    # daysUnique = OrderedDict((x, True) for x in date).keys()
    # idsUnique  = OrderedDict((x, True) for x in day_id).keys()
    # dictDaysAndIds = dict(zip(daysUnique, idsUnique))
    
    ids = data['id'][since_day:since_day+24*numOfDays]
    x_time = data['dateTime'][since_day:since_day+24*numOfDays]
    #x_time_float = mpl.dates.date2num(x_time)
    y_grid = data['loadGrid'][since_day:since_day+24*numOfDays]
    y_cons = data['loadCons'][since_day:since_day+24*numOfDays]
    y_prod = data['loadProd'][since_day:since_day+24*numOfDays]

    return (x_time, y_grid, y_cons, y_prod, ids)#, dictDaysAndIds)

def get_houses_csvs():
    files = []
    for (dirpath, dirnames, filenames) in walk(PATH_TO_DATA):
        files.extend(filenames)
        break
    
    return files

def get_dict_day_id(fileName):
    data = read_datafile(PATH_TO_DATA + fileName)
    
    date = data['date']
    day_id = data['dayId']
    
    daysUnique = OrderedDict((x, True) for x in date).keys()
    idsUnique  = OrderedDict((x, True) for x in day_id).keys()
    
    return dict(zip(daysUnique, idsUnique))
