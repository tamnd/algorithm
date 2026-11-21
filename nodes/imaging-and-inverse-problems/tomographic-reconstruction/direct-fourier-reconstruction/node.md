---
tag: 1BAE5C
kind: algorithm
slug: direct-fourier-reconstruction
name: Direct Fourier reconstruction
aliases:
- Fourier reconstruction for tomography
area: imaging-and-inverse-problems/tomographic-reconstruction
level: core
summary: Reconstruct a CT slice from the 1D transforms of its projections. Place them on radial lines, interpolate onto a Cartesian grid and take an inverse 2D FFT.
solves: [tomographic-reconstruction-problem]
model: real-ram
complexity:
  vars: {a: the number of projection angles, d: the number of detector bins, n: the side of the n x n output image}
  time: {worst: "O(a d log d + n^2 log n)"}
  space: {extra: "O(a d + n^2)"}
properties: {deterministic: true, in_place: false, recursive: false, iterative: false, linear: true}
history:
  year: 1956
  people: [R. N. Bracewell]
  note: Bracewell reconstructed radio sources from strip scans through the 2D Fourier transform. Stark and coworkers studied the polar-to-Cartesian interpolation for CT in 1981.
prereqs: [radon-transform, sinogram, fourier-slice-theorem]
see_also: [filtered-back-projection, nonuniform-fft, density-compensation, polar-format-algorithm, multidimensional-fft, bilinear-interpolation, single-particle-reconstruction, shepp-logan-phantom]
sources:
  - paper: doi:10.1071/PH560198
    title: R. N. Bracewell, Strip integration in radio astronomy, Australian Journal of Physics 9, 1956
    locator: pp. 198 to 217
  - paper: doi:10.1109/TASSP.1981.1163528
    title: H. Stark, J. W. Woods, I. Paul and R. Hingorani, Direct Fourier reconstruction in computer tomography, IEEE Transactions on Acoustics, Speech, and Signal Processing 29(2), 1981
    locator: pp. 237 to 245 (the interpolation from the polar grid to the Cartesian grid)
  - paper: doi:10.1109/TMI.1985.4307723
    title: J. D. O'Sullivan, A fast sinc function gridding algorithm for Fourier inversion in computer tomography, IEEE Transactions on Medical Imaging 4(4), 1985
    locator: pp. 200 to 207
  - book: isbn:9780898714944
    title: A. C. Kak and M. Slaney, Principles of Computerized Tomographic Imaging, SIAM Classics in Applied Mathematics 33, 2001
    locator: Chapter 3, Section 3.2, equation 22 and Fig. 3.7, pp. 58 to 59 (the method and its interpolation error), Section 3.3.1, p. 62 (the comparison with filtered back-projection), and Section 3.7, p. 110 (the history)
  - book: isbn:9780898714937
    title: F. Natterer, The Mathematics of Computerized Tomography, SIAM Classics in Applied Mathematics 32, 2001
    locator: Section V.2, Fourier reconstruction
---

Direct Fourier reconstruction solves the [tomographic reconstruction problem](/tomographic-reconstruction-problem/) in the Fourier domain. By the [Fourier slice theorem](/fourier-slice-theorem/), the 1D Fourier transform of each projection in the [sinogram](/sinogram/) gives the 2D Fourier transform of the image on one line through the origin. The method computes these lines with the [fast Fourier transform](/fast-fourier-transform/), interpolates the values from the polar grid onto a Cartesian grid, and takes one inverse 2D FFT. With $a$ angles, $d$ detector bins and an $n \times n$ image it takes $O(a d \log d + n^2 \log n)$ time. The interpolation step is its weak point, and [filtered back-projection](/filtered-back-projection/) usually gives better images at a higher cost.

## In plain words

Each projection of the object tells you one line of the object's frequency picture. If you take the projections at many angles, you get many lines through the center of the frequency plane, like the spokes of a wheel. When you know the whole frequency plane, one inverse transform gives back the object.

The fast inverse transform needs the values on a square grid, but the spokes give them on circles and rays. So the method estimates each grid value from the nearest spoke values. Near the center the spokes are close together and the estimate is good. Far from the center the spokes spread apart, and the estimates of the fine detail get worse.

