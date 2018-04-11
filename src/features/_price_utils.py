import numpy as np
import price_data as pd


dayByHours = list(range(24))

def graph_price_during_day(ax, price_data, c='k', label='Price'):
    ax.plot(dayByHours, price_data, c=c, label=label)
    ax.set_ylim(0, 0.1)
    ax.set_xticks(dayByHours)

    ax.set_title(label)    
    ax.set_xlabel('Day')
    ax.set_ylabel('Dollar')


def get_prices_per_hour(daysByHours):
    hour_prices = []
    for day in daysByHours[::24]:
        if 6 <= day.month and day.month <= 9:
            if day.weekday() == 5 or day.weekday() == 6:
                hour_prices += pd.dayWeekendSummer
            else:
                hour_prices += pd.dayWeekSummer
        else:
            hour_prices += pd.dayNonSummer
    
    return hour_prices
    

def get_cost_per_hour(hour_prices, hour_kw):
    hour_prices = np.array(hour_prices)
    hour_kw = np.array(list(map(lambda x: max(0, x), hour_kw)))

    return hour_prices * hour_kw