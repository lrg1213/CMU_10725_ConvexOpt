import cffi

ffi = cffi.FFI()
ffi.cdef('void prox_dp_C(int n, double *y, double lam, double *theta);')

ffi.set_source('_prox', r'''
extern "C" {
    void prox_dp_C(int n, double *y, double lam, double *theta);
}
''', sources=['prox.cpp'], source_extension='.cpp')

ffi.compile(verbose=True)

import _prox
import numpy as np

def prox_dp(n, y, lam, theta):
    '''
    Dynamic programming algorithm for the 1d fused lasso problem:
    \min_\theta \frac{1}{2} \sum_i (y_i - \theta_i)^2 + 
                            \lambda \sum_i |\theta_i - \theta_{i+1}|
    (Ryan's implementation of Nick Johnson's algorithm)

    Input:
        n: int
        y: np.float64 array of shape (n,)
        lam: float

    Output:
        theta: np.float64 array of shape (n,)
    '''
    assert y.dtype == np.float64 and y.shape[0] == n
    assert theta.dtype == np.float64 and theta.shape[0] == n

    _prox.lib.prox_dp_C(n, ffi.from_buffer('double[]', y), lam, ffi.from_buffer('double[]', theta))
