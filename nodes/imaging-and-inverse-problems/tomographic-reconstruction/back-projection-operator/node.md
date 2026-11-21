---
tag: ACE0CH
kind: definition
slug: back-projection-operator
name: Back-projection operator
aliases:
- backprojection
- unfiltered back-projection
area: imaging-and-inverse-problems/tomographic-reconstruction
level: core
summary: The adjoint of the Radon transform, which sets each point to the sum of the projection values on all lines through it and gives a blurred image.
model: real-ram
prereqs: [radon-transform]
see_also: [radon-transform, sinogram, filtered-back-projection, ramp-filter, radon-inversion-formula, universal-back-projection, sar-backprojection, sirt]
sources:
  - book: isbn:9780898714937
    title: F. Natterer, The Mathematics of Computerized Tomography, SIAM Classics in Applied Mathematics 32, 2001
    locator: Section II.1 (the backprojection operator as the adjoint of R, and the convolution form of its product with R)
  - book: isbn:9780898714944
    title: A. C. Kak and M. Slaney, Principles of Computerized Tomographic Imaging, SIAM Classics in Applied Mathematics 33, 2001
    locator: Chapter 3, Section 3.3.1 (backprojection as the smearing of each filtered projection over the image plane)
---

The back-projection operator $\mathcal{R}^\#$ takes data on lines back to the plane. It sets the value at a point $x$ to the integral, over all angles, of the data on the line through $x$ at that angle. It is the adjoint of the [Radon transform](/radon-transform/) in $L^2$, but it is not its inverse: applied to the data of an object, it gives the object blurred by the kernel $1/|x|$. [Filtered back-projection](/filtered-back-projection/) applies it after a [ramp filter](/ramp-filter/) and then gets the object back. The [universal back-projection](/universal-back-projection/) of photoacoustic tomography has a similar name but a different meaning: it is an exact inversion formula for spherical means, with its own weights and derivatives, not the adjoint of $\mathcal{R}$.

## Definition

Let $\omega(\theta) = (\cos\theta, \sin\theta)$. For a function $g$ on $[0, \pi) \times \mathbb{R}$, the **back projection** of $g$ is the function on the plane
$$\mathcal{R}^\# g(x) = \int_0^\pi g(\theta, x\cdot\omega(\theta))\,d\theta.$$
For each angle, $x\cdot\omega(\theta)$ is the position $s$ of the line through $x$ with normal $\omega(\theta)$. So $\mathcal{R}^\#$ smears each projection $g(\theta, \cdot)$ evenly along the direction $\omega^\perp(\theta)$ of its lines, and adds the smears of all angles.

**Adjoint.** For $f \in L^2(\mathbb{R}^2)$ with compact support and $g \in L^2([0, \pi) \times \mathbb{R})$ with compact support in $s$,
$$\int_0^\pi\!\!\int \mathcal{R}f(\theta, s)\,g(\theta, s)\,ds\,d\theta = \int_{\mathbb{R}^2} f(x)\,\mathcal{R}^\# g(x)\,dx.$$
*Proof.* For a fixed $\theta$, the map $(s, t) \mapsto x = s\,\omega + t\,\omega^\perp$ is a rotation, so $dx = ds\,dt$ and $s = x\cdot\omega$. So $\int \mathcal{R}f(\theta, s)\,g(\theta, s)\,ds = \iint f(s\omega + t\omega^\perp)\,g(\theta, s)\,dt\,ds = \int f(x)\,g(\theta, x\cdot\omega)\,dx$. Integrate over $\theta$ and exchange the order by Fubini's theorem. $\square$

**The blur of back projection.** Let $f$ be continuous with compact support. Then
$$\mathcal{R}^\#\mathcal{R}f(x) = \int_{\mathbb{R}^2} \frac{f(y)}{|x - y|}\,dy = \left(\frac{1}{|\cdot|} * f\right)(x).$$
*Proof.* $\mathcal{R}^\#\mathcal{R}f(x) = \int_0^\pi\int f((x\cdot\omega)\,\omega + t\,\omega^\perp)\,dt\,d\theta$. Since $x = (x\cdot\omega)\,\omega + (x\cdot\omega^\perp)\,\omega^\perp$, the shift $t \to t + x\cdot\omega^\perp$ turns the inner integral into $\int f(x + t\,\omega^\perp)\,dt$. The map $(\theta, t) \mapsto y = x + t\,\omega^\perp(\theta)$ with $\theta \in [0, \pi)$ and $t \in \mathbb{R}$ is polar coordinates about $x$ with a signed radius, so $dy = |t|\,dt\,d\theta$ and $|t| = |y - x|$. $\square$

