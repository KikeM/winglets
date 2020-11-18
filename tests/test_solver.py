import pytest

import winglets as wl
from winglets.conventions import WingSectionParameters, WingletParameters
from Geometry import Point
import numpy as np
import copy


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

    def test_solver_cl(self, flying_wing):

        solver = wl.WingSolver(
            model=flying_wing, altitude=ALTITUDE, mach=MACH, design_cl=CL
        )

        problem = solver.solve_cl(cl=CL)

        results = dict(CDi=problem.CDi, CL=problem.CL, CY=problem.CY, Cm=problem.Cm)

        expected = {
            "CDi": 0.005628463699660433,
            "CL": 0.450000000047246,
            "CY": 2.4779738805569054e-18,
            "Cm": -51.54775985252588,
        }

        assert np.isclose(CL, results["CL"])
        assert expected == results


class TestFlyingWingWinglets:
    def test_solver_alpha(self, flying_wing_winglets):

        solver = wl.WingSolver(
            model=flying_wing_winglets, altitude=ALTITUDE, mach=MACH, design_cl=CL
        )

        problem = solver.solve_alpha(alpha=ALPHA)

        results = dict(CDi=problem.CDi, CL=problem.CL, CY=problem.CY, Cm=problem.Cm)

        expected = {
            "CDi": 0.0007242762891006443,
            "CL": 0.17764159123044967,
            "CY": -1.741880084277064e-18,
            "Cm": -24.95466810536716,
        }

        assert expected == results

    def test_solver_cl(self, flying_wing_winglets):

        solver = wl.WingSolver(
            model=flying_wing_winglets, altitude=ALTITUDE, mach=MACH, design_cl=CL
        )

        problem = solver.solve_cl(cl=CL)

        results = dict(CDi=problem.CDi, CL=problem.CL, CY=problem.CY, Cm=problem.Cm)

        expected = {
            "CDi": 0.005506017922663848,
            "CL": 0.45000000002963597,
            "CY": -1.6635832920379426e-19,
            "Cm": -51.68174866448192,
        }

        assert np.isclose(CL, results["CL"])
        assert expected == results