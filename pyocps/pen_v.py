import numpy as np

# Function of penalizing infeasible solutions

VLoadMax = 1.1  # Upper voltage bound
VLoadMin = 0.9  # Lower voltage bound
PF = 5000  # Penalty factor


def penv(Vbus):
    global VLoadMax, VLoadMin, PF
    Penalty = np.array([])
    for i in range(1, np.size(Vbus, axis=0)):
        if (Vbus[i - 1] > VLoadMax) or (Vbus[i - 1] < VLoadMin):
            Penalty[i] = PF
        else:
            Penalty[i] = 0
    PenaltyVoltage = sum(Penalty)

    return PenaltyVoltage