With the Fourier transform in ordinary frequency, the transform of $1/|x|$ in the plane is $1/|\xi|$. So $\mathcal{F}(\mathcal{R}^\#\mathcal{R}f)(\xi) = \mathcal{F}f(\xi)/|\xi|$. Back projection damps the frequency $|\xi|$ by the factor $1/|\xi|$. The ramp filter $|\sigma|$ on each projection cancels this factor, which is the [Radon inversion formula](/radon-inversion-formula/) $f = \mathcal{R}^\#(h * \mathcal{R}f)$.

**Discrete form.** For a sinogram $P[k][j]$ at the angles $\theta_k = k\pi/a$ and the bin centers $s_j = (j - (d-1)/2)\tau$, the discrete back projection is
$$B[P](x) = \frac{\pi}{a}\sum_{k=0}^{a-1} P_k(x\cdot\omega(\theta_k)),$$
where $P_k(s)$ reads row $k$ at the position $s$ by linear interpolation between bin centers, with 0 outside the detector. The factor $\pi/a$ is the angle step. For a projection matrix $A$ whose rows hold the weights of each pixel in each bin, $B$ is a scaled $A^T$. Iterative methods such as [SIRT](/sirt/) use $A^T$ in this role.

## Examples and non-examples

**The unit disk.** The disk $|x| \le 1$ with density 1 has $\mathcal{R}f(\theta, s) = 2\sqrt{1 - s^2}$. At the center, $\mathcal{R}^\#\mathcal{R}f(0) = \int_0^\pi 2\,d\theta = 2\pi = 6.28319$. At $x = (0.5, 0)$ it is $\int_0^\pi 2\sqrt{1 - 0.25\cos^2\theta}\,d\theta = 5.86985$, and at $x = (0.9, 0)$ it is 4.68679. The convolution $\int_{|y| \le 1} |x - y|^{-1}\,dy$ gives the same numbers. The true value is 1 at each of these points. The image is a dome, not a flat disk, and it does not vanish outside the disk.

**The Gaussian.** For $f(x) = e^{-\pi|x|^2}$, $\mathcal{R}f(\theta, s) = e^{-\pi s^2}$, so $\mathcal{R}^\#\mathcal{R}f(0) = \pi$, while $f(0) = 1$. The other side gives the same: $\int e^{-\pi|y|^2}/|y|\,dy = 2\pi\int_0^\infty e^{-\pi r^2}\,dr = \pi$.

**A point.** The sinogram of a unit point at the origin is $\delta(s)$ at each angle. Its back projection is $1/|x|$, a peak with a slow tail. This is the point spread function of unfiltered back projection, and the tail is the reason for the blur.

**Data over $[0, 2\pi)$.** Back projection over the full circle counts each line twice and gives $2\,\mathcal{R}^\#$. A discrete back projector over $[0, 2\pi)$ with $a$ angles needs the weight $\pi/a$, not $2\pi/a$.

**Non-example: the inverse.** $\mathcal{R}^\#$ is not $\mathcal{R}^{-1}$, as the disk shows. Neither is any scalar multiple of it, because the factor $1/|\xi|$ differs for each frequency.

**Non-example: SAR back projection.** [SAR back projection](/sar-backprojection/) sums radar echoes along range curves with a phase correction. It has the same idea of summing data over all curves through a point, but its data are complex echoes over time, and it is the adjoint of a different forward operator.

## Related definitions

- [Radon transform](/radon-transform/): the operator whose adjoint is $\mathcal{R}^\#$.
- [Ramp filter](/ramp-filter/): the filter $|\sigma|$ that undoes the $1/|\xi|$ factor.
- [Filtered back-projection](/filtered-back-projection/): the algorithm $\mathcal{R}^\#(h * \cdot)$.
- [Radon inversion formula](/radon-inversion-formula/): the exact inverse, in Fourier form and in Hilbert form.
- [Universal back-projection](/universal-back-projection/): the inversion formula of photoacoustic tomography, a different operator.
- [Forward operator](/forward-operator/): the general notion of an operator and its adjoint.

## References
