---
tag: M3HFA2
kind: algorithm
slug: filtered-back-projection
name: Filtered back-projection
aliases:
- FBP
- convolution back-projection
area: imaging-and-inverse-problems/tomographic-reconstruction
level: core
summary: Reconstruct a CT slice from parallel projections. Convolve each projection with a band-limited ramp kernel, then back-project the filtered projections over all angles.
solves: [tomographic-reconstruction-problem]
model: real-ram
complexity:
  vars: {a: the number of projection angles, d: the number of detector bins, n: the side of the n x n output image}
  time: {worst: "O(a d log d + a n^2)"}
  space: {extra: "O(a d + n^2)"}
properties: {deterministic: true, in_place: false, recursive: false, iterative: false, linear: true}
history:
  year: 1971
  people: [G. N. Ramachandran, A. V. Lakshminarayanan]
  note: Ramachandran and Lakshminarayanan replaced the Fourier transforms of reconstruction by a convolution with the sampled band-limited ramp.
prereqs: [radon-transform, fourier-slice-theorem, ramp-filter, back-projection-operator]
see_also: [direct-fourier-reconstruction, fan-beam-filtered-back-projection, feldkamp-davis-kress, sart, kaczmarz-method, shepp-logan-phantom, sinogram, convolution-via-fft]
sources:
  - paper: doi:10.1073/pnas.68.9.2236
    title: G. N. Ramachandran and A. V. Lakshminarayanan, Three-dimensional reconstruction from radiographs and electron micrographs, application of convolutions instead of Fourier transforms, Proceedings of the National Academy of Sciences 68(9), 1971
    locator: pp. 2236 to 2240
  - paper: doi:10.1109/TNS.1974.6499235
    title: L. A. Shepp and B. F. Logan, The Fourier reconstruction of a head section, IEEE Transactions on Nuclear Science 21(3), 1974
    locator: pp. 21 to 43 (the smoother kernel and the head phantom)
  - book: isbn:9780898714944
    title: A. C. Kak and M. Slaney, Principles of Computerized Tomographic Imaging, SIAM Classics in Applied Mathematics 33, 2001
    locator: Chapter 3, Section 3.3 (the filtered back-projection formula, equation 45, and the computer implementation of Section 3.3.3)
  - book: isbn:9780898714937
    title: F. Natterer, The Mathematics of Computerized Tomography, SIAM Classics in Applied Mathematics 32, 2001
    locator: Section V.1, filtered backprojection
---

Filtered back-projection (FBP) reconstructs a 2D image from its parallel-beam projections, which is the [tomographic reconstruction problem](/tomographic-reconstruction-problem/). It convolves each projection with a [ramp filter](/ramp-filter/) and then applies the [back-projection operator](/back-projection-operator/) to the filtered projections. It is a direct discretization of the inversion formula that follows from the [Fourier slice theorem](/fourier-slice-theorem/). With $a$ angles, $d$ detector bins and an $n \times n$ image it takes $O(a d \log d + a n^2)$ time, and it is the standard reconstruction of parallel-beam and fan-beam CT.

## In plain words

A CT scanner measures, at each angle, how much the object absorbs along many parallel rays. If you smear each of these profiles back across the image along the direction of its rays and add all the smears, you get a blurred copy of the object. The center of the object gets too much weight, because every smear passes through it.

FBP removes the blur before it smears. It sharpens each profile with a fixed filter. The filter makes the profile go negative just outside each edge. When the smears are added, these negative parts cancel the blur of the other angles, and the true image is left. The filter is the same for each angle, so the method is one short loop: filter each profile, then smear it.

## The problem

