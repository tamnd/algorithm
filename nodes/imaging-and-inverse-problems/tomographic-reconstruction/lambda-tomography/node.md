---
tag: 8VWFH5
kind: algorithm
slug: lambda-tomography
name: Lambda tomography
aliases:
- local tomography
area: imaging-and-inverse-problems/tomographic-reconstruction
level: advanced
summary: Reconstruct Lambda f, the square root of minus the Laplacian of f, from local data. It is not f, but it has the same edges, and each value needs only the rays near the point.
solves: [interior-tomography]
model: real-ram
complexity:
  vars: {a: the number of projection angles, d: the number of detector bins, n: the side of the n x n output image}
  time: {worst: "O(a d + a n^2)"}
  space: {extra: "O(a d + n^2)"}
properties: {deterministic: true, in_place: false, recursive: false, iterative: false, linear: true}
history:
  year: 1992
  people: [A. Faridani, E. L. Ritman, K. T. Smith]
  note: Faridani, Ritman and Smith analyzed local tomography and showed that Lambda f has the same singularities as f.
prereqs: [radon-transform, back-projection-operator, filtered-back-projection]
see_also: [interior-tomography, ramp-filter, fourier-slice-theorem, limited-angle-tomography, radon-inversion-formula, sinogram, hilbert-transform, fan-beam-filtered-back-projection]
sources:
  - paper: doi:10.1137/0152026
    title: A. Faridani, E. L. Ritman and K. T. Smith, Local Tomography, SIAM Journal on Applied Mathematics 52(2), 1992
    locator: pp. 459 to 484
  - paper: doi:10.1137/S0036139995286357
    title: A. Faridani, D. V. Finch, E. L. Ritman and K. T. Smith, Local Tomography II, SIAM Journal on Applied Mathematics 57(4), 1997
    locator: pp. 1095 to 1127
---

Lambda tomography reconstructs, from parallel-beam CT data, the image $\Lambda f = (-\Delta)^{1/2} f$ in place of the attenuation $f$. The algorithm is filtered back-projection with the [ramp filter](/ramp-filter/) replaced by minus the second derivative: $\Lambda f = \frac{1}{2\pi}\mathcal{R}^\#(-\partial_s^2\mathcal{R}f)$. A second derivative is local, so the value at a point needs only the rays that pass near that point. This makes the method work on truncated projections, where the [interior problem](/interior-tomography/) has no unique solution for $f$. The output is not $f$. It has the same edges as $f$, at the same places, but its values are different: $\Lambda f$ has no mean value and is unbounded at a jump. With $a$ angles, $d$ bins and an $n \times n$ image it takes $O(a d + a n^2)$ time.

## In plain words

Ordinary CT needs every ray through the whole object. The filter of ordinary CT has long tails, so a pixel is affected by rays that pass far from it. If the detector is too small and some rays are missing, every pixel gets some error.

Lambda tomography uses a short filter: at each detector cell, it compares the reading with its two neighbors. A pixel then depends only on the rays that pass close to it. If the region of interest is fully covered by the measured rays, the missing rays do not matter.

The price is that the picture is not the density. It is a sharpened version of the density, in which a constant area is close to flat but each boundary shows as a strong bright and dark line. For finding edges, cracks and the shape of a structure, this is often enough.

## The problem

The data is a parallel sinogram $P[k][j]$ for $k = 0, \ldots, a - 1$ and $j = 0, \ldots, d - 1$. Row $k$ samples $\mathcal{R}f(\theta_k, \cdot)$ at $\theta_k = k\pi/a$, and bin $j$ has its center at $s_j = (j - (d-1)/2)\tau$. Here $\mathcal{R}f(\theta, s) = \int f(s\,\omega + t\,\omega^\perp)\,dt$ is the [Radon transform](/radon-transform/), with $\omega = (\cos\theta, \sin\theta)$ and $\omega^\perp = (-\sin\theta, \cos\theta)$. The back-projection is $\mathcal{R}^\# q(x) = \int_0^\pi q(\theta, x\cdot\omega(\theta))\,d\theta$, the [back-projection operator](/back-projection-operator/). Bins outside the measured range count as 0. The output is an $n \times n$ image on $[-1, 1]^2$, with pixel $(i, j)$ centered at $x_j = -1 + (2j+1)/n$ and $y_i = 1 - (2i+1)/n$.

With the Fourier transform in ordinary frequency, $\Lambda$ multiplies $\hat f(\xi)$ by $2\pi|\xi|$, and $\Lambda^{-1}$ multiplies it by $1/(2\pi|\xi|)$. The algorithm evaluates
$$\Lambda f = \frac{1}{2\pi}\,\mathcal{R}^\#\left(-\partial_s^2\,\mathcal{R}f\right), \qquad \text{and optionally} \qquad \Lambda f + \mu\,\Lambda^{-1}f = \frac{1}{2\pi}\,\mathcal{R}^\#\left((-\partial_s^2 + \mu)\,\mathcal{R}f\right).$$
Some texts write $\mathcal{R}^\#(-\partial_s^2\mathcal{R}f)$ without the constant. The constant $1/(2\pi)$ makes the output equal to $\Lambda f$ in this convention. The term $\mu\Lambda^{-1}f$ is not local. It adds a smooth image that brings back some of the contrast between regions.