## The problem

The data is a sinogram $P[k][j]$ for $k = 0, \ldots, a - 1$ and $j = 0, \ldots, d - 1$. Row $k$ samples the projection $\mathcal{R}f(\theta_k, \cdot)$ of the [Radon transform](/radon-transform/) of an unknown image $f$ at the angle $\theta_k = k\pi/a$. Bin $j$ has its center at $s_j = (j - (d-1)/2)\tau$, with the detector spacing $\tau$. The output is an $n \times n$ image on $[-1, 1]^2$, with $n$ even. Pixel $(i, j)$ has its center at $x_j = -1 + (2j+1)/n$ and $y_i = 1 - (2i+1)/n$, so the pixel size is $h = 2/n$.

The Fourier transform uses ordinary frequency, $\mathcal{F}f(\xi) = \int f(x) e^{-2\pi i x\cdot\xi}\,dx$. The Fourier slice theorem then reads $\mathcal{F}_1(\mathcal{R}f(\theta, \cdot))(\sigma) = \mathcal{F}f(\sigma\,\omega(\theta))$, with $\omega(\theta) = (\cos\theta, \sin\theta)$ and no other constant.

## The algorithm

```pseudo id=main
DFR(P, τ, n)                  ▷ P[k][j]: angle θ_k = kπ/a, bin center s_j = (j - (d-1)/2) τ
L1  a, d ← the size of P; L ← the smallest power of 2 with L ≥ 4d; N ← 2n; Δξ ← 1/(N h) with h = 2/n
L2  for k ← 0 to a - 1 do
L3      S_k[l] ← τ e^{2πi τ σ_l (d-1)/2} · DFT_L(P[k] padded with zeros to L)[l], with σ_l = l/(Lτ) signed
L4  for u, v ← -N/2 .. N/2 - 1 do
L5      (θ, σ) ← the angle in [0, π) and the signed radius with σ ω(θ) = (u, v) Δξ
L6      F ← 0 if |σ| > 1/(2τ), else the bilinear interpolation of S in (θ, σ)
L7      G[v mod N][u mod N] ← F e^{πi(u+v)/N} Δξ²
L8  g ← N² IDFT2_N(G)
L9  return f[i][j] = Re g[(n/2 - 1 - i) mod N][(j - n/2) mod N]
```

Line L3 turns each projection into samples of $\mathcal{F}f$ on the radial line at the angle $\theta_k$. The factor $\tau$ makes the DFT a Riemann sum of the Fourier integral. The phase factor moves the origin of the detector from bin 0 to the bin position $(d-1)/2$. The signed frequency $\sigma_l$ is $l/(L\tau)$ for $l < L/2$ and $(l - L)/(L\tau)$ otherwise. The padding to $L \ge 4d$ does not add information, but it makes the radial samples four times denser, so the radial interpolation of line L6 is more accurate.

Lines L4 to L7 fill the Cartesian grid. Line L5 folds each frequency into the half plane of the data: a point with a negative polar angle $\phi$ has $\theta = \phi + \pi$ and a negative radius. Line L6 interpolates linearly between the two nearest angles and, on each of them, between the two nearest radial samples. The angle $\pi$ is not in the data, so the upper neighbor of the last angle is the angle 0 with the radius negated. The factor $e^{\pi i(u+v)/N}$ in line L7 is a shift by half a pixel, because the pixel centers lie between the points of the DFT grid. Lines L8 and L9 then evaluate the inverse Fourier integral at the pixel centers by one inverse 2D DFT (a [multidimensional FFT](/multidimensional-fft/)). The grid has $N = 2n$ points per axis, so the image repeats with the period $Nh = 4$, which is twice the side of the square. The copies of the image do not overlap it.

## Example

Take the Gaussian $f(x) = e^{-4\pi|x|^2}$. Its projection is $\mathcal{R}f(\theta, s) = \frac{1}{2} e^{-4\pi s^2}$ at each angle, and its transform is $\mathcal{F}f(\xi) = \frac{1}{4} e^{-\pi|\xi|^2/4}$. Use $a = 32$ angles, $d = 47$ bins, $\tau = 2\sqrt{2}/47 = 0.06018$ and $n = 32$. Then $L = 256$, the radial spacing is $1/(L\tau) = 0.06491$, the band edge is $1/(2\tau) = 8.3085$, and the grid has $N = 64$ and $\Delta\xi = 0.25$, so it reaches the frequency 8.

