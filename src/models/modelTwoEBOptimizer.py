from models.optimizer import *

class ModelTwoEBOptimizer(Optimizer):
    def __init__(self, ids, dateTime, loadGrid, loadCons, loadProd):
        super().__init__(ids, dateTime, loadGrid, loadCons, loadProd)
        self.battDischarge = [0] * len(self.loadCons)
        self.gridThreshold = 1.5
    
    def optimize(self):
        for idx, (prod_i, cons_i) in enumerate(zip(self.loadProd, self.loadCons)):
            
            batt_tmp = self.battCharge[idx-1] + prod_i

            if batt_tmp >= self.batteryCapacity:
                self.battCharge[idx] = self.batteryCapacity
                self.prodUsage[idx] = self.batteryCapacity - self.battCharge[idx-1]
            else:
                self.battCharge[idx] = batt_tmp
                self.prodUsage[idx] = prod_i


            if cons_i > self.gridThreshold:
                self.newGrid[idx] = self.gridThreshold
                self.battCharge[idx] -= max(0, cons_i - self.gridThreshold)

                #??                
                self.battDischarge[idx] += max(0, cons_i - self.gridThreshold)
                self.battDischarge[idx] += min(0, self.battCharge[idx])

                self.newGrid[idx] -= min(0, self.battCharge[idx])
                self.battCharge[idx] = max(0, self.battCharge[idx]) 
            else:
                self.newGrid[idx] = cons_i
            
            
    def getReport(self):
        updateDict = super().getReport()
        updateDict.update({ "battDischarge": self.battDischarge,
                            "gridThreshold": self.gridThreshold})
        return updateDict
