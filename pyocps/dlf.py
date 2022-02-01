# https://stackoverflow.com/questions/15884527/how-can-i-prevent-the-typeerror-list-indices-must-be-integers-not-tuple-when-c

# https://stackoverflow.com/questions/15884527/how-can-i-prevent-the-typeerror-list-indices-must-be-integers-not-tuple-when-c

import math

import numpy as np

# Function of backward forward load flow


def dlf(Strdata, Loaddata, LoadOffPeak):
    """
    Strdata ->> 1 - from/
                2 - to/
                3 - Length(km)/
                4 - R(ohm/km)/
                5 - X(ohm / km)/
                6 - Imax(Amp)/
                7 - Capacitor (kvar)

    Loaddata->> 1 - bus/
                2 - P(kw)/
                3 - Q(kw)
                
    Parameters:
    -----------
    Strdata: list
    Loaddata:
    LoadOffPeak:
    """
    
    PLoss = np.array([])
    Nsec = np.array(Strdata)[:, 0].size  # Number of sections (or to buses)
    Isec = np.zeros((Nsec, 1))
    Vbase = 23000  # V base of the system (v)
    Isec = np.zeros((Nsec, 1))
    Vbus = Vbase * np.ones((Nsec, 1))
    Cbus = np.zeros((Nsec, 1))
    Sbus = np.zeros((Nsec, 1))
    Rsec = np.zeros((Nsec, 1))
    Xsec = np.zeros((Nsec, 1))
    Zsec = np.zeros((Nsec, 1))
    Rsec = np.array(Strdata)[:, [3]] * np.array(Strdata)[:, [2]]
    Xsec = np.array(Strdata)[:, [4]] * np.array(Strdata)[:, [2]]
    Zsec = np.vectorize(complex)(Rsec, Xsec)

    # * ======================== Init Algorithm =============================== * #

    BI = np.zeros((Nsec, Nsec + 1), int)
    BI[0, 0] = 1
    BV = np.array(BI, complex)

    for k in range(1, Nsec + 1):
        BI2 = np.tri(k, Nsec)
        BV2 = np.tri(k, Nsec)
        BI = np.transpose(BI2)
        BV = BV2 * np.transpose(Zsec[:])

    Cbus = np.array(Strdata)[:, [1]]
    Cbus2 = np.array(Strdata)[:, [6]] * 1000
    Cbus = np.copy(Cbus2)

    Sbus = np.array(Loaddata)[:, [0]]
    Sbus2 = np.vectorize(complex)(
        np.array(Loaddata)[:, [1]], LoadOffPeak[:, [0]]
    )
    Sbus = Sbus2 * 1000
    Iter = 0
    NERROR = 1
    S_bus = Sbus - np.array(Cbus * (Vbus / Vbase) ** 2, complex)
    Ibus = (S_bus / (np.sqrt(3) * Vbus)).conjugate()

    while (Iter <= 100) and (NERROR > np.exp(-6)):
        Iter = +1
        OldIbus = Ibus
        VD = np.sqrt(3) * np.dot(np.dot(BV, BI), Ibus)
        Isec = np.dot(BI, Ibus)
        Vbus = Vbase - VD
        S_bus = Sbus - np.array(
            Cbus * (Vbus / Vbase) ** 2, complex
        )  # for P constant
        Ibus = (S_bus / (np.sqrt(3) * Vbus)).conjugate()
        NERROR = np.max(np.max(abs(Ibus - OldIbus)))

    # * ======================== End Algorithm =============================== * #

    LossSec = 3 * abs(Isec) ** 2.0 * (Rsec) / 1000
    PLoss = np.sum(LossSec)
    Vbus = abs(Vbus) / Vbase  # voltage of to buses

    return PLoss, Vbus, Isec
