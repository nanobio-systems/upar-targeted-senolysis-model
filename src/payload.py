import numpy as np
from scipy.integrate import solve_ivp
import sys
from pathlib import Path
sys.path.append(str(Path().resolve().parent))
from src.constants import *

def payload_ode(t, y, version, i_np, kelim, b_np=None, a=None, n=None, k=None, vmax=None, khalf=None, krel=None):

    if version == None or version == 1:
        P = y[0]
        I = i_np(t)

        dPdt = krel * I - kelim * P

        return [dPdt]
    
    elif version == 2:

        U, P = y
        B = b_np(t)

        F = min(k * t**n, 1 - 1e-7)
        dFdt = n * k * t**(n-1)

        R = dFdt / max(1 - F, 1e-12)

        uptake_flux = vmax * B / (khalf + B)

        dUdt = a * uptake_flux - R * U

        dPdt = R * U - kelim * P

        return [dUdt, dPdt]

    else:
        raise ValueError("version must be 1 (first-order) or 2 (Ritger-Peppas)")

class PayloadResult:
    def __init__(self, t, P, U=None):
        self.t = t
        self.P = P
        self.U = U

def run_payload_model(endo_sol, bind_sol=None, version=None, n=None, vmax=None):

    I_interp = lambda t: np.interp(
        t, endo_sol.t, endo_sol.y[0])

    T_END = endo_sol.t[-1]

    if version == None or version == 1:

        P0 = [0]

        T_START = 0

        t_span = (T_START, T_END)
        t_eval = endo_sol.t[endo_sol.t >= T_START]
        sol = solve_ivp(payload_ode,
            t_span, P0,
            t_eval=t_eval, 
            args=(version, I_interp, KELIM, None, None, None, None, None, None, KREL)
        )

        return sol

    elif version == 2:

        khalf = vmax / KINT # MM Approx. not QSS Approx.

        B_interp = lambda t: np.interp(
            t, bind_sol.t, bind_sol.y[0])

        T_END = endo_sol.t[-1]
        u0, p0 = 0, 0
        y0 = [u0, p0]

        T_START = 1.0e-6

        t_eval = endo_sol.t[(endo_sol.t >= T_START) & (endo_sol.t <= T_END)]

        if len(t_eval) == 0 or t_eval[0] > T_START:
            t_eval = np.insert(t_eval, 0, T_START)

        t_span = (T_START, T_END)

        sol = solve_ivp(payload_ode,
                    t_span, y0=y0,
                    t_eval=t_eval, 
                    args=(version, I_interp, KELIM, B_interp, a, n, k, vmax, khalf, KREL)
                )

        return PayloadResult(t=sol.t, P=sol.y[1], U=sol.y[0])
    