from enum import Enum, auto
from functools import partial

import aerosandbox as sbx
from fluids.atmosphere import ATMOSPHERE_1976
from scipy.optimize import minimize_scalar


class SolverMode(Enum):

    ALPHA = auto()
    CL = auto()


class WingSolver:

    MAX_ITER_CL = 1000
    NAME = "WingSolver"

    def __init__(self, model, altitude, mach, design_cl):
        """
        Parameters
        ----------
        model :
        altitude :
        mach :
        design_cl :

        """

        self.model = model
        self.altitude = altitude
        self.mach = mach
        self.design_cl = design_cl

        # Compute velocity in m/s
        atmosphere = ATMOSPHERE_1976(altitude)
        speed_sound = atmosphere.sonic_velocity(atmosphere.T)

        self.velocity = mach * speed_sound
        self._atmosphere = atmosphere

        # Code results
        self.CL = None
        self.CY = None
        self.CDi = None

    @property
    def airplane(self):

        wings = [self.model.planform]

        return sbx.Airplane(name=self.NAME, xyz_ref=[0, 0, 0], wings=wings)

    def solve_alpha(self, alpha):
        """Solve aerodynamical problem for an angle of attack.

        Parameters
        ----------
        alpha : float
            In degress.

        Return
        ------
        aerosandbox.vlm3
        """

        problem = self._solve(value=alpha, mode=SolverMode.ALPHA)

        return problem

    def solve_cl(self, cl):
        """Solve aerodynamical problem for a lift coefficient.

        Parameters
        ----------
        cl : float

        Return
        ------
        aerosandbox.vlm3
        """

        problem = self._solve(value=cl, mode=SolverMode.CL)

        return problem

    def _solve(self, value, mode=None):
        """Create and solve VLM3 problem.

        Parameters
        ----------
        value : float
        mode : str

        Returns
        -------
        aero_problem : VLM3-like object
        """

        # Create vlm3-object
        if mode == SolverMode.ALPHA:

            atmosphere = self._atmosphere
            rho = atmosphere.density(T=atmosphere.T, P=atmosphere.P)

            aero_problem = sbx.vlm3(
                airplane=self.airplane,
                op_point=sbx.OperatingPoint(
                    velocity=self.velocity, alpha=value, density=rho
                ),
            )

        elif mode == SolverMode.CL:

            aero_problem = self._find_alpha_for_cl(cl=value)

        else:
            raise NotImplementedError("'mode' must be either 'alpha' or 'cl'.")

        # Solve
        aero_problem.run(verbose=False)

        self.CL = aero_problem.CL
        self.CDi = aero_problem.CDi
        self.CY = aero_problem.CY
        self.alpha = aero_problem.op_point.alpha

        return aero_problem

    def _error_cl(self, alpha, cl_target):
        """Objective function to find the correct angle of attack for
        the corresponding lift coefficient.

        Parameters
        ----------
        alpha : float
        cl_target : float

        Returns
        -------
        float
        """
        # Solve problem for angle attack iteration
        aero_problem = self._solve(value=alpha, mode=SolverMode.ALPHA)

        # Compute objective function
        error = (aero_problem.CL - cl_target) ** 2.0

        return error

    def _find_alpha_for_cl(self, cl):
        """Run VLM3 problem for a prescribed lift coefficient.

        Parameters
        ----------
        cl: float

        Returns
        -------
        VLM3-like

        Raises
        ------
        ValueError
        """
        # Create objective function and solver configuration
        func = partial(self._error_cl, cl_target=cl)
        _options = dict(maxiter=self.MAX_ITER_CL)

        # Minimize
        sol = minimize_scalar(fun=func, options=_options)

        if sol.success == True:

            # Collect angle of attack from solver
            alpha = sol.x

            # Solve VLM3 problem for the angle of attack corresponding
            # to the request CL
            aero_problem = self._solve(value=alpha, mode=SolverMode.ALPHA)

            return aero_problem

        else:
            raise ValueError(
                "The solver did not converge to find an angle of attack for the demanded Cl"
            )
