import aerosandbox as sbx
import numpy as np
from Geometry import Point

from winglets.conventions import WingletParameters, WingSectionParameters

# Extract conventions
CHORD = WingSectionParameters.CHORD.value
LE_LOCATION = WingSectionParameters.LE_LOCATION.value
TWIST = WingSectionParameters.TWIST.value
AIRFOIL = WingSectionParameters.AIRFOIL.value

W_SPAN = WingletParameters.SPAN.value
W_ANGLE_CANT = WingletParameters.ANGLE_CANT.value
W_ANGLE_SWEEP = WingletParameters.ANGLE_SWEEP.value
W_CHORD_ROOT = WingletParameters.CHORD_ROOT.value
W_TAPER_RATIO = WingletParameters.TAPER_RATIO.value
W_AIRFOIL = WingletParameters.AIRFOIL.value


class FlyingWing:

    NAME = "flying_wing"

    def __init__(self, sections, winglet_parameters=None):
        """Wing planform implementation.

        Parameters
        ----------
        sections : list of dicts
        winglet : dict

        Attributes
        ----------
        planform : aerosandbox.Wing
        """
        # Store sections sorted by span-wise direction
        self.sections = self.__sort_sections__(sections)

        # Store winglet configuration
        self.winglet_parameters = winglet_parameters

        self.planform = None
        self.winglet = None
        self.winglet_dimensions = dict()

    @staticmethod
    def __sort_sections__(sections):
        _sort_func = lambda section: section[LE_LOCATION].y
        return sorted(sections, key=_sort_func)

    @property
    def __wingtip_section__(self):
        # Get furthest section
        furthest_section = max(
            self.sections, key=lambda section: section[LE_LOCATION].y
        )
        return furthest_section

    @property
    def span(self):

        # Get furthest section
        furthest_section = self.__wingtip_section__

        # Return y-axis location
        return 2.0 * furthest_section[LE_LOCATION].y

    @property
    def wing_tip_chord(self):

        # Get furthest section
        furthest_section = self.__wingtip_section__

        # Return y-axis location
        return furthest_section[CHORD]

    @property
    def airplane(self):

        return sbx.Airplane(name=self.NAME, xyz_ref=[0, 0, 0], wings=self.wings)

    @property
    def wings(self):

        _wings = [self.planform]

        if self.winglet_parameters is not None:
            _wings.extend(self.winglet)

        return _wings

    def create_wing_planform(self):
        """Create planform object.

        Returns
        -------
        aerosanbox.Wing
        """

        # Create sections
        sections = []

        for _section in self.sections:

            _coordinates = list(_section[LE_LOCATION])
            _airfoil = sbx.Airfoil(name=_section[AIRFOIL])

            _sbx_section = sbx.WingXSec(
                xyz_le=_coordinates,  # Coordinates of the XSec's leading edge, **relative** to the wing's leading edge.
                chord=_section[CHORD],
                twist=_section[TWIST],  # degrees
                airfoil=_airfoil,
            )

            sections.append(_sbx_section)

        # Create wing
        planform = sbx.Wing(
            name=self.NAME,
            xyz_le=[0.0, 0.0, 0.0],  # Coordinates of the wing's leading edge
            symmetric=True,
            xsecs=sections,
        )

        self.planform = planform

        return planform

    def create_winglet(self):
        """Create winglet according to parametrization."""

        # Compute dimensions based on wing referenced values
        parameters = self.winglet_parameters

        # Chords
        chord_root = self.wing_tip_chord * parameters[W_CHORD_ROOT]
        chord_tip = chord_root * parameters[W_TAPER_RATIO]

        self.winglet_dimensions["chord_root"] = chord_root
        self.winglet_dimensions["chord_tip"] = chord_tip

        # Length
        self.winglet_dimensions["length"] = self.span * parameters[W_SPAN]

        self._create_winglet()

    @staticmethod
    def get_winglet_vector(length, sweep, cant):
        """
        Compute winglet tip coordinates in the winglet's
        LE frame of reference.

        Parameters
        ----------
        length: float
        sweep: float, degrees
        cant: float, degrees

        Returns
        -------
        Point
        """

        # Convert degrees to radians
        _sweep = np.deg2rad(sweep)
        _cant = np.deg2rad(cant)

        # Compute unit vector
        unit_vector = Point(
            [
                np.sin(_sweep) * np.cos(_cant),
                np.cos(_sweep) * np.cos(_cant),
                np.sin(_cant),
            ]
        )

        # Scale with length
        vector = length * unit_vector

        return vector

    def _create_winglet(self):
        """Generate winglet.

        Returns
        -------
        aerosandbox.Wing
        """

        # Extract winglet configuration
        parameters = self.winglet_parameters
        dimensions = self.winglet_dimensions

        location_tip = self.get_winglet_vector(
            length=dimensions["length"],
            sweep=parameters[W_ANGLE_SWEEP],
            cant=parameters[W_ANGLE_CANT],
        )

        # Slightly separete from the wing
        _epsilon_winglet_wing = Point([0, 0, 0.01])

        # Get wing tip section
        _section = self.__wingtip_section__
        _coordinates = list(_section[LE_LOCATION])
        coordinates_weld = _coordinates + _epsilon_winglet_wing

        # Match TE of wing tip and winglet root chord
        chord_root = dimensions["chord_root"]
        chord_tip = dimensions["chord_tip"]

        coordinates_weld.x += _section[CHORD] - chord_root

        winglet_airfoil = sbx.Airfoil(name=parameters[W_AIRFOIL])

        winglet = sbx.Wing(
            name="Winglet",
            xyz_le=list(coordinates_weld),
            symmetric=True,
            xsecs=[
                sbx.WingXSec(
                    xyz_le=[0, 0, 0],
                    chord=chord_root,
                    twist=0.0,
                    airfoil=winglet_airfoil,
                ),
                sbx.WingXSec(
                    xyz_le=list(location_tip),
                    chord=chord_tip,
                    twist=0.0,
                    airfoil=winglet_airfoil,
                ),
            ],
        )

        self.winglet = [winglet]

        return winglet
