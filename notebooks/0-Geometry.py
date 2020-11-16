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

from aerosandbox import *
from Geometry import Point
from model import generate_winglets, winglet_tip_coordinates

# ## Planform

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

# ---
# ## Winglets

# ### Winglet locations

# +
_epsilon_winglet_wing = Point([0, 0, 0.00])

# Slightly separete from the wing
WINGLET_LE_LOCATIONS_RHS = WING_LE_LOCATIONS[-1] + _epsilon_winglet_wing

# Match TE of wing tip and winglet root chord
WINGLET_LE_LOCATIONS_RHS.x += WING_CHORDS[-1] - WINGLET_CHORD_ROOT
# -

# ### Generate winglets

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

# ---
# ## Build Airplane

# +
wings = []
wings.extend([planform])

if USE_WINGLET == True:
    wings.extend(winglets)
else:
    pass

glider = Airplane(name="Ass5 wing", xyz_ref=[0, 0, 0], wings=wings)  # CG location
