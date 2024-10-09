import numpy as np
import pytest

from TongueIterator import TongueIterator
from tongue_families import eval_doubling_plus_tent

from .fixtures import generate_params_fixed

def create_test_iterator(periodicity_tol=1.e-4):
    options = {
        'periodicity_tol': periodicity_tol
    }
    ti = TongueIterator('2x+T', options_dynamics=options)
    return ti

def test_starting_points():
    ti = create_test_iterator()
    a, b = generate_params_fixed()
    default_starting_point = 0.123
    nb_starting_points = 5
    starting_points = ti.setup_starting_points(a, b,
                                               default_starting_point,
                                               nb_starting_points=nb_starting_points)
    assert(starting_points.shape == (3, 2, nb_starting_points))
    expected_starting_points_data = [0.123, 0.323, 0.523, 0.723, 0.923]
    expected_starting_points = np.array([
        [expected_starting_points_data] * 2,
        [expected_starting_points_data] * 2,
        [expected_starting_points_data] * 2,
    ])
    assert(np.allclose(expected_starting_points, starting_points))

def test_iterate():
    ti = create_test_iterator()
    a, b = generate_params_fixed(n_a=2, n_b=2)
    x_0_list = [ 0.123, 0.456, 0.789, ]
    x_0_data = np.array(x_0_list)
    x_0 = np.array([
        [ x_0_list, x_0_list ],
        [ x_0_list, x_0_list ],
    ])
    nb_it = 1
    x_n = ti.iterate(a, b, x_0, nb_it=nb_it)
    assert(x_n.shape == (2,2,3))
    expected_x_n = [
        [
            [ eval_doubling_plus_tent(0., 1., x) for x in x_0_data ],
            [ eval_doubling_plus_tent(0., 0.789, x) for x in x_0_data ],
        ],
        [
            [ eval_doubling_plus_tent(0.567, 1., x) for x in x_0_data ],
            [ eval_doubling_plus_tent(0.567, 0.789, x) for x in x_0_data ],
        ],
    ]
    assert(np.allclose(x_n, expected_x_n))
    nb_it = 3
    x_n = ti.iterate(a, b, x_0, nb_it=nb_it)
    assert(x_n.shape == (2,2,3))
    expected_x_n = [
        [
            [
    eval_doubling_plus_tent(0., 1., eval_doubling_plus_tent(0., 1., eval_doubling_plus_tent(0., 1., x)))
    for x in x_0_data
            ],
            [
    eval_doubling_plus_tent(0., 0.789, eval_doubling_plus_tent(0., 0.789, eval_doubling_plus_tent(0., 0.789, x)))
    for x in x_0_data
            ],
        ],
        [
            [
    eval_doubling_plus_tent(0.567, 1., eval_doubling_plus_tent(0.567, 1., eval_doubling_plus_tent(0.567, 1., x)))
    for x in x_0_data
            ],
            [
    eval_doubling_plus_tent(0.567, 0.789, eval_doubling_plus_tent(0.567, 0.789, eval_doubling_plus_tent(0.567, 0.789, x)))
    for x in x_0_data
            ],
        ],
    ]
    assert(np.allclose(x_n, expected_x_n))

def test_compute_orbits():
    ti = create_test_iterator()
    a, b = generate_params_fixed(n_a=2, n_b=2)
    x_0_list = [ 0.123, 0.456, 0.789, ]
    x_0_data = np.array(x_0_list)
    x_0 = np.array([
        [ x_0_list, x_0_list ],
        [ x_0_list, x_0_list ],
    ])
    nb_it = 2
    orbits = ti.compute_orbits(a, b, x_0, nb_it)
    assert(orbits.shape == (2, 2, 3, nb_it+1))
    x_1 = ti.iterate(a, b, x_0, 1)
    x_2 = ti.iterate(a, b, x_1, 1)
    assert(np.allclose(orbits[..., 0], x_0))
    assert(np.allclose(orbits[..., 1], x_1))
    assert(np.allclose(orbits[..., 2], x_2))

def test_compute_periods_periods():
    ti = create_test_iterator()
    max_period = 4
    periodic_orbits = [
        [ 0.1, 0.1, 0.1, 0.1, 0.1, ],
        [ 0.2, 0.3, 0.2, 0.3, 0.2, ],
        [ 0.4, 0.5, 0.6, 0.4, 0.5, ],
        [ 0.7, 0.8, 0.9, 0.11, 0.7, ],
        [ 0.12, 0.13, 0.14, 0.15, 0.16, ],
    ]
    expected_periods_data = [ 5, 1, 2, 3, 4, 2, 5, 5 ]
    orbits_data = [ periodic_orbits[p-1] for p in expected_periods_data ]
    orbits = np.array(orbits_data).reshape((2,2,2,5))
    periods = ti.compute_periods(orbits,
                                 max_period,
                                 return_type='min periods')
    assert(periods.shape == (2, 2,))
    for i in range(2):
        for j in range(2):
            assert(periods[i,j] == min(expected_periods_data[4*i+2*j:4*i+2*j+2]))




    