## The algorithm

```pseudo id=main
LAMBDA(P, τ, n, μ)               ▷ P[k][j]: angle θ_k = kπ/a, bin center s_j = (j - (d-1)/2) τ
L1  a, d ← the number of rows and of columns of P
L2  q_k[j] ← -(P[k][j+1] - 2 P[k][j] + P[k][j-1])/τ² + μ P[k][j] for each k and j   ▷ P = 0 outside
L3  for each pixel (i, j) with center (x_j, y_i) do
L4      f[i][j] ← Σ_k LININTERP(q_k, (x_j cos θ_k + y_i sin θ_k)/τ + (d-1)/2)
L5  return f/(2a)
```

Line L2 is the central second difference, which approximates $-\partial_s^2$, plus the optional term. Line L4 is the discrete back-projection, with linear interpolation and 0 outside the detector. Line L5 applies the weight $\frac{1}{2\pi}\cdot\frac{\pi}{a} = \frac{1}{2a}$. With $\mu = 0$, the value at a pixel $x$ uses only the bins whose centers lie within $2\tau$ of $x\cdot\omega(\theta_k)$ in each row.

## Example

Take the disk of radius $R = 1/2$ with density 1. Its projection is $2\sqrt{1/4 - s^2}$ at every angle. With $d = 7$ bins and $\tau = 1/4$:

| quantity | values at $j = 0, \ldots, 6$ |
|---|---|
| projection $P[k][j]$ | 0, 0, 0.8660, 1, 0.8660, 0, 0 |
| filtered $q_k[j]$ | 0, -13.8564, 11.7128, 4.2872, 11.7128, -13.8564, 0 |

The center value is $q_k[3] = -(0.8660 - 2 + 0.8660) \cdot 16 = 4.2872$. With $a = 4$ angles the value at the origin is $\frac{1}{8} \cdot 4 \cdot 4.2872 = 2.1436$. The filtered profile is large and positive just inside the edge and negative just outside it, which is how the edge shows up.

The exact $\Lambda f$ of this disk follows from the formula. The projection $p(s) = 2\sqrt{R^2 - s^2}$ has $-p''(s) = 2R^2/(R^2 - s^2)^{3/2}$, so for $|x| < R$, with $k = |x|/R$,
$$\Lambda f(x) = \frac{1}{2\pi}\int_0^\pi \frac{2R^2\,d\theta}{(R^2 - |x|^2\cos^2\theta)^{3/2}} = \frac{2E(k)}{\pi R\,(1 - k^2)},$$
where $E(k) = \int_0^{\pi/2}\sqrt{1 - k^2\sin^2\phi}\,d\phi$ is the complete elliptic integral of the second kind. At the center $E(0) = \pi/2$ and $\Lambda f(0) = 1/R = 2$, so the coarse example above is off by 7 percent. The value grows like $1/(\pi(R - |x|))$ near the edge.

A finer grid, measured with the code: $a = 32$ angles, $d = 65$ bins, $\tau = 2\sqrt{2}/65 = 0.0435$. These are measurements of this setup.

| point $x = (x_1, 0)$ | code | exact $\Lambda f$ |
|---|---|---|
| $x_1 = 0$ | 2.0038 | 2 |
| $x_1 = 0.25$ | 2.5143 | 2.4912 |
| $x_1 = 0.4$ | 4.7938 | 4.5142 |
| $x_1 = 0.45$ | 8.1860 | 7.8518 |
| $x_1 = 0.6$, outside the disk | -2.6084 | negative |

For the Gaussian $f(x) = e^{-4\pi|x|^2}$ the exact value at the origin is $\Lambda f(0) = \int 2\pi|\xi| \cdot \frac{1}{4}e^{-\pi|\xi|^2/4}\,d\xi = 2\pi$. The code gives $6.2090$ there, and its largest error over the $16 \times 16$ grid against the exact formula is $0.108$.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) has four parts. First, by the [Fourier slice theorem](/fourier-slice-theorem/) and polar coordinates, back-projecting a projection filtered by the multiplier $m(\sigma)$ gives the image filtered by $m(|\xi|)/|\xi|$. With $m(\sigma) = 4\pi^2\sigma^2$, the multiplier of $-\partial_s^2$, this gives $2\pi\Lambda f$, and with $m = 1$ it gives $2\pi\Lambda^{-1}f$. Second, the formula needs $\partial_s^2\mathcal{R}f$ only on the lines through the point, so it is local. Third, the second difference has the error $O(\tau^2)$, the linear interpolation has the error $O(\tau^2)$, and the sum over angles is the trapezoidal rule for a periodic function. The discrete value at a point uses only the bins within $2\tau$ of the lines through it. Fourth, $\Lambda$ is an elliptic pseudodifferential operator of order 1, so $\Lambda f$ and $f$ have the same singular support. This is the theorem behind the method: the edges are in the right places.

