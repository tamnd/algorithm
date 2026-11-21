---
tag: ZSW55A
kind: theorem
slug: fourier-slice-theorem
name: Fourier slice theorem
aliases:
- projection-slice theorem
- central slice theorem
area: imaging-and-inverse-problems/tomographic-reconstruction
level: core
summary: The 1D Fourier transform of a parallel projection at angle theta equals the 2D Fourier transform of the object along the line through the origin at that angle.
model: real-ram
prereqs: [radon-transform]
see_also: [radon-transform, radon-inversion-formula, filtered-back-projection, direct-fourier-reconstruction, diffraction-tomography, common-lines-method, polar-format-algorithm, convolution-theorem]
sources:
  - paper: doi:10.1071/PH560198
    title: R. N. Bracewell, Strip integration in radio astronomy, Australian Journal of Physics 9, 1956
    locator: pp. 198 to 217 (the 1D transform of a strip scan as a line of the 2D transform)
  - book: isbn:9780898714937
    title: F. Natterer, The Mathematics of Computerized Tomography, SIAM Classics in Applied Mathematics 32, 2001
    locator: Section II.1 (the projection theorem for the Radon and X-ray transforms, with the factor (2 pi)^((n-1)/2) of the unitary Fourier transform)
  - book: isbn:9780898714944
    title: A. C. Kak and M. Slaney, Principles of Computerized Tomographic Imaging, SIAM Classics in Applied Mathematics 33, 2001
    locator: Chapter 3, Section 3.2, pp. 56 to 60 (the Fourier slice theorem); Section 3.7, p. 110 (its history)
  - paper: doi:10.1090/S0002-9904-1977-14406-6
    title: K. T. Smith, D. C. Solmon and S. L. Wagner, Practical and mathematical aspects of the problem of reconstructing objects from radiographs, Bulletin of the American Mathematical Society 83(6), 1977
    locator: pp. 1227 to 1270 (finitely many projections do not determine an object with compact support)
---

The Fourier slice theorem says that a projection of an object carries one line of the object's Fourier transform. Take the projection of $f$ at the angle $\theta$, which is the [Radon transform](/radon-transform/) $\mathcal{R}f(\theta, \cdot)$, and take its 1D Fourier transform. The result is the 2D Fourier transform of $f$ on the line through the origin with the direction $\omega(\theta)$. All reconstruction methods of parallel-beam CT rest on it: [filtered back-projection](/filtered-back-projection/), [direct Fourier reconstruction](/direct-fourier-reconstruction/) and the [Radon inversion formula](/radon-inversion-formula/). The Fourier diffraction theorem of [diffraction tomography](/diffraction-tomography/) is its analog for waves under the Born or Rytov approximation: there a projection gives the transform on an arc of a circle, not on a line.

## Statement

The Fourier transform uses ordinary frequency: $\mathcal{F}f(\xi) = \int_{\mathbb{R}^n} f(x)\,e^{-2\pi i x\cdot\xi}\,dx$ and $\mathcal{F}_1 p(\sigma) = \int_{\mathbb{R}} p(s)\,e^{-2\pi i s\sigma}\,ds$. Let $\omega(\theta) = (\cos\theta, \sin\theta)$.

**Theorem (Fourier slice).** Let $f \in L^1(\mathbb{R}^2)$ and $\theta \in [0, \pi)$. Then the projection $p_\theta = \mathcal{R}f(\theta, \cdot)$ is in $L^1(\mathbb{R})$, and for every $\sigma \in \mathbb{R}$
$$\mathcal{F}_1 p_\theta(\sigma) = \mathcal{F}f(\sigma\,\omega(\theta)).$$

