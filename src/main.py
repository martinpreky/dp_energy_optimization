import sys
import os
module_path = os.path.abspath(os.path.join('data\\external'))
if module_path not in sys.path:
    sys.path.append(module_path)

import features._data_utils as dutils
from models.modelOneEBOptimizer import *
from models.modelOneLBFGSBOptimizer import *
from models.modelOnePSOOptimizer import *
from models.modelTwoEBOptimizer import *
from models.modelTwoLBFGSBOptimizer import *
from models.modelTwoPSOOptimizer import *
from models.modelThreeEBOptimizer import *
from models.modelThreeLBFGSBOptimizer import *
from models.modelThreePSOOptimizer import *

import numpy as np
import pandas as pd
import multiprocessing as mp



def opt(house):
    dutils.PATH_TO_DATA = 'data/raw/'
    day = 1
    numberOfDays = 365
    x, grid, cons, prod, ids = dutils.init_data(house, numberOfDays, day)

    m = ModelThreePSOOptimizer(ids, x, grid, cons, prod)
    m.optimize()

    csvName = "data/interim/"+house+"_"+m.__class__.__name__+"_"+str(day)+"_"+str(numberOfDays)+".csv"
    return (m, csvName)

if __name__ == '__main__':
    
    dutils.PATH_TO_DATA = 'data/raw/'    
    with mp.Pool(2) as pool:

        allHouses = dutils.get_houses_csvs()
        firstXhouses = allHouses[:2]

        for (model, pathFile) in pool.imap_unordered(opt, firstXhouses):
            print(pathFile)
            df = pd.DataFrame(data=model.getReport())
            df.to_csv(path_or_buf=pathFile, sep=";", na_rep="N/A")
        
        print("end of for loop")
        pool.close()
        pool.join()
    
    
    # house = "dataid1103.csv"
    # day = 70
    # numberOfDays = 20
    # x, grid, cons, prod, ids = dutils.init_data(house, numberOfDays, day)

    # m = ModelOneEBOptimizer(ids, x, grid, cons, prod)
    # m = ModelOneLBFGSBOptimizer(ids, x, grid, cons, prod)
    # m = ModelOnePSOOptimizer(ids, x, grid, cons, prod)
    # m = ModelTwoEBOptimizer(ids, x, grid, cons, prod)
    # m = ModelTwoLBFGSBOptimizer(ids, x, grid, cons, prod)
    # m = ModelTwoPSOOptimizer(ids, x, grid, cons, prod)
    # m = ModelThreeEBOptimizer(ids, x, grid, cons, prod)
    # m = ModelThreeLBFGSBOptimizer(ids, x, grid, cons, prod)
    # m = ModelThreePSOOptimizer(ids, x, grid, cons, prod)
    
    # m.optimize()
    # m.showPlot()
    # report = m.getReport()
    # print(report)

