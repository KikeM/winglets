from winglets.conventions import WingletParameters, WingSectionParameters
from Geometry import Point

# Flying wing
CHORD = WingSectionParameters.CHORD.value
LE_LOCATION = WingSectionParameters.LE_LOCATION.value
TWIST = WingSectionParameters.TWIST.value
AIRFOIL = WingSectionParameters.AIRFOIL.value

# Winglet
SPAN = WingletParameters.SPAN.value
ANGLE_CANT = WingletParameters.ANGLE_CANT.value
ANGLE_SWEEP = WingletParameters.ANGLE_SWEEP.value
CHORD_ROOT = WingletParameters.CHORD_ROOT.value
TAPER_RATIO = WingletParameters.TAPER_RATIO.value
W_AIRFOIL = WingletParameters.AIRFOIL.value


def get_base_winglet_parametrization():

    winglet_parameters = {
        SPAN: 0.05,
        TAPER_RATIO: 0.32,
        CHORD_ROOT: 0.65,
        ANGLE_SWEEP: 38,
        ANGLE_CANT: 45,
        W_AIRFOIL: "naca0012",
    }

    return winglet_parameters


def get_base_sections():
    """Wing planform sections."""

    WING_AIRFOIL = "naca4412"

    _sections = [
        {
            CHORD: 5.6,
            LE_LOCATION: Point([0.0, 0.0, 0.0]),
            TWIST: 0.0,
            AIRFOIL: WING_AIRFOIL,
        },
        {
            CHORD: 3.6,
            LE_LOCATION: Point([2.34, 4.6, 0.2]),
            TWIST: -2.0,
            AIRFOIL: WING_AIRFOIL,
        },
        {
            CHORD: 1.26,
            LE_LOCATION: Point([5.5, 14.04, 0.61]),
            TWIST: -5.0,
            AIRFOIL: WING_AIRFOIL,
        },
    ]

    return _sections
