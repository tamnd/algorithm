---
tag: Y13A7M
kind: definition
slug: sinogram
name: Sinogram
area: imaging-and-inverse-problems/tomographic-reconstruction
level: intro
summary: The Radon transform data shown as an image over angle and detector position, where each point of the object traces a sinusoid.
model: real-ram
prereqs: [radon-transform]
see_also: [radon-transform, back-projection-operator, filtered-back-projection, fan-to-parallel-rebinning, shepp-logan-phantom, metal-artifact-reduction, sparse-view-ct-reconstruction, hough-transform]
sources:
  - book: isbn:9780898714944
    title: A. C. Kak and M. Slaney, Principles of Computerized Tomographic Imaging, SIAM Classics in Applied Mathematics 33, 2001
    locator: Chapter 3, Section 3.1, pp. 49 to 56 (parallel projections at a set of angles)
  - book: isbn:9780898714937
    title: F. Natterer, The Mathematics of Computerized Tomography, SIAM Classics in Applied Mathematics 32, 2001
    locator: Section II.4, the ranges (the moment conditions); Chapter III, sampling and resolution
---

A sinogram is the data of parallel-beam tomography, the [Radon transform](/radon-transform/) $\mathcal{R}f(\theta, s)$, drawn as an image with the angle $\theta$ on one axis and the detector position $s$ on the other. Each row is one projection. A single point of the object at $(x_0, y_0)$ contributes only on the curve $s = x_0\cos\theta + y_0\sin\theta$, which is a sinusoid in $\theta$. So the image of any object is a sum of sinusoids, and this gives the name. Reconstruction methods such as [filtered back-projection](/filtered-back-projection/) take a sinogram as input.

## Definition

Let $f$ be an integrable function on the plane with Radon transform $\mathcal{R}f(\theta, s) = \int f(s\,\omega + t\,\omega^\perp)\,dt$, where $\omega = (\cos\theta, \sin\theta)$ and $\omega^\perp = (-\sin\theta, \cos\theta)$. The **sinogram** of $f$ is the function $\mathcal{R}f$ on the strip $[0, \pi) \times \mathbb{R}$, seen as an image.

A scanner measures a **discrete sinogram**: an array $P[k][j]$ with $a$ rows and $d$ columns. Row $k$ belongs to the angle $\theta_k = k\pi/a$, and column $j$ to the detector bin with center $s_j = (j - (d-1)/2)\tau$, where $\tau$ is the detector spacing. Ideally $P[k][j] = \mathcal{R}f(\theta_k, s_j)$, or an average of $\mathcal{R}f$ over the bin. Some systems store angles over $[0, 2\pi)$; then each line is measured twice, because $\mathcal{R}f(\theta + \pi, -s) = \mathcal{R}f(\theta, s)$.

**The sinusoid of a point.** Write the point in polar form, $(x_0, y_0) = r(\cos\phi, \sin\phi)$. Then
$$s = x_0\cos\theta + y_0\sin\theta = r\cos(\theta - \phi).$$
The amplitude of the sinusoid is the distance $r$ of the point from the center of rotation, and its phase is the polar angle $\phi$. Points at the center give a straight line $s = 0$. The rows at $\theta$ and at $\theta + \pi$ are mirror images in $s$, so the sinogram over $[0, \pi)$ joins its own mirror image at the edge $\theta = \pi$.

**Properties.** Each of these holds for every integrable $f$:

- **Support.** If $f$ vanishes outside the disk of radius $r_0$ about the origin, the sinogram vanishes for $|s| > r_0$. A detector of half-width $r_0$ then sees the whole object.
- **Constant row mass.** $\int \mathcal{R}f(\theta, s)\,ds = \int f\,dx$ for each $\theta$, so all rows have the same sum.
- **Centroid sinusoid.** If $M = \int f\,dx \ne 0$ and $c$ is the centroid of $f$, then $\int s\,\mathcal{R}f(\theta, s)\,ds = M\,c\cdot\omega(\theta)$. So the centroid of each row lies on the sinusoid of the point $c$. A detector whose center is off by $\delta$ adds $\delta$ to every row centroid, which is a simple way to find the center of rotation.
- **Higher moments.** The $k$-th moment of each row is a homogeneous polynomial of degree $k$ in $\cos\theta$ and $\sin\theta$ (the Helgason-Ludwig conditions, Natterer, Section II.4). Measured sinograms with noise or [beam hardening](/beam-hardening/) fail these conditions.

## Examples and non-examples

**One point.** The point $(0.5, 0.25)$ has $r = 0.55902$ and $\phi = 0.46365$ rad. Its sinusoid passes through these values:

| $\theta$ | 0 | $\pi/4$ | $\pi/2$ | $3\pi/4$ |
|---|---|---|---|---|
| $s = 0.5\cos\theta + 0.25\sin\theta$ | 0.5 | 0.53033 | 0.25 | -0.17678 |

The largest value is $r = 0.55902$ at $\theta = \phi$.

**A centered disk.** The disk of radius $1/2$ with density 1 has the projection $2\sqrt{1/4 - s^2}$ at each angle. Its sinogram has equal rows: a band of half-width $1/2$ about $s = 0$. A disk of radius $\rho$ centered at $c$ gives a band of the same width that follows the sinusoid of $c$.

**The Shepp-Logan phantom.** The ten ellipses of the [Shepp-Logan phantom](/shepp-logan-phantom/) give a sinogram with a closed form, the sum of the ellipse projections. The head fills a band whose half-width goes between 0.69 at $\theta = 0$ and 0.92 at $\theta = \pi/2$, the extents of the outer ellipse along $\omega$.

**Sampling.** A discrete sinogram with $a$ angles and $d$ bins has equal sample spacing on the outer ring of the Fourier plane when $a \approx \pi d/2$, the rule derived on the [filtered back-projection](/filtered-back-projection/) page. With far fewer rows the problem becomes [sparse-view CT](/sparse-view-ct-reconstruction/).

**Non-example: raw intensities.** The detector counts $I$ are not a sinogram in this sense. The values $-\ln(I/I_0)$ are, by the [Beer-Lambert law](/beer-lambert-law/), and only for a monochromatic beam without scatter.

**Non-example: fan-beam data.** A fan-beam scanner records the data over the source angle and the fan angle. A point does not trace the sinusoid above in these coordinates, and the rows are not parallel projections. [Fan-to-parallel rebinning](/fan-to-parallel-rebinning/) resorts the data into a parallel sinogram.

## Related definitions

- [Radon transform](/radon-transform/): the function that the sinogram shows.
- [Back-projection operator](/back-projection-operator/): the adjoint, which maps a sinogram back to an image by summing along each sinusoid.
- [Hough transform](/hough-transform/): in its $(\theta, \rho)$ form, an edge point votes along the same sinusoid; the Hough accumulator of a point set is a discrete sinogram of the points.
- [Metal artifact reduction](/metal-artifact-reduction/): methods that find the trace of a metal object in the sinogram and replace it.

## References
