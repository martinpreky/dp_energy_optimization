offPeakPrice = off = 0.00493
midPeakPrice = mid = 0.05040
onPeakPrice  = on  = 0.09761 

# Summer - June - September     6 - 9
#Non-Summer - October - May     10 - 5

dayWeekSummer = [
    off, off, off, off, off, off, off,      # 00 - 06 #7
    mid, mid, mid, mid, mid, mid, mid, mid, # 06 - 14 #8
    on, on, on, on, on, on,                 # 14 - 20 #6
    mid, mid,                               # 20 - 22 #2
    off                                     # 22 - 23 #1 
]

dayNonSummer = dayWeekendSummer = [
    off, off, off, off, off, off, off,      # 00 - 06 #7
    mid, mid, mid, mid, mid, mid, mid, mid, 
    mid, mid, mid, mid, mid, mid, mid, mid, # 06 - 22 #16
    off                                     # 22 - 23 #1
]