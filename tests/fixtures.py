import numpy as np

def generate_test_array(start=0., end=1., size: int = 3) -> np.ndarray:
    return np.linspace(start, end, num=size, endpoint=False)


def generate_params_fixed(n_a = 3, n_b=2) -> tuple[np.ndarray, np.ndarray]:
    a = np.array([
        [0., 0.],
        [0.567, 0.567],
        [0.678, 0.678],
    ])
    b = np.array([
        [1.0, 0.789,],
        [1.0, 0.789,],
        [1.0, 0.789,],
    ])
    return a[:n_a, :n_b], b[:n_a, :n_b]
