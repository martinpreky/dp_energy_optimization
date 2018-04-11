import pyswarm as ps
from models.optimizer import *
import features.costFunctionStrategies as strategy

class ModelOnePSOOptimizer(Optimizer):

    def __init__(self, ids, dateTime, loadGrid, loadCons, loadProd):
        super().__init__(ids, dateTime, loadGrid, loadCons, loadProd)
        self.lb = [0] * len(self.loadCons)
        self.ub = [0.01] + [self.batteryCapacity] * (len(self.loadCons) - 1)
        self.fopt = 0
    
    def optimize(self):

        self.battCharge, self.fopt = ps.pso(strategy.costFuncOnMinE,
                                    self.lb,
                                    self.ub,
                                    args=(self.loadCons, self.loadProd),
                                    debug=False,
                                    swarmsize=2000,
                                    maxiter=100000)
        
        self.newGrid = strategy.newGridEvolution(self.battCharge, self.loadCons, self.loadProd)
        self.prodUsage = strategy.costEvolutionProduction(self.battCharge, self.loadCons, self.loadProd)
        
        #  price_grid = putils.get_cost_per_hour(price, new_grid)
        
    def getReport(self):
        updateDict = super().getReport()
        updateDict.update({ "lb": self.lb,
                            "ub": self.ub,
                            "fopt": self.fopt})
        return updateDict