import scipy.optimize as opt
import numpy as np
from models.optimizer import *
import features.costFunctionStrategies as strategy

class ModelTwoLBFGSBOptimizer(Optimizer):

    def __init__(self, ids, dateTime, loadGrid, loadCons, loadProd):
        super().__init__(ids, dateTime, loadGrid, loadCons, loadProd)
        self.RESULT = ""
        self.bounds = np.array([]) #[(0,0)] + [(0,self.batteryCapacity)] * (len(self.loadCons) - 1)
        self.newGrid = np.array([])
        self.prodUsage = np.array([])
        self.battCharge = np.array([])
    
    def optimize(self):
    
        numberOfDays = int (len(self.dateTime) / 24)
        oneDayBounds = 0
        oneDayNewGrid = 0
        oneDayProdUsage = 0
        oneDayBattCharge = 0

        for idx, (oneDayLoadCons, oneDayLoadProd) in enumerate(zip(np.split(self.loadCons, numberOfDays), np.split(self.loadProd, numberOfDays))):

            if idx is 0:
                oneDayBounds = [(0,0)] + [(0,self.batteryCapacity)] * 23
            else:
                oneDayBounds = [(0, self.battCharge[-1])] + [(0,self.batteryCapacity)] * 23

            RESULT = opt.minimize(  strategy.costFuncOnMinEDiff,
                                    np.repeat(0, 24), 
                                    args=(oneDayLoadCons, oneDayLoadProd),
                                    bounds = oneDayBounds, 
                                    method = 'L-BFGS-B',
                                    options = {'disp': False, 'maxiter': 15000, 'maxfun': 3000000})
            
            oneDayNewGrid = strategy.newGridEvolution(RESULT.x, oneDayLoadCons, oneDayLoadProd)
            oneDayProdUsage = strategy.costEvolutionProduction(RESULT.x, oneDayLoadCons, oneDayLoadProd)
            oneDayBattCharge = RESULT.x
        
            if len(self.bounds) is 0:
                self.bounds = oneDayBounds
            else:
                self.bounds = np.append(self.bounds, oneDayBounds, axis=0)
            self.newGrid = np.append(self.newGrid, oneDayNewGrid)
            self.prodUsage = np.append(self.prodUsage, oneDayProdUsage)
            self.battCharge = np.append(self.battCharge, oneDayBattCharge)


    def getReport(self):
        updateDict = super().getReport()
        lb = self.bounds[:,0]
        ub = self.bounds[:,1]
        updateDict.update({ "lb": lb,
                            "ub": ub
                            # "RESULT.fun": self.RESULT.fun,
                            # "RESULT.success": self.RESULT.success,
                            # "RESULT.message": self.RESULT.message,
                            # "RESULT.nfev": self.RESULT.nfev,
                            # "RESULT.nit": self.RESULT.nit
                            })
        return updateDict