The data is a sinogram $P[k][j]$ for $k = 0, \ldots, a - 1$ and $j = 0, \ldots, d - 1$. Row $k$ samples the projection $\mathcal{R}f(\theta_k, \cdot)$ of an unknown image $f$ at the angle $\theta_k = k\pi/a$. Bin $j$ has its center at $s_j = (j - (d-1)/2)\tau$, with the detector spacing $\tau$. Here $\mathcal{R}f(\theta, s) = \int f(s\,\omega + t\,\omega^\perp)\,dt$ is the [Radon transform](/radon-transform/), with $\omega = (\cos\theta, \sin\theta)$ and $\omega^\perp = (-\sin\theta, \cos\theta)$. The output is an $n \times n$ image on the square $[-1, 1]^2$. Pixel $(i, j)$ has its center at $x_j = -1 + (2j+1)/n$ and $y_i = 1 - (2i+1)/n$, so row 0 is at the top and $y$ goes up.

FBP evaluates the inversion formula
$$f(x) = \int_0^\pi (h * \mathcal{R}f(\theta, \cdot))(x \cdot \omega(\theta))\,d\theta,$$
where $h$ is the filter with the frequency response $|\sigma|$. With the Fourier transform in ordinary frequency, this formula has no other constant. The proof is on the page of the [Radon inversion formula](/radon-inversion-formula/) and in the proof below.

## The algorithm

```pseudo id=main
FBP(P, τ, n)                  ▷ P[k][j]: angle θ_k = kπ/a, bin center s_j = (j - (d-1)/2) τ
L1  a, d ← the number of rows and of columns of P
L2  h[m] ← h(mτ) for m = -(d-1) .. d-1     ▷ Ram-Lak or Shepp-Logan kernel
L3  L ← the smallest power of 2 with L ≥ 2d - 1
L4  Ĥ ← DFT_L(h), with h[m] stored at index m mod L
L5  for k ← 0 to a - 1 do
L6      q_k ← τ · (the first d entries of IDFT_L(DFT_L(P[k] padded with zeros to L) · Ĥ))
L7  for each pixel (i, j) with center (x_j, y_i) do
L8      f[i][j] ← (π/a) Σ_k LININTERP(q_k, (x_j cos θ_k + y_i sin θ_k)/τ + (d-1)/2)
L9  return f
```

Line L2 samples the ramp filter cut off at the Nyquist frequency $1/(2\tau)$ of the detector. The Ram-Lak kernel of Ramachandran and Lakshminarayanan is
$$h(0) = \frac{1}{4\tau^2}, \qquad h(m\tau) = 0 \text{ for even } m \ne 0, \qquad h(m\tau) = -\frac{1}{m^2\pi^2\tau^2} \text{ for odd } m.$$
The kernel of Shepp and Logan is $h(m\tau) = -2/(\pi^2\tau^2(4m^2 - 1))$. Its frequency response is $|\nu|\,\mathrm{sinc}(\nu\tau)$, so it damps the highest frequencies and the noise there. Lines L3 to L6 compute the aperiodic [discrete convolution](/discrete-convolution/) $q_k[j] = \tau \sum_{l=0}^{d-1} h((j - l)\tau)\,P[k][l]$ with the [fast Fourier transform](/fast-fourier-transform/). The zero padding to $L \ge 2d - 1$ makes the [circular convolution](/circular-convolution/) of the DFT equal to the aperiodic one on the $d$ outputs. Line L8 is the discrete back projection: the sum over the angles approximates the integral over $[0, \pi)$, and LININTERP reads the filtered projection between two bin centers by linear interpolation, with 0 outside the detector. The factor $\pi/a$ is the angle step.

## Example

Take the disk of radius $1/2$ with density 1. Its projection is $2\sqrt{1/4 - s^2}$ at each angle. With $d = 7$ bins and $\tau = 1/4$ the bin centers are $s = -0.75, -0.5, \ldots, 0.75$, and

| quantity | values at $j = 0, \ldots, 6$ |
|---|---|
| projection $P[k][j]$ | 0, 0, 0.8660, 1, 0.8660, 0, 0 |
| kernel $h(m\tau)$, $m = -3, \ldots, 3$ | -0.1801, 0, -1.6211, 4, -1.6211, 0, -0.1801 |
| filtered $q_k[j]$ | -0.0450, -0.3900, 0.4607, 0.2980, 0.4607, -0.3900, -0.0450 |

