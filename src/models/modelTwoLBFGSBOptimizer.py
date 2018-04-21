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
    
        windowSize = 2
        daySize = 24
    
        numberOfDays = int (len(self.dateTime) / daySize)
        windowBounds = 0
        
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


        # for idx, (wLoadCons, wLoadProd) in enumerate(zip(np.split(self.loadCons, numberOfDays), np.split(self.loadProd, numberOfDays))):

        for idx, (wLoadCons, wLoadProd) in enumerate(zip(windowsLoadCons, windowsLoadProd)):

            if idx is 0:
                windowBounds = [(0,0)] + [(0,self.batteryCapacity)] * ((windowSize * daySize) - 1)
                lastCharge = 0
                lastGrid = 0
            else:
                windowBounds = [(0, self.battCharge[-1])] + [(0,self.batteryCapacity)] * ((windowSize * daySize) - 1)
                lastCharge = self.battCharge[-1]
                lastGrid = self.newGrid[-1]

            RESULT = opt.minimize(  strategy.costFuncOnMinEDiff,
                                    np.repeat(0, (windowSize * daySize)), 
                                    args=(wLoadCons, wLoadProd, lastCharge, lastGrid),
                                    bounds = windowBounds, 
                                    method = 'L-BFGS-B',
                                    options = {'disp': False, 'maxiter': 15000, 'maxfun': 3000000})
            
            oneDayNewGrid = strategy.newGridEvolution(RESULT.x[:daySize], wLoadCons[:daySize], wLoadProd[:daySize], lastCharge)
            oneDayProdUsage = strategy.costEvolutionProduction(RESULT.x[:daySize], wLoadCons[:daySize], wLoadProd[:daySize], lastCharge)
            oneDayBattCharge = RESULT.x[:daySize]
        
            if len(self.bounds) is 0:
                self.bounds = windowBounds[:daySize]
            else:
                self.bounds = np.append(self.bounds, windowBounds[:daySize], axis=0)
            self.newGrid = np.append(self.newGrid, oneDayNewGrid)
            self.prodUsage = np.append(self.prodUsage, oneDayProdUsage)
            self.battCharge = np.append(self.battCharge, oneDayBattCharge)
        
        # By Sliding Window we are one day short, appending zeros to be equal with other arrays lengths
        self.bounds = np.append(self.bounds, [(0,0)]*daySize, axis=0) 
        self.newGrid = np.append(self.newGrid, [0]*daySize) 
        self.prodUsage = np.append(self.prodUsage, [0]*daySize) 
        self.battCharge = np.append(self.battCharge, [0]*daySize) 


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