## Complexity

In the real-RAM model, line L2 takes $O(d)$ per row, $O(a d)$ in total. Lines L3 and L4 take $O(1)$ per angle and pixel, $O(a n^2)$ in total. The total is $O(a d + a n^2)$ time and $O(a d + n^2)$ space. The filter is cheaper than the ramp filter of FBP, which takes $O(d \log d)$ per row with an FFT, but the back-projection dominates both. To reconstruct only a region of interest with $n_r$ pixels, the cost is $O(a d + a n_r)$, and the data needs to cover only the lines that meet the region.

## Properties

- **Local.** With $\mu = 0$ the value at a point depends only on the data on lines within a small distance of the point. Truncated projections give exact values (up to discretization) inside the region that the measured lines cover.
- **Not the density.** $\Lambda f$ has the Fourier transform $2\pi|\xi|\hat f(\xi)$, which is 0 at $\xi = 0$. So $\int\Lambda f\,dx = 0$ for an integrable $\Lambda f$, and a large constant region has a value near 0 far from its edges.
- **Same edges.** $\Lambda f$ is smooth exactly where $f$ is smooth. At a jump, $\Lambda f$ is unbounded, with opposite signs on the two sides, as the disk example shows.
- **Linear.** The output is a linear function of the data.
- **Noise.** The filter of line L2 with the factor $1/(2\pi)$ has the response $4\sin^2(\pi\nu\tau)/(2\pi\tau^2)$. At the Nyquist frequency $\nu = 1/(2\tau)$ this is $2/(\pi\tau^2)$, against $1/(2\tau)$ for the ramp of FBP, so it amplifies the noise at high frequency by the factor $4/(\pi\tau)$ more. Practical codes smooth the data first.

## Variants and improvements

- **Lambda plus a smooth part.** $\Lambda f + \mu\Lambda^{-1}f$ adds back some low-frequency contrast. The second term is not local, so with truncated data it is only approximate. The code supports it with the parameter $\mu$.
- **Smoothed kernels.** Replace $-\partial_s^2$ by a smooth kernel with the same behavior at high frequency, such as the second derivative of a Gaussian. The result is a smoothed $\Lambda f$, and the locality radius grows to the width of the kernel.
- **Fan-beam and cone-beam data.** The same idea works for divergent beams with a change of variables, as in [fan-beam filtered back-projection](/fan-beam-filtered-back-projection/).
- **Exact interior reconstruction.** If extra knowledge is available, for example the values of $f$ on a small subregion, the interior problem has a unique solution and other methods recover $f$ itself ([interior tomography](/interior-tomography/)).

## When to use it

Use lambda tomography when the detector does not cover the whole object, or when only a small region is of interest, and the goal is to find edges, boundaries or small features, not to measure densities. Examples are a region of interest scan of a large sample in micro CT, or the search for cracks in a part. Do not use it when the attenuation values themselves matter. In that case use full data and [filtered back-projection](/filtered-back-projection/), or interior tomography with extra knowledge.

## Pitfalls

- **Reading the values as densities.** $\Lambda f$ is not $f$. A region of constant density shows as nearly 0 inside, with strong lines at its boundary.
- **The missing constant.** The formula $\mathcal{R}^\#(-\partial_s^2\mathcal{R}f)$ without the factor $1/(2\pi)$ gives $2\pi\Lambda f$. The scale does not matter for edge detection, but it matters when the result is combined with other images.
- **Noise.** The second difference has a large gain at high frequency. Without smoothing the image is dominated by noise.
- **Wrong edges for the variant.** The term $\mu\Lambda^{-1}f$ is not local, so with truncated data it adds an error that is smooth but not small. Choose $\mu$ by experiment and do not read the result as $f$.
- **Data that is not zero at the detector ends.** The code treats the bins outside the detector as 0. At a truncated detector the second difference at the last bin then sees a jump and gives a large value. These values only affect pixels whose lines pass within $2\tau$ of the detector end, so keep the region of interest at least that far inside.

## Implementations

## History

Faridani, Ritman and Smith published their paper Local Tomography in 1992. They based the method on the operator $\Lambda$ and on the fact that $\Lambda f$ has the same singularities as $f$. Faridani, Finch, Ritman and Smith continued the work in Local Tomography II in 1997. The formula itself follows from the Fourier slice theorem in the same way as filtered back-projection.

## References
