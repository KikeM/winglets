from functools import partial

import numpy as np
from scipy.optimize import minimize

import winglets as wl
from winglets.conventions import OperationPoint, WingletParameters

ALTITUDE = OperationPoint.ALTITUDE.value
MACH = OperationPoint.MACH.value
CL = OperationPoint.CL.value

NAME_CD = "CDi"
NAME_CM = "Cm"


class WingletOptimizer:
    def __init__(
        self, base, target, operation_point, initial_winglet, interpolation_factor=0.5
    ):
        """Winglet Optimizer.

        Parameters
        ----------
        base : winglets.FlyingWing
        target : winglets.FlyingWing
        operation_point : dict
        initial_winglet : dict
        interpolation_factor : float
        """

        # Collect design CL
        self.CL = operation_point[CL]

        # Collect models
        self.base = base
        self.target = target
        self.operation_point = operation_point
        self.interpolation_factor = interpolation_factor
        self.initial_winglet = initial_winglet

        self.optimum = None

    def _create_solver(self, model):
        """Create solver at the operational point.

        Parameters
        ----------
        model : winglets.FlyingWing

        Returns
        -------
        solver : winglets.WingSolver
        """

        _altitude = self.operation_point[ALTITUDE]
        _mach = self.operation_point[MACH]

        solver = wl.WingSolver(model=model, altitude=_altitude, mach=_mach)

        return solver

    def _update_wing(self, model, x):
        """Update winglet configuration with design vector values.

        Parameters
        ----------
        model : winglets.FlyingWing
        x : np.array
        """

        base_parameters = list(self.initial_winglet.values())

        new_parameters = self.initial_winglet.copy()

        # Modify cant angle
        ANGLE_CANT = WingletParameters.ANGLE_CANT.value
        new_parameters[ANGLE_CANT] *= x[0]

        model.winglet_parameters = new_parameters

        model.remove_winglet()
        model.create_winglet()

        return new_parameters

    def put_up(self):
        """Compute initial target values.

        Returns
        -------
        results : dict
        """

        solver = self._create_solver(self.base)

        results = self.__solve__(solver=solver)

        self.base_results = results.copy()

        return results

    def __solve__(self, solver):
        """Solve problem for constant CL.

        Parameters
        ----------
        solver : winglets.WingSolver

        Returns
        -------
        results : dict
        """
        problem = solver.solve_cl(cl=self.CL)

        results = {NAME_CD: problem.CDi, NAME_CM: problem.Cm}

        return results

    def _compute_objective_function(self, x, k):
        """Multiobjective function.

        Parameters
        ----------
        x : np.array
        k : float

        Returns
        -------
        J : float
        """

        results, _ = self._compute_state(x)

        # Scale with initial values
        base_results = self.base_results
        for key in results.keys():
            results[key] /= base_results[key]

        cd = results[NAME_CD]
        cm = results[NAME_CM]

        # Compute interpolated objective function
        J = k * cd + (1.0 - k) * cm

        return J

    def _compute_state(self, x):
        """Compute state for a given design vector.

        Parameters
        ----------
        x : np.array

        Returns
        -------
        results : dict
        parameters : dict

        Notes
        -----
        This method should be called from the objective function
        or a posteriori evaluator.
        """

        # Update geometry with new parameters
        parameters = self._update_wing(model=self.target, x=x)

        # Create solver and get solution
        solver_target = self._create_solver(model=self.target)
        results = self.__solve__(solver_target)

        return results, parameters

    def optimize(self):
        """Optimize winglet configuration.

        Returns
        -------
        optimum : scipy.optimize.optimize.OptimizeResult
        """

        func = partial(self._compute_objective_function, k=self.interpolation_factor)

        # All but the airfoil shape are degrees of freedom
        # dofs = len(self.initial_winglet) - 1
        dofs = 1  # Cant angle
        x0 = np.ones(shape=dofs)

        optimum = minimize(fun=func, x0=x0, bounds=[(0.01, 1.8)])

        self.optimum = optimum

        return optimum

    def evaluate_optimum(self):
        """Evaluate problem for optimal solution.

        Returns
        -------
        result : dict
        optimized_parameters : dict

        Raises
        ------
        ValueError : If called before optimize sucess call.
        """
        if self.optimum is None:
            raise ValueError("You must call the `optimize` method before evaluation.")

        x = self.optimum.x

        results, optimized_parameters = self._compute_state(x=x)

        return results, optimized_parameters