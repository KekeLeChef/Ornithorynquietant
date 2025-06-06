import matplotlot.pyplot as plt

sigma = 5.67e-8  # W/m^2/K^4
S = 141646 * 10**6 #m^2

def change_temp_nuit(Ti, Pa, Cp, dt):
    dT = (1/Cp * (-sigma*S)*(Ti**4)+Pa*S)*dt
    return dT

def change_temp_jour(Ti, Pa, Cp, Ps, dt):
    dT = (1/Cp * (-sigma*S)*(Ti**4)+Pa*S+Ps*S)*dt
    return dT


























