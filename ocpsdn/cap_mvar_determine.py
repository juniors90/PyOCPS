# Function of allocating MVAr to the generated population
from tkinter.tix import PopupMenu
import numpy as np

No_Cap_Type = 7  # Number of capacitor types
Cap_MVar = 4 * np.array([0, 150, 300, 450, 600, 900, 1200])
#            Bus   P    Q
Loaddata = [
    [2, 1840, 460],
    [3, 980, 340],
    [4, 1790, 446],
    [5, 1598, 1840],
    [6, 1610, 600],
    [7, 780, 110],
    [8, 1150, 60],
    [9, 980, 130],
    [10, 1640, 200],
]
NBus = len(Loaddata) + 1  # Number of buses

# Function of allocating MVAr to the generated population
def cap_Mvar_determine(p):
    global Cap_MVar, NBus
    pop = np.array([])
    for i in range(1, np.size(p, axis=0)):
        pop_row = p[i, :]
        pop_row_MVar = np.zeros((1, NBus - 1), float)
        for j in range(1, NBus - 1):
            pop_row_MVar[j] = Cap_MVar[pop_row[j]]
        pop[
            i - 1,
        ] = pop_row_MVar
    return pop


# python -m ipykernel install --user --name venv --display-name "MATLAB virtual env"
