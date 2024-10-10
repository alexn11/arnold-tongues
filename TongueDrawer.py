
import numpy as np

from images_utils import create_grid, convert_values_to_colours, save_image, make_palette
from TongueIterator import TongueIterator

default_is_periodic_colours = [
    [1, 0, 0, 1],
    [0, 1, 1, 1],
]


default_type_colors = [
    [.1, 1., 0.2, 1.],
    [.1, 0.2, 1., 1.],
    [0.66, 0.2, 0.66, 1.],
    [0.66, 0.66, 0.2, 1.],
    [0.77, 0.77, 0., 1.],
    [1., 1., 1., 1.],
    [1., 0, 0, 1.],
    [0.66, 0.2, 0.66, 1.],
    [0.66, 0.66, 0.2, 1.],
    [0.33, 0.12, 0.19, 1.],
    [0.67, 0.247, 0.89, 1.],
    [0.12, 0.87, 0.56, 1],
]


class TongueDrawer:
    def __init__(self, family_name: str,
                 options_dynamics: dict = {},
                 options_domain: dict = {},
                 options_image: dict = {},
                 options_other: dict = {}):
        self.family = family_name
        self.iterator = TongueIterator(family_name, options_dynamics=options_dynamics)
        self.set_options(options_domain=options_domain,
                         options_dynamics=options_dynamics,
                         options_image=options_image,
                         options_other=options_other)
    def set_domain_options(self, options_domain):
        self.a_start, self.a_end = options_domain.get('a_range', (0., 1.))
        self.b_start, self.b_end = options_domain.get('b_range', (0.5, 1.))
        self.b = options_domain.get('b', 0.875)
    def set_dynamics_options(self, options_dynamics: dict):
        self.default_starting_point = options_dynamics.get('default_starting_point', 0.2)
        self.nb_starting_points = options_dynamics.get('nb_starting_points', 1)
        self.nb_initial_iterations = options_dynamics.get('nb_initial_iterations', 0)
        self.max_period = options_dynamics.get('max_period', 1)
    def set_other_options(self, options_other: dict):
        self.do_show_progress = options_other.get('show_progress', True)
        self.do_output_images_as_stream = options_other.get('stream', False)
    def set_image_options(self, options_image: dict):
        self.image_width = options_image.get('width', 400)
        self.image_height = options_image.get('height', 200)
        self.image_names = options_image.get('image_names',
                                        {
                                            'is_periodic': 'is-periodic',
                                            'periods': 'periods',
                                        })
        self.image_is_periodic_colours = np.array(options_image.get('is_periodic_colours', default_is_periodic_colours))
        image_periods_colours = options_image.get('periods_colours')
        if(image_periods_colours is None):
            if(len(default_type_colors) > self.max_period):
                image_periods_colours = default_type_colors
            else:
                image_periods_colours = make_palette(self.max_period + 1)
        elif(isinstance(image_periods_colours, str)):
            image_periods_colours = make_palette(self.max_period + 1, colour_map_name=image_periods_colours)
        if(len(image_periods_colours) <= self.max_period):
            raise ValueError(f'not enough colours ({len(image_periods_colours)}) for max period = {self.max_period}')
        self.image_periods_colours = np.array(image_periods_colours)
    def set_options(self,
                    options_domain: dict = {},
                    options_dynamics: dict = {},
                    options_image: dict = {},
                    options_other: dict = {}):
        self.set_domain_options(options_domain)
        self.set_dynamics_options(options_dynamics)
        self.set_image_options(options_image)
        self.set_other_options(options_other)
    def setup_parameter_grid(self,):
        parameter_grid = create_grid(self.a_start, self.a_end,
                                     self.b_start, self.b_end,
                                     self.image_width, self.image_height,
                                     output_type='real',)
        print(f'parameter grid (na, nb, 2): {parameter_grid.shape}')
        self._parameter_grid = parameter_grid
        self._a = self._parameter_grid[..., 0]
        self._b = self._parameter_grid[..., 1]
    def compute_starting_points(self,) -> np.ndarray:
        starting_points = self.iterator.setup_starting_points(
                                            self._a, self._b,
                                            self.default_starting_point,
                                            nb_starting_points=self.nb_starting_points)
        print(f'starting_points (na, nb, Ns): {starting_points.shape}')
        return starting_points
    def compute_fates_and_periods(self, ):
        starting_points = self.compute_starting_points()
        periods = self.iterator.determine_periodicities(self._a, self._b, starting_points,
                                                        max_period=self.max_period,
                                                        nb_initial_iterations=self.nb_initial_iterations,
                                                        do_show_progress=self.do_show_progress,
                                                        return_type='min periods')
        print(f'periods detected (na, nb, Ns): {periods.shape}')
        parameter_fates: np.ndarray = (periods <= self.max_period).astype(int)
        #parameter_fates = np.where(periods <= self.max_period, axis=-1).astype(int)
        print(f'parameter fates (na, nb): {parameter_fates.shape} - dtype={parameter_fates.dtype}')
        self._parameter_fates = parameter_fates
        #periods = periods.min(axis=-1)
        print(f'periods (na, nb): {periods.shape} - dtype={periods.dtype}')
        self._periods = periods
    def compute_the_tongues(self,):
        self.setup_parameter_grid()
        self.compute_fates_and_periods()
    def draw_is_periodic(self,):
        image = convert_values_to_colours(self._parameter_fates,
                                          colours=self.image_is_periodic_colours,)
        return save_image(self.image_names['is_periodic'], image, as_stream=self.do_output_images_as_stream)
    def draw_periods(self, ):
        image = convert_values_to_colours(self._parameter_fates,
                                          self.image_periods_colours,
                                          shading_values = self.max_period + 1 - self._periods,
                                          max_shading_value=self.max_period)
        return save_image(self.image_names['periods'], image, as_stream=self.do_output_images_as_stream)
    def draw_the_tongues(self, do_compute=True) -> dict:
        if(do_compute):
            self.compute_the_tongues()
        image_outputs = {}
        if('is_periodic' in self.image_names):
            image_is_periodic = self.draw_is_periodic()
            image_outputs['is_periodic'] = image_outputs
        if('periods' in self.image_names):
            image_periods = self.draw_periods()
            image_outputs['periods'] = image_periods
        return image_outputs
