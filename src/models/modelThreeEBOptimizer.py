from models.optimizer import *
from price_data import offPeakPrice
import features._price_utils as putils

class ModelThreeEBOptimizer(Optimizer):
    def __init__(self, ids, dateTime, loadGrid, loadCons, loadProd):
        super().__init__(ids, dateTime, loadGrid, loadCons, loadProd)
        self.priceThreshold = offPeakPrice
        self.battDischarge = [0] * len(self.loadCons)
        self.hourlyPrices = putils.get_prices_per_hour(self.dateTime)
    
    def optimize(self):
        for idx, (prod_i, cons_i, price_i) in enumerate(zip(self.loadProd, self.loadCons, self.hourlyPrices)):
            
            batt_tmp = self.battCharge[idx-1] + prod_i
            
            if batt_tmp >= self.batteryCapacity:
                self.battCharge[idx] = self.batteryCapacity
                self.prodUsage[idx] = self.batteryCapacity - self.battCharge[idx-1]
            else:
                self.battCharge[idx] = batt_tmp
                self.prodUsage[idx] = prod_i
            
            
            if (price_i <= self.priceThreshold):
                self.newGrid[idx] += cons_i
            else:
                # Ak je cons vacsia, tak rozdiel sa bere z gridu a baterka ostane vybita
                # Ak je cons mensia, z gridu sa nic neberie, a cons sa odcita od baterky
                # Do battery discharge pridavam to, co z battery charge odcitam. Resp. "Pred" - "Po"
                self.newGrid[idx] += max(0, cons_i - self.battCharge[idx])
                self.battDischarge[idx] = min(cons_i, self.battCharge[idx])
                self.battCharge[idx] -= min(cons_i, self.battCharge[idx])

    def getReport(self):
        updateDict = super().getReport()
        updateDict.update({ "battDischarge": self.battDischarge,
                            "priceThreshold": self.priceThreshold,
                            "hourlyPrices": self.hourlyPrices})
        return updateDict