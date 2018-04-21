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

        windowSize = 2
        daySize = 24
    
        numberOfDays = int (len(self.dateTime) / daySize)
        windowLb = 0
        windowUb = 0
        windowBattCharge = 0

        oneDayNewGrid = 0
        oneDayProdUsage = 0
        oneDayBattCharge = 0

        # This code is not general, for Two days size windows ... 
        tmpFirstLoadCons = np.split(self.loadCons[:-daySize], numberOfDays - 1)
        tmpLastLoadCons = np.split(self.loadCons[daySize:], numberOfDays - 1)
        windowsLoadCons = np.hstack((tmpFirstLoadCons, tmpLastLoadCons))

        tmpFirstLoadProd = np.split(self.loadProd[:-daySize], numberOfDays - 1)
        tmpLastLoadProd = np.split(self.loadProd[daySize:], numberOfDays - 1)
        windowsLoadProd = np.hstack((tmpFirstLoadProd, tmpLastLoadProd))

        tmpFirstPrices = np.split(self.prices[:-daySize], numberOfDays - 1)
        tmpLastPrices = np.split(self.prices[daySize:], numberOfDays - 1)
        windowsPrices = np.hstack((tmpFirstPrices, tmpLastPrices))


        # for idx, (oneDayLoadCons, oneDayLoadProd) in enumerate(zip(np.split(self.loadCons, numberOfDays), np.split(self.loadProd, numberOfDays))):
        for idx, (wLoadCons, wLoadProd, wPrice) in enumerate(zip(windowsLoadCons, windowsLoadProd, windowsPrices)):

            windowLb = [0] * (windowSize * daySize)
            if idx is 0:
                windowUb = [0.01] + [self.batteryCapacity] * ((windowSize * daySize) - 1)
                lastCharge = 0
            else:
                windowUb = [0.01 if self.battCharge[-1] <= 0 else self.battCharge[-1]] + [self.batteryCapacity] * ((windowSize * daySize) - 1)
                lastCharge = self.battCharge[-1]

            windowBattCharge, fopt = ps.pso(strategy.costFuncOnMinPrice,
                                        windowLb,
                                        windowUb,
                                        args=(wLoadCons, wLoadProd, wPrice, lastCharge),
                                        debug=False,
                                        swarmsize=30,
                                        maxiter=100000)
            
            oneDayNewGrid = strategy.newGridEvolution(windowBattCharge[:daySize], wLoadCons[:daySize], wLoadProd[:daySize], lastCharge)
            oneDayProdUsage = strategy.costEvolutionProduction(windowBattCharge[:daySize], wLoadCons[:daySize], wLoadProd[:daySize], lastCharge)
            oneDayBattCharge = windowBattCharge[:daySize]

            self.lb = np.append(self.lb, windowLb[:daySize])
            self.ub = np.append(self.ub, windowUb[:daySize])
            self.newGrid = np.append(self.newGrid, oneDayNewGrid)
            self.prodUsage = np.append(self.prodUsage, oneDayProdUsage)
            self.battCharge = np.append(self.battCharge, oneDayBattCharge)

        self.lb = np.append(self.lb, [0]*daySize) 
        self.ub = np.append(self.ub, [0]*daySize) 
        self.newGrid = np.append(self.newGrid, [0]*daySize) 
        self.prodUsage = np.append(self.prodUsage, [0]*daySize) 
        self.battCharge = np.append(self.battCharge, [0]*daySize)   
        
    def getReport(self):
        updateDict = super().getReport()
        updateDict.update({ "lb": self.lb,
                            "ub": self.ub,
                            # "fopt": self.fopt
                            })
        return updateDict