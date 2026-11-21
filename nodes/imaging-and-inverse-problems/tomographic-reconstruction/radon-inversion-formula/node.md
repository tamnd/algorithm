---
tag: WR750Q
kind: theorem
slug: radon-inversion-formula
name: Radon inversion formula
aliases:
- Radon's inversion theorem
area: imaging-and-inverse-problems/tomographic-reconstruction
level: core
summary: A function is recovered from its Radon transform by applying the Hilbert transform and a derivative in the radial variable, then back-projecting.
model: real-ram
prereqs: [fourier-slice-theorem, back-projection-operator, hilbert-transform]
see_also: [filtered-back-projection, ramp-filter, tomographic-reconstruction-problem, lambda-tomography, interior-tomography, degree-of-ill-posedness, grangeat-formula, novikov-inversion-formula]
sources:
  - paper: "J. Radon, Über die Bestimmung von Funktionen durch ihre Integralwerte längs gewisser Mannigfaltigkeiten, Berichte über die Verhandlungen der Königlich-Sächsischen Gesellschaft der Wissenschaften zu Leipzig, Math.-Phys. Klasse 69, 1917, pages 262 to 277"
    locator: the inversion formula in the plane through the mean values over the lines at distance q from a point
  - book: isbn:9780898714937
    title: F. Natterer, The Mathematics of Computerized Tomography, SIAM Classics in Applied Mathematics 32, 2001
    locator: Section II.2, inversion formulas; Section II.5, Sobolev space estimates; Section IV.3 (the singular value decomposition of the Radon transform)
  - book: isbn:9780898714944
    title: A. C. Kak and M. Slaney, Principles of Computerized Tomographic Imaging, SIAM Classics in Applied Mathematics 33, 2001
    locator: Chapter 3, Section 3.3.2, p. 67 (the filtered back-projection formula, equation 45) and pp. 67 to 68 (the Hilbert transform form)
  - paper: doi:10.1063/1.1729798
    title: A. M. Cormack, Representation of a function by its line integrals, with some radiological applications, Journal of Applied Physics 34(9), 1963
    locator: pp. 2722 to 2727
---

The Radon inversion formula recovers a function from all its line integrals. In the plane it says that $f$ is the back projection of the projections after a fixed filter: the derivative in $s$ followed by the [Hilbert transform](/hilbert-transform/), or the same thing in one step, the [ramp filter](/ramp-filter/) $|\sigma|$. It follows from the [Fourier slice theorem](/fourier-slice-theorem/) and polar coordinates in the Fourier plane. [Filtered back-projection](/filtered-back-projection/) is its discretization. In the plane the formula is not local, because the Hilbert transform is not. In three dimensions the formula for plane integrals needs only a second derivative, and it is local.

## Statement

Conventions: $\omega(\theta) = (\cos\theta, \sin\theta)$; $\mathcal{R}f(\theta, s) = \int f(s\,\omega + t\,\omega^\perp)\,dt$ for $\theta \in [0, \pi)$; the [back-projection operator](/back-projection-operator/) is $\mathcal{R}^\# g(x) = \int_0^\pi g(\theta, x\cdot\omega(\theta))\,d\theta$; the Fourier transform is $\mathcal{F}f(\xi) = \int f(x)\,e^{-2\pi i x\cdot\xi}\,dx$; and the Hilbert transform is $Hg(s) = \frac{1}{\pi}\,\mathrm{p.v.}\!\int \frac{g(t)}{s - t}\,dt$, whose Fourier multiplier is $-i\,\mathrm{sgn}\,\sigma$.

**Theorem 1 (Fourier form).** Let $f \in L^1(\mathbb{R}^2)$ be continuous, with $\mathcal{F}f \in L^1(\mathbb{R}^2)$. Put $p_\theta = \mathcal{R}f(\theta, \cdot)$ and
$$q_\theta(s) = \int_{-\infty}^{\infty} |\sigma|\,\mathcal{F}_1 p_\theta(\sigma)\,e^{2\pi i s\sigma}\,d\sigma.$$
For almost every $\theta$ this integral converges absolutely for every $s$, and for every $x \in \mathbb{R}^2$
$$f(x) = \int_0^\pi q_\theta(x\cdot\omega(\theta))\,d\theta = \mathcal{R}^\# q(x).$$

