import price_utils as putils
import datetime as datetime
from scipy.optimize import minimize
import numpy as np

def calc_greedy_price_optim(x_time, cons, prod, battery_capacity=float("inf"), price_treshold = 1):
    # Normalizovanie prod na 0 alebo kladne
    prod = list(map(lambda x: max(0, x), prod))
    grid = [0] * len(cons)
    batt_charge = [0] * len(cons)
    batt_discharge = [0] * len(cons)
    hour_prices = putils.get_prices_per_hour(x_time)
    
    for idx, (prod_i, cons_i, price_i) in enumerate(zip(prod, cons, hour_prices)):
        # Do baterky dam predoslu hodnotu + produkciu
        batt_charge[idx] = batt_charge[idx-1] + prod_i
        # Bateria nebude viac nabita ako jej kapacita
        batt_charge[idx] = min(batt_charge[idx], battery_capacity)   
        
        # print("{0:2d}. cons: {1:.2f}    prod: {2:.2f}".format(idx, cons_i, prod_i))
        # print("V baterke pred: {0:.2f}".format(batt_charge[idx]))

        if (price_i <= price_treshold):
            grid[idx] += cons_i
        else:
            # Ak je cons vacsia, tak rozdiel sa bere z gridu a baterka ostane vybita
            # Ak je cons mensia, z gridu sa nic neberie, a cons sa odcita od baterky
            # Do battery discharge pridavam to, co z battery charge odcitam. Resp. "Pred" - "Po"
            grid[idx] += max(0, cons_i - batt_charge[idx])
            batt_discharge[idx] = min(cons_i, batt_charge[idx])
            batt_charge[idx] -= min(cons_i, batt_charge[idx])


        # print("V baterke po: {0:.2f}".format(batt_charge[idx]))
        # print("Z gridu: {0:.2f}".format(grid[idx]))
    
    return (grid, batt_charge, batt_discharge)



def calc_alg_batt_usage(x_time, cons, prod, battery_capacity=float("inf")):
    prices = np.array(putils.get_prices_per_hour(x_time))

    # Normalizovanie prod na 0 alebo kladne
    prod = list(map(lambda x: max(0, x), prod))

    def f(x):
        batt_charge = [0] * len(x)
        grid = [0] * len(x)
        for idx,w in enumerate(x):
            batt_charge[idx] = batt_charge[idx-1] + prod[idx]
            batt_charge[idx] = min(battery_capacity, batt_charge[idx])
            
            # Pozor: tu w udava kolko ma ostat, cize rozdiel = kolko odislo
            pred = batt_charge[idx]
            po = batt_charge[idx] * w

            z_baterie = pred - po

            grid[idx] += max(0, cons[idx] - z_baterie)
            batt_charge[idx] = po

        return sum(grid*prices)

    x0 = np.array([1] * len(prod))

    res = minimize(f, x0, method='L-BFGS-B',  options={'xtol': 1e-8, 'disp': True, 'maxiter':5000})
    return res.x

