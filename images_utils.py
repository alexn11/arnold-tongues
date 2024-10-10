from matplotlib import colormaps
import numpy
import numpy as np
from PIL import Image


def save_image(image_name: str,
               pixels: np.ndarray,
               do_flip: bool = False,
               silent: bool=False):
   rgba8_pixels = np.round(255 * pixels).astype(np.uint8).transpose(1, 0, 2)
   image = Image.fromarray(rgba8_pixels)
   if (do_flip):
      image = image.transpose(Image.FLIP_TOP_BOTTOM)
   if(not image_name.endswith('.png')):
      image_name = image_name + '.png'
   if(not silent):
      print(f'saving image to: "{image_name}"')
   image.save(image_name, "PNG")


def convert_point_coordinates_to_image_coordinates(
                 image_width,
                 image_height,
                 min_x,
                 max_x,
                 min_y,
                 max_y,
                 point_list: numpy.ndarray):
    def is_outside_domain(p):
       return (p[:,0] < min_x) | (p[:,0] >= max_x) | (p[:,1] < min_y) | (p[:,1] >= max_y)
    def is_outside_image(ix, iy):
       return (ix >= image_width) | (iy >= image_height)
    def project(x, y):
       x: numpy.ndarray
       ix = numpy.round(x_convert_factor * (x - min_x))
       iy = numpy.round(image_height - 1 - y_convert_factor * (y - min_y))
       return ix, iy
    x_convert_factor = image_width / (max_x - min_x)
    y_convert_factor = image_height / (max_y - min_y)
    image_point_list = point_list[~is_outside_domain(point_list)]
    image_point_list[:, 0], image_point_list[:, 1] = project(image_point_list[:, 0], image_point_list[:, 1])
    image_point_list = image_point_list[~is_outside_image(image_point_list[:, 0], image_point_list[:, 1])]
    image_point_list = image_point_list.astype(int)
    return image_point_list


def draw_points(image_width,
                image_height,
                background_color,
                point_color,
                min_x,
                max_x,
                min_y,
                max_y,
                point_list: numpy.ndarray):
    pixels = numpy.zeros((image_width, image_height, 4))
    pixels[:,:,:] = background_color
    points_to_draw = convert_point_coordinates_to_image_coordinates(image_width, image_height,
                                                                    min_x, max_x, min_y, max_y,
                                                                    point_list)
    #print(f'point to draw: {points_to_draw.shape}')
    pixels[points_to_draw[:,0], points_to_draw[:,1]] = point_color
    return pixels


def create_grid(x_start, x_end, y_start, y_end,
                width, height,
                output_shape='grid',
                output_type='complex',
                _indexing='ij'):
   x = numpy.linspace(x_start, x_end, endpoint=False, num=width)
   y = numpy.linspace(y_end, y_start, endpoint=False, num=height)
   if(output_shape == 'axes'):
      return x, y
   elif(output_shape != 'grid'):
      raise ValueError(f'unexpected output shape specification: "{output_shape}"')
   x, y = numpy.meshgrid(x, y, indexing=_indexing)
   if(output_type == 'complex'):
      grid = x + 1.j * y
   elif(output_type == 'real'):
      grid = numpy.zeros((width, height, 2))
      grid[..., 0] = x
      grid[..., 1] = y
   else:
      raise ValueError(f'unsupported output type: "{output_type}"')
   return grid


def convert_values_to_colours(values: numpy.ndarray[int],
                              colours: numpy.ndarray,
                              shading_values: None | numpy.ndarray = None,
                              max_shading_value: None | int = None) -> numpy.ndarray:
   #print(f'values: {values.shape} ({values.dtype})')
   #print(f'values FLAT: {values.flatten().shape} ({values.dtype})')
   #image = colours[values.flatten()].reshape(values.shape)
   image = colours[values]
   if(shading_values is not None):
      if(max_shading_value is None):
         max_shading_value = shading_values.max()
      for c in range(image.shape[-1] - 1):
         image[..., c] = image[..., c] * shading_values / max_shading_value
   return image

def make_palette(nb_colours: int, colour_map_name='magma') -> list[list]:
   colour_map = colormaps[colour_map_name]
   return [ list(colour_map(i * 256 / nb_colours)) for i in range(nb_colours) ]