**Theorem 2 (Hilbert form).** Let $f$ be a Schwartz function on $\mathbb{R}^2$. Then for every $x$
$$f(x) = \frac{1}{2\pi}\,\mathcal{R}^\#\big(H\,\partial_s\,\mathcal{R}f\big)(x),$$
where $H$ and $\partial_s$ act on the variable $s$ for each fixed $\theta$. Radon's own form of this result is
$$f(x) = -\frac{1}{\pi}\int_0^\infty \frac{dF_x(q)}{q}, \qquad F_x(q) = \frac{1}{\pi}\int_0^\pi \mathcal{R}f(\theta, x\cdot\omega(\theta) + q)\,d\theta,$$
where $F_x(q)$ is the mean of the line integrals over the lines at distance $q$ from $x$.

**Theorem 3 (three dimensions).** Let $f$ be a Schwartz function on $\mathbb{R}^3$, let $\mathcal{R}f(\omega, s) = \int_{x\cdot\omega = s} f\,dA$ for $\omega \in S^2$ be the transform over planes, and let $\mathcal{R}^\# g(x) = \int_{S^2} g(\omega, x\cdot\omega)\,d\omega$. Then
$$f(x) = -\frac{1}{8\pi^2}\,\mathcal{R}^\#\big(\partial_s^2\,\mathcal{R}f\big)(x).$$

**Example.** For the Gaussian $f(x) = e^{-\pi|x|^2}$ in the plane, $\mathcal{R}f(\theta, s) = e^{-\pi s^2}$. Then $\partial_s\mathcal{R}f = -2\pi s\,e^{-\pi s^2}$ and $H\partial_s\mathcal{R}f(\theta, 0) = \frac{1}{\pi}\int 2\pi e^{-\pi t^2}\,dt = 2$. The back projection at the origin gives $\pi \cdot 2$, and $\frac{1}{2\pi}\cdot 2\pi = 1 = f(0)$. In Radon's form, $F_0(q) = e^{-\pi q^2}$, $dF_0/dq = -2\pi q\,e^{-\pi q^2}$, and $-\frac{1}{\pi}\int_0^\infty (-2\pi)\,e^{-\pi q^2}\,dq = 1$. For the Gaussian in $\mathbb{R}^3$, $\mathcal{R}f(\omega, s) = e^{-\pi s^2}$, $\partial_s^2\mathcal{R}f(\omega, 0) = -2\pi$, the back projection over the sphere of area $4\pi$ gives $-8\pi^2$, and Theorem 3 gives 1.

## In plain words

Smearing every projection back across the image gives a blurred copy of the object, because each smear also adds weight far from the place where it belongs. The blur weakens fine detail in proportion to its fineness. So sharpen each projection first, by a filter that boosts each wave in proportion to its frequency, and the smears then add up to the object exactly. The filter is a slope followed by a fixed spreading step. In the plane this step mixes values from the whole projection, so every point of the image depends on rays far away from it. In space, with integrals over planes, the filter is a plain second derivative, and each point depends only on the planes that pass close to it.

## Proof

