import pytest

from winglets import Wing
from winglets.conventions import WingSectionParameters
from Geometry import Point

import copy


@pytest.fixture
def sections():
    """Planform sections."""

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

    return _sections


def test_instantiate_wing(sections):

    wing = Wing(sections=sections, winglet=None)

    pass


def test_instantiate_wing_sort_sections(sections):
    """Test the sections are sorted in the correct order."""

    expected_sections = copy.deepcopy(sections)

    # Swap sections order
    swap = copy.deepcopy(sections[1])
    sections[1] = sections[0]
    sections[0] = swap

    # Instantiate
    wing = Wing(sections=sections, winglet=None)

    # Check the sections are in the right order again
    result_sections = wing.sections

    assert expected_sections == result_sections


def test_build_planform(sections):

    wing = Wing(sections=sections, winglet=None)

    wing.create_wing_planform()

    pass
