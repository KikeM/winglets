# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.7.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
from aerosandbox import *

from scipy.optimize import minimize_scalar


# -


def run_aero_problem_alpha(alpha):
    """
    Run VLM3 problem for a prescribed angle of attack.

    Parameters
    ----------
    alpha: float
        deg

    Returns
    -------
    VLM3-like
    """

    aero_problem = vlm3(
        airplane=glider,
        op_point=OperatingPoint(velocity=MACH * speed_sound, alpha=alpha),
    )

    aero_problem.run(verbose=False)  # Runs and prints results to console

    return aero_problem


def find_cl(alpha, cl_target):
    """
    Minimizing function to find the correct angle of attack for
    the corresponding lift coefficient.

    Parameters
    ----------
    alpha: float
        deg

    Returns
    -------
    float
    """
    aero_problem = run_aero_problem_alpha(alpha)

    aero_problem.run(verbose=False)  # Runs and prints results to console

    return (aero_problem.CL - cl_target) ** 2.0


def run_aero_problem_cl(cl):
    """
    Run VLM3 problem for a prescribed angle of attack.

    Parameters
    ----------
    cl: float

    Returns
    -------
    VLM3-like
    """
    sol = minimize_scalar(find_cl, args=(cl), options=dict(maxiter=1000))

    if sol.success == True:

        alpha = sol.x

        aero_problem = run_aero_problem_alpha(alpha)

    else:
        raise ValueError("No convergence")

    return aero_problem
