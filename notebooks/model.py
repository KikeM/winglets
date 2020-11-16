from Geometry import Point
import numpy as np
from aerosandbox import *


def make_symmetric(point, axis="x"):
    """
    Return symmetric point w.r.t. axis.

    Parameters
    ----------
    point: Point-like

    axis: str
        'x', 'y', 'z'

    Returns
    -------
    Point
    """
    if axis == "x":
        return point - Point([2.0 * point.x, 0, 0])

    if axis == "y":
        return point - Point([0, 2.0 * point.y, 0])

    if axis == "z":
        return point - Point([0, 0, 2.0 * point.z])


def winglet_tip_coordinates(length, sweep, cant):
    """
    Compute winglet tip coordinates in the winglet's
    LE frame of reference.

    Parameters
    ----------
    length: float

    sweep: float
        rad

    cant: float
        rad

    Returns
    -------
    Point
    """
    return length * Point(
        [np.sin(sweep) * np.sin(cant), np.cos(sweep) * np.sin(cant), np.cos(cant)]
    )


def generate_winglet(
    airfoil, location_le, length, chord, ratio_taper, sweep, cant, twist
):

    location_tip = winglet_tip_coordinates(length, sweep, cant)

    return Wing(
        name="Winglet",
        xyz_le=list(location_le),
        symmetric=False,
        xsecs=[
            WingXSec(
                xyz_le=[0, 0, 0],
                chord=chord,
                twist=twist["root"],
                airfoil=Airfoil(name=airfoil),
            ),
            WingXSec(
                xyz_le=list(location_tip),
                chord=chord * ratio_taper,
                twist=twist["tip"],
                airfoil=Airfoil(name=airfoil),
            ),
        ],
    )


def generate_winglets(
    airfoil, location_le, length, chord, ratio_taper, sweep, cant, twist
):
    """
    Generate winglet models for AeroSandbox.

    Parameters
    ----------
    airfoil: str

    location_le: Point-like

    length: float

    chord: float

    ratio_taper: float

    sweep: float
        rad

    cant: float
        rad

    twist: dict
        - Keys: ['root', 'tip']
        - Values: float
            deg

    Returns
    -------
    list of Wing-like
    """
    # Compute right-hand side winglet
    winglet_rhs = generate_winglet(
        airfoil=airfoil,
        location_le=location_le,
        length=length,
        chord=chord,
        ratio_taper=ratio_taper,
        sweep=sweep,
        cant=cant,
        twist=twist,
    )

    winglet_rhs.name = "winglet-rhs"

    # Compute the left-hand side winglet
    location_le_lhs = make_symmetric(location_le, axis="y")

    winglet_lhs = generate_winglet(
        airfoil=airfoil,
        location_le=location_le_lhs,
        length=length,
        chord=chord,
        ratio_taper=ratio_taper,
        sweep=sweep,
        cant=cant,
        twist=twist,
    )

    winglet_lhs.name = "winglet-lhs"

    return [winglet_rhs, winglet_lhs]
