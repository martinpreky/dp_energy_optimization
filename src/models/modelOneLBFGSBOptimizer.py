import scipy.optimize as opt
import numpy as np
from models.optimizer import *
import features.costFunctionStrategies as strategy

class ModelOneLBFGSBOptimizer(Optimizer):

    def __init__(self, ids, dateTime, loadGrid, loadCons, loadProd):
        super().__init__(ids, dateTime, loadGrid, loadCons, loadProd)
        self.bounds = [(0,0)] + [(0,self.batteryCapacity)] * (len(self.loadCons) - 1)
        self.RESULT = ""
    
    def optimize(self):
    
    

        self.RESULT = opt.minimize(  strategy.costFuncOnMinE,
                                np.repeat(0, len(self.loadCons)), 
                                args=(self.loadCons, self.loadProd),
                                bounds = self.bounds, 
                                method = 'L-BFGS-B',
                                options = {'disp': False, 'maxiter': 15000, 'maxfun': 3000000})
        
        self.newGrid = strategy.newGridEvolution(self.RESULT.x, self.loadCons, self.loadProd)
        self.prodUsage = strategy.costEvolutionProduction(self.RESULT.x, self.loadCons, self.loadProd)
        self.battCharge = self.RESULT.x

        #  price_grid = putils.get_cost_per_hour(price, new_grid)

    def getReport(self):
        updateDict = super().getReport()
        updateDict.update({ "bounds": self.bounds,
                            "RESULT.fun": self.RESULT.fun,
                            "RESULT.success": self.RESULT.success,
                            "RESULT.message": self.RESULT.message,
                            "RESULT.nfev": self.RESULT.nfev,
                            "RESULT.nit": self.RESULT.nit})
        return updateDict
