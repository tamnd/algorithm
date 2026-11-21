---
tag: JVBXZD
kind: definition
slug: x-ray-transform
name: X-ray transform
aliases:
- ray transform
area: imaging-and-inverse-problems/tomographic-reconstruction
level: core
summary: The map that takes a function in n dimensions to its integrals along lines, equal to the Radon transform in the plane and different from it in space.
model: real-ram
prereqs: [radon-transform]
see_also: [radon-transform, fourier-slice-theorem, back-projection-operator, feldkamp-davis-kress, tuy-condition, grangeat-formula, katsevich-algorithm, attenuated-radon-transform]
sources:
  - paper: doi:10.1016/0022-247X(76)90008-1
    title: D. C. Solmon, The X-ray transform, Journal of Mathematical Analysis and Applications 56(1), 1976
    locator: pp. 61 to 83 (the X-ray transform in n dimensions, its Fourier slice relation and its inversion)
  - book: isbn:9780898714937
    title: F. Natterer, The Mathematics of Computerized Tomography, SIAM Classics in Applied Mathematics 32, 2001
    locator: Section II.1 (the X-ray transform P and the divergent beam transform D next to the Radon transform R)
  - paper: doi:10.1090/S0002-9904-1977-14406-6
    title: K. T. Smith, D. C. Solmon and S. L. Wagner, Practical and mathematical aspects of the problem of reconstructing objects from radiographs, Bulletin of the American Mathematical Society 83(6), 1977
    locator: pp. 1227 to 1270 (the X-ray and divergent beam transforms and what finite data determine)
---

The X-ray transform takes a function $f$ on $\mathbb{R}^n$ to its integrals along all straight lines. It models X-ray imaging in any dimension, because a ray measures the integral of the attenuation along a line, by the [Beer-Lambert law](/beer-lambert-law/). In the plane the lines are the hyperplanes, so the X-ray transform and the [Radon transform](/radon-transform/) are the same thing with a different parametrization. In $\mathbb{R}^3$ they differ: the Radon transform integrates over planes and the X-ray transform over lines, and CT scanners measure line integrals.

## Definition

Let $f \in L^1(\mathbb{R}^n)$. For a direction $\theta \in S^{n-1}$ and a point $x$ in the hyperplane $\theta^\perp = \{x : x\cdot\theta = 0\}$, the **X-ray transform** of $f$ is
$$\mathcal{P}f(\theta, x) = \int_{-\infty}^{\infty} f(x + t\theta)\,dt.$$
Each line in $\mathbb{R}^n$ is $\{x + t\theta\}$ for exactly one pair $(\pm\theta, x)$ with $x \in \theta^\perp$, and $\mathcal{P}f(-\theta, x) = \mathcal{P}f(\theta, x)$. For a fixed $\theta$, the function $\mathcal{P}f(\theta, \cdot)$ on $\theta^\perp$ is the parallel projection, or radiograph, in the direction $\theta$. By Fubini's theorem $\int_{\theta^\perp} |\mathcal{P}f(\theta, x)|\,dx \le \|f\|_1$, so the integral exists for almost every $x$.

**The plane.** For $n = 2$, take $\theta = \omega^\perp(\phi) = (-\sin\phi, \cos\phi)$ and $x = s\,\omega(\phi)$ with $\omega(\phi) = (\cos\phi, \sin\phi)$. Then $\mathcal{P}f(\omega^\perp(\phi), s\,\omega(\phi)) = \mathcal{R}f(\phi, s)$. The X-ray transform names a line by its direction, the Radon transform by its normal.

**The divergent beam transform.** A point source at $a$ gives the integrals along half-lines, $\mathcal{D}f(a, \theta) = \int_0^\infty f(a + t\theta)\,dt$. For $f$ with support away from $a$, $\mathcal{D}f(a, \theta) + \mathcal{D}f(a, -\theta) = \mathcal{P}f(\theta, x)$ with $x$ the projection of $a$ on $\theta^\perp$. Fan-beam and cone-beam CT measure $\mathcal{D}f$ for sources on a curve.

