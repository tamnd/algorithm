---
tag: 2Y6GKS
kind: algorithm
slug: fan-beam-filtered-back-projection
name: Fan-beam filtered back-projection
aliases:
- fan-beam FBP
area: imaging-and-inverse-problems/tomographic-reconstruction
level: core
summary: Reconstruct a CT slice from rays that diverge from a point source. Weight each projection, filter it with a modified ramp, and back-project with the inverse squared source distance.
solves: [tomographic-reconstruction-problem]
model: real-ram
complexity:
  vars: {a: the number of source positions, d: the number of detector bins, n: the side of the n x n output image}
  time: {worst: "O(a d log d + a n^2)"}
  space: {extra: "O(a d + n^2)"}
properties: {deterministic: true, in_place: false, recursive: false, iterative: false, linear: true}
history:
  year: 1976
  people: [G. T. Herman, A. V. Lakshminarayanan, A. Naparstek]
  note: Herman, Lakshminarayanan and Naparstek gave a convolution method that works on divergent rays directly, without rebinning to parallel rays.
prereqs: [filtered-back-projection, radon-transform, ramp-filter]
see_also: [fan-to-parallel-rebinning, feldkamp-davis-kress, back-projection-operator, sinogram, shepp-logan-phantom, x-ray-transform, sart, lambda-tomography]
sources:
  - paper: doi:10.1016/0010-4825(76)90065-2
    title: G. T. Herman, A. V. Lakshminarayanan and A. Naparstek, Convolution reconstruction techniques for divergent beams, Computers in Biology and Medicine 6(4), 1976
    locator: pp. 259 to 271
  - paper: doi:10.1118/1.595078
    title: D. L. Parker, Optimal short scan convolution reconstruction for fan beam CT, Medical Physics 9(2), 1982
    locator: pp. 254 to 257 (the short-scan weights)
  - book: isbn:9780898714944
    title: A. C. Kak and M. Slaney, Principles of Computerized Tomographic Imaging, SIAM Classics in Applied Mathematics 33, 2001
    locator: Chapter 3, Section 3.4 (reconstruction from fan projections, equiangular rays and equally spaced collinear detectors) and Section 3.5 (a limited number of views)
---

Fan-beam filtered back-projection reconstructs a 2D image from the data of a CT scanner whose rays leave a point source and spread out in a fan. It is a version of [filtered back-projection](/filtered-back-projection/) that works on the fan data directly. Each projection is multiplied by a cosine weight and convolved with a modified ramp kernel, and each filtered projection is smeared back along its diverging rays with the weight $1/L^2$, where $L$ is the distance from the source. With $a$ source positions, $d$ detector bins and an $n \times n$ image it takes $O(a d \log d + a n^2)$ time with an FFT. A full scan of $2\pi$ gives each line twice. A short scan of $\pi$ plus the fan angle is enough with Parker's weights.

## In plain words

In a fan-beam scanner a small X-ray source and a curved detector turn around the patient together. The rays from the source fan out over the patient, so one projection does not hold parallel rays.

The method makes three changes to parallel FBP. First, each reading gets a cosine weight, because the fan spaces the rays unevenly. Second, the filter shape is stretched in the same way that the fan stretches the spacing of the rays. Third, when a filtered projection is smeared back, each point gets the value of the ray from the source through it, divided by the square of its distance to the source. Points near the source see the fan through a wide angle, and the division corrects for that. Then the sum over all source positions gives the image, as in the parallel case.

## The problem

The source at the angle $\beta$ is at $S(\beta) = D\,\omega^\perp(\beta)$, at the distance $D$ from the center of rotation, with $\omega(\beta) = (\cos\beta, \sin\beta)$ and $\omega^\perp(\beta) = (-\sin\beta, \cos\beta)$. The ray with the fan angle $\gamma$ leaves $S(\beta)$ in the direction $-\omega^\perp(\beta + \gamma)$. It is the line $\{x : x\cdot\omega(\theta) = s\}$ with $\theta = \beta + \gamma$ and $s = D\sin\gamma$. So the fan data is
$$g(\beta, \gamma) = \mathcal{R}f(\beta + \gamma, D\sin\gamma),$$
where $\mathcal{R}f(\theta, s) = \int f(s\,\omega + t\,\omega^\perp)\,dt$ is the [Radon transform](/radon-transform/). Each value is a line integral of the attenuation, which the scanner gets from the intensities by the [Beer-Lambert law](/beer-lambert-law/). The unknown $f$ is zero outside a disk of radius $r < D$.

