import pyswarm as ps
import numpy as np
from models.optimizer import *
import features.costFunctionStrategies as strategy

class ModelThreePSOOptimizer(Optimizer):

    def __init__(self, ids, dateTime, loadGrid, loadCons, loadProd):
        super().__init__(ids, dateTime, loadGrid, loadCons, loadProd)
        # self.lb = [0] * len(self.loadCons)
        # self.ub = [0.01] + [self.batteryCapacity] * (len(self.loadCons) - 1)
        # self.fopt = 0
        self.lb = np.array([])
        self.ub = np.array([])
        self.newGrid = np.array([])
        self.prodUsage = np.array([])
        self.battCharge = np.array([])
        self.prices = np.array(self.prices)
    
    def optimize(self):

        numberOfDays = int (len(self.dateTime) / 24)
        oneDayLb = 0
        oneDayUb = 0
        oneDayNewGrid = 0
        oneDayProdUsage = 0
        oneDayBattCharge = 0

        for idx, (oneDayLoadCons, oneDayLoadProd, oneDayPrices) in enumerate(zip(np.split(self.loadCons, numberOfDays), np.split(self.loadProd, numberOfDays), np.split(self.prices, numberOfDays))):
            
            oneDayLb = [0] * 24
            if idx is 0:
                oneDayUb = [0.01] + [self.batteryCapacity] * 23
            else:
                oneDayUb = [0.01 if self.battCharge[-1] <= 0 else self.battCharge[-1]] + [self.batteryCapacity] * 23


            oneDayBattCharge, fopt = ps.pso(strategy.costFuncOnMinPrice,
                                        oneDayLb,
                                        oneDayUb,
                                        args=(oneDayLoadCons, oneDayLoadProd, oneDayPrices),
                                        debug=False,
                                        swarmsize=20,
                                        maxiter=100000)
            
            oneDayNewGrid = strategy.newGridEvolution(oneDayBattCharge, oneDayLoadCons, oneDayLoadProd)
            oneDayProdUsage = strategy.costEvolutionProduction(oneDayBattCharge, oneDayLoadCons, oneDayLoadProd)

            self.lb = np.append(self.lb, oneDayLb)
            self.ub = np.append(self.ub, oneDayUb)
            self.newGrid = np.append(self.newGrid, oneDayNewGrid)
            self.prodUsage = np.append(self.prodUsage, oneDayProdUsage)
            self.battCharge = np.append(self.battCharge, oneDayBattCharge)    
        
    def getReport(self):
        updateDict = super().getReport()
        updateDict.update({ "lb": self.lb,
                            "ub": self.ub,
                            # "fopt": self.fopt
                            })
        return updateDict