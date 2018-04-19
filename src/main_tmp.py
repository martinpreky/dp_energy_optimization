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


if __name__ == '__main__':
    
    dutils.PATH_TO_DATA = 'data/raw/'  

    allHouses = dutils.get_houses_csvs()
    house = allHouses[0]
        
    day = 1
    numberOfDays = 20
    x, grid, cons, prod, ids = dutils.init_data(house, numberOfDays, day)

    model = ModelTwoLBFGSBOptimizer(ids, x, grid, cons, prod)
    model.defineDataAttrs(house, numberOfDays, day)

    model.optimize()

    pathFile = "data/interim/" + model.getCsvName()
    print(pathFile)

    df = pd.DataFrame(data=model.getReport())
    df.to_csv(path_or_buf=pathFile, sep=";", na_rep="N/A")