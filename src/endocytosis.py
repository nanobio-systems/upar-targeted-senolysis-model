import numpy as np
from scipy.integrate import solve_ivp
import sys
from pathlib import Path
sys.path.append(str(Path().resolve().parent))
from src.constants import *

def endocytosis_ode(t, y, bound_complexes, kint=None, khalf=None, kclear=None, vmax=None, version=None):
    
    I = y[0]
    B = bound_complexes(t)

    if version == None or version == 1:
        dIdt = kint * B - kclear * I
    if version == 2:
        dIdt = (vmax * B) / (khalf + B) - kclear * I

    return [dIdt]

def run_endocytosis_model(binding_sol, khalf, vmax=None, version=None):
    
    B_interp = lambda t: np.interp(
        t, binding_sol.t, binding_sol.y[0]
        )

    T_END = binding_sol.t[-1]
    I0 = [0]

    t_span = (T_START, T_END)
    t_eval = binding_sol.t
    sol = solve_ivp(endocytosis_ode,
        t_span, I0,
        t_eval=t_eval, 
        args=(B_interp, KINT, khalf, KCLEAR, vmax, version)
    )

    return sol

# control dense outputs or smth..?? look at past research