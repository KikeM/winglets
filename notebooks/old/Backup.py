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

# %load_ext autoreload
# %autoreload 2

# +
from aerosandbox import *

import matplotlib.pyplot as plt
from Geometry import Point

from model import make_symmetric, generate_winglets

from fluids.atmosphere import ATMOSPHERE_1976

from scipy.optimize import minimize_scalar

# -

# ## Operation point

ALTITUDE = 11000
MACH = 0.75
CL = 0.45

# +
atmosphere = ATMOSPHERE_1976(ALTITUDE)

speed_sound = atmosphere.sonic_velocity(atmosphere.T)
# -

# ## Geometry definitions

# ### Main wing definition
#
# Define the wing parameters with the axes defined towards the right-side wing.

# +
WING_AIRFOIL = "naca4412"

WING_CHORDS = [5.6, 3.6, 1.26]
WING_LE_LOCATIONS = [
    Point([0.0, 0.0, 0.0]),
    Point([2.34, 4.6, 0.2]),
    Point([5.5, 14.04, 0.61]),
]
# -

# ### Winglet definition

# +
WINGLET_AIRFOIL = "naca0012"

WINGLET_TAPER_RATIO = 0.32

WINGLET_ANGLES = dict(sweep=38, cant=90)  # deg

# Convert to radians
WINGLET_ANGLES = dict((key, np.deg2rad(angle)) for key, angle in WINGLET_ANGLES.items())

wing_span = WING_LE_LOCATIONS[-1].y
WINGLET_LENGTH = 0.05 * wing_span  # meters
WINGLET_CHORD_ROOT = 0.65 * WING_CHORDS[-1]  # m

# These are not converted to radians because AeroSandbox takes them as degrees
WINGLET_TWIST = dict(root=0, tip=0)

# +
_epsilon_winglet_wing = Point([0, 0, 0.00])

# Slightly separete from the wing
WINGLET_LE_LOCATIONS_RHS = WING_LE_LOCATIONS[-1] + _epsilon_winglet_wing

# Match TE of wing tip and winglet root chord
WINGLET_LE_LOCATIONS_RHS.x += WING_CHORDS[-1] - WINGLET_CHORD_ROOT
# -

planform = Wing(
    name="main wing",
    xyz_le=[0, 0, 0],  # Coordinates of the wing's leading edge
    symmetric=True,
    xsecs=[  # The wing's cross ("X") sections
        # Root
        WingXSec(
            xyz_le=list(
                WING_LE_LOCATIONS[0]
            ),  # Coordinates of the XSec's leading edge, relative to the wing's leading edge.
            chord=WING_CHORDS[0],
            twist=2,  # degrees
            airfoil=Airfoil(name=WING_AIRFOIL),
        ),
        # Mid
        WingXSec(
            xyz_le=list(WING_LE_LOCATIONS[1]),
            chord=WING_CHORDS[1],
            twist=0,
            airfoil=Airfoil(name=WING_AIRFOIL),
        ),
        # Tip
        WingXSec(
            xyz_le=list(WING_LE_LOCATIONS[2]),
            chord=WING_CHORDS[2],
            twist=-2,
            airfoil=Airfoil(name=WING_AIRFOIL),
        ),
    ],
)

winglets = generate_winglets(
    airfoil=WINGLET_AIRFOIL,
    location_le=WINGLET_LE_LOCATIONS_RHS,
    length=WINGLET_LENGTH,
    chord=WINGLET_CHORD_ROOT,
    ratio_taper=WINGLET_TAPER_RATIO,
    sweep=WINGLET_ANGLES["sweep"],
    cant=WINGLET_ANGLES["cant"],
    twist=WINGLET_TWIST,
)

# Group all wings

wings = []
wings.extend([planform])
# wings.extend(winglets)

glider = Airplane(name="Ass5 wing", xyz_ref=[0, 0, 0], wings=wings)  # CG location


def run_aero_problem(alpha):
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


def find_cl(alpha):
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
    aero_problem = run_aero_problem(alpha)

    aero_problem.run(verbose=False)  # Runs and prints results to console

    return (aero_problem.CL - CL) ** 2.0


# +
sol = minimize_scalar(find_cl)

if sol.success == True:

    alpha = sol.x

    aero_problem = run_aero_problem(alpha)

else:
    raise ValueError("No convergence")
# -

aero_problem.CDi
