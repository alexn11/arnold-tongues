import numpy as np

from TongueDrawer import TongueDrawer

def test_setup_parameter_grid():
    options_domain = {
        'a_range': (0., 1.2),
        'b_range': (0.4, 1.),
    }
    options_image = {
        'width': 3,
        'height': 2,
    }
    tg = TongueDrawer('2x+T', options_domain=options_domain, options_image=options_image)
    tg.setup_parameter_grid()
    #expected_a_data = np.linspace(0., 1.2, num=3, endpoint=False)
    #expected_b_data = np.linspace(1., 0.4, num=2, endpoint=False)
    expected_a_data = [ 0., 0.4, 0.8, ]
    expected_b_data = [ 1., 0.7, ]
    expected_a_list = [
        [ expected_a_data[i], expected_a_data[i] ]
        for i in range(3)
    ]
    expected_b_list = [
        expected_b_data, expected_b_data, expected_b_data
    ]
    expected_a = np.array(expected_a_list)
    assert(np.allclose(tg._a, expected_a))
    expected_b = np.array(expected_b_list)
    assert(np.allclose(tg._b, expected_b))
    expected_parameter_grid = [
        [ [expected_a_data[i], expected_b_data[j]] for j in range(2) ]
        for i in range(3)
    ]
    assert(np.allclose(tg._parameter_grid, expected_parameter_grid))





