**Theorem 1.** Since $f$ is continuous and $f, \mathcal{F}f \in L^1$, the Fourier inversion formula holds at every point: $f(x) = \int \mathcal{F}f(\xi)\,e^{2\pi i x\cdot\xi}\,d\xi$. Use polar coordinates with a signed radius, $\xi = \sigma\,\omega(\theta)$ with $\theta \in [0, \pi)$ and $\sigma \in \mathbb{R}$. This map covers the plane once except for the origin, and $d\xi = |\sigma|\,d\sigma\,d\theta$. So
$$f(x) = \int_0^\pi\!\!\int_{-\infty}^{\infty} \mathcal{F}f(\sigma\omega)\,e^{2\pi i\sigma\,x\cdot\omega}\,|\sigma|\,d\sigma\,d\theta.$$
The same change of variables gives $\int_0^\pi\int |\sigma|\,|\mathcal{F}f(\sigma\omega)|\,d\sigma\,d\theta = \|\mathcal{F}f\|_1 < \infty$, so by Fubini's theorem the inner integral converges absolutely for almost every $\theta$. By the Fourier slice theorem, $\mathcal{F}f(\sigma\omega(\theta)) = \mathcal{F}_1 p_\theta(\sigma)$, so the inner integral is $q_\theta(x\cdot\omega)$. $\square$

**Theorem 2.** For a Schwartz function $f$, each projection $p_\theta$ is a Schwartz function of $s$, with derivatives bounded uniformly in $\theta$, and $\mathcal{F}f$ is a Schwartz function, so Theorem 1 applies. The derivative $\partial_s$ has the multiplier $2\pi i\sigma$ and $H$ has the multiplier $-i\,\mathrm{sgn}\,\sigma$. Since $\partial_s p_\theta$ is a Schwartz function, $H\partial_s p_\theta$ is a bounded smooth function whose Fourier transform is $(-i\,\mathrm{sgn}\,\sigma)(2\pi i\sigma)\,\mathcal{F}_1 p_\theta(\sigma) = 2\pi|\sigma|\,\mathcal{F}_1 p_\theta(\sigma)$, which is integrable. So $\frac{1}{2\pi}H\partial_s p_\theta = q_\theta$, and Theorem 1 gives the claim.

For Radon's form, fix $x$ and put $g(q) = \frac{1}{\pi}\int_0^\pi \partial_s p_\theta(x\cdot\omega + q)\,d\theta = F_x'(q)$. By Theorem 2 and the definition of $H$,
$$f(x) = \frac{1}{2\pi}\int_0^\pi \frac{1}{\pi}\,\mathrm{p.v.}\!\int \frac{\partial_s p_\theta(x\cdot\omega + q)}{-q}\,dq\,d\theta = -\frac{1}{2\pi}\,\mathrm{p.v.}\!\int_{-\infty}^{\infty}\frac{g(q)}{q}\,dq,$$
after the shift $t = x\cdot\omega + q$. The rule $p_\theta(-s) = \mathcal{R}f(\theta + \pi, s)$ shows that $F_x$ is even in $q$, so $g$ is odd and $g(q)/q$ is even and bounded near 0. The principal value is then $2\int_0^\infty g(q)/q\,dq$, which gives $f(x) = -\frac{1}{\pi}\int_0^\infty F_x'(q)/q\,dq$. $\square$

**Theorem 3.** Fourier inversion in polar coordinates $\xi = \sigma\omega$ with $\omega \in S^2$ and $\sigma \ge 0$ gives $f(x) = \int_{S^2}\int_0^\infty \mathcal{F}f(\sigma\omega)\,e^{2\pi i\sigma\,x\cdot\omega}\,\sigma^2\,d\sigma\,d\omega$. The integrand is unchanged under $(\omega, \sigma) \to (-\omega, -\sigma)$, so the integral over $\sigma \ge 0$ is half the integral over $\sigma \in \mathbb{R}$. The Fourier slice theorem in $\mathbb{R}^3$ gives $\mathcal{F}f(\sigma\omega) = \mathcal{F}_1(\mathcal{R}f(\omega, \cdot))(\sigma)$, and $\sigma^2$ is the multiplier of $-\frac{1}{4\pi^2}\partial_s^2$. So
$$f(x) = \frac{1}{2}\int_{S^2} \left(-\frac{1}{4\pi^2}\right)\partial_s^2\,\mathcal{R}f(\omega, x\cdot\omega)\,d\omega = -\frac{1}{8\pi^2}\,\mathcal{R}^\#\big(\partial_s^2\mathcal{R}f\big)(x). \qquad\square$$