Follow the grid point $(u, v) = (8, 4)$, which is $\xi = (2, 1)$:

| step | value |
|---|---|
| radius $\rho$ and polar angle $\phi$ | 2.2361 and 0.46365 rad |
| angle index $\phi a/\pi$ | 4.7227, between the angles 4 and 5 |
| radial index $\rho L\tau$ | 34.449, between the samples 34 and 35 |
| $S_4[34]$ and $S_4[35]$ (the same at the angle 5) | 0.0054526 and 0.0043395 |
| interpolated value $0.551 \cdot 0.0054526 + 0.449 \cdot 0.0043395$ | 0.0049532 |
| true value $\mathcal{F}f(2, 1)$ | 0.0049257 |

The spectrum is radial, so the two angles give the same values and only the radial interpolation makes an error, here 0.6 percent. The spectrum is convex in the radius there, so the chord lies above the curve. At this radius the arc between two angles is $\pi\rho/a = 0.2195$, more than three times the radial spacing. For an image without radial symmetry, the angular interpolation is the larger error.

The table gives the error of the code below on analytic projections in the same setup. The FBP column is [filtered back-projection](/filtered-back-projection/) with the Ram-Lak kernel on the same data. These numbers are measurements of this setup, not bounds.

| phantom | DFR, bilinear | DFR, nearest | FBP |
|---|---|---|---|
| Gaussian $e^{-4\pi\vert x\vert^2}$, largest error | 0.0005 | 0.0033 | 0.0170 |
| disk of radius $1/2$, largest error for $\vert x\vert < 0.35$ | 0.0125 | 0.0242 | 0.0098 |
| [Shepp-Logan phantom](/shepp-logan-phantom/), largest error for $\vert x\vert < 0.35$ | 0.072 | 0.184 | |
| Shepp-Logan phantom, value at pixel $(16, 16)$, true 1.02 | 1.048 | 1.054 | 1.0217 |

On the smooth Gaussian the method is better than FBP, because the spectrum is smooth and the interpolation is accurate. On the disk and the phantom, whose spectra oscillate, it is worse, and the errors spread over the whole image.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) treats the three stages. First, if each projection is band-limited to $|\nu| < 1/(2\tau)$ and zero outside the detector, the scaled and phase-shifted DFT of line L3 equals $\mathcal{F}f$ on the radial line, by the Fourier slice theorem and the [sampling theorem](/sampling-theorem/). Second, the inverse DFT of lines L7 to L9 equals, at each pixel center, the Riemann sum $\sum_{u,v} F(u\Delta\xi, v\Delta\xi)\, e^{2\pi i x\cdot(u,v)\Delta\xi}\,\Delta\xi^2$. Third, with the exact spectrum on the whole lattice, this sum is the Fourier series of the periodized image, and it equals $f$ on $[-1, 1]^2$ because the period 4 is larger than the support. So the only approximations are the interpolation of line L6 and the truncation of the spectrum to the box and the band.

## Complexity

In the real-RAM model with an FFT:

- Lines L2 and L3 take $a$ FFTs of length $L < 8d$, so $O(a d \log d)$.
- Lines L4 to L7 take $O(1)$ for each of the $N^2 = 4n^2$ grid points, so $O(n^2)$.
- Line L8 is an inverse 2D FFT of size $N \times N$, so $O(n^2 \log n)$.

The total is $O(a d \log d + n^2 \log n)$ time and $O(a d + n^2)$ extra space. In the usual case $a \approx d \approx n$ this is $O(n^2 \log n)$, against $O(n^3)$ for filtered back-projection. With a direct DFT in place of the FFT, line L8 takes $O(n^3)$ and lines L2 and L3 take $O(a d^2)$.

## Properties

