from typing import Literal, Callable

import numpy as np
from tqdm import tqdm

from tongue_families import eval_doubling_plus_straight_sine, eval_doubling_plus_tent, eval_double_dsm, eval_dsm
from tongue_families import eval_test_map

class TongueIterator:
    def __init__(self,
                 family_name: Literal['dsm', '2xdsm', '2x+S', '2x+T', 'test'],
                 options_dynamics: dict = {}):
        self.family_name = family_name
        self.setup_mappings()
        self.set_options(options_dynamics)
    def setup_mappings(self):
        match(self.family_name):
            case '2x+S':
                self.mapping_for_iterate = eval_doubling_plus_straight_sine
            case '2x+T':
                self.mapping_for_iterate = eval_doubling_plus_tent
            case 'dsm':
                self.mapping_for_iterate = eval_dsm
            case '2xdsm':
                self.mapping_for_iterate = eval_double_dsm
            case 'test':
                self.mapping_for_iterate = eval_test_map
            case _:
                raise ValueError(f'unsupported family: "{self.family_name}')
    def set_options(self, options_dynamics: dict):
        self.periodicity_tol = options_dynamics.get('periodicity_tol', 1e-3)
    def __set_progress_bar(self, start=0, end=0, do_show_progress=True):
        it_range = range(start, end)
        if(do_show_progress):
            it_range = tqdm(it_range)
        return it_range
    def setup_starting_points(self,
                              a: np.ndarray, b: np.ndarray,
                              default_starting_point: float,
                              nb_starting_points: int = 1):
        starting_points_data = np.linspace(default_starting_point,
                                           default_starting_point + 1.,
                                           nb_starting_points,
                                           endpoint=False)
        starting_points_data = np.mod(starting_points_data, 1.)
        parameters_shape = np.broadcast(a, b).shape
        # there's probably a way to use repeat/tile or something like that:
        starting_points = np.zeros(parameters_shape + (nb_starting_points,))
        starting_points[..., :] = starting_points_data
        return starting_points
    def iterate(self,
                a: np.ndarray, b: np.ndarray, x: np.ndarray,
                nb_it: int,
                do_show_progress: bool=True) -> np.ndarray:
        y = x
        it_range = self.__set_progress_bar(end=nb_it, do_show_progress=do_show_progress)
        for it in it_range:
            y = self.mapping_for_iterate(a[..., None], b[..., None], y)
        return y
    def compute_orbits(self,
                       a: np.ndarray, b: np.ndarray, x_0: np.ndarray,
                       nb_it: int,
                       do_show_progress: bool = True) -> np.ndarray:
        orbits = np.zeros(x_0.shape + (nb_it+1,))
        orbits[..., 0] = x_0
        it_range = self.__set_progress_bar(start=1, end=nb_it+1, do_show_progress=do_show_progress)
        for it in it_range:
            orbits[..., it] = self.mapping_for_iterate(a[..., None], b[..., None], orbits[..., it-1])
        return orbits
    def compute_periods(self,
                        orbits: np.ndarray,
                        max_period: int = 1,
                        return_type: Literal['filters', 'min periods'] = 'min periods'
                        ) -> list[np.ndarray] | np.ndarray:
        detected_periods_filters = [
            np.abs(orbits[..., -1-period] - orbits[..., -1]) <= self.periodicity_tol
            for period in range(1, max_period + 1)
        ]
        if(return_type == 'filters'):
            return detected_periods_filters
        if(return_type != 'min periods'):
            raise ValueError(f'unsupported return type: "{return_type}"')
        detected_periods_filters = np.stack(detected_periods_filters, axis=-1)
        # https://numpy.org/doc/stable/reference/generated/numpy.argmax.html#numpy-argmax > returns > notes
        periods = np.argmax(detected_periods_filters, axis=-1)
        periods = np.where(np.any(detected_periods_filters, axis=-1), periods + 1, max_period + 1)
        periods = periods.min(axis=-1)
        return periods
    def determine_periodicities(self,
                                a: np.ndarray, b: np.ndarray, x_0: np.ndarray,
                                max_period: int = 1,
                                nb_initial_iterations: int = 0,
                                do_show_progress: bool = True,
                                return_type='min periods') -> list[np.ndarray] | np.ndarray:
        orbit_starts = self.iterate(a, b, x_0, nb_initial_iterations,
                                    do_show_progress=do_show_progress)
        orbits = self.compute_orbits(a, b, orbit_starts, max_period,
                                     do_show_progress=do_show_progress)
        return self.compute_periods(orbits,
                                    max_period=max_period,
                                    return_type=return_type)




