import pytest

import winglets as wl
from winglets.conventions import WingSectionParameters, WingletParameters
from Geometry import Point
import numpy as np
import copy
from numpy.testing import assert_allclose

ALTITUDE = 11000
MACH = 0.75
CL = 0.45
ALPHA = 0.0

CHORD = WingSectionParameters.CHORD.value
LE_LOCATION = WingSectionParameters.LE_LOCATION.value
TWIST = WingSectionParameters.TWIST.value
AIRFOIL = WingSectionParameters.AIRFOIL.value


@pytest.fixture
def sections():
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


@pytest.fixture
def flying_wing(sections):
    """Flying wing with winglets."""

    _wing = wl.FlyingWing(sections=sections, winglet_parameters=None)

    _wing.create_wing_planform()

    return _wing


@pytest.fixture
def flying_wing_winglets(sections):
    """Flying wing with winglets."""

    SPAN = WingletParameters.SPAN.value
    ANGLE_CANT = WingletParameters.ANGLE_CANT.value
    ANGLE_SWEEP = WingletParameters.ANGLE_SWEEP.value
    CHORD_ROOT = WingletParameters.CHORD_ROOT.value
    TAPER_RATIO = WingletParameters.TAPER_RATIO.value
    W_AIRFOIL = WingletParameters.AIRFOIL.value

    winglet_parameters = {
        SPAN: 0.05,
        TAPER_RATIO: 0.32,
        CHORD_ROOT: 0.65,
        ANGLE_SWEEP: 38,
        ANGLE_CANT: 45,
        W_AIRFOIL: "naca0012",
    }

    _wing = wl.FlyingWing(sections=sections, winglet_parameters=winglet_parameters)

    _wing.create_wing_planform()
    _wing.create_winglet()

    return _wing


class TestFlyingWing:
    def test_solver_alpha(self, flying_wing):

        solver = wl.WingSolver(
            model=flying_wing, altitude=ALTITUDE, mach=MACH, design_cl=CL
        )

        problem = solver.solve_alpha(alpha=ALPHA)

        results = dict(CDi=problem.CDi, CL=problem.CL, CY=problem.CY, Cm=problem.Cm)

        expected = {
            "CDi": 0.0007621840201544735,
            "CL": 0.17823297687249956,
            "CY": 1.8207861772476683e-18,
            "Cm": -25.046729432809073,
        }

        assert expected == results

    @pytest.mark.skip(msg="This blocks the test suite to show the plots")
    def test_solver_draw(self, flying_wing):

        solver = wl.WingSolver(
            model=flying_wing, altitude=ALTITUDE, mach=MACH, design_cl=CL
        )

        problem = solver.solve_alpha(alpha=5.0)

        problem.draw()

    def test_solver_cl(self, flying_wing):

        solver = wl.WingSolver(
            model=flying_wing, altitude=ALTITUDE, mach=MACH, design_cl=CL
        )

        problem = solver.solve_cl(cl=CL)

        results = dict(CDi=problem.CDi, CL=problem.CL, CY=problem.CY, Cm=problem.Cm)

        expected = {
            "CDi": 0.005628661627242771,
            "CL": 0.45000738453912104,
            "CY": 2.271288523678805e-18,
            "Cm": -51.54848089843833,
        }

        assert expected == results


class TestFlyingWingWinglets:
    def test_solver_alpha(self, flying_wing_winglets):

        solver = wl.WingSolver(
            model=flying_wing_winglets, altitude=ALTITUDE, mach=MACH, design_cl=CL
        )

        problem = solver.solve_alpha(alpha=ALPHA)

        results = dict(CDi=problem.CDi, CL=problem.CL, CY=problem.CY, Cm=problem.Cm)

        expected = {
            "CDi": 0.0007211988080825468,
            "CL": 0.17779760329872044,
            "CY": 1.9875634350427656e-19,
            "Cm": -24.98033280975764,
        }

        assert expected == results

    @pytest.mark.skip(msg="This blocks the test suite to show the plots")
    def test_solver_draw(self, flying_wing_winglets):

        solver = wl.WingSolver(
            model=flying_wing_winglets, altitude=ALTITUDE, mach=MACH, design_cl=CL
        )

        problem = solver.solve_alpha(alpha=5.0)

        problem.draw()

    def test_solver_cl(self, flying_wing_winglets):

        solver = wl.WingSolver(
            model=flying_wing_winglets, altitude=ALTITUDE, mach=MACH, design_cl=CL
        )

        problem = solver.solve_cl(cl=CL)

        results = dict(CDi=problem.CDi, CL=problem.CL, CY=problem.CY, Cm=problem.Cm)

        expected = {
            "CDi": 0.005320054099686794,
            "CL": 0.4500048433740413,
            "CY": 1.794018700567938e-18,
            "Cm": -51.88601630585104,
        }

        assert np.isclose(CL, results["CL"], rtol=solver.TOL_CL, atol=solver.TOL_CL)
        assert expected == results