import numpy as np
from .tensor_data import (
    count,
    index_to_position,
    broadcast_index,
    shape_broadcast,
    MAX_DIMS,
)
from numba import njit, prange

count = njit()(count)
index_to_position = njit()(index_to_position)
broadcast_index = njit()(broadcast_index)


def tensor_map(fn):
    """
    Higher-order tensor map function.

    Args:
        fn: function mappings floats-to-floats to apply.
        out (array): storage for out tensor.
        out_shape (array): shape for out tensor.
        out_strides (array): strides for out tensor.
        in_storage (array): storage for in tensor.
        in_shape (array): shape for in tensor.
        in_strides (array): strides for in tensor.
    """

    def _map(out, out_shape, out_strides, in_storage, in_shape, in_strides):
        # TODO: Implement for Task GN3.
        raise NotImplementedError('Need to implement for Task GN3')

    return njit(parallel=True)(_map)


def map(fn):
    f = tensor_map(njit()(fn))

    def ret(a, out=None):
        if out is None:
            out = a.zeros(a.shape)
        f(*out.tuple(), *a.tuple())
        return out

    return ret


def tensor_zip(fn):
    """
    Higher-order tensor zipWith (or map2) function.

    Args:
        fn: function mappings two floats to float to apply.
        out (array): storage for `out` tensor.
        out_shape (array): shape for `out` tensor.
        out_strides (array): strides for `out` tensor.
        a_storage (array): storage for `a` tensor.
        a_shape (array): shape for `a` tensor.
        a_strides (array): strides for `a` tensor.
        b_storage (array): storage for `b` tensor.
        b_shape (array): shape for `b` tensor.
        b_strides (array): strides for `b` tensor.
    """

    def _zip(out, out_shape, out_strides, a, a_shape, a_strides, b, b_shape, b_strides):
        # TODO: Implement for Task GN3.
        raise NotImplementedError('Need to implement for Task GN3')

    return njit(parallel=True)(_zip)


def zip(fn):

    f = tensor_zip(njit()(fn))

    def ret(a, b):
        c_shape = shape_broadcast(a.shape, b.shape)
        out = a.zeros(c_shape)
        f(*out.tuple(), *a.tuple(), *b.tuple())
        return out

    return ret


def tensor_reduce(fn):
    """
    Higher-order tensor reduce function.

    Args:
        fn: reduction function mapping two floats to float.
        out (array): storage for `out` tensor.
        out_shape (array): shape for `out` tensor.
        out_strides (array): strides for `out` tensor.
        a_storage (array): storage for `a` tensor.
        a_shape (array): shape for `a` tensor.
        a_strides (array): strides for `a` tensor.
        reduce_shape (array): shape of reduction (1 for dimension kept, shape value for dimensions summed out)
        reduce_size (int): size of reduce shape
    """

    def _reduce(
        out, out_shape, out_strides, a, a_shape, a_strides, reduce_shape, reduce_size
    ):
        # TODO: Implement for Task GN3.
        raise NotImplementedError('Need to implement for Task GN3')

    return njit(parallel=True)(_reduce)


def reduce(fn, start=0.0):
    f = tensor_reduce(njit()(fn))

    def ret(a, dims=None, out=None):
        if out is None:
            out_shape = list(a.shape)
            for d in dims:
                out_shape[d] = 1
            # Other values when not sum.
            out = a.zeros(tuple(out_shape))
            out._tensor._storage[:] = start

        diff = len(a.shape) - len(out.shape)

        reduce_shape = []
        reduce_size = 1
        for i, s in enumerate(a.shape):
            if i < diff or out.shape[i - diff] == 1:
                reduce_shape.append(s)
                reduce_size *= s
            else:
                reduce_shape.append(1)
        # assert len(out.shape) == len(a.shape)
        f(*out.tuple(), *a.tuple(), np.array(reduce_shape), reduce_size)
        return out

    return ret


@njit(parallel=True)
def tensor_matrix_multiply(
    out, out_shape, out_strides, a, a_shape, a_strides, b, b_shape, b_strides
):

    # TODO: Implement for Task 3.1.
    raise NotImplementedError('Need to implement for Task 3.1')


def matrix_multiply(a, b):
    # Create out shape
    ls = list(a.shape)
    assert a.shape[-1] == b.shape[-2]
    ls[-1] = b.shape[-1]
    out = a.zeros(tuple(ls))

    # Call main function
    tensor_matrix_multiply(*out.tuple(), *a.tuple(), *b.tuple())
    return out


class FastOps:
    map = map
    zip = zip
    reduce = reduce
    matrix_multiply = matrix_multiply