The same holds in $\mathbb{R}^n$ for the Radon transform over hyperplanes: for $f \in L^1(\mathbb{R}^n)$ and $\omega \in S^{n-1}$, the 1D transform of $s \mapsto \mathcal{R}f(\omega, s)$ at $\sigma$ is $\mathcal{F}f(\sigma\omega)$. In this convention there is no constant. With the unitary transform $\hat f(\xi) = (2\pi)^{-n/2}\int f(x)\,e^{-i x\cdot\xi}\,dx$ used by Natterer, the theorem reads $\widehat{\mathcal{R}f}(\omega, \sigma) = (2\pi)^{(n-1)/2}\hat f(\sigma\omega)$.

**Example.** For the unit disk, $f = 1$ on $|x| \le 1$, the projection is $2\sqrt{1 - s^2}$ at each angle. At $\sigma = 0.5$, numerical quadrature of $\int_{-1}^1 2\sqrt{1 - s^2}\cos(\pi s)\,ds$ gives 0.569231. The 2D transform of the disk is $\mathcal{F}f(\xi) = J_1(2\pi|\xi|)/|\xi|$, with $J_1$ the Bessel function of order 1, and at $|\xi| = 0.5$ it is $J_1(\pi)/0.5 = 0.569231$. For the Gaussian $e^{-\pi|x|^2}$, both sides equal $e^{-\pi\sigma^2}$.

## In plain words

Shine parallel rays through a flat object and record how much each ray loses. The record is a 1D profile. Break the profile into waves along the detector. Each of these waves is also a wave of the object itself, one that runs across the object in the direction of the detector and is constant along the rays. So the profile tells you exactly the waves of the object that run in one direction, and nothing about the waves in other directions. Turn the object and you get another direction. With all directions, you know all waves of the object, and so the object.

## Proof

Fix $\theta$ and write $\omega = \omega(\theta)$ and $\omega^\perp = (-\sin\theta, \cos\theta)$. The map $(s, t) \mapsto x = s\,\omega + t\,\omega^\perp$ is a rotation of the plane, so it keeps area, $dx = ds\,dt$, and $x\cdot\omega = s$.

First, $p_\theta \in L^1$. By Tonelli's theorem and the change of variables,
$$\int |p_\theta(s)|\,ds \le \iint |f(s\omega + t\omega^\perp)|\,dt\,ds = \int |f(x)|\,dx = \|f\|_1 < \infty.$$
So $p_\theta(s)$ is finite for almost every $s$, and $p_\theta$ is integrable.

Next, for $\sigma \in \mathbb{R}$ the function $(s, t) \mapsto f(s\omega + t\omega^\perp)\,e^{-2\pi i s\sigma}$ is integrable on $\mathbb{R}^2$, with the same bound. So Fubini's theorem applies:
$$\mathcal{F}_1 p_\theta(\sigma) = \int \left(\int f(s\omega + t\omega^\perp)\,dt\right) e^{-2\pi i s\sigma}\,ds = \int_{\mathbb{R}^2} f(x)\,e^{-2\pi i (x\cdot\omega)\sigma}\,dx = \mathcal{F}f(\sigma\omega).$$
The middle step uses $s = x\cdot\omega$ and $dx = ds\,dt$. $\square$

In $\mathbb{R}^n$ the proof is the same, with $x = s\,\omega + y$ for $y \in \omega^\perp$ and $dx = ds\,dy$. For the unitary transform, the 1D transform carries $(2\pi)^{-1/2}$ and the $n$-dimensional one $(2\pi)^{-n/2}$, which gives the factor $(2\pi)^{(n-1)/2}$.

## Consequences