- **Linear.** The output is a linear function of the sinogram, because each step is linear.
- **One inverse transform.** The whole image comes from one 2D FFT. The cost does not grow with the product of the number of angles and the number of pixels, as it does for back projection.
- **Global errors.** An error at one frequency changes every pixel by a plane wave. So the interpolation error is not local, unlike the error of the linear interpolation in back projection.
- **Accurate at low frequencies.** The polar samples are dense near the origin and sparse at the band edge. The low frequencies, which hold the mean values of large regions, come out well, and the fine detail is the least accurate.
- **Real output.** The interpolation reads the values at $\xi$ and $-\xi$ from the same samples with the same weights, so the grid spectrum is Hermitian and the inverse transform is real up to rounding.

## Variants and improvements

- **Better interpolation.** Nearest-neighbor interpolation is the cheapest and the worst. Bilinear interpolation in the angle and the radius, as in line L6, is a good default. Stark, Woods, Paul and Hingorani studied interpolation methods that make this error smaller, and Kak and Slaney refer to their paper for such methods (Section 3.7). An exact recovery from samples on radial lines is possible in theory, but it leads to badly conditioned systems (Kak and Slaney, Section 3.2).
- **Gridding.** O'Sullivan convolved each polar sample with a small kernel onto the Cartesian grid, with weights for the sample density, and divided the image by the transform of the kernel at the end. This is the gridding method of MRI. See [density compensation](/density-compensation/).
- **Nonuniform FFT.** A [nonuniform FFT](/nonuniform-fft/) evaluates the inverse transform of the polar samples directly, with a controlled error and at about the cost of an FFT.
- **Oversampling.** A larger $L$ in line L1 or a larger grid factor in place of $N = 2n$ reduces the interpolation error at the cost of more memory.
- **Other fields.** The same polar-to-Cartesian step appears in the [polar format algorithm](/polar-format-algorithm/) of radar imaging and in [single-particle reconstruction](/single-particle-reconstruction/) of electron microscopy, where the data are 2D slices of a 3D spectrum.

## When to use it

Use direct Fourier reconstruction when speed matters more than image quality, when the image is large and the projections are many, or when the object is smooth. It is also the natural route when the data come in the Fourier domain, as in MRI and radar. For sharp edges and fine detail at the same cost scale, prefer [filtered back-projection](/filtered-back-projection/), which interpolates in space, where linear interpolation is accurate. For dense polar data the sampling rule $a \approx \pi d/2$ of filtered back-projection applies here too: with fewer angles, the outer ring of the Fourier plane has gaps that no interpolation fills.

## Pitfalls

- **Nearest-neighbor artifacts.** Rounding each grid point to the nearest polar sample gives errors that the inverse transform spreads over the whole image as streaks and rings. In the table above it more than doubles the error inside the phantom.
- **Sparse outer samples.** The arc between two angles grows with the radius. At the band edge it is $\pi/(2a\tau)$, so too few angles leave the high frequencies to guesswork.
- **The angle wrap.** The data cover $[0, \pi)$, so the grid points with a negative polar angle need $\theta + \pi$ and a negative radius, and the points just below the angle $\pi$ need the angle 0 with the radius negated. Without this, the interpolation jumps across the negative $x$ axis.
- **The missing phase.** The DFT treats bin 0 as the origin, but the center of rotation is at bin $(d-1)/2$. Without the phase factor of line L3 each projection moves by $(d-1)\tau/2$, and the image is wrong. Without the half-pixel factor of line L7 the image moves by half a pixel.
- **Too small a grid.** With $N = n$ the period of the image equals the side of the square. Then the edges of the object wrap to the opposite side.

## Implementations

## History

Bracewell showed in 1956 that the 1D Fourier transform of a strip scan of a radio source is a line of its 2D transform, so that scans at several angles fill the 2D transform. DeRosier and Klug used the same idea in 1968 for 3D structures in electron microscopy, and several groups then applied it to radiography (Kak and Slaney, Section 3.7). Kak and Slaney prefer filtered back-projection, because it can start after the first projection and because linear interpolation is more accurate in space than in the Fourier plane. Stark, Woods, Paul and Hingorani studied this interpolation in 1981 and gave methods that reduce its error. O'Sullivan introduced the gridding method in 1985.

## References
