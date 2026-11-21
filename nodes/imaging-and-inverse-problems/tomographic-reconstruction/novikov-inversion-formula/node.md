---
tag: NZ4FX2
kind: theorem
slug: novikov-inversion-formula
name: Novikov inversion formula
area: imaging-and-inverse-problems/tomographic-reconstruction
level: research
summary: An explicit formula that inverts the attenuated Radon transform in the plane for a known attenuation map, found by Novikov in 2002.
model: real-ram
prereqs: [attenuated-radon-transform, radon-inversion-formula, hilbert-transform]
see_also: [radon-transform, filtered-back-projection, back-projection-operator, emission-tomography-model, mlem-reconstruction, degree-of-ill-posedness, fourier-slice-theorem, tomographic-reconstruction-problem]
sources:
  - paper: doi:10.1007/BF02384507
    title: R. G. Novikov, An inversion formula for the attenuated X-ray transformation, Arkiv for Matematik 40(1), 2002
    locator: pp. 145 to 167 (the inversion formula and its proof)
  - paper: doi:10.1088/0266-5611/17/1/309
    title: F. Natterer, Inversion of the attenuated Radon transform, Inverse Problems 17(1), 2001
    locator: pp. 113 to 119 (the form of the formula with h = (1/2)(I + iH) R mu, and a short proof)
  - paper: doi:10.1088/0266-5611/17/2/309
    title: L. A. Kunyansky, A new SPECT reconstruction algorithm based on the Novikov explicit inversion formula, Inverse Problems 17(2), 2001
    locator: pp. 293 to 306 (a discrete implementation and numerical tests)
  - paper: doi:10.1137/0139029
    title: O. Tretiak and C. Metz, The exponential Radon transform, SIAM Journal on Applied Mathematics 39(2), 1980
    locator: pp. 341 to 354 (the earlier inversion for a constant attenuation)
---

The Novikov inversion formula recovers a function $f$ in the plane from its [attenuated Radon transform](/attenuated-radon-transform/) $g = \mathcal{R}_\mu f$, when the attenuation map $\mu$ is known. It is the inverse for SPECT data with a measured attenuation map. Like the [Radon inversion formula](/radon-inversion-formula/), it is a filter in the detector variable followed by a weighted back projection. The filter is the [Hilbert transform](/hilbert-transform/) between two multiplications by complex factors built from the Radon transform of $\mu$, and the back projection has the weight $e^{D\mu}$. For $\mu = 0$ it is the classical formula. Novikov published it in 2002, and Natterer gave a short form and proof in 2001.

## Statement

Use the notation of the [attenuated Radon transform](/attenuated-radon-transform/) page: $\omega = (\cos\theta, \sin\theta)$, $\omega^\perp = (-\sin\theta, \cos\theta)$, $D\mu(x, v) = \int_0^\infty \mu(x + \tau v)\,d\tau$, and
$$g(\theta, s) = \mathcal{R}_\mu f(\theta, s) = \int f(s\omega + t\omega^\perp)\, e^{-D\mu(s\omega + t\omega^\perp,\ \omega^\perp)}\,dt, \qquad \theta \in [0, 2\pi).$$
Let $H$ be the Hilbert transform in $s$, $(Hu)(s) = \frac{1}{\pi}\,\mathrm{p.v.}\!\int \frac{u(t)}{s - t}\,dt$, and let $\mathcal{R}\mu$ be the Radon transform of $\mu$ on $[0, 2\pi) \times \mathbb{R}$.

**Theorem (Novikov 2002, in the form of Natterer 2001).** Let $f$ and $\mu$ be smooth functions with compact support in $\mathbb{R}^2$. Put
$$h(\theta, \cdot) = \tfrac12\,(I + iH)\,\mathcal{R}\mu(\theta, \cdot).$$
Then for every $x \in \mathbb{R}^2$
$$f(x) = \frac{1}{4\pi}\,\mathrm{Re}\,\mathrm{div}_x \int_0^{2\pi} \omega\, e^{D\mu(x, \omega^\perp)}\, \big(e^{-h} H e^{h} g\big)(\theta, x\cdot\omega)\,d\theta.$$
Here $e^{-h} H e^{h} g$ means, for each $\theta$: multiply $g(\theta, \cdot)$ by $e^{h(\theta, \cdot)}$, apply $H$ in $s$, and multiply by $e^{-h(\theta, \cdot)}$. The result is evaluated at $s = x\cdot\omega$.

