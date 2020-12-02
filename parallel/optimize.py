# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.7.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import copy
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
import winglets as wl
from Geometry import Point
from winglets.conventions import (
    OperationPoint,
    WingletParameters,
    WingSectionParameters,
)
from winglets.optimizer import NAME_CD, NAME_CM
from winglets.utils import get_base_winglet_parametrization, get_bounds


def get_operation_point():

    ALTITUDE = OperationPoint.ALTITUDE.value
    MACH = OperationPoint.MACH.value
    CL = OperationPoint.CL.value

    _dict = {ALTITUDE: 11000, MACH: 0.75, CL: 0.45}

    return _dict


def get_sections():
    """Wing planform sections."""

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


def get_flying_wing(sections):
    """Flying wing with winglets."""
    _wing = wl.FlyingWing(sections=sections, winglet_parameters=None)

    _wing.create_wing_planform()

    return _wing


def get_flying_wing_winglets(sections):
    """Flying wing with winglets."""

    winglet_parameters = get_base_winglet_parametrization()

    _wing = wl.FlyingWing(sections=sections, winglet_parameters=winglet_parameters)

    _wing.create_wing_planform()
    _wing.create_winglet()

    return _wing


def __optimize__(
    k, flying_wing, flying_wing_winglets, operation_point, initial_winglet
):

    optimizer = wl.WingletOptimizer(
        base=flying_wing,
        target=flying_wing_winglets,
        operation_point=operation_point,
        initial_winglet=initial_winglet,
        interpolation_factor=k,
    )

    print(f"Starting with k = {k}, MAX_ITER = {optimizer.MAX_ITER}")

    # Put up
    optimizer.put_up()
    _lower, _upper = get_bounds()
    optimizer.set_bounds(lower=_lower, upper=_upper)

    # Optimize
    result = optimizer.optimize()

    # Save
    path = Path(__file__).parent

    path_file = path / f"results_{k}.pkl"

    with path_file.open(mode="wb") as fp:
        pickle.dump(optimizer, fp)

    print(f"Done with k = {k}! Optimization success? {optimizer.success}")


if __name__ == "__main__":

    from functools import partial
    from multiprocessing import Pool

    # Create inputs
    _sections = get_sections()
    flying_wing = get_flying_wing(sections=_sections)
    flying_wing_winglets = get_flying_wing_winglets(sections=_sections)
    operation_point = get_operation_point()
    initial_winglet = get_base_winglet_parametrization(twist_zero=False)

    optimize_my_winglet = partial(
        __optimize__,
        flying_wing=flying_wing,
        flying_wing_winglets=flying_wing_winglets,
        operation_point=operation_point,
        initial_winglet=initial_winglet,
    )

    # ks = np.linspace(start=0.0, stop=1.0, num=11)

    # ks = np.delete(ks, [4,5,6])

    # ks = [0.0, 0.1, 0.2, 0.3]
    ks = [0.2]
    
    ks = np.round(ks, 2)

    ks = ks[::-1]

    print(ks)

    with Pool(processes=1) as pool:

        pool.map(optimize_my_winglet, ks)
