import aerosandbox as sbx
from winglets.conventions import WingSectionParameters, WingletParameters


# Extract conventions
CHORD = WingSectionParameters.CHORD.value
LE_LOCATION = WingSectionParameters.LE_LOCATION.value
TWIST = WingSectionParameters.TWIST.value
AIRFOIL = WingSectionParameters.AIRFOIL.value


class Wing:

    NAME = "flying_wing"

    def __init__(self, sections, winglet=None):
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
        _sort_func = lambda section: section[LE_LOCATION].y
        self.sections = sorted(sections, key=_sort_func)

        # Store winglet configuration
        self.winglet = winglet

        self.planform = None

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
