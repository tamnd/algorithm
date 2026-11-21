---
tag: D52MD2
kind: algorithm
slug: fan-to-parallel-rebinning
name: Fan-to-parallel rebinning
aliases:
- fan-beam rebinning
area: imaging-and-inverse-problems/tomographic-reconstruction
level: core
summary: Turn fan-beam CT data into a parallel-beam sinogram. Each parallel ray is a fan ray with a known source angle and fan angle, read from the fan data by interpolation.
solves: [tomographic-reconstruction-problem]
model: real-ram
complexity:
  vars: {a: the number of parallel angles, d: the number of parallel detector bins, n: the side of the n x n output image}
  time: {worst: "O(a d)"}
  space: {extra: "O(a d)"}
properties: {deterministic: true, in_place: false, recursive: false, iterative: false, linear: true}
prereqs: [radon-transform, sinogram, filtered-back-projection]
see_also: [fan-beam-filtered-back-projection, bilinear-interpolation, feldkamp-davis-kress, back-projection-operator, sart, x-ray-transform]
sources:
  - book: isbn:9780898714944
    title: A. C. Kak and M. Slaney, Principles of Computerized Tomographic Imaging, SIAM Classics in Applied Mathematics 33, 2001
    locator: Chapter 3, Section 3.4 (reconstruction from fan projections, the subsection on a re-sorting algorithm) and Section 3.3 (parallel projections)
  - paper: doi:10.1016/0010-4825(76)90065-2
    title: G. T. Herman, A. V. Lakshminarayanan and A. Naparstek, Convolution reconstruction techniques for divergent beams, Computers in Biology and Medicine 6(4), 1976
    locator: pp. 259 to 271 (the direct method that rebinning competes with)
---

Fan-to-parallel rebinning converts the data of a fan-beam CT scanner into a parallel-beam [sinogram](/sinogram/). Each ray of a parallel projection is also a ray of some fan: its source angle and its fan angle follow from the angle and the offset of the line by one arcsine. The algorithm reads that fan ray from the measured data by [bilinear interpolation](/bilinear-interpolation/) and stores it. After rebinning, ordinary parallel-beam [filtered back-projection](/filtered-back-projection/), or any other parallel method, reconstructs the image. Rebinning an $a \times d$ parallel sinogram takes $O(a d)$ time. Kak and Slaney call it re-sorting.

## In plain words

A fan-beam scanner measures many rays at each source position, and the rays spread out from the source. A parallel scanner measures, at each angle, rays that are all parallel. The two scanners measure the same kind of thing: the total absorption along straight lines. Only the way the lines are grouped differs.

Rebinning regroups the lines. For each line that a parallel projection needs, it finds the source position from which that line was shot and the detector cell that caught it. The scanner rarely has a source exactly at that position, or a cell exactly at that spot, so the value is mixed from the four nearest measurements. When every parallel line has a value, the data looks as if a parallel scanner had made it, and the parallel method takes over.

## The problem

The source at the angle $\beta$ is at $S(\beta) = D\,\omega^\perp(\beta)$, at the distance $D$ from the center, with $\omega(\beta) = (\cos\beta, \sin\beta)$ and $\omega^\perp(\beta) = (-\sin\beta, \cos\beta)$. The ray with the fan angle $\gamma$ is the line with the angle $\theta = \beta + \gamma$ and the offset $s = D\sin\gamma$, so the fan data is
$$g(\beta, \gamma) = \mathcal{R}f(\beta + \gamma, D\sin\gamma),$$
with the [Radon transform](/radon-transform/) $\mathcal{R}f(\theta, s) = \int f(s\,\omega + t\,\omega^\perp)\,dt$. The input is a full scan $g[k][j] = g(\beta_k, \gamma_j)$ with $\beta_k = 2\pi k/a_f$ for $k = 0, \ldots, a_f - 1$ and an equiangular detector $\gamma_j = (j - (d_f-1)/2)\alpha$. A flat detector at $t_j = (j - (d_f-1)/2)\tau_f$ through the center has the fan angle $\arctan(t_j/D)$.

