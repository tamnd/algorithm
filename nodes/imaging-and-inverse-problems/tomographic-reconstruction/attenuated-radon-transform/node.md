---
tag: KJR2GS
kind: definition
slug: attenuated-radon-transform
name: Attenuated Radon transform
area: imaging-and-inverse-problems/tomographic-reconstruction
level: advanced
summary: The Radon transform with an exponential weight from the attenuation along each line, the model of SPECT data.
model: real-ram
prereqs: [radon-transform, beer-lambert-law]
see_also: [novikov-inversion-formula, x-ray-transform, emission-tomography-model, back-projection-operator, sinogram, radon-inversion-formula, hilbert-transform, mlem-reconstruction]
sources:
  - paper: doi:10.1007/BF02384507
    title: R. G. Novikov, An inversion formula for the attenuated X-ray transformation, Arkiv for Matematik 40(1), 2002
    locator: pp. 145 to 167 (the attenuated transform in the plane and its explicit inversion)
  - paper: doi:10.1088/0266-5611/17/1/309
    title: F. Natterer, Inversion of the attenuated Radon transform, Inverse Problems 17(1), 2001
    locator: pp. 113 to 119 (the definition with the divergent beam transform, and a short derivation of the inversion)
  - paper: doi:10.1137/0139029
    title: O. Tretiak and C. Metz, The exponential Radon transform, SIAM Journal on Applied Mathematics 39(2), 1980
    locator: pp. 341 to 354 (the case of a constant attenuation and its inversion)
  - book: isbn:9780898716221
    title: F. Natterer and F. Wubbeling, Mathematical Methods in Image Reconstruction, SIAM, 2001
    locator: Chapter 2, Integral Geometry, pp. 9 to 40 (the attenuated Radon transform among the integral transforms of tomography; general locator)
---

The attenuated Radon transform is the model of single photon emission computed tomography (SPECT). A tracer with activity $f(x)$ sends out photons, and a photon that starts at $x$ and moves toward the detector is absorbed on its way with a rate $\mu$, the attenuation map. By the [Beer-Lambert law](/beer-lambert-law/), the photon reaches the detector with the probability $\exp(-\int \mu)$, where the integral runs from $x$ to the detector. So each measured line integral of $f$ has a weight that depends on the point and on the direction of travel. With $\mu = 0$ it is the [Radon transform](/radon-transform/). For a known $\mu$, the [Novikov inversion formula](/novikov-inversion-formula/) recovers $f$ exactly.

## Definition

Let $\omega(\theta) = (\cos\theta, \sin\theta)$ and $\omega^\perp(\theta) = (-\sin\theta, \cos\theta)$, as on the [Radon transform](/radon-transform/) page. For an attenuation map $\mu \ge 0$ and a direction $v$, the **divergent beam transform** is
$$D\mu(x, v) = \int_0^\infty \mu(x + \tau v)\,d\tau,$$
the integral of $\mu$ on the half line from $x$ in the direction $v$. For $f$ and $\mu$ continuous with compact support, the **attenuated Radon transform** of $f$ is
$$\mathcal{R}_\mu f(\theta, s) = \int_{-\infty}^{\infty} f(s\,\omega + t\,\omega^\perp)\, e^{-D\mu(s\omega + t\omega^\perp,\ \omega^\perp)}\,dt, \qquad \theta \in [0, 2\pi),\ s \in \mathbb{R},$$
with $\omega = \omega(\theta)$ and $\omega^\perp = \omega^\perp(\theta)$. The integral runs over the line $x \cdot \omega = s$, as for the Radon transform. The weight $e^{-D\mu}$ is the fraction of the photons from the point $s\omega + t\omega^\perp$ that reach a detector far away in the direction $\omega^\perp$. This is the convention of Natterer; other papers put the detector on the other side, which changes $\omega^\perp$ to $-\omega^\perp$.

The angle runs over the full circle $[0, 2\pi)$. The pairs $(\theta, s)$ and $(\theta + \pi, -s)$ give the same line, but the photons move in opposite directions, so the weights differ. In general $\mathcal{R}_\mu f(\theta + \pi, -s) \ne \mathcal{R}_\mu f(\theta, s)$, and the data on $[0, \pi)$ do not determine the data on $[\pi, 2\pi)$. A SPECT camera that turns through $360$ degrees measures both.

Some properties follow from the definition.

