import copy

import aerosandbox as sbx
import pytest
from Geometry import Point
from winglets import FlyingWing
from winglets.conventions import WingSectionParameters, WingletParameters


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
def winglet_parameters():
    """Flying wing with winglets."""

    SPAN = WingletParameters.SPAN.value
    ANGLE_CANT = WingletParameters.ANGLE_CANT.value
    ANGLE_SWEEP = WingletParameters.ANGLE_SWEEP.value
    CHORD_ROOT = WingletParameters.CHORD_ROOT.value
    TAPER_RATIO = WingletParameters.TAPER_RATIO.value
    W_AIRFOIL = WingletParameters.AIRFOIL.value

    _winglet_parameters = {
        SPAN: 0.05,
        TAPER_RATIO: 0.32,
        CHORD_ROOT: 0.65,
        ANGLE_SWEEP: 38,
        ANGLE_CANT: 45,
        W_AIRFOIL: "naca0012",
    }

    return _winglet_parameters


@pytest.fixture
def op_point():

    return sbx.OperatingPoint(velocity=1.0, alpha=1.0, density=1.0)


def test_instantiate_wing(sections):

    wing = FlyingWing(sections=sections, winglet_parameters=None)

    pass


def test_instantiate_wing_sort_sections(sections):
    """Test the sections are sorted in the correct order."""

    expected_sections = copy.deepcopy(sections)

    # Swap sections order
    swap = copy.deepcopy(sections[1])
    sections[1] = sections[0]
    sections[0] = swap

    # Instantiate
    wing = FlyingWing(sections=sections, winglet_parameters=None)

    # Check the sections are in the right order again
    result_sections = wing.sections

    assert expected_sections == result_sections


def test_build_planform(op_point, sections):

    wing = FlyingWing(sections=sections, winglet_parameters=None)

    wing.create_wing_planform()

    # Check the geometry has been correctly instantiated
    problem = sbx.vlm3(
        airplane=wing.airplane,
        op_point=op_point,
    )

    problem.verbose = False
    problem.make_panels()
    problem.setup_geometry()


def test_build_winglet(op_point, sections, winglet_parameters):

    wing = FlyingWing(sections=sections, winglet_parameters=winglet_parameters)

    wing.create_wing_planform()
    wing.create_winglet()

    # Check the geometry has been correctly instantiated
    problem = sbx.vlm3(
        airplane=wing.airplane,
        op_point=op_point,
    )

    problem.verbose = False
    problem.make_panels()
    problem.setup_geometry()


def test_span(sections):

    wing = FlyingWing(sections=sections, winglet_parameters=None)

    wing.create_wing_planform()

    expected = 28.08

    result = wing.span

    assert expected == result


def test_wingtip_chord(sections):

    wing = FlyingWing(sections=sections, winglet_parameters=None)

    wing.create_wing_planform()

    expected = 1.26

    result = wing.wing_tip_chord

    assert expected == result
