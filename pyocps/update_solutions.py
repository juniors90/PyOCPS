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

import numpy as np

from .define_parameters import (
    Cap_Price,
    Ke,
    Kp,
    Strdata,
    Loaddata,
    T_OffPeak,
    T_Medium,
    T_Peak,
    NLoadLevel,
    No_Cap_Type,
)
from .cap_mvar_determine import cap_mvar_determine
from .dlf import dlf
from .pen_v import pen_v

## Mirate UpdateSolutions.m to update_solutions.py

## Function of updating solutions

def update_solutions(
    GTeacher, p, Xmean, f, PenaltyVoltage, LoadOffPeak, LoadMedium, LoadPeak
):
    global Cap_Price, Ke, Kp, Strdata, Loaddata, T_OffPeak, T_Medium, T_Peak, NLoadLevel, No_Cap_Type
    # # # # # # # # # # # # # # # Teacher phase # # # # # # # # # # # # # # #
    rand = 0
    PLoss = np.array([])
    PenaltyVoltageL = np.array([])
    Nsec = np.array(Strdata)[:, 0].size  # Number of sections (or to buses)
    Isec = np.zeros((Nsec, 1), float)
    pnew = np.array([])
    fnew = np.array([])
    pop = cap_mvar_determine(pnew)
    PenaltyVoltageNew = np.array([])
    PenaltyVoltage = np.array([])
    for i in (1, np.size(p, axis=0) + 1):

        TF = round(1 + rand)
        pnew[i - 1, :] = p[i - 1, :] + np.random.random(1, np.size(p, axis=1) * (GTeacher - TF * Xmean))
        pnew[i - 1, :] = round(pnew[i - 1, :])
        for k in (1, np.size(p, axis=1) + 1):
            if pnew[i - 1, k - 1] > No_Cap_Type:
                pnew[i - 1, k - 1] = No_Cap_Type
            elif pnew[i - 1, k - 1] < 1:
                pnew[i - 1, k - 1] = 1

        pop[i, :] = cap_mvar_determine(pnew[i, :])
        Load = np.array([])
        Load[:, 0] = LoadOffPeak - pop[i, :][:, np.newaxis]
        Load[:, 1] = LoadMedium - pop[i, :][:, np.newaxis]
        Load[:, 2] = LoadPeak - pop[i, :][:, np.newaxis]
        Total_Cap_Price = sum(Cap_Price[pnew[i, :]])

        for il in range(1, NLoadLevel + 1):
            Loaddata[:, 2] = Load[:, il - 1]
            PLoss[i - 1, il - 1], Vbus, Isec[i - 1, il - 1, :] = dlf(Strdata, Loaddata)
            PenaltyVoltageL[i - 1, il - 1] = pen_v(Vbus)

        PenaltyVoltageNew[i] = sum(PenaltyVoltageL[i, :], 2)
        fnew[i] = Ke * (T_OffPeak * PLoss[i, 0] + T_Medium * PLoss[i, 1] + T_Peak * PLoss[i, 2]) + Kp * PLoss(i, 1) + Total_Cap_Price
        fnew[i] = fnew[i] + PenaltyVoltageNew[i]

        if fnew[i] < f[i]:
            p[i, :] = pnew[i, :]
            f[i] = fnew[i]
            PenaltyVoltage[i] = PenaltyVoltageNew[i]

        # # # # # # # # # # # Student phase # # # # # # # # # # # # # # # # # # # # #

        j = round(1 + rand * (i - 1))

        if j != i:
            if f[i] < f[j]:
                pnew[i - 1, :] = p[i - 1, :] + np.random.random(1, np.size(p, axis=1)) * (p[i - 1, :] - p[j - 1, :])
            else:
                pnew[i - 1, :] = p[i - 1, :] + np.random.random(1, np.size(p, axis=1)) * (p[j - 1, :] - p[i - 1, :])

            pnew[i - 1, :] = round(pnew[i - 1, :])

            for k in range(1, np.size(p, axis=1)):
                if pnew[i - 1, k - 1] > No_Cap_Type:
                    pnew[i - 1, k - 1] = No_Cap_Type
                elif pnew[i - 1, k - 1] < 1:
                    pnew[i - 1, k - 1] = 1

            pop[i - 1, :] = cap_mvar_determine(pnew[i - 1, :])
            Load[:, 0] = LoadOffPeak - pop[i - 1, :][:, np.newaxis]
            Load[:, 1] = LoadMedium - pop[i - 1, :][:, np.newaxis]
            Load[:, 2] = LoadPeak - pop[i - 1, :][:, np.newaxis]
            Total_Cap_Price = sum(Cap_Price((pnew[i - 1, :])))

            for il in range(1, NLoadLevel + 1):
                Loaddata[:, 2] = Load[:, il - 1]
                PLoss[i - 1, il - 1], Vbus, Isec[i - 1, il - 1, :] = dlf(Strdata, Loaddata)
                PenaltyVoltageL[i - 1, il - 1] = pen_v(Vbus)

            PenaltyVoltageNew[i] = sum(PenaltyVoltageL[i - 1, :], 2)
            fnew[i] = Ke * (T_OffPeak * PLoss(i, 1) + T_Medium * PLoss(i, 2) + T_Peak * PLoss(i, 3)) + Kp * PLoss(i, 1) + Total_Cap_Price
            fnew[i] = fnew[i] + PenaltyVoltageNew[i]

            if fnew[i] < f[i]:
                p[i, :] = pnew[i, :]
                f[i] = fnew[i]
                PenaltyVoltage[i] = PenaltyVoltageNew[i]

    GTeacherValue, index = min(f)
    GTeacher = p[index, :]
    PenaltyVoltageBest = PenaltyVoltage[index]
    Xmean = p.mean(axis=0)
    return f, p, GTeacher, GTeacherValue, Xmean, PenaltyVoltage, PenaltyVoltageBest
