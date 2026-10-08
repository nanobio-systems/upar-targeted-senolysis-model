import numpy as np
from scipy.integrate import solve_ivp
import sys
from pathlib import Path
sys.path.append(str(Path().resolve().parent))
from src.constants import *

def binding_ode(t, y, kon, koff, kint, n, rt):

    B = y[0]

    dBdt = kon * n * (rt - B) - B * (koff + kint)

    return [dBdt]

def run_binding_model(rt, koff, duration):

    B0 = [0]
    T_END = duration

    t_span = (T_START, T_END)

    t_eval = np.linspace(
        T_START,
        T_END,
        500
    )

    sol = solve_ivp(
        binding_ode,
        t_span,
        B0,
        t_eval=t_eval,
        args=(KON, koff, KINT, n0, rt)
    )

    return sol
