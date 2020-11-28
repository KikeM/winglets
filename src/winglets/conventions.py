from enum import Enum, auto


class OperationPoint(Enum):

    ALTITUDE = "altitude"
    MACH = "Mach"
    CL = "CL"


class WingSectionParameters(Enum):

    CHORD = "chord"
    LE_LOCATION = "coordinatesLeadingEdge"
    TWIST = "twistAngle"
    AIRFOIL = "airfoil"


class WingletParameters(Enum):

    SPAN = 0
    CHORD_ROOT = 1
    TAPER_RATIO = 2
    ANGLE_SWEEP = 3
    ANGLE_CANT = 4
    ANGLE_TWIST_ROOT = 5
    ANGLE_TWIST_TIP = 6
    AIRFOIL = "wingletAirfoil"
