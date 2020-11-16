import pytest

import winglets as wl
from winglets.conventions import WingSectionParameters
from Geometry import Point

import copy


@pytest.fixture
def wing():
    """Wing object."""

    WING_AIRFOIL = "naca4412"

    CHORD = WingSectionParameters.CHORD.value
    LE_LOCATION = WingSectionParameters.LE_LOCATION.value
    TWIST = WingSectionParameters.TWIST.value
    AIRFOIL = WingSectionParameters.AIRFOIL.value

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

    _wing = wl.Wing(sections=_sections, winglet=None)

    _wing.create_wing_planform()

    return _wing


def test_solver_no_winglet(wing):

    ALTITUDE = 11000
    MACH = 0.75
    CL = 0.45
    ALPHA = 0.0

    solver = wl.WingSolver(model=wing, altitude=ALTITUDE, mach=MACH, design_cl=CL)

    problem = solver.solve_alpha(ALPHA)

    pass
