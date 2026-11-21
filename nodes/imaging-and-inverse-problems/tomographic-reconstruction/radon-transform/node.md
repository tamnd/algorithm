---
tag: 27X3XV
kind: definition
slug: radon-transform
name: Radon transform
area: imaging-and-inverse-problems/tomographic-reconstruction
level: intro
summary: The map that takes a function on the plane to its integrals along all lines, indexed by the angle and the signed distance of the line from the origin.
model: real-ram
prereqs: [forward-operator]
see_also: [x-ray-transform, sinogram, back-projection-operator, fourier-slice-theorem, radon-inversion-formula, attenuated-radon-transform, parabolic-radon-transform, hough-transform]
sources:
  - paper: "J. Radon, Über die Bestimmung von Funktionen durch ihre Integralwerte längs gewisser Mannigfaltigkeiten, Berichte über die Verhandlungen der Königlich-Sächsischen Gesellschaft der Wissenschaften zu Leipzig, Math.-Phys. Klasse 69, 1917, pages 262 to 277"
    locator: the definition of the line integrals of a function on the plane and their inversion
  - book: isbn:9780898714937
    title: F. Natterer, The Mathematics of Computerized Tomography, SIAM Classics in Applied Mathematics 32, 2001
    locator: Section II.1, definition and elementary properties of some integral operators; Section II.4, the ranges
  - book: isbn:9780898714944
    title: A. C. Kak and M. Slaney, Principles of Computerized Tomographic Imaging, SIAM Classics in Applied Mathematics 33, 2001
    locator: Chapter 3, Section 3.1, pp. 49 to 56 (line integrals and projections, the Shepp-Logan phantom of Fig. 3.4 and the projection of an ellipse, equation 5)
  - paper: doi:10.1063/1.1729798
    title: A. M. Cormack, Representation of a function by its line integrals, with some radiological applications, Journal of Applied Physics 34(9), 1963
    locator: pp. 2722 to 2727
---

The Radon transform takes a function $f$ on the plane to the set of its integrals along all lines. It is the [forward operator](/forward-operator/) of parallel-beam CT, where each line integral is the log of an X-ray intensity ratio by the [Beer-Lambert law](/beer-lambert-law/). In the plane it is the same object as the [X-ray transform](/x-ray-transform/); in $n \ge 3$ dimensions the Radon transform integrates over hyperplanes, the X-ray transform over lines. The [parabolic Radon transform](/parabolic-radon-transform/) of seismic processing is a different transform: it sums a data gather along parabolas in time and offset, not a function along straight lines.

## Definition

Let $\omega(\theta) = (\cos\theta, \sin\theta)$ and $\omega^\perp(\theta) = (-\sin\theta, \cos\theta)$. For $f \in L^1(\mathbb{R}^2)$, the **Radon transform** of $f$ is the function
$$\mathcal{R}f(\theta, s) = \int_{-\infty}^{\infty} f(s\,\omega(\theta) + t\,\omega^\perp(\theta))\,dt, \qquad \theta \in [0, \pi),\ s \in \mathbb{R}.$$
The integral runs over the line $\{x : x \cdot \omega(\theta) = s\}$, that is, $x_1\cos\theta + x_2\sin\theta = s$. The number $s$ is the signed distance of the line from the origin, and $\omega(\theta)$ is its unit normal. By Fubini's theorem the integral exists for almost every $(\theta, s)$, and $\int |\mathcal{R}f(\theta, s)|\,ds \le \|f\|_1$ for each $\theta$. For a continuous $f$ with compact support it exists for every $(\theta, s)$. The function $\mathcal{R}f(\theta, \cdot)$ for one fixed $\theta$ is the **projection** at the angle $\theta$.

The pair $(\theta + \pi, -s)$ gives the same line as $(\theta, s)$, so if $\theta$ is allowed in $[0, 2\pi)$ then $\mathcal{R}f(\theta + \pi, -s) = \mathcal{R}f(\theta, s)$ and each line appears twice. This page and the other tomography pages use $\theta \in [0, \pi)$ and $s \in \mathbb{R}$, the convention of Kak and Slaney. Natterer writes $\theta$ for the unit vector itself, on the circle $S^1$.

In $\mathbb{R}^n$ the Radon transform integrates over hyperplanes: $\mathcal{R}f(\omega, s) = \int_{x\cdot\omega = s} f(x)\,dA(x)$ for $\omega \in S^{n-1}$, where $dA$ is the $(n-1)$-dimensional surface measure. For $n = 2$ this is the definition above.

Some properties follow at once from the definition. They hold for every $f \in L^1(\mathbb{R}^2)$.

