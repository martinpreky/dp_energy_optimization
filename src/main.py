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

if __name__ == '__main__':
    print(__name__)
    dutils.PATH_TO_DATA = 'data/raw/'
    house = "dataid1103.csv"
    day = 70
    numberOfDays = 1
    x, grid, cons, prod, ids = dutils.init_data(house, numberOfDays, day)

    # m = ModelOneEBOptimizer(ids, x, grid, cons, prod)
    m = ModelOneLBFGSBOptimizer(ids, x, grid, cons, prod)
    # m = ModelOnePSOOptimizer(ids, x, grid, cons, prod)
    # m = ModelTwoEBOptimizer(ids, x, grid, cons, prod)
    # m = ModelTwoLBFGSBOptimizer(ids, x, grid, cons, prod)
    # m = ModelTwoPSOOptimizer(ids, x, grid, cons, prod)
    # m = ModelThreeEBOptimizer(ids, x, grid, cons, prod)
    # m = ModelThreeLBFGSBOptimizer(ids, x, grid, cons, prod)
    # m = ModelThreePSOOptimizer(ids, x, grid, cons, prod)
    
    m.optimize()
    m.showPlot()
    # report = m.getReport()
    # print(report)