An equiangular detector samples $\gamma_j = (j - (d-1)/2)\alpha$ for $j = 0, \ldots, d - 1$. A flat detector samples $t_j = (j - (d-1)/2)\tau$ on a line through the center normal to the central ray, and its ray has the fan angle $\arctan(t_j/D)$. A full scan takes $\beta_k = 2\pi k/a$ for $k = 0, \ldots, a - 1$. The output is an $n \times n$ image on $[-1, 1]^2$. Pixel $(i, j)$ has its center at $x_j = -1 + (2j+1)/n$ and $y_i = 1 - (2i+1)/n$, so row 0 is at the top and $y$ goes up.

For a point $x$ and a source $S(\beta)$, let $L$ be the distance from the source to $x$ and $\gamma'$ the fan angle of the ray through $x$:
$$L\cos\gamma' = D - x\cdot\omega^\perp(\beta), \qquad L\sin\gamma' = x\cdot\omega(\beta).$$
The algorithm evaluates the fan-beam inversion formula
$$f(x) = \int_0^{2\pi} \frac{1}{L^2}\int \kappa(\gamma' - \gamma)\,D\cos\gamma\,g(\beta, \gamma)\,d\gamma\,d\beta, \qquad \kappa(u) = \frac{1}{2}\left(\frac{u}{\sin u}\right)^2 h(u),$$
where $h$ is the [ramp filter](/ramp-filter/), the filter with the frequency response $|\sigma|$ in ordinary frequency. The proof below derives it from the parallel formula.

## The algorithm

```pseudo id=main
FAN-FBP(g, D, α, n)             ▷ g[k][j]: source angle β_k = 2πk/a, fan angle γ_j = (j - (d-1)/2) α
L1  a, d ← the number of rows and of columns of g
L2  κ[m] ← 1/(8α²) for m = 0, 0 for even m, -1/(2π² sin²(mα)) for odd m, m = -(d-1) .. d-1
L3  for k ← 0 to a - 1 do
L4      p[j] ← D cos(γ_j) · g[k][j] for each j
L5      q_k[j] ← α Σ_l κ[j - l] p[l] for each j      ▷ direct sum, or an FFT with zero padding to 2d - 1
L6  for each pixel (i, j) with center x = (x_j, y_i) do
L7      for each k: (L cos γ', L sin γ') ← (D - x·ω⊥(β_k), x·ω(β_k))
L8      f[i][j] ← Σ_k LININTERP(q_k, γ'/α + (d-1)/2) / L²
L9  return (2π/a) · f
```

Line L2 is the sampled kernel $\kappa(m\alpha) = \frac{1}{2}(m\alpha/\sin m\alpha)^2 h_B(m\alpha)$, where $h_B$ is the Ram-Lak kernel: the ramp cut off at the Nyquist frequency $1/(2\alpha)$ of the angular sampling. Since $h_B(m\alpha) = -1/(m^2\pi^2\alpha^2)$ for odd $m$, the factor $(m\alpha)^2$ cancels and only $\sin^2(m\alpha)$ remains. Line L4 is the cosine weight. Line L5 is an aperiodic [discrete convolution](/discrete-convolution/). Line L8 reads the filtered projection at the fan angle $\gamma'$ of the ray through the pixel, by linear interpolation with 0 outside the detector, and divides by $L^2$. Line L9 multiplies by the angle step.

For a flat detector, line L4 uses the weight $D/\sqrt{D^2 + t_j^2}$, line L2 uses $h_B/2$ with the spacing $\tau$, and line L8 reads the filtered projection at $t' = D\,x\cdot\omega/(D - x\cdot\omega^\perp)$ and divides by $U^2$ with $U = (D - x\cdot\omega^\perp)/D$. The code has both versions.

**Short scan.** Each line is measured twice in a full scan: the ray $(\beta, \gamma)$ and the ray $(\beta + \pi + 2\gamma, -\gamma)$ are the same line. A scan over $\beta \in [0, \pi + 2\delta]$, with $\delta$ at least the half fan angle, measures every line at least once. Parker's weights are
$$w(\beta, \gamma) = \begin{cases} \sin^2\!\left(\frac{\pi}{4}\frac{\beta}{\delta - \gamma}\right) & 0 \le \beta < 2(\delta - \gamma), \\ 1 & 2(\delta - \gamma) \le \beta \le \pi - 2\gamma, \\ \sin^2\!\left(\frac{\pi}{4}\frac{\pi + 2\delta - \beta}{\delta + \gamma}\right) & \pi - 2\gamma < \beta \le \pi + 2\delta, \end{cases}$$
and the weights of the two copies of each line add to 1. The short scan multiplies line L4 by $w(\beta_k, \gamma_j)$, takes $\beta_k = k(\pi + 2\delta)/a$, and uses the factor $2(\pi + 2\delta)/a$ in line L9. The formulas here are written in the geometry of this page. Parker's paper uses its own angle conventions.

## Example

Take the disk of radius $1/2$ with density 1 and a source at $D = 2$. Use $d = 5$ bins with $\alpha = 0.15$ and $a = 4$ source positions. The ray with fan angle $\gamma$ is at the distance $s = 2\sin\gamma$ from the center, and its line integral is $2\sqrt{1/4 - s^2}$. The disk is the same at each angle, so all four rows of $g$ are equal.

| quantity | values at $j = 0, \ldots, 4$ |
|---|---|
| fan angle $\gamma_j$ | -0.30, -0.15, 0, 0.15, 0.30 |
| data $g[k][j]$ | 0, 0.8017, 1, 0.8017, 0 |
| weighted $p[j] = 2\cos(\gamma_j)\,g[k][j]$ | 0, 1.5854, 2, 1.5854, 0 |
| filtered $q_k[j]$ | -0.6031, 0.6406, 0.5877, 0.6406, -0.6031 |

The kernel values are $\kappa(0) = 1/(8 \cdot 0.15^2) = 5.5556$, $\kappa(\pm 0.15) = -2.2685$, $\kappa(\pm 0.45) = -0.2678$, and 0 at the even offsets. So $q_k[2] = 0.15\,(5.5556 \cdot 2 - 2 \cdot 2.2685 \cdot 1.5854) = 0.5877$. At the center of the disk, $L = D = 2$ and $\gamma' = 0$ for every source, so line L8 gives $4 \cdot 0.5877/4 = 0.5877$ and line L9 gives $(2\pi/4) \cdot 0.5877 = 0.9232$. The true value is 1. The error comes from the coarse sampling.

A finer setup gives a smaller error. The table gives the measured error of the code on exact fan data with $D = 3$, a fan that covers the disk of radius $\sqrt{2}$ (half fan angle $28.13°$), $d = 49$ bins with $\alpha = 0.02045$, and $n = 32$. These numbers are measurements of this setup, not bounds.

| scan and phantom | result |
|---|---|
| full scan, $a = 64$, Gaussian $e^{-4\pi\vert x\vert^2}$, largest error | 0.0179 |
| short scan with Parker's weights, $a = 40$ over $\pi + 2\delta$, same Gaussian | 0.0182 |
| full scan, flat detector, $a = 64$, same Gaussian | 0.0215 |
| full scan, modified [Shepp-Logan phantom](/shepp-logan-phantom/) (first 5 ellipses), pixel $(16, 16)$, true 0.2 | 0.2097 |
| same, pixel $(8, 16)$ inside the small top ellipse, true 0.3 | 0.3087 |

The short scan uses 40 source positions against 64 for the full scan, and the error is almost the same.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) starts from the parallel formula $f(x) = \frac{1}{2}\int_0^{2\pi} (h * \mathcal{R}f(\theta, \cdot))(x\cdot\omega)\,d\theta$, with the ramp written as a finite-part integral. It changes the variables from $(\theta, s)$ to $(\beta, \gamma)$. The Jacobian of $(\theta, s) = (\beta + \gamma, D\sin\gamma)$ is $D\cos\gamma$, which gives the weight of line L4. The distance from $x$ to the ray $(\beta, \gamma)$ is $x\cdot\omega(\beta + \gamma) - D\sin\gamma = L\sin(\gamma' - \gamma)$. The ramp kernel is homogeneous of degree $-2$, so $h(L\sin u) = L^{-2}(u/\sin u)^2 h(u)$. This gives both the factor $1/L^2$ and the kernel $\kappa$. A lemma on finite parts shows that the change of the cut around the singular point does not change the result, and that the singular terms on both sides cancel. The same argument gives the flat-detector formula. For the short scan, any weight whose values on the two copies of each line add to 1 gives the same image, and Parker's weights have this property. The discrete algorithm then approximates the formula by the band-limited kernel, the sum over the bins, linear interpolation and the sum over the source angles.

## Complexity

In the real-RAM model:

- Line L2 takes $O(d)$.
- Lines L3 to L5 take $O(d^2)$ for each source with the direct sum, or $O(d \log d)$ with an FFT of length at least $2d - 1$, so $O(a d^2)$ or $O(a d \log d)$ in total.
- Lines L6 to L8 take $O(1)$ for each source and pixel, so $O(a n^2)$.

The total is $O(a d \log d + a n^2)$ time with an FFT and $O(a d^2 + a n^2)$ with the direct sum, which the code uses. The extra space is $O(a d + n^2)$ for the filtered projections and the image. This is the same order as parallel-beam FBP. The weight $1/L^2$ and the angle $\gamma'$ cost a few more operations per pixel than the parallel back-projection.

## Properties

- **Linear.** The output is a linear function of the fan data, as the code tests.
- **Exact in the limit.** The continuous formula is exact for a smooth $f$ supported inside the scan circle. The only errors come from the band limit and the sampling.
- **Not shift-invariant in the back-projection.** The weight $1/L^2$ depends on the pixel and the source, so the noise and the resolution vary across the image more than with parallel FBP.
- **Redundant full scan.** A full scan measures each line twice. The two copies add with the weight $\frac{1}{2}$ each, which is the $\frac{1}{2}$ inside $\kappa$.
- **Not local.** As in parallel FBP, the kernel decays like $1/\gamma^2$ and does not vanish, so a truncated detector gives errors everywhere ([interior tomography](/interior-tomography/)).

## Variants and improvements

- **Rebinning.** [Fan-to-parallel rebinning](/fan-to-parallel-rebinning/) interpolates the fan data to parallel rays and then runs parallel FBP. The back-projection has no $1/L^2$ weight, but the interpolation smooths the data.
- **Flat detector.** The formula with $t = D\tan\gamma$ uses the plain ramp $h/2$ and the weight $D/\sqrt{D^2 + t^2}$. This is the 2D case of the [Feldkamp-Davis-Kress](/feldkamp-davis-kress/) algorithm.
- **Short scan.** Parker's weights reduce the scan to $\pi$ plus the fan angle. Other smooth weights with the same sum rule also work, and the proof covers all of them.
- **Windows.** Multiply the ramp by a [window function](/window-functions/) to reduce noise at the cost of resolution, as in parallel FBP.
- **Iterative methods.** [SART](/sart/) and [SIRT](/sirt/) take any ray geometry, including fan beams, and handle few views better.

## When to use it

Use it for 2D CT with a fan-beam scanner, a full scan or a short scan, and an untruncated detector. It works on the data as the scanner records it, with no interpolation before the filter. If the data is rebinned anyway for other reasons, or if a parallel FBP code is at hand, rebinning is simpler. For a cone of rays in 3D, use [Feldkamp-Davis-Kress](/feldkamp-davis-kress/) for a circular scan or [Katsevich's algorithm](/katsevich-algorithm/) for a helical scan.

## Pitfalls

- **The wrong kernel.** The kernel in $\gamma$ is not the parallel ramp. Using $h_B(m\alpha)$ in place of $\kappa(m\alpha)$ drops the factor $(u/\sin u)^2$ and the $\frac{1}{2}$. The scale is then wrong by a factor 2, and the shape of the kernel is wrong away from its center.
- **Missing $1/L^2$.** Without the distance weight, each view adds its smear with the wrong weight, and the weight error depends on the pixel. The image is then off by a factor that varies across the image.
- **Short scan without weights.** A scan over $\pi + 2\delta$ counts some lines twice and others once. The proof needs weights whose values on the two copies of each line add to 1. Weights that jump from 0 to 1 satisfy the sum rule, but the ramp filter turns a jump in the data into a long tail, so the discrete result is worse. Parker's weights change smoothly.
- **Weights in the wrong convention.** Parker's formulas depend on the sign of $\gamma$ and on the start angle. Check the sum rule $w(\beta, \gamma) + w(\beta + \pi + 2\gamma, -\gamma) = 1$ in the geometry of the code, as the test does.
- **Center of rotation.** The central ray must hit the detector at the position $(d-1)/2$. An offset of a fraction of a bin gives ring-like blur, as in parallel FBP.

## Implementations

## History

CT scanners of the 1970s moved to fan beams, which need fewer motions than a parallel scan. One way to reconstruct is to rebin the fan data to parallel rays. Herman, Lakshminarayanan and Naparstek gave in 1976 a convolution method for divergent rays, which filters the fan data directly. The formula with the weight $1/L^2$ and the kernel $\kappa$ is the form that Kak and Slaney derive for equiangular rays and for equally spaced collinear detectors in their Section 3.4. Parker gave his short-scan weights in 1982, with smooth ramps at both ends of the scan.

## References
