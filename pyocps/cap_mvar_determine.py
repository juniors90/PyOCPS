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

# Function of allocating MVAr to the generated population
import numpy as np

from .define_parameters import Cap_MVar, NBus

# Function of allocating MVAr to the generated population
def cap_mvar_determine(p):
    global Cap_MVar, NBus
    pop = np.array([])
    for i in range(1, np.size(p, axis=0) + 1):
        pop_row = p[i - 1, :]
        pop_row_MVar = np.zeros((1, NBus - 1), float)
        for j in range(1, NBus):
            pop_row_MVar[j - 1] = Cap_MVar[pop_row[j - 1]]
        pop[i - 1, :] = pop_row_MVar
    return pop