- **Linear in $f$.** $\mathcal{R}_\mu(\alpha f + \beta g) = \alpha\,\mathcal{R}_\mu f + \beta\,\mathcal{R}_\mu g$ for a fixed $\mu$.
- **Not linear in $\mu$.** The map $\mu \mapsto \mathcal{R}_\mu f$ is nonlinear, because $\mu$ is in an exponent. Finding both $f$ and $\mu$ from $\mathcal{R}_\mu f$ alone is a different and harder problem.
- **Reduces to the Radon transform.** For $\mu = 0$, $\mathcal{R}_0 f(\theta, s) = \mathcal{R}f(\theta, s)$ for every $\theta \in [0, 2\pi)$.
- **Bounded by the Radon transform.** Since $\mu \ge 0$, the weight is in $(0, 1]$, so $0 \le \mathcal{R}_\mu f \le \mathcal{R}f$ for $f \ge 0$.
- **Adjoint.** For a fixed $\mu$, the adjoint is the attenuated back projection $\mathcal{R}_\mu^\# g(x) = \int_0^{2\pi} e^{-D\mu(x, \omega^\perp(\theta))}\, g(\theta, x \cdot \omega(\theta))\,d\theta$. It is the [back-projection operator](/back-projection-operator/) with the same weight.
- **A discrete form.** A system matrix for SPECT puts the weight $e^{-D\mu}$, computed for each pixel and each direction, into the row of each ray. The result is a nonnegative matrix for the [emission tomography model](/emission-tomography-model/), and [MLEM](/mlem-reconstruction/) applies to it directly.

## Examples and non-examples

**A uniform disk.** Let $f = 1$ and $\mu = \mu_0$ on the unit disk, and 0 outside. Put $h = \sqrt{1 - s^2}$ for $|s| \le 1$. The line at distance $s$ meets the disk for $t \in [-h, h]$, and the photon from the point $t$ crosses the length $h - t$ of the disk on its way out. So
$$\mathcal{R}_\mu f(\theta, s) = \int_{-h}^{h} e^{-\mu_0 (h - t)}\,dt = \frac{1 - e^{-2\mu_0 h}}{\mu_0}.$$
At $\mu_0 = 1$ and $s = 0$ this is $1 - e^{-2} = 0.864665$, against the Radon value $2$. As $\mu_0 \to 0$ it tends to $2h$, the Radon transform of the disk. Here the data do not depend on $\theta$, and they are the same for $(\theta, s)$ and $(\theta + \pi, -s)$, because the object and the attenuation are symmetric.

**A point source off center.** Let $f$ be a unit point mass at $x_0 = (0.5, 0)$, and $\mu = 1$ on the unit disk. Then $\mathcal{R}_\mu f(\theta, s) = \delta(s - x_0\cdot\omega)\, e^{-D\mu(x_0, \omega^\perp)}$. At $\theta = \pi/2$, $\omega^\perp = (-1, 0)$, and the photon crosses the length $1.5$ of the disk: the weight is $e^{-1.5} = 0.2231$. At $\theta = 3\pi/2$, which gives the same line, $\omega^\perp = (1, 0)$ and the length is $0.5$: the weight is $e^{-0.5} = 0.6065$. The two directions of one line give different data. This is why the full circle of angles is needed.

**Non-example: PET data.** In positron emission tomography the two photons of one event move in opposite directions along the same line, and both must reach the detectors. The product of the two weights is $e^{-\mathcal{R}\mu(\theta, s)}$, the same for every point of the line. So PET data are $e^{-\mathcal{R}\mu}\,\mathcal{R}f$: the Radon transform times a known factor, which a transmission scan measures. It is not an attenuated Radon transform in the sense above, and the attenuation correction is a division.

**A special case: constant attenuation.** If $\mu = \mu_0$ on a known convex region that holds the support of $f$, the weight can be split into a factor that depends only on the line and the factor $e^{\mu_0 t}$. After this correction the data are the exponential Radon transform $\int f(s\omega + t\omega^\perp)\, e^{\mu_0 t}\,dt$. Tretiak and Metz (1980) inverted it with a filtered back projection with a modified filter.

**Non-example: a transmission scan.** In transmission CT the source is outside the body, and the data are $e^{-\mathcal{R}\mu}$ for the attenuation $\mu$ itself. Taking the log gives the Radon transform of $\mu$. There is no emission activity $f$ and no weight inside the integral.

## Related definitions

- [Radon transform](/radon-transform/): the case $\mu = 0$.
- [X-ray transform](/x-ray-transform/): the line integrals in any dimension; the attenuated X-ray transform adds the same weight.
- [Novikov inversion formula](/novikov-inversion-formula/): the explicit inverse of $\mathcal{R}_\mu$ in the plane for a known $\mu$.
- [Radon inversion formula](/radon-inversion-formula/): the inverse for $\mu = 0$, which the Novikov formula reduces to.
- [Hilbert transform](/hilbert-transform/): the filter in $s$ that appears in both inversion formulas.
- [Emission tomography model](/emission-tomography-model/): the Poisson model for the counts, where a discrete $\mathcal{R}_\mu$ is the system matrix of SPECT.
- [Sinogram](/sinogram/): the data shown as an image over $(\theta, s)$; for SPECT it covers $\theta \in [0, 2\pi)$.

## References
