from enum import Enum


class WingSectionParameters(Enum):

    CHORD = "chord"
    LE_LOCATION = "coordinatesLeadingEdge"
    TWIST = "twistAngle"
    AIRFOIL = "airfoil"


class WingletParameters(Enum):

    SPAN = "wingletSpan"
    CHORD_ROOT = "wingletRootChord"
    TAPER_RATIO = "wingletTaperRatio"
    ANGLE_SWEEP = "wingletSweepAngle"
    ANGLE_CANT = "wingletCantAngle"
    ANGLE_TWIST_ROOT = "wingletTwistRoot"
    ANGLE_TWIST_TIP = "wingletTwistTip"
    AIRFOIL = "wingletAirfoil"
