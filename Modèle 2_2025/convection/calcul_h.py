"""

Ce programme permet de calculer le coefficient de convection h dans la formule du flux thermique convectif

"""

def calcul_h(T_sol, T_air) :
    lam = 0.026 # en W / (m.K), la conductivité thermique de l'air
    Lc = 0.05 # en m, la longueur caractéristique correspondant à notre situation


    n = 1/4
    if T_sol >= T_air :
        C = 0.54
    else :
        C = 0.27


    g = 9.81 # en m / s**2, la constante de gravité
    nu = 1.5e-5 # en m**2 / s, viscosité cinématique de l'air
    alpha = 2e-5 # en m**2 / s, diffusivité thermique de l'air
    beta = 1 / T_air

    Gr = (g * beta * (T_sol - T_air) * Lc**3) / nu**2 # nombre de Grashof

    Pr = nu / alpha # nombre de Prandtl

    Ra = Gr * Pr # nombre de Rayleigh

    Nu = C * abs(Ra)**(1/4)

    h = Nu * lam / Lc # par def du nombre de Nusselt

    print(h)
    return h


#exemple d'utilisation de la fonction
T_sol = 290
T_air = 300
calcul_h(T_sol, T_air)
