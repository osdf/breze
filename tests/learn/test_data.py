# -*- coding: utf-8 -*-

import numpy as np
import scipy
import nose.tools

from breze.learn.data import (
    shuffle, padzeros, windowify, interpolate, skip, one_hot)
from breze.learn.utils import theano_floatx


@nose.tools.nottest
def make_test_data():
    return theano_floatx(scipy.random.random((13, 5)))[0]


def test_shuffle():
    """Testing whether shuffle does not crash."""
    D = make_test_data()
    before = D.tolist()
    shuffle(D)
    after = D.tolist()
    before.sort()
    after.sort()
    assert after == before, "Shuffle mutated data."


def test_padzeros():
    """Test if padding with zeros works fine."""
    seqs = [
        scipy.array((1, 1)).reshape(2, 1),
        scipy.array((1, 1, 1, 1, 1)).reshape(5, 1),
        scipy.array((1, 1, 1, 1, 1, 1, 1)).reshape(7, 1),
    ]

    seqs = padzeros(seqs)

    assert (seqs[0] == scipy.array((0, 0, 0, 0, 0, 1, 1)).reshape(7, 1)).all(), \
            "padding went wrong"
    assert (seqs[1] == scipy.array((0, 0, 1, 1, 1, 1, 1)).reshape(7, 1)).all(), \
            "padding went wrong"
    assert (seqs[2] == scipy.array((1, 1, 1, 1, 1, 1, 1)).reshape(7, 1)).all(), \
            "padding went wrong"


def test_skip():
    """Test if only keeping every n'th sample works."""
    X = scipy.vstack((scipy.arange(25), scipy.arange(25)))
    X_ = skip(X, 2, 5)
    print X_
    des = scipy.vstack((scipy.array([0, 1, 2, 3, 4, 10, 11, 12, 13, 14, 20, 21, 22, 23 ,24]),
                       scipy.array([0, 1, 2, 3, 4, 10, 11, 12, 13, 14, 20, 21, 22, 23 ,24])))

    assert (X_ == des).all(), 'wrong result'


def test_windowify():
    """Test if windowifying sequences works."""
    x1 = scipy.array([[1], [2], [3], [4]])
    x2 = scipy.array([[10], [11], [12]])
    X = [x1, x2]
    W = windowify(X, 2)
    assert W.shape == (5, 2, 1), "result has wrong shape: %s" % str(W.shape)
    desired = \
        scipy.array([[  1.,   2.],
                     [  2.,   3.],
                     [  3.,   4.],
                     [ 10.,  11.],
                     [ 11.,  12.]])[:, :, scipy.newaxis]
    assert (W == desired).all(), "result has wrong entries"


def test_windowify_offset():
    """Test if windowifying sequences works with an offset."""
    x1 = scipy.array([[1], [2], [3], [4], [5]])
    x2 = scipy.array([[10], [11], [12], [13]])
    X = [x1, x2]
    W = windowify(X, 2, 2)
    assert W.shape == (4, 2, 1), "result has wrong shape: %s" % str(W.shape)
    desired = \
        scipy.array([[  1.,   2.],
                     [  3.,   4.],
                     [ 10.,  11.],
                     [ 12.,  13.]])[:, :,scipy.newaxis]
    assert (W == desired).all(), "result has wrong entries"


def test_interpolate():
    """Test if interpolation of sequential data works."""
    x = scipy.array([[0, 1, 2],
                     [3, 4, 5],
                     [6, 7, 8]])
    desired = scipy.array([[ 0. ,  1. ,  2. ],
                           [ 1.2,  2.2,  3.2],
                           [ 2.4,  3.4,  4.4],
                           [ 3.6,  4.6,  5.6],
                           [ 4.8,  5.8,  6.8],
                           [ 6. ,  7. ,  8. ]])
    x_ = interpolate(x, 2)
    assert np.allclose(x_, desired), "result has wrong values"


def test_one_hot():
    arr = np.array([0, 1, 2, 1, 3])
    desired = np.zeros((5, 4))
    for i, j in enumerate(arr):
        desired[i, j] = 1

    assert np.allclose(desired, one_hot(arr))
    assert np.allclose(desired, one_hot(arr, 4))