- **Linear.** $\mathcal{R}(\alpha f + \beta g) = \alpha\,\mathcal{R}f + \beta\,\mathcal{R}g$.
- **Shift.** If $g(x) = f(x - a)$, then $\mathcal{R}g(\theta, s) = \mathcal{R}f(\theta, s - a\cdot\omega(\theta))$. A shift of the object shifts each projection by the component of $a$ along $\omega$.
- **Rotation.** If $g$ is $f$ rotated by the angle $\alpha$, then $\mathcal{R}g(\theta, s) = \mathcal{R}f(\theta - \alpha, s)$, with the angle taken modulo $\pi$ together with the sign rule above. A radial $f$ has the same projection at each angle.
- **Mass.** $\int \mathcal{R}f(\theta, s)\,ds = \int f(x)\,dx$ for each $\theta$.
- **Moments.** For each integer $k \ge 0$, $\int s^k\,\mathcal{R}f(\theta, s)\,ds = \int (x\cdot\omega)^k f(x)\,dx$, which is a homogeneous polynomial of degree $k$ in $\cos\theta$ and $\sin\theta$ when the moments of $f$ exist. These are the Helgason-Ludwig range conditions (Natterer, Section II.4). A function $g(\theta, s)$ that fails them is not the Radon transform of any function, so noisy data are in general outside the range.
- **Bounded on a disk.** If $f$ vanishes outside the unit disk, the Cauchy-Schwarz inequality on a chord of length at most 2 gives $|\mathcal{R}f(\theta, s)|^2 \le 2\int |f(s\omega + t\omega^\perp)|^2\,dt$. Integration over $s$ and over $\theta \in [0, \pi)$ gives $\|\mathcal{R}f\|^2 \le 2\pi\|f\|^2$ in $L^2$. So $\mathcal{R}$ is a bounded operator from $L^2$ of the disk to $L^2([0, \pi) \times [-1, 1])$. Its adjoint is the [back-projection operator](/back-projection-operator/).

## Examples and non-examples

**The unit disk.** Let $f = 1$ on $|x| \le 1$ and 0 outside. The line at distance $|s| \le 1$ cuts the disk in a chord of length $2\sqrt{1 - s^2}$, so $\mathcal{R}f(\theta, s) = 2\sqrt{1 - s^2}$ for $|s| \le 1$ and 0 otherwise, at each angle. The mass check gives $\int_{-1}^1 2\sqrt{1 - s^2}\,ds = \pi$, the area of the disk.

**An ellipse.** Let $f = \rho$ on the ellipse $x_1^2/A^2 + x_2^2/B^2 \le 1$ and 0 outside. Put $a(\theta)^2 = A^2\cos^2\theta + B^2\sin^2\theta$. Then
$$\mathcal{R}f(\theta, s) = \frac{2\rho A B}{a(\theta)^2}\sqrt{a(\theta)^2 - s^2} \quad \text{for } |s| \le a(\theta),$$
and 0 otherwise (Kak and Slaney, equation 5). For $A = 0.69$, $B = 0.92$, $\rho = 2$, $\theta = 0.3$ and $s = 0.2$: $a(\theta)^2 = 0.50844$ and $\mathcal{R}f = 3.41810$. The shift and rotation rules then give the projection of any ellipse, and a sum of ellipses gives the projection of the [Shepp-Logan phantom](/shepp-logan-phantom/) in closed form.

**The Gaussian.** For $f(x) = e^{-\pi|x|^2}$, the integral along each line is $\mathcal{R}f(\theta, s) = e^{-\pi s^2}\int e^{-\pi t^2}\,dt = e^{-\pi s^2}$. Its 1D Fourier transform is $e^{-\pi\sigma^2}$, which is the 2D transform of $f$ on the line through the origin, as the [Fourier slice theorem](/fourier-slice-theorem/) says.

**A point.** A unit point mass at $x_0$ is not a function, but the limit of narrow bumps gives the distribution $\delta(s - x_0\cdot\omega(\theta))$: the projection is a spike at $s = x_0\cdot\omega(\theta)$. As $\theta$ goes from 0 to $\pi$, the spike traces a sinusoid. This is the origin of the name [sinogram](/sinogram/) for the image of $\mathcal{R}f$.

**Non-example: the constant function.** $f = 1$ on all of $\mathbb{R}^2$ is not in $L^1$, and every line integral is infinite. The definition needs decay or compact support.

**Non-example: a discrete projector.** A pixel-driven or ray-driven matrix, such as the [Siddon algorithm](/siddon-algorithm/) or the [Joseph projector](/joseph-projector/), is a discretization of $\mathcal{R}$ for a pixel image, not the transform itself. Its rows differ from the exact line integrals by a discretization error, and its adjoint is a discrete back projection.

**Non-example: Radon's theorem on convex sets.** Radon's theorem in convex geometry (any $d + 2$ points in $\mathbb{R}^d$ split into two sets whose convex hulls meet) carries the same name but has no relation to this transform.

## Related definitions

- [X-ray transform](/x-ray-transform/): integrals over lines in $\mathbb{R}^n$. It equals the Radon transform for $n = 2$.
- [Sinogram](/sinogram/): the data $\mathcal{R}f$ shown as an image over $(\theta, s)$.
- [Back-projection operator](/back-projection-operator/): the adjoint $\mathcal{R}^\#$, which sums over all lines through a point.
- [Fourier slice theorem](/fourier-slice-theorem/): the 1D transform of a projection is a line of the 2D transform of $f$.
- [Radon inversion formula](/radon-inversion-formula/): $f$ from $\mathcal{R}f$, by a filter in $s$ and back projection.
- [Attenuated Radon transform](/attenuated-radon-transform/): the line integrals with an exponential weight, the model of SPECT.
- [Hough transform](/hough-transform/): a discrete relative that votes for lines through the edge points of an image.
- [Tomographic reconstruction problem](/tomographic-reconstruction-problem/): the inverse problem of finding $f$ from samples of $\mathcal{R}f$.

## References