The center value is $q_k[3] = \tau(4 \cdot 1 - 2 \cdot 1.6211 \cdot 0.8660) = 0.2980$. The filter makes the values negative just outside the disk, at $j = 1$ and $j = 5$. The disk is the same at each angle, so with $a = 4$ angles the value at the origin is $(\pi/4) \cdot 4 \cdot 0.2980 = 0.9363$. The true value is 1. The error comes from the coarse detector: 7 bins of width $1/4$ cannot hold the sharp edge of the disk.

A finer setup gives a smaller error. The table gives the error of the code below on analytic projections with $a = 32$ angles, $d = 47$ bins, $\tau = 2\sqrt{2}/47$ and $n = 32$. These numbers are measurements of this setup, not bounds.

| phantom | Ram-Lak kernel | Shepp-Logan kernel |
|---|---|---|
| Gaussian $e^{-4\pi\vert x\vert^2}$, largest error | 0.0170 | 0.0239 |
| disk of radius $1/2$, largest error for $\vert x\vert < 0.35$ | 0.0098 | 0.0093 |
| disk of radius $1/2$, largest error at the edge | 0.40 | 0.40 |
| [Shepp-Logan phantom](/shepp-logan-phantom/), value at pixel $(16, 16)$, true 1.02 | 1.0217 | 1.0206 |

The large error at the edge of the disk is not a fault of the method. A pixel that the edge cuts has no single true value, and the band limit of the detector smooths the jump over about two bins.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) has four steps. First, the Fourier slice theorem and polar coordinates in the Fourier plane give $f = \mathcal{R}^\#(h * \mathcal{R}f)$ for continuous $f$ with an integrable Fourier transform. The Jacobian $|\sigma|$ of polar coordinates is the ramp. Second, the Ram-Lak values of line L2 are the samples of the inverse transform of $|\nu|$ on $|\nu| \le 1/(2\tau)$. Third, if each projection is band-limited to $|\nu| < 1/(2\tau)$, the discrete sum of line L6 gives the exact samples of the filtered projection, by the [sampling theorem](/sampling-theorem/). Fourth, with $L \ge 2d - 1$ the FFT product of lines L3 to L6 equals that sum, by the [convolution theorem](/convolution-theorem/). Line L8 is then the trapezoidal rule in $\theta$ for a function of period $\pi$, plus linear interpolation in $s$. These two steps are the only approximations on band-limited data.

## Complexity

In the real-RAM model with an FFT:

- Line L4 takes $O(d \log d)$, because $L < 4d$.
- Lines L5 and L6 take $a$ FFTs and $a$ inverse FFTs of length $L$, so $O(a d \log d)$.
- Lines L7 and L8 take $O(1)$ for each angle and pixel, so $O(a n^2)$.

The total is $O(a d \log d + a n^2)$ time and $O(a d + n^2)$ extra space. Without an FFT, the direct sum of line L6 takes $O(a d^2)$. In the usual case $a \approx d \approx n$, the back projection dominates and the total is $O(n^3)$. [Direct Fourier reconstruction](/direct-fourier-reconstruction/) takes $O(a d \log d + n^2 \log n)$, but it needs an interpolation in the Fourier plane, which gives worse artifacts.

## Properties

- **Linear.** The output is a linear function of the sinogram. Noise in the data maps to noise in the image by a fixed linear map, and the ramp amplifies the high frequencies of the noise.
- **One pass.** There is no iteration and no stopping rule. Each projection can be filtered and back-projected as soon as it arrives.
- **Not local in 2D.** The ramp kernel decays like $1/s^2$ and does not vanish. So the value at a pixel depends on rays far from it, and truncated projections give errors everywhere ([interior tomography](/interior-tomography/)).
- **The back projection is an adjoint.** Let $A$ be the pixel-driven projection matrix that puts the value of each pixel, times the pixel area $(2/n)^2$ over $\tau$, on the two nearest bins with linear weights. Then lines L7 and L8 apply $(\pi/a)\,(\tau/(2/n)^2)\,A^T$ to the filtered sinogram.

