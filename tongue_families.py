import numpy
import numpy as np

FloatOrArray = float | np.ndarray
two_pi = 2. * np.pi

def compute_mod_1(x: FloatOrArray) -> FloatOrArray:
    return numpy.mod(x, 1.)

def eval_tent(x: numpy.ndarray) -> FloatOrArray:
    return numpy.where(x <= 0.5, 2.*x, 2.*(1. - x) )

def eval_tent_mod_1(x: numpy.ndarray) -> FloatOrArray:
    return eval_tent(compute_mod_1(x))

def eval_diff_tent(x: numpy.ndarray) -> FloatOrArray:
    return numpy.where(x <= 0.5, 2. -2.)

def eval_lifted_doubling_plus_tent(a: FloatOrArray, b: FloatOrArray, x: FloatOrArray) -> FloatOrArray:
    #print(f'eval lifted 2x+T: a={a.shape}, b={b.shape}, x={x.shape}')
    #print(f'eval lifted 2x+T: y={(2. * x + a + b * eval_tent_mod_1(x)).shape}')
    return 2. * x + a + b * eval_tent_mod_1(x)

def eval_doubling_plus_tent(a: FloatOrArray, b: FloatOrArray, x: FloatOrArray) -> FloatOrArray:
    #print(f'eval 2x+T: a={a.shape}, b={b.shape}, x={x.shape}')
    y = eval_lifted_doubling_plus_tent (a, b, x)
    #print(f'eval 2x+T: y={y.shape}')
    return compute_mod_1(y)

def eval_diff_doubling_plus_tent(a: FloatOrArray, b: FloatOrArray, x: FloatOrArray) -> FloatOrArray:
    return 2. + b * eval_diff_tent(x)

def eval_lifted_dsm(a: FloatOrArray, b: FloatOrArray, x: FloatOrArray) -> FloatOrArray:
    return 2. * x + a - (b / numpy.pi) * numpy.sin(two_pi * x)

def eval_dsm(a, b, x: FloatOrArray):
    return compute_mod_1(eval_lifted_dsm(a, b, x)) 

def eval_lifted_double_dsm(a, b, x):
    return 2. * x + a - (b / two_pi) * numpy.sin(2. * two_pi * x)

def eval_double_dsm(a, b, x):
    return compute_mod_1(eval_lifted_double_dsm (a, b, x)) 

def evaluate_straight_sine(x: FloatOrArray):
  y = numpy.where(x <= 0.25, 4.*x, numpy.nan)
  y = numpy.where(numpy.isnan(y) & (x <= 0.75), 2. - 4. * x, 4. * x - 4.)
  return y

def compute_doubling_plus_straight_sine_critical_points(a, b):
  return [ 0., 0. ]

def evaluate_lifted_doubling_plus_straight_sine(a, b, x):
  return 2. * x + a + 0.5 * b * evaluate_straight_sine(x)

def eval_doubling_plus_straight_sine(a, b, x):
  return numpy.mod(evaluate_lifted_doubling_plus_straight_sine(a, b, x), 1.)

def eval_test_map(a, b, x):
   return np.mod(x + a - b, 1.)
