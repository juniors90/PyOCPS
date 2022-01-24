# https://stackoverflow.com/questions/15884527/how-can-i-prevent-the-typeerror-list-indices-must-be-integers-not-tuple-when-c

# https://stackoverflow.com/questions/15884527/how-can-i-prevent-the-typeerror-list-indices-must-be-integers-not-tuple-when-c

import math

import numpy as np

# Function of backward forward load flow


def dlf(Strdata, Loaddata):
    """
    Strdata->> 1 - from/
               2 - to/
               3 - Length(km)/
               4 - R(ohm/km)/
               5 - X(ohm / km)/
               6 - Imax(Amp)/
               7 - Capacitor (kvar)
    Loaddata->> 1 - bus/
                2 - P(kw)/
                3 - Q(kw)
    """
    PLoss = np.array([])
    Nsec = np.array(Strdata)[:, 0].size  # Number of sections (or to buses)
    Vbase = 23000  # V base of the system (v)
    Isec = np.zeros((Nsec, 1), float)
    Vbus = Vbase * np.ones((Nsec, 1), float)
    Cbus = np.zeros((Nsec, 1), float)
    Sbus = np.zeros((Nsec, 1), float)
    Rsec = np.array(Strdata)[:, 3] * np.array(Strdata)[:, 2]
    Xsec = np.array(Strdata)[:, 4] * np.array(Strdata)[:, 2]
    Zsec = Rsec + 1j * Xsec

    # * ======================== Init Algorithm =============================== #

    BI = np.zeros((Nsec, Nsec + 1), float)
    BI[0, 0] = 1
    BV = BI
    for k in range(1, Nsec - 1):
        np.array(BI)[:, np.array(Strdata, int)[k, 2]] = np.array(BI)[:, np.array(Strdata, int)[k, 1]]
        np.array(BI)[k, np.array(Strdata, int)[k, 2]] = 1
        np.array(BV)[:, np.array(Strdata, int)[k, 2]] = np.array(BV)[:, np.array(Strdata, int)[k, 1]]
        np.array(BV, dtype="complex_")[k, np.array(Strdata, int)[k, 2]] = Zsec[k - 1]

    BI[:, 0] = []
    BV[:, 0] = []
    BV = BV.transpose()
    Cbus[np.array(Strdata)[:, 2]] = np.array(Strdata)[:, 7] * 1000
    Sbus[np.array(Loaddata)[:, 1]] = (np.array(Loaddata)[:, 2] + 1j * np.array(Loaddata)[:, 3]) * 100
    Cbus[0, :] = []
    Sbus[0, :] = []
    Iter = 0

    NERROR = 1
    # for P constant
    S_bus = Sbus - 1j * (Cbus * (Vbus / Vbase)**2) # for P constan
    Ibus = np.conj(S_bus / (np.sqrt(3) * Vbus))

    while (Iter < 100) and (NERROR > math.exp(-5)):
        Iter = Iter + 1
        OldIbus = Ibus
        VD = np.sqrt(3) * (BV * BI) * Ibus
        Isec = BI * Ibus
        Vbus = Vbase - VD
        # for P constant
        S_bus = Sbus - 1j * (Cbus * (Vbus / Vbase)**2) # for P constant
        Ibus = (S_bus / (np.sqrt(3) * Vbus)).conjugate()
        NERROR = max(max(abs(Ibus - OldIbus)))

    # * ======================== End Algorithm =============================== #

    LossSec = 3 * abs(Isec) ** 2 * (Rsec) / 1000
    PLoss = sum(LossSec)
    Vbus = abs(Vbus) / Vbase  # voltage of to buses

    return PLoss, Vbus, Isec