## Variants and improvements

- **Windowed ramps.** Multiply the ramp by a window (Shepp-Logan, cosine, Hamming, Hann) to reduce noise at the cost of resolution. See [window functions](/window-functions/).
- **The Hilbert form.** Since $|\sigma| = (2\pi)^{-1}\,(2\pi i\sigma)(-i\,\mathrm{sgn}\,\sigma)$, the filter is a derivative followed by the [Hilbert transform](/hilbert-transform/): $f = (2\pi)^{-1}\mathcal{R}^\#\,H\,\partial_s \mathcal{R}f$.
- **Fan beam and cone beam.** [Fan-beam FBP](/fan-beam-filtered-back-projection/) adds a weight and a distance factor. Another way is [fan-to-parallel rebinning](/fan-to-parallel-rebinning/) followed by parallel FBP. The [Feldkamp-Davis-Kress](/feldkamp-davis-kress/) method extends it to a circular cone beam, where it is exact only in the plane of the source circle.
- **Local reconstruction.** [Lambda tomography](/lambda-tomography/) replaces the ramp by a second derivative, which is local, and recovers the edges but not the values.
- **Iterative methods.** [SART](/sart/), [SIRT](/sirt/), the [Kaczmarz method](/kaczmarz-method/) and [MLEM](/mlem-reconstruction/) cost more, but they handle few views, missing angles and Poisson noise better.

## When to use it

Use FBP when the projections are complete, dense and not too noisy: many angles over $[0, \pi)$, an untruncated detector and enough dose. It is fast, it has no parameters except the window, and its output is linear and easy to analyze. For equal sample spacing on the outer ring of the Fourier plane, the arc between two angles at the radius $1/(2\tau)$, which is $\pi/(2a\tau)$, must equal the radial step $1/(d\tau)$. This gives the rule $a \approx \pi d/2$. With far fewer angles, or with missing angles, use an iterative method ([sparse-view CT](/sparse-view-ct-reconstruction/), [limited-angle tomography](/limited-angle-tomography/)).

## Pitfalls

- **Circular wrap.** Without zero padding to at least $2d - 1$, the DFT product is a circular convolution. The negative tail of the kernel then wraps around and corrupts both ends of each filtered projection.
- **Sampling $|k|$ on the DFT grid.** A ramp sampled in the DFT domain is zero at the zero frequency, but the band-limited ramp restricted to $d$ spatial samples is not. The result is a constant offset and a dished image. Sample the kernel in space, as in line L2, and transform it (Kak and Slaney, Section 3.3.3).
- **Wrong angle range or weight.** The angles must cover $[0, \pi)$ evenly with the weight $\pi/a$. Data over $[0, 2\pi)$ holds each line twice. Then the angle step is $2\pi/a$ and the sum counts each line twice, so the weight is again $\pi/a$, with $a$ the number of angles over $[0, 2\pi)$.
- **Detector offset.** The center of rotation must project to the position $(d-1)/2$ in bin units. An offset of half a bin blurs the image, and larger offsets give arcs around points.
- **No log transform.** The method needs line integrals. Transmission data must first become $-\ln(I/I_0)$ by the [Beer-Lambert law](/beer-lambert-law/).

## Implementations

## History

The formula that FBP discretizes is the [Radon inversion formula](/radon-inversion-formula/) in its Fourier form. Ramachandran and Lakshminarayanan published in 1971 the method of convolution with the sampled band-limited ramp, in place of the Fourier transforms of the earlier methods. Shepp and Logan proposed their smoother kernel in 1974, in the same paper that introduced their head phantom. Kak and Slaney give the discrete form with the zero padding rule that the code follows.

## References
