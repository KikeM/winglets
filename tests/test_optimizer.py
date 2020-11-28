import copy

import numpy as np
import pytest
import winglets as wl
from Geometry import Point
from numpy.testing import assert_allclose
from winglets.conventions import (
    OperationPoint,
    WingletParameters,
    WingSectionParameters,
)
from winglets.utils import get_base_winglet_parametrization

from scipy.optimize.optimize import OptimizeResult

CHORD = WingSectionParameters.CHORD.value
LE_LOCATION = WingSectionParameters.LE_LOCATION.value
TWIST = WingSectionParameters.TWIST.value
AIRFOIL = WingSectionParameters.AIRFOIL.value


@pytest.fixture
def operation_point():

    ALTITUDE = OperationPoint.ALTITUDE.value
    MACH = OperationPoint.MACH.value
    CL = OperationPoint.CL.value

    _dict = {ALTITUDE: 11000, MACH: 0.75, CL: 0.45}

    return _dict


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


@pytest.fixture(scope="function")
def optimizer(operation_point, flying_wing, flying_wing_winglets):

    _optimizer = wl.WingletOptimizer(
        base=flying_wing,
        target=flying_wing_winglets,
        operation_point=operation_point,
        initial_winglet=get_base_winglet_parametrization(),
    )

    return _optimizer


class TestOptimizer:
    def test_put_up(self, optimizer):

        from winglets.optimizer import NAME_CD, NAME_CM

        results = optimizer.put_up()

        expected = {NAME_CD: 0.005628661627242771, NAME_CM: -51.54848089843833}

        assert expected == results

    def test_optimization_cant_angle(self, optimizer):

        optimizer.interpolation_factor = 0.55555556

        optimizer.put_up()
        result = optimizer.optimize()

        expected_cant_angle = 38.4241091

        result_cant_angle = (
            result.x * optimizer.initial_winglet[WingletParameters.ANGLE_CANT.value]
        )

        assert_allclose(
            desired=expected_cant_angle, actual=result_cant_angle, rtol=1e-3
        )

        pass

    def test_evaluate_optimal_point(self, optimizer):

        result = OptimizeResult(
            fun=0.9723818601228951,
            hess_inv=None,
            jac=np.array([7.32747193e-07]),
            message=b"CONVERGENCE NORM_OF_PROJECTED_GRADIENT_<=_PGTOL",
            nfev=10,
            nit=4,
            njev=5,
            status=0,
            success=True,
            x=np.array([0.85397381]),
        )

        optimizer.optimum = result

        targets, parameters = optimizer.evaluate_optimum()

        expected_targets = {"CDi": 0.005316969443946267, "Cm": -51.91339550388924}
        expected_parameters = {
            0: 0.05,
            2: 0.32,
            1: 0.65,
            3: 38,
            4: 38.42882145,
            "wingletAirfoil": "naca0012",
        }

        assert expected_parameters == parameters
        assert expected_targets == targets

    def test_evaluate_optimal_point_raise(self, optimizer):

        try:
            targets, parameters = optimizer.evaluate_optimum()
        except ValueError as error:
            message = error.args[0]

        expected_message = "You must call the `optimize` method before evaluation."

        assert expected_message == message

    @pytest.mark.skip(msg="Not implemented yet.")
    def test_global_optimization(self, optimizer):

        pass
