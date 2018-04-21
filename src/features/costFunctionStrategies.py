import numpy as np

def costFuncOnMinE(X, CONS, PROD, lastCharge):
    batt_diff = np.insert(np.diff(X), 0, X[0] - lastCharge)
    return sum(np.array(CONS + batt_diff - PROD).clip(0,100))

def costFuncOnMinEDiff(X, CONS, PROD, lastCharge, lastGrid):
    batt_diff = np.insert(np.diff(X), 0, X[0] - lastCharge)
    grid = np.array(CONS + batt_diff - PROD) #.clip(0,100)
    grid_diff = np.insert(np.diff(grid), 0, grid[0] - lastGrid)
    return sum(np.abs(grid_diff))

def costFuncOnMinPrice(X, CONS, PROD, PRICE, lastCharge):
    batt_diff = np.insert(np.diff(X), 0, X[0] - lastCharge)
    return sum(np.array(CONS + batt_diff - PROD).clip(0,100) * PRICE)

def newGridEvolution(X, CONS, PROD, lastCharge):
    batt_diff = np.insert(np.diff(X), 0, X[0] - lastCharge)
    return np.array(CONS + batt_diff - PROD).clip(0,100)

def costEvolutionProduction(X, CONS, PROD, lastCharge):
    # batt_diff = np.insert(np.diff(X), 0, 0).clip(0, 100)
    # return PROD - (PROD - (CONS + batt_diff)).clip(0,100)
    batt_diff = np.insert(np.diff(X), 0,  X[0] - lastCharge)
    load = np.array(CONS + batt_diff)
    return np.where(load >= PROD, PROD, load).clip(0, 100)