**Fourier slice relation.** With the Fourier transform in ordinary frequency, $\mathcal{F}f(\xi) = \int f(x) e^{-2\pi i x\cdot\xi}\,dx$, the $(n-1)$-dimensional transform of the projection on $\theta^\perp$ is
$$\int_{\theta^\perp} \mathcal{P}f(\theta, x)\, e^{-2\pi i x\cdot\xi}\,dx = \mathcal{F}f(\xi) \quad \text{for } \xi \in \theta^\perp.$$
The proof is Fubini's theorem: write each $y \in \mathbb{R}^n$ as $x + t\theta$, and note that $e^{-2\pi i y\cdot\xi} = e^{-2\pi i x\cdot\xi}$ when $\xi \perp \theta$. So one radiograph gives $\mathcal{F}f$ on the whole hyperplane $\theta^\perp$, not only on a line as in the 2D [Fourier slice theorem](/fourier-slice-theorem/). With Natterer's unitary transform the same relation has the factor $(2\pi)^{1/2}$.

## Examples and non-examples

**The ball in 3D.** Let $f = 1$ on the unit ball of $\mathbb{R}^3$. A line at distance $r = |x| \le 1$ from the center cuts a chord of length $2\sqrt{1 - r^2}$, so $\mathcal{P}f(\theta, x) = 2\sqrt{1 - |x|^2}$ for $|x| \le 1$ in each direction. The plane at distance $s$ cuts a disk of radius $\sqrt{1 - s^2}$, so the 3D Radon transform is $\mathcal{R}f(\omega, s) = \pi(1 - s^2)$. The two transforms of the same ball are different functions. Both have the right mass: $\int_0^1 2\sqrt{1 - r^2}\,2\pi r\,dr = 4\pi/3$ and $\int_{-1}^1 \pi(1 - s^2)\,ds = 4\pi/3$, the volume of the ball.

**The Gaussian in 3D.** For $f(x) = e^{-\pi|x|^2}$, $\mathcal{P}f(\theta, x) = e^{-\pi|x|^2}$ on $\theta^\perp$, a 2D Gaussian, and $\mathcal{R}f(\omega, s) = e^{-\pi s^2}$. Both match $\mathcal{F}f(\xi) = e^{-\pi|\xi|^2}$ through the slice relation above and through the slice theorem for planes.

**From lines to planes.** Integrating the radiograph $\mathcal{P}f(\theta, \cdot)$ along a line in $\theta^\perp$ gives the integral of $f$ over a plane that contains $\theta$. So the X-ray transform determines the 3D Radon transform on all planes that contain a measured direction. The [Grangeat formula](/grangeat-formula/) uses a related identity for cone-beam data, where only a derivative of the plane integrals is available.

**Enough directions.** In $\mathbb{R}^3$ the lines form a 4-parameter family and $f$ has 3 variables, so not all lines are needed. If the directions $\theta$ fill one great circle, for example all directions with $\theta_3 = 0$, then each measured line lies in a plane $x_3 = c$, and the data are the 2D Radon transforms of all these slices. This is slice-by-slice CT, and it determines $f$.

**Non-example: the 3D Radon transform.** Integrals of $f$ over planes are not X-ray data. In 3D they are the data of the Radon inversion formula $f = -(8\pi^2)^{-1}\mathcal{R}^\#\partial_s^2\mathcal{R}f$, which is local, while X-ray data in a plane need the nonlocal 2D formula ([Radon inversion formula](/radon-inversion-formula/)).

**Non-example: a circular cone-beam scan.** A source that moves on one circle measures $\mathcal{D}f$ for a set of lines that does not meet the [Tuy condition](/tuy-condition/). The data do not determine $f$ off the plane of the circle in a stable way, and the [Feldkamp-Davis-Kress](/feldkamp-davis-kress/) method is an approximation there. A helical source orbit meets the condition, and the [Katsevich algorithm](/katsevich-algorithm/) inverts it exactly.

## Related definitions

- [Radon transform](/radon-transform/): integrals over hyperplanes. It is the X-ray transform when $n = 2$.
- [Back-projection operator](/back-projection-operator/): the adjoint, which sums over all measured lines through a point.
- [Fourier slice theorem](/fourier-slice-theorem/): the 2D form of the slice relation above.
- [Attenuated Radon transform](/attenuated-radon-transform/): line integrals with an exponential weight along the line.
- [Tuy condition](/tuy-condition/): the condition on a source curve under which cone-beam data determine $f$.

## References
