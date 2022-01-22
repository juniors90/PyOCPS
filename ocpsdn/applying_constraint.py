from typing import List

import numpy as np

No_Cap_Type = 7


def applying_constraint(p: List) -> List:
    global No_Cap_Type
    for i in range(1, np.size(p, axis=0)):
        for j in np.size(1, np.size(p, axis=1)):
            if p[i, j] > No_Cap_Type:
                p[i, j] = No_Cap_Type
            elif p[i, j] < 1:
                p[i, j] = 1
            else:
                p[i, j] = p[i, j]
    return p