- **Uniqueness.** If $f \in L^1(\mathbb{R}^2)$ and $\mathcal{R}f = 0$ for almost every line, then $\mathcal{F}f = 0$ on almost every line through the origin. Since $\mathcal{F}f$ is continuous, $\mathcal{F}f = 0$ everywhere, and $f = 0$ by the uniqueness of the Fourier transform. So $\mathcal{R}$ is injective on $L^1(\mathbb{R}^2)$.
- **Inversion.** Write the inverse Fourier transform in polar coordinates with $\theta \in [0, \pi)$ and $\sigma \in \mathbb{R}$, where $d\xi = |\sigma|\,d\sigma\,d\theta$, and replace $\mathcal{F}f(\sigma\omega)$ by $\mathcal{F}_1 p_\theta(\sigma)$. The result is $f = \mathcal{R}^\#(h * \mathcal{R}f)$, where $h$ has the frequency response $|\sigma|$ (the [ramp filter](/ramp-filter/)) and $\mathcal{R}^\#$ is the [back-projection operator](/back-projection-operator/). The full statement and its hypotheses are on the page of the [Radon inversion formula](/radon-inversion-formula/).
- **Fourier reconstruction.** The 1D transforms of the projections fill the Fourier plane on a polar grid. Interpolation onto a Cartesian grid and an inverse 2D FFT give [direct Fourier reconstruction](/direct-fourier-reconstruction/).
- **Convolution.** For $f, g \in L^1(\mathbb{R}^2)$, $\mathcal{R}(f * g)(\theta, \cdot) = \mathcal{R}f(\theta, \cdot) * \mathcal{R}g(\theta, \cdot)$, a 1D convolution in $s$. Both sides have the 1D transform $\mathcal{F}f(\sigma\omega)\,\mathcal{F}g(\sigma\omega)$ by the theorem and the [convolution theorem](/convolution-theorem/). A blur of the object is a blur of each projection.
- **Band limits.** If $\mathcal{F}f$ vanishes for $|\xi| > b$, each projection is band-limited to $b$. By the [sampling theorem](/sampling-theorem/), a detector spacing $\tau < 1/(2b)$ then gives all of $\mathcal{F}f$ on each measured line.
- **Few projections.** Finitely many projections give $\mathcal{F}f$ on finitely many lines only. There are nonzero functions with compact support whose transform vanishes on any given finite set of lines, so finitely many projections do not determine $f$ (Smith, Solmon and Wagner 1977). Results for finite data hold for functions that are essentially band-limited.
- **Other fields.** Two 2D projections of a 3D object have transforms that are planes through the origin, and two planes meet in a line. The [common lines method](/common-lines-method/) of cryo-electron microscopy finds the relative orientation from this line. The [polar format algorithm](/polar-format-algorithm/) of radar imaging uses the same polar geometry.

## Tightness

- **The hypothesis $f \in L^1$.** It cannot be dropped to $f \in L^2$. The function $f(x) = 1/((2 + |x|)\ln(2 + |x|))$ is in $L^2(\mathbb{R}^2)$, because $\int^\infty r\,dr/(r^2\ln^2 r) < \infty$. But along every line $\int dt/((2 + |t|)\ln(2 + |t|))$ diverges, so no projection exists. For $f \in L^2$ with compact support the theorem holds, because such $f$ is in $L^1$.
- **The constant.** The equality without a constant holds only for the ordinary-frequency transform, or for the angular-frequency transform $\int f e^{-i x\cdot\xi}\,dx$ on both sides. Mixing conventions gives a factor $(2\pi)^{(n-1)/2}$, as in Natterer.
- **Lines through the origin.** One projection gives $\mathcal{F}f$ on one line through the origin and nowhere else. The transform on a line that misses the origin is not a projection of $f$; it is a projection of $f$ times a plane wave.
- **The straight-ray model.** The theorem is about line integrals. If the measured rays bend or scatter, as for ultrasound or for light when the wavelength is not small compared with the features, the data are not the Radon transform. Under the first Born approximation the data give $\mathcal{F}f$ on arcs instead ([diffraction tomography](/diffraction-tomography/)).

## History

Radon solved the inversion problem in 1917 without the Fourier transform. Bracewell showed in 1956 that the 1D transform of a strip scan of a radio source is a line of its 2D transform, so that scans at several angles fill the 2D transform. DeRosier and Klug used the same relation in 1968 for 3D reconstruction in electron microscopy (Kak and Slaney, Section 3.7). The relation is also behind the convolution method of Ramachandran and Lakshminarayanan of 1971, which turned the Fourier route into [filtered back-projection](/filtered-back-projection/).

## References
