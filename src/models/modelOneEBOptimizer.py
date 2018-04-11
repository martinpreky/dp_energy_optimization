from models.optimizer import *


class ModelOneEBOptimizer(Optimizer):
    
    def __init__(self, ids, dateTime, loadGrid, loadCons, loadProd):
        super().__init__(ids, dateTime, loadGrid, loadCons, loadProd)
        self.battDischarge = [0] * len(self.loadCons)
    
    def optimize(self):
        for idx, (prod_i, cons_i) in enumerate(zip(self.loadProd, self.loadCons)):

            batt_tmp = self.battCharge[idx-1] + prod_i

            if batt_tmp >= self.batteryCapacity:
                self.battCharge[idx] = self.batteryCapacity
                self.prodUsage[idx] = self.batteryCapacity - self.battCharge[idx-1]
            else:
                self.battCharge[idx] = batt_tmp
                self.prodUsage[idx] = prod_i


            self.newGrid[idx] += max(0, cons_i - self.battCharge[idx])
            self.battDischarge[idx] = min(cons_i, self.battCharge[idx])
            self.battCharge[idx] -= min(cons_i, self.battCharge[idx])

    def getReport(self):
        updateDict = super().getReport()
        updateDict.update({"battDischarge": self.battDischarge})
        return updateDict
    