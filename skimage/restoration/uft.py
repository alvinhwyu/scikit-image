# -*- coding: utf-8 -*-
# uft.py --- Unitary fourier transform

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Function of unitary fourier transform and utilities

This module implement unitary fourier transform, that is ortho-normal
transform. They are especially and useful for convolution [1]: they
respect the Parseval equality, the value of the null frequency is
equal to

.. math::  \frac{1}{\sqrt{n}} \sum_i x_i

or the Fourier tranform have the same energy than the original image
(see ``image_quad_norm`` function). The transform is applied from the
last axes for performance reason (c order array). You may use directly
the numpy.fft module for more sophisticated purpose.

References
----------
.. [1] B. R. Hunt "A matrix theory proof of the discrete convolution
       theorem", IEEE Trans. on Audio and Electroacoustics,
       vol. au-19, no. 4, pp. 285-288, dec. 1971

"""

from __future__ import division, print_function

import numpy as np

__credits__ = ["François Orieux"]
__license__ = "mit"
__version__ = "1.0.0"
__maintainer__ = "Francois Orieux"
__keywords__ = "fft"


def ufftn(inarray, dim=None):
    """N-dim unitary Fourier transform

    Parameters
    ----------
    inarray : ndarray
        The array to transform.
    dim : int, optional
        The ``dim`` last axis along wich to compute the transform. All
        axes by default.

    Returns
    -------
    outarray : ndarray (same shape than inarray)
        The unitary N-D Fourier transform of ``inarray``.

    Examples
    --------
    >>> input = np.ones((3, 3, 3))
    >>> output = ufftn(input)
    >>> np.allclose(np.sum(input) / np.sqrt(input.size), output[0, 0, 0])
    True
    >>> output.shape
    (3, 3, 3)
    """
    if dim is None:
        dim = inarray.ndim
    outarray = np.fft.fftn(inarray, axes=range(-dim, 0))
    return outarray / np.sqrt(np.prod(inarray.shape[-dim:]))


def uifftn(inarray, dim=None):
    """N-dim unitary inverse Fourier transform

    Parameters
    ----------
    inarray : ndarray
        The array to transform.
    dim : int, optional
        The ``dim`` last axis along wich to compute the transform. All
        axes by default.

    Returns
    -------
    outarray : ndarray (same shape than inarray)
        The unitary inverse N-D Fourier transform of ``inarray``.

    Examples
    --------
    >>> input = np.ones((3, 3, 3))
    >>> output = uifftn(input)
    >>> np.allclose(np.sum(input) / np.sqrt(input.size), output[0, 0, 0])
    True
    >>> output.shape
    (3, 3, 3)
    """
    if dim is None:
        dim = inarray.ndim
    outarray = np.fft.ifftn(inarray, axes=range(-dim, 0))
    return outarray * np.sqrt(np.prod(inarray.shape[-dim:]))


def urfftn(inarray, dim=None):
    """N-dim real unitary Fourier transform

    This transform consider the Hermitian property of the transform on
    real input

    Parameters
    ----------
    inarray : ndarray
        The array to transform.
    dim : int, optional
        The ``dim`` last axis along wich to compute the transform. All
        axes by default.

    Returns
    -------
    outarray : ndarray (the last dim as  N / 2 + 1 lenght)
        The unitary N-D real Fourier transform of ``inarray``.

    Notes
    -----
    The ``urfft`` functions assume an input array of real
    values. Consequently, the output have an Hermitian property and
    redondant values are not computed and returned.

    Examples
    --------
    >>> input = np.ones((5, 5, 5))
    >>> output = urfftn(input)
    >>> np.allclose(np.sum(input) / np.sqrt(input.size), output[0, 0, 0])
    True
    >>> output.shape
    (5, 5, 3)
    """
    if dim is None:
        dim = inarray.ndim
    outarray = np.fft.rfftn(inarray, axes=range(-dim, 0))
    return outarray / np.sqrt(np.prod(inarray.shape[-dim:]))


def uirfftn(inarray, dim=None, shape=None):
    """N-dim real unitary Fourier transform

    This transform consider the Hermitian property of the transform
    from complex to real real input.

    Parameters
    ----------
    inarray : ndarray
        The array to transform.
    dim : int, optional
        The ``dim`` last axis along wich to compute the transform. All
        axes by default.
    shape : tuple of int
        The shape of the output. The shape of ``rfft`` is ambiguous in
        case of odd shape. In this case, the parameter must be
        used. see ``np.fft.irfftn``.

    Returns
    -------
    outarray : ndarray
        The unitary N-D inverse real Fourier transform of ``inarray``.

    Notes
    -----
    The ``uirfft`` function assume that output array is of real
    values. Consequently, the input is assumed of having an Hermitian
    property and redondant values are implicit.

    Examples
    --------
    >>> input = np.ones((5, 5, 5))
    >>> output = uirfftn(urfftn(input), shape=input.shape)
    >>> np.allclose(input, output)
    True
    >>> output.shape
    (5, 5, 5)
    """
    if dim is None:
        dim = inarray.ndim
    outarray = np.fft.irfftn(inarray, shape, axes=range(-dim, 0))
    return outarray * np.sqrt(np.prod(outarray.shape[-dim:]))


def ufft2(inarray):
    """2-dim unitary Fourier transform

    Compute the Fourier transform on the last 2 axes.

    Parameters
    ----------
    inarray : ndarray
        The array to transform.

    Returns
    -------
    outarray : ndarray (same shape than inarray)
        The unitary 2-D Fourier transform of ``inarray``.

    See Also
    --------
    uifft2, ufftn, urfftn

    Examples
    --------
    >>> input = np.ones((10, 128, 128))
    >>> output = ufft2(input)
    >>> np.allclose(np.sum(input[1, ...]) / np.sqrt(input[1, ...].size), output[1, 0, 0])
    True
    >>> output.shape
    (10, 128, 128)
    """
    return ufftn(inarray, 2)


def uifft2(inarray):
    """2-dim inverse unitary Fourier transform

    Compute the inverse Fourier transform on the last 2 axes.

    Parameters
    ----------
    inarray : ndarray
        The array to transform.

    Returns
    -------
    outarray : ndarray (same shape than inarray)
        The unitary 2-D inverse Fourier transform of ``inarray``.

    See Also
    --------
    uifft2, uifftn, uirfftn

    Examples
    --------
    >>> input = np.ones((10, 128, 128))
    >>> output = uifft2(input)
    >>> np.allclose(np.sum(input[1, ...]) / np.sqrt(input[1, ...].size), output[0, 0, 0])
    True
    >>> output.shape
    (10, 128, 128)
    """
    return uifftn(inarray, 2)


def urfft2(inarray):
    """2-dim real unitary Fourier transform

    Compute the real Fourier transform on the last 2 axes. This
    transform consider the Hermitian property of the transform from
    complex to real real input.

    Parameters
    ----------
    inarray : ndarray
        The array to transform.

    Returns
    -------
    outarray : ndarray (the last dim as (N - 1) *2 lenght)
        The unitary 2-D real Fourier transform of ``inarray``.

    See Also
    --------
    ufft2, ufftn, urfftn

    Examples
    --------
    >>> input = np.ones((10, 128, 128))
    >>> output = urfft2(input)
    >>> np.allclose(np.sum(input[1,...]) / np.sqrt(input[1,...].size), output[1, 0, 0])
    True
    >>> output.shape
    (10, 128, 65)
    """
    return urfftn(inarray, 2)


def uirfft2(inarray, shape=None):
    """2-dim real unitary Fourier transform

    Compute the real inverse Fourier transform on the last 2 axes.
    This transform consider the Hermitian property of the transform
    from complex to real real input.

    Parameters
    ----------
    inarray : ndarray
        The array to transform.

    Returns
    -------
    outarray : ndarray (the last dim as (N - 1) *2 lenght)
        The unitary 2-D inverse real Fourier transform of ``inarray``.

    See Also
    --------
    urfft2, uifftn, uirfftn

    Examples
    --------
    >>> input = np.ones((10, 128, 128))
    >>> output = uirfftn(urfftn(input), shape=input.shape)
    >>> np.allclose(input, output)
    True
    >>> output.shape
    (10, 128, 128)
    """
    return uirfftn(inarray, 2, shape=shape)


def image_quad_norm(inarray):
    """Return quadratic norm of images in Fourier space

    This function detect if the image suppose the hermitian property.

    Parameters
    ----------
    inarray : ndarray
        The images are supposed to be in the last two axes

    Returns
    -------
    norm : float
        The quadratic norm of ``inarray``.

    Examples
    --------
    >>> input = np.ones((5, 5))
    >>> image_quad_norm(ufft2(input)) == np.sum(np.abs(input)**2)
    True
    >>> image_quad_norm(ufft2(input)) == image_quad_norm(urfft2(input))
    True
    """
    # If there is an hermitian symmetry
    if inarray.shape[-1] != inarray.shape[-2]:
        return 2 * np.sum(np.sum(np.abs(inarray)**2, axis=-1), axis=-1) - \
            np.sum(np.abs(inarray[..., 0])**2, axis=-1)
    else:
        return np.sum(np.sum(np.abs(inarray)**2, axis=-1), axis=-1)


def ir2tf(imp_resp, shape, dim=None, is_real=True):
    """Compute the transfer function of IR

    This function make the necessary correct zero-padding, zero
    convention, correct fft2 etc... to compute the transfer function
    of IR. To use with unitary Fourier transform for the signal (ufftn
    or equivalent).

    Parameters
    ----------
    imp_resp : ndarray
       The impulsionnal responses.
    shape : tuple of int
       A tuple of integer corresponding to the target shape of the
       tranfert function.
    dim : int, optional
        The ``dim`` last axis along wich to compute the transform. All
        axes by default.
    is_real : boolean (optionnal, default True)
       If True, imp_resp is supposed real and the hermissian property
       is used with rfftn Fourier transform.

    Returns
    -------
    y : complex ndarray
       The tranfert function of shape ``shape``.

    See Also
    --------
    ufftn, uifftn, urfftn, uirfftn

    Examples
    --------
    >>> np.all(np.array([[4, 0], [0, 0]]) == ir2tf(np.ones((2, 2)), (2, 2)))
    True
    >>> ir2tf(np.ones((2, 2)), (512, 512)).shape == (512, 257)
    True
    >>> ir2tf(np.ones((2, 2)), (512, 512), is_real=False).shape == (512, 512)
    True

    Notes
    -----
    The input array can be composed of multiple dimentionnal IR with
    an arbitraru number of IR. The individual IR must be accesed
    through first axes. The last ``dim`` axes of space definition. The
    ``dim`` parameter must be specified to compute the transform only
    along these last axes.
    """
    if not dim:
        dim = imp_resp.ndim
    # Zero padding and fill
    irpadded = np.zeros(shape)
    irpadded[tuple([slice(0, s) for s in imp_resp.shape])] = imp_resp
    # Roll for zero convention of the fft to avoid the phase
    # problem. Work with odd and even size.
    for axis, axis_size in enumerate(imp_resp.shape):
        if axis >= imp_resp.ndim - dim:
            irpadded = np.roll(irpadded,
                               shift=-int(np.floor(axis_size / 2)),
                               axis=axis)
    if is_real:
        return np.fft.rfftn(irpadded, axes=range(-dim, 0))
    else:
        return np.fft.fftn(irpadded, axes=range(-dim, 0))


def laplacian(ndim, shape, is_real=True):
    """Return the transfert function of the laplacian

    Laplacian is the second order difference, on line and column.

    Parameters
    ----------
    ndim : int
        The dimension of the laplacian
    shape : tuple, shape
        The support on which to compute the transfert function
    is_real : boolean (optionnal, default True)
       If True, imp_resp is supposed real and the hermissian property
       is used with rfftn Fourier transform to return the transfert
       function.

    Returns
    -------
    tf : array_like, complex
        The transfert function
    impr : array_like, real
        The laplacian

    Examples
    --------
    >>> tf, ir = laplacian(2, (32, 32))
    >>> np.all(ir == np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]]))
    True
    >>> np.all(tf == ir2tf(ir, (32, 32)))
    True
    """
    impr = np.zeros([3] * ndim)
    for dim in range(ndim):
        idx = tuple([slice(1, 2)] * dim +
                    [slice(None)] +
                    [slice(1, 2)] * (ndim - dim - 1))
        impr[idx] = np.array([-1.0,
                              0.0,
                              -1.0]).reshape([-1 if i == dim else 1
                                              for i in range(ndim)])
    impr[([slice(1, 2)] * ndim)] = 2.0 * ndim
    return ir2tf(impr, shape, is_real=is_real), impr
