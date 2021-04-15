import numpy as np

# =============================================================================
# NEGATIVIZE
# flipping over the stride (usually 4 to 3 --> thirds to sixths) 
# and rotating the lydian bunch between dominant and tonic yields lovely results
# 'negative' makes a lot of sense here.
# =============================================================================

def negativize(a_kpdve):
    k = (a_kpdve[0] + 9) % 12
    p = 3 if a_kpdve[2] == 2 else 0
    d = 7 - a_kpdve[2]
    v = 7 - a_kpdve[3]
    e = a_kpdve[4]

    return np.array([k,p,d,v,e])