The formula uses the data for all $\theta \in [0, 2\pi)$. For a known $\mu$ it shows that $\mathcal{R}_\mu$ is one-to-one on these functions.

## In plain words

In SPECT the body absorbs part of the light on its way out. How much it absorbs depends on where the light starts and on the side the camera looks from. So the data are not the plain sums along lines that ordinary CT uses.

If the absorption is known, for example from a separate X-ray scan, the formula undoes it exactly. It has three steps. First, it multiplies each projection by a correction that comes from the absorption along each line. Second, it applies the same filter as ordinary CT. Third, it undoes the correction and smears each filtered projection back over the image with a weight that is larger where the absorption on the way to the camera is larger.

Without absorption, all the corrections disappear, and the formula is the usual filtered back projection.

## Proof

The full proof is in Novikov (2002) and, shorter, in Natterer (2001). This section proves the case $\mu = 0$ and gives the structure of the general proof as a sketch.

**The case $\mu = 0$.** Then $h = 0$, $e^{D\mu} = 1$ and $g = \mathcal{R}f$. Put $u(\theta, s) = (Hg)(\theta, s)$. Since $\nabla_x (x\cdot\omega) = \omega$ and $\omega\cdot\omega = 1$,
$$\mathrm{div}_x\big[\omega\, u(\theta, x\cdot\omega)\big] = \partial_s u(\theta, x\cdot\omega) = (H\partial_s g)(\theta, x\cdot\omega).$$
Everything is real, so the formula reads $f(x) = \frac{1}{4\pi}\int_0^{2\pi} (H\partial_s \mathcal{R}f)(\theta, x\cdot\omega)\,d\theta$. The pairs $\theta$ and $\theta + \pi$ give the same value: $\mathcal{R}f(\theta + \pi, -s) = \mathcal{R}f(\theta, s)$, so $u = \partial_s \mathcal{R}f$ satisfies $u(\theta + \pi, s) = -u(\theta, -s)$. A change of variable $t \to -t$ in the integral of $H$ then gives $(Hu)(\theta + \pi, s) = (Hu)(\theta, -s)$, so the integrand has the same value at $\theta + \pi$ and at $\theta$. So the integral over $[0, 2\pi)$ is twice the integral over $[0, \pi)$, and $f(x) = \frac{1}{2\pi}\int_0^\pi (H\partial_s\mathcal{R}f)(\theta, x\cdot\omega)\,d\theta$. This is the [Radon inversion formula](/radon-inversion-formula/) with this normalization of $H$. $\square$

**The general case (sketch).** The steps of Natterer's proof are these.

1. *A transport equation.* For each direction $v = \omega^\perp$, let $u$ solve $v\cdot\nabla u + \mu u = f$ with $u \to 0$ far back along $v$. Since $\partial_t e^{-D\mu(x + tv, v)} = \mu\, e^{-D\mu(x + tv, v)}$, the integrating factor gives $\partial_t\big(e^{-D\mu} u\big) = e^{-D\mu} f$ along each line. Far ahead along $v$, $D\mu = 0$, so the limit of $u$ there is $g(\theta, x\cdot\omega)$. So the data are the outgoing values of a transport equation.
2. *A complex family.* Write the direction as a point on the unit circle of $\mathbb{C}$ and replace it by a complex number $\lambda$. For $|\lambda| \ne 1$ the transport operator becomes an elliptic first-order operator in $x$, and the equation has a unique solution that decays at infinity. It depends analytically on $\lambda$ inside and outside the unit circle.
3. *The jump.* On the circle the solution from inside and the solution from outside differ. The jump is a Cauchy-type integral, and the Plemelj formulas write it with the Hilbert transform of the data in $s$. The factor $e^{h}$ appears here: $(I + iH)$ maps a real function to the boundary value of a function that is analytic in a half plane of the variable $s$. So $e^{\pm h}$ are boundary values of analytic functions, and they absorb the term $\mu u$, as the integrating factor $e^{-D\mu}$ does on each line.
4. *The limit.* Cauchy's formula in $\lambda$, and the behavior of the solution as $\lambda \to 0$, give $f$ as the real part of a divergence. The back projection over $\theta \in [0, 2\pi)$ comes from the integral along the circle, and $e^{D\mu(x, \omega^\perp)}$ undoes the integrating factor at the point $x$.

