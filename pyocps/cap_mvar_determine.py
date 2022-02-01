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

# Function of allocating MVAr to the generated population
def cap_mvar_determine(p, Cap_MVar, NBus):
    pop = np.zeros((100,NBus-1), int)
    for i in range(len(p)):
        pop_row = p[i]
        pop_row_MVar = np.zeros((1, NBus - 1), int)
        for j in range(0,NBus-1):
            pop_row_MVar[0,j] = Cap_MVar[pop_row[j]-1] 
        pop[i, :] = pop_row_MVar[0]
    return pop
