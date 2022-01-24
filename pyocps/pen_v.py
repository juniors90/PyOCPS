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

# Function of penalizing infeasible solutions

VLoadMax = 1.1  # Upper voltage bound
VLoadMin = 0.9  # Lower voltage bound
PF = 5000  # Penalty factor


def pen_v(Vbus):
    global VLoadMax, VLoadMin, PF
    penalty = np.array([])
    for i in range(1, np.size(Vbus, axis=0)):
        if (Vbus[i - 1] > VLoadMax) or (Vbus[i - 1] < VLoadMin):
            penalty[i] = PF
        else:
            penalty[i] = 0
    PenaltyVoltage = sum(penalty)

    return PenaltyVoltage