## Consequences

- **Filtered back-projection.** Theorem 1 is the formula $f = \mathcal{R}^\#(h * \mathcal{R}f)$ with the ramp $h$, $\mathcal{F}_1 h = |\sigma|$. Cutting the ramp off at the Nyquist frequency of the detector and sampling it gives the kernels of [filtered back-projection](/filtered-back-projection/).
- **Not local in the plane.** The Hilbert transform at $s$ uses $g(t)$ for all $t$, with weight $1/(s - t)$. So $f(x)$ depends on lines far from $x$, and data truncated to the lines that meet a region of interest do not give $f$ there by this formula ([interior tomography](/interior-tomography/)). [Lambda tomography](/lambda-tomography/) drops the Hilbert transform and recovers a local image with the same edges.
- **Local in space.** In $\mathbb{R}^3$, Theorem 3 needs only the plane integrals over planes near $x$, in a neighborhood of $s = x\cdot\omega$ for each $\omega$. The same holds in every odd dimension, with $\partial_s^{n-1}$. Cone-beam methods reach the plane integrals through the [Grangeat formula](/grangeat-formula/).
- **Instability.** The ramp multiplies the frequency $\sigma$ of the data by $|\sigma|$, so high-frequency noise grows without bound. The Radon transform on functions in the unit disk gains half a derivative in Sobolev norms (Natterer, Section II.5), and its distinct singular values decay like $m^{-1/2}$ (Natterer, Section IV.3). The value with index $m$ has multiplicity $m + 1$, so if each singular value is counted with its multiplicity, the $k$-th one decays like $k^{-1/4}$. On this page the [degree](/degree-of-ill-posedness/) of ill-posedness is the Sobolev order: the inversion is mildly ill-posed, of degree $1/2$.
- **Attenuation.** With an exponential weight along each line the formula fails. The [Novikov inversion formula](/novikov-inversion-formula/) replaces it for the attenuated transform.

## Tightness

- **Continuity and $\mathcal{F}f \in L^1$.** Theorem 1 needs pointwise Fourier inversion. For the unit disk, $\mathcal{F}f(\xi) = J_1(2\pi|\xi|)/|\xi|$ decays like $|\xi|^{-3/2}$, so $\mathcal{F}f \notin L^1(\mathbb{R}^2)$ and $|\sigma|\,\mathcal{F}_1 p_\theta$ is not integrable. The formula then needs a limit, for example a ramp cut off at a band limit that grows. At the edge of the disk no limit can give a single value. The [filtered back-projection](/filtered-back-projection/) page measures this effect.
- **All angles and all $s$.** The formula integrates over all $\theta \in [0, \pi)$ and all $s$. Finitely many angles do not determine $f$ (see the [Fourier slice theorem](/fourier-slice-theorem/)), and a missing range of angles makes the problem severely ill-posed ([limited-angle tomography](/limited-angle-tomography/)).
- **The constants.** $\frac{1}{2\pi}$ in Theorem 2 and $-\frac{1}{8\pi^2}$ in Theorem 3 hold for $\theta \in [0, \pi)$ in the plane, for the full sphere $S^2$ in space, and for ordinary frequency. A back projection over $[0, 2\pi)$ doubles the result, and a unitary Fourier convention moves the factors of $2\pi$.

## History

Radon published the inversion in 1917, for the plane through the mean values $F_x(q)$, and he gave the formulas for hyperplanes in higher dimensions in the same paper. Cormack found an inversion again in 1963 by circular harmonic expansions, for X-ray data, without knowing Radon's work. Hounsfield built the first clinical CT scanner, and Cormack and Hounsfield shared the 1979 Nobel Prize in Physiology or Medicine. Ramachandran and Lakshminarayanan turned the Fourier form into a convolution in 1971, which is [filtered back-projection](/filtered-back-projection/).

## References
