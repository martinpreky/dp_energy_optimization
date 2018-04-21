from matplotlib import pyplot as plt
import features._price_utils as putils

class Optimizer():

    def __init__(self, ids, dateTime, loadGrid, loadCons, loadProd):
        self.id = ids
        self.dateTime = dateTime
        self.loadGrid = loadGrid
        self.loadCons = loadCons
        self.loadProd = loadProd.clip(0, 100) # list(map(lambda x: max(0, x), []))

        self.prices = putils.get_prices_per_hour(dateTime)

        self.newGrid = [0] * len(self.loadCons)
        self.battCharge = [0] * len(self.loadCons)
        self.prodUsage = [0] * len(self.loadCons)

        self.batteryCapacity = 13.5
    
    def optimize(self):
        pass
    
    def defineDataAttrs(self, houseName, numberOfDays, sinceDay):
        self.houseName = houseName
        self.numberOfDays = numberOfDays
        self.sinceDay = sinceDay
    
    def getCsvName(self):
        return  str(self.houseName + 
                    "_" + 
                    self.__class__.__name__ + 
                    "_" + 
                    str(self.sinceDay) + 
                    "_" + 
                    str(self.numberOfDays) + 
                    ".csv")
        
    def getReport(self):
        return {"id": self.id,
                "dateTime": self.dateTime,
                "loadGrid": self.loadGrid,
                "loadProd": self.loadProd,
                "loadCons": self.loadCons,

                "newGrid": self.newGrid,
                "battCharge": self.battCharge,
                "prodUsage": self.prodUsage,

                "prices": self.prices,

                "batteryCapacity": self.batteryCapacity}
    
    def showPlot(self):
        plt.clf()
        # plt.plot(self.dateTime, self.loadGrid, c='b', label='Load Grid')
        plt.plot(self.dateTime, self.loadProd, c='g', label='Load Prod')
        plt.plot(self.dateTime, self.loadCons, c='r', ls='dashed', label='Load Cons')

        plt.plot(self.dateTime, self.battCharge, c='y', label='Battery Charge')
        plt.plot(self.dateTime, self.prodUsage, c='k', ls='dotted', label="Production Usage")
        plt.plot(self.dateTime, self.newGrid, c='m', label='Load New Grid')

        plt.legend()
        plt.tight_layout()
        plt.show()
    