The output is the parallel sinogram $P[k][j] \approx \mathcal{R}f(\theta_k, s_j)$ with $\theta_k = k\pi/a$ for $k = 0, \ldots, a - 1$ and $s_j = (j - (d-1)/2)\tau$. The reconstruction after it is an $n \times n$ image on $[-1, 1]^2$, with pixel $(i, j)$ centered at $x_j = -1 + (2j+1)/n$ and $y_i = 1 - (2i+1)/n$.

Inverting $\theta = \beta + \gamma$ and $s = D\sin\gamma$ gives
$$\gamma = \arcsin(s/D), \qquad \beta = \theta - \gamma \pmod{2\pi}.$$

## The algorithm

```pseudo id=main
REBIN(g, D, α, a, d, τ)         ▷ g[k][j]: β_k = 2πk/a_f, γ_j = (j - (d_f-1)/2) α
L1  a_f, d_f ← the number of rows and of columns of g
L2  for k ← 0 to a - 1 do
L3      θ ← kπ/a
L4      for j ← 0 to d - 1 do
L5          s ← (j - (d-1)/2) τ
L6          γ ← arcsin(s/D); β ← (θ - γ) mod 2π
L7          u ← β a_f/(2π); v ← γ/α + (d_f-1)/2
L8          P[k][j] ← BILINEAR(g, u, v)      ▷ periodic in u, zero outside the detector in v
L9  return P
```

Line L6 is the inverse map above. Line L7 turns $(\beta, \gamma)$ into fractional indices into the fan data. For a flat detector, line L7 uses $v = D\tan\gamma/\tau_f + (d_f-1)/2$. Line L8 reads the four nearest samples. The rows wrap around, because row $a_f$ would be row 0 again.

A full scan holds each line twice: $(\theta, s)$ and $(\theta + \pi, -s)$. The ray $(\beta, \gamma)$ and the ray $(\beta + \pi + 2\gamma, -\gamma)$ are the same line. An option of the code takes the mean of the two interpolated copies. This changes nothing for exact data and halves the variance of independent noise.

The reconstruction step is plain parallel FBP: filter each row of $P$ with the Ram-Lak kernel and back-project over $[0, \pi)$ with the weight $\pi/a$.

## Example

Take $D = 2$, a fan scan with $a_f = 8$ source positions ($\Delta\beta = \pi/4$) and $d_f = 9$ bins with $\alpha = 0.1$. Rebin the parallel sample $\theta = 0.3$, $s = 0.5$.

- Line L6: $\gamma = \arcsin(0.25) = 0.25268$ and $\beta = 0.3 - 0.25268 = 0.04732$.
- Line L7: $u = 0.04732/(\pi/4) = 0.06025$ and $v = 0.25268/0.1 + 4 = 6.52680$.
- Line L8 mixes the source positions 0 and 1 with the weights $0.93975$ and $0.06025$, and the bins 6 and 7 with the weights $0.47320$ and $0.52680$.

Let the object be the unit disk with density 1. Its fan data does not depend on $\beta$, and the ray with the fan angle $\gamma$ has the length $2\sqrt{1 - 4\sin^2\gamma}$ inside the disk. Bin 6 ($\gamma = 0.2$) holds $1.83534$ and bin 7 ($\gamma = 0.3$) holds $1.61328$. The interpolated value is $0.47320 \cdot 1.83534 + 0.52680 \cdot 1.61328 = 1.71836$. The true value is $2\sqrt{1 - 0.25} = 1.73205$. The error of $0.0137$ comes from the linear interpolation across the curved profile.

A larger setup, measured with the code: $D = 3$, a fan that covers the disk of radius $\sqrt{2}$, $a_f = 64$, $d_f = 49$, rebinned to $a = 32$ angles and $d = 47$ bins with $\tau = 2\sqrt{2}/47$, and $n = 32$. The smooth object is the blob $e^{-4\pi\vert x - c\vert^2}$ with $c = (0.3, -0.2)$. These numbers are measurements of this setup, not bounds.

| quantity | value |
|---|---|
| largest error of the rebinned sinogram, blob, equiangular detector | 0.0030 |
| same, mean of the two copies | 0.0028 |
| same, flat detector | 0.0084 |
| largest image error, blob, rebinning and parallel FBP | 0.0243 |
| largest image error, blob, parallel FBP on exact parallel data | 0.0153 |
| largest error of the rebinned sinogram, modified Shepp-Logan phantom (5 ellipses) | 0.114 |
| image value at pixel $(16, 16)$ of that phantom, true 0.2 | 0.2102 |

