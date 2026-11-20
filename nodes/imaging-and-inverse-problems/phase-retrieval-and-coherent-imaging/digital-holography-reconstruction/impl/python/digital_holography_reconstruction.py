# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/digital-holography-reconstruction/. The authors are listed in prov/JPPVSQ.jsonl.

"""Off-axis digital holography: sideband filtering, demodulation and refocusing.

Conventions:
- Images are n1 x n2 lists of rows, pixel (i, j) at y = i d and x = j d, on a
  periodic grid. The DFT is unnormalized forward with exp(-2 pi i j k / n)
  (imgkit). DFT index k stands for the signed index k if 2 k < n, else k - n.
- Time dependence exp(-i omega t): the plane wave with the spatial frequency
  f travels toward +z with the factor exp(2 pi i z sqrt(1 / lambda^2 - |f|^2)).
- The reference wave on the sensor is R = r exp(2 pi i (cy i / n1 + cx j / n2))
  with r > 0 and the integer carrier (cy, cx), a tilted plane wave.
- The hologram is h = |R + O|^2 = |R|^2 + |O|^2 + conj(R) O + R conj(O). The
  term conj(R) O is the object wave times exp(-2 pi i c . x), so its spectrum
  is the object spectrum moved to -c. That is the sideband we keep.

Cost: one forward and one inverse 2D DFT, O(n^2 log n) for n x n images with
n a power of two.
"""

import cmath
import math

from imgkit import dft2, idft2


def signed_index(k, n):
    """k if 2 k < n, else k - n."""
    return k if 2 * k < n else k - n


def transfer(n1, n2, d, wavelength, z):
    """The angular spectrum transfer function of free space, evanescent waves set to 0."""
    inv2 = 1.0 / (wavelength * wavelength)
    h = [[0j] * n2 for _ in range(n1)]
    for k in range(n1):
        fy = signed_index(k, n1) / (n1 * d)
        for l in range(n2):
            fx = signed_index(l, n2) / (n2 * d)
            w = inv2 - fx * fx - fy * fy
            if w > 0.0:
                h[k][l] = cmath.exp(2j * math.pi * z * math.sqrt(w))
    return h


def propagate(u, d, wavelength, z):
    """Angular spectrum propagation of the sampled field u by the distance z."""
    spec = dft2(u)
    h = transfer(len(u), len(u[0]), d, wavelength, z)
    return idft2([[s * t for s, t in zip(rs, rh)] for rs, rh in zip(spec, h)])


def reference_wave(n1, n2, r, carrier):
    """R = r exp(2 pi i (cy i / n1 + cx j / n2)) on the grid."""
    cy, cx = carrier
    return [[r * cmath.exp(2j * math.pi * (cy * i / n1 + cx * j / n2)) for j in range(n2)] for i in range(n1)]


def record_hologram(obj_at_sensor, r, carrier):
    """The intensity |R + O|^2 on the sensor (real numbers)."""
    ref = reference_wave(len(obj_at_sensor), len(obj_at_sensor[0]), r, carrier)
    return [[abs(a + b) ** 2 for a, b in zip(ra, ro)] for ra, ro in zip(ref, obj_at_sensor)]


def find_carrier(hologram, exclude):
    """The carrier, up to sign, from the largest spectral peak outside the central square.

    The central square |ky|, |kx| <= exclude holds |R|^2 and |O|^2. This
    assumes that the object spectrum peaks at zero frequency, as it does when
    the object wave has a strong unscattered part; then the two sidebands
    peak at -c and +c. The hologram is real, so its spectrum has
    |H(k)| = |H(-k)| and the two peaks are equally high: the data alone
    cannot tell c from -c. The peak with kx > 0, or ky > 0 when kx = 0, is
    returned. Choosing the wrong sign reconstructs the twin wave.
    """
    spec = dft2(hologram)
    n1, n2 = len(spec), len(spec[0])
    best, arg = -1.0, (0, 0)
    for k in range(n1):
        for l in range(n2):
            ky, kx = signed_index(k, n1), signed_index(l, n2)
            if abs(ky) <= exclude and abs(kx) <= exclude:
                continue
            if kx < 0 or (kx == 0 and ky < 0):
                continue
            v = abs(spec[k][l])
            if v > best:
                best, arg = v, (ky, kx)
    return arg


def reconstruct(hologram, carrier, band, r, d, wavelength, z):
    """The object wave at distance z before the sensor (z = 0 gives the wave on the sensor).

    carrier = (cy, cx) is the integer carrier of the reference, band = B the
    half-width of the square passband in DFT indices, r the reference
    amplitude. The sideband conj(R) O, centered at -c, is cut out, moved to
    the center, divided by r and propagated by -z.
    """
    n1, n2 = len(hologram), len(hologram[0])
    cy, cx = carrier
    spec = dft2(hologram)  # @line L1
    hz = transfer(n1, n2, d, wavelength, -z)
    out = [[0j] * n2 for _ in range(n1)]
    for k in range(n1):  # @line L2
        for l in range(n2):
            if abs(signed_index(k, n1)) <= band and abs(signed_index(l, n2)) <= band:  # @line L3
                out[k][l] = spec[(k - cy) % n1][(l - cx) % n2] / r  # @line L4
                out[k][l] *= hz[k][l]  # @line L5
    return idft2(out)  # @line L6
