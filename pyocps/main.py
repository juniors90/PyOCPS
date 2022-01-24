#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the
# PyOCPS Project (https://github.com/juniors90/PyOCPS/).
# Copyright (c) 2022, Ferreira Juan David
# License: MIT
# Full Text: https://github.com/juniors90/PyOCPS/blob/master/LICENSE

# =============================================================================
# DOCS
# =============================================================================

"""PyOCPS.
Implementation of Optimal Capacitor Placement and Sizing
in Distribution Networks using Python.
"""

# =============================================================================
# IMPORTS
# =============================================================================


## Mirate main.m to main.py

import time

from matplotlib.figure import Figure

import numpy as np

from .define_parameters import (
    No_Cap_Type,
    NBus,
    No_pop,
    Iter,
    Cap_Price,
    Ke,
    Loaddata,
    Strdata,
    T_OffPeak,
    T_Medium,
    T_Peak,
    NLoadLevel,
    Kp,
)
from .cap_mvar_determine import cap_mvar_determine
from .dlf import dlf
from .pen_v import pen_v
from .update_solutions import update_solutions

# Main mfile should be run

tic = time.time()  # Comienza a contar el tiempo

PLoss = np.zeros((No_pop, 1), float)
f = np.zeros((No_pop, 1), float)
LoadDataBase = np.array(Loaddata)[:, 2]
LoadOffPeak = 0.3 * np.array(LoadDataBase)
LoadMedium = 0.6 * np.array(LoadDataBase)
LoadPeak = np.array(LoadDataBase)
np.array(Loaddata)[:, 2] = np.array(LoadOffPeak)

## Evaluating Initial conditions

PLossOutOffPeak0, VbusOutOffPeak0, IsecOut0 = dlf(Strdata, Loaddata)
np.array(Loaddata)[:, 2] = LoadMedium
PLossOutMedium0, VbusOutMedium0, IsecOut0 = dlf(Strdata, Loaddata)
np.array(Loaddata)[:, 2] = LoadPeak
PLossOutPeak0, VbusOutPeak0, Isec0 = dlf(Strdata, Loaddata)
EnergyLossIni = (
    T_OffPeak * PLossOutOffPeak0
    + T_Medium * PLossOutMedium0
    + T_Peak * PLossOutPeak0
)
np.array(Loaddata)[:, 2] = LoadDataBase

#

p = np.ceil(
    np.random.random(No_pop, NBus - 1) * No_Cap_Type
)  # * Initial popoulation
pop = cap_mvar_determine(p)  # * Allocation MVAr to the generated population
Load = np.array([])
PenaltyVoltageL = np.array([])
PenaltyVoltage = np.array([])

for i in range(1, np.size(p, axis=0) + 1):
    np.array(pop)[i, :] = cap_mvar_determine(p[i, :])
    np.array(Load)[:, 0] = (
        LoadOffPeak - (np.array(pop)[i, :]).conj().transpose()
    )
    np.array(Load)[:, 1] = (
        LoadMedium - (np.array(pop)[i, :]).conj().transpose()
    )
    np.array(Load)[:, 2] = LoadPeak - (np.array(pop)[i, :]).conj().transpose()
    Total_Cap_Price = sum(Cap_Price(p[i, :]))

    Isec = np.array([])
    for il in range(1, NLoadLevel + 1):
        np.array(Loaddata)[:, 2] = np.array(Load)[:, il - 1]
        PLoss[i, il], Vbus, Isec[i, il, :] = dlf(
            Strdata, Loaddata
        )  # Running load flow
        PenaltyVoltageL[i - 1, il - 1] = pen_v(
            Vbus
        )  # Calculating amount of penalties

    PenaltyVoltage[i] = sum(PenaltyVoltageL[i, :], 1)
    f[i] = (
        Ke
        * (
            T_OffPeak * PLoss[i, 1]
            + T_Medium * PLoss[i, 2]
            + T_Peak * PLoss[i, 3]
        )
        + Kp * PLoss[i, 1]
        + Total_Cap_Price
    )  # Calculating objective function
    f[i] = f[i] + PenaltyVoltage[i]

PBest = p
PBestValue = f
GTeacherValue, index = min(f)
GTeacher = PBest[index, :]  # # # The best solution
Xmean = np.mean(p)

fff = np.array([])

for k in range(1, Iter + 1):
    f, p, GTeacher, GTeacherValue, Xmean, PenaltyVoltage, PenaltyVoltageBest = update_solutions(GTeacher, p, Xmean, f, PenaltyVoltage, LoadOffPeak, LoadMedium, LoadPeak)
    ## Generating new solutions
    fff[k - 1] = GTeacherValue

toc = time.time()  # Termina de contar el tiempo

ij = np.arahe(1, Iter + 1)

fig = Figure()
ax = fig.subplots()
ax.plot(ij, fff)
