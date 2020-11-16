from enum import Enum


class WingSectionParameters(Enum):

    CHORD = "chord"
    LE_LOCATION = "coordinatesLeadingEdge"
    TWIST = "twistAngle"
    AIRFOIL = "airfoil"


class WingletParameters(Enum):

    SPAN = "span"
    CHORD_ROOT = "rootChord"
    TAPER_RATIO = "taperRatio"
    ANGLE_SWEEP = "sweepAngle"
    ANGLE_CANT = "cantAngle"
    INCIDENCE_ANGLE_ROOT = "incidenceAngleRoot"
    INCIDENCE_ANGLE_TIP = "incidenceAngleTip"