The sinogram error of the phantom is large only at the edges of the ellipses, where the profile has a square-root corner that linear interpolation cannot follow.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) has three parts. First, for $|s| < D$ the map of line L6 gives the only fan ray that is the wanted line, so with exact data at the right points the rebinned sinogram is exact. Second, bilinear interpolation reproduces data of the form $c + e\gamma$ exactly and has the error at most $(\Delta\beta^2 M_1 + \alpha^2 M_2)/8$, where $M_1$ and $M_2$ bound the second derivatives of the fan data in $\beta$ and $\gamma$. Third, parallel FBP is linear, and its discrete operator has the norm at most $\pi/(2\tau)$ in the maximum norm. So the rebinning error adds at most $\pi/(2\tau)$ times the largest sinogram error to the image, on top of the error of parallel FBP.

## Complexity

In the real-RAM model, lines L5 to L8 take $O(1)$ time for each of the $a d$ parallel samples, so rebinning takes $O(a d)$ time and $O(a d)$ space for the output. The fan data is read but not copied. The parallel FBP after it takes $O(a d \log d + a n^2)$ with an FFT, or $O(a d^2 + a n^2)$ with the direct sum that the code uses. Rebinning is cheap next to the reconstruction.

## Properties

- **Linear.** The output is a fixed linear combination of the input, with at most 4 nonzero weights per output sample (8 with the mean of two copies).
- **Exact map, approximate values.** The geometry is exact. The only error is the interpolation, which is second order for smooth data.
- **Smoothing.** Linear interpolation is a low-pass filter. It reduces the resolution a little and correlates the noise of neighboring samples.
- **Detector independence.** The parallel method after it does not need to know anything about the fan geometry.

## Variants and improvements

- **Direct fan-beam FBP.** [Fan-beam filtered back-projection](/fan-beam-filtered-back-projection/) avoids the interpolation before the filter, at the cost of a distance weight in the back-projection.
- **Better interpolation.** Cubic or windowed sinc interpolation in $\gamma$ reduces the smoothing. Interpolation in $\beta$ matters less when the source angles are dense.
- **Two separate steps.** Each parallel angle mixes rays from many source angles, but for a fixed fan angle the map $\beta = \theta - \gamma$ is a shift. Some codes interpolate first in $\beta$ for each fan angle, then in $s$ for each parallel angle.
- **Short scans.** Data over $\pi$ plus the fan angle also fills the parallel sinogram over $[0, \pi)$. Each line then exists at least once, and the code needs the copy rule to find it.
- **Cone beam.** Rebinning the rows of a helical cone-beam scan to parallel fans is a step of several practical helical methods. The exact helical method on this site is [Katsevich's algorithm](/katsevich-algorithm/).

## When to use it

Use rebinning when a good parallel-beam code is at hand and the fan data is dense, so the interpolation error is small. It also helps when a method needs parallel data, such as [direct Fourier reconstruction](/direct-fourier-reconstruction/) or a method that uses the parallel range conditions. When the source angles are sparse, the interpolation in $\beta$ is coarse, and direct fan-beam FBP is better.

## Pitfalls

- **The wrong sign of the fan angle.** With the other sign convention for $\gamma$, line L6 must use $\beta = \theta + \gamma$. Test the map on a point object at a known place, as the test of the code does with $\theta = \beta + \gamma$ and $s = D\sin\gamma$.
- **No wrap in $\beta$.** The source angle is periodic. A sample with $\beta$ between the last source and $2\pi$ must mix the last row with row 0.
- **Parallel bins outside the fan.** If $|s| \ge D\sin\gamma_{\max}$, the line is not in the data. The code returns 0, which is right only if the object lies inside the fan.
- **Offsets in the detector.** A shift of the central ray by a fraction of a bin moves every rebinned sample and blurs the image.

## Implementations

## History

The first CT scanners used parallel translate and rotate motions, and fan-beam scanners came soon after. Reordering the fan rays into parallel projections was the natural first way to reuse the parallel methods. Herman, Lakshminarayanan and Naparstek gave in 1976 a convolution method on the fan data directly. Kak and Slaney treat the re-sorting algorithm and the direct methods side by side in their Section 3.4.

## References