The sketch is not a proof; the details of steps 2 to 4 need the cited papers.

**A numerical check (a measurement).** Take $\mu = 1$ on the unit disk and 0 outside, so that $\mathcal{R}\mu = 2\sqrt{1 - s^2}$ and $H\mathcal{R}\mu = 2s$ for $|s| < 1$, and a Gaussian $f(x) = \exp(-|x - c|^2/(2\cdot 0.12^2))$ with $c = (0.3, 0.1)$. The data were computed by quadrature on 256 angles in $[0, 2\pi)$ and 501 values of $s$, the Hilbert transform by a discrete rule on the same grid, and the divergence in closed form. At the 6 points $(0.3, 0.1)$, $(0.4, 0.1)$, $(0.3, 0.25)$, $(0.2, 0)$, $(-0.3, -0.4)$ and $(0, 0.5)$, the formula gave $f$ with an error below $2 \cdot 10^{-5}$; for example $0.70664$ against $0.70665$ at $(0.4, 0.1)$. With $\omega^\perp$ replaced by $-\omega^\perp$ in the back projection weight, the result was off by 7 to 16 percent at the points where $f$ is not small, so the sign conventions above match each other. The attenuation map of this test is not smooth at the edge of the disk, while the theorem assumes a smooth one.

## Consequences

- **Filtered back projection for SPECT.** The formula is a filter in $s$ for each angle and a weighted back projection, so it has the structure and the cost of [filtered back projection](/filtered-back-projection/): for $a$ angles, $d$ bins and an $n \times n$ image, $O(a d^2 + a n^2)$ if the filter is applied by a sum over the bins, or $O(a\, d \log d + a n^2)$ with an FFT-based Hilbert transform. Kunyansky (2001) implemented it and tested it on simulated SPECT data.
- **Uniqueness.** For a known $\mu$, $f$ is determined by $\mathcal{R}_\mu f$ on $[0, 2\pi) \times \mathbb{R}$.
- **Constant attenuation.** For $\mu$ constant on a convex region, the formula gives an inversion of the exponential Radon transform, the case that Tretiak and Metz solved in 1980.
- **The same instability as CT.** The formula has one derivative and one Hilbert transform, as the Radon inversion formula does, so noise in $g$ is amplified in a similar way. For a smooth $\mu$ the problem is expected to have the same [degree of ill-posedness](/degree-of-ill-posedness/), $1/2$, as the Radon transform; this page does not prove it. In practice the filter is cut off at high frequencies, as in CT.
- **A reference for iterative methods.** With Poisson data, iterative methods on the [emission tomography model](/emission-tomography-model/), such as [MLEM](/mlem-reconstruction/) with the attenuation in the system matrix, are the common choice. The formula is the exact answer for noise-free data and is useful to test them.

## Tightness

- **The full circle of angles.** The formula uses $g$ for all $\theta \in [0, 2\pi)$. For $\mu \ne 0$, the data on $[\pi, 2\pi)$ are not a copy of the data on $[0, \pi)$, and the formula does not apply to a half scan.
- **A known attenuation.** The formula needs $\mu$. Finding both $f$ and $\mu$ from emission data alone is a different problem, and it is not solved by this formula.
- **Smoothness.** The theorem is stated for smooth $f$ and $\mu$. The numerical check above suggests that it still works for a $\mu$ with a jump, but that is a measurement for one example, not a theorem on this page.
- **The plane.** The formula is two-dimensional. Parallel-hole SPECT measures a stack of planes, so it applies plane by plane; other geometries need other formulas.
- **Not an algorithm for noisy data.** Exact inversion of noisy data amplifies the noise; the formula says nothing about a regularized solution.

## History

Tretiak and Metz (1980) inverted the attenuated transform when the attenuation is constant on a known convex region. For a general known attenuation, the explicit inversion in the plane was an open problem in SPECT for about two decades. Novikov found the explicit formula; it appeared in 2002 in Arkiv for Matematik. Natterer (2001) gave the formula with the function $h = \frac12(I + iH)\mathcal{R}\mu$ and a short proof based on analytic functions. Kunyansky (2001) turned it into a reconstruction algorithm and tested it numerically.

## References
