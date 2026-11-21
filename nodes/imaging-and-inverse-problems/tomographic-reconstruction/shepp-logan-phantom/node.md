---
tag: YSNZHZ
kind: definition
slug: shepp-logan-phantom
name: Shepp-Logan phantom
aliases:
- head phantom
area: imaging-and-inverse-problems/tomographic-reconstruction
level: intro
summary: A standard test image of ten ellipses that models a head section, whose Radon transform is known in closed form.
model: real-ram
prereqs: [radon-transform]
see_also: [radon-transform, sinogram, filtered-back-projection, direct-fourier-reconstruction, ramp-filter, sparse-view-ct-reconstruction, sart, psnr]
sources:
  - paper: doi:10.1109/TNS.1974.6499235
    title: L. A. Shepp and B. F. Logan, The Fourier reconstruction of a head section, IEEE Transactions on Nuclear Science 21(3), 1974
    locator: pp. 21 to 43 (the head phantom of ten ellipses and its use to compare reconstruction methods)
  - book: isbn:9780898714944
    title: A. C. Kak and M. Slaney, Principles of Computerized Tomographic Imaging, SIAM Classics in Applied Mathematics 33, 2001
    locator: Chapter 3, Section 3.1, Fig. 3.4 (the phantom and its values), equations 5 and 6 (the projection of an ellipse and of a shifted and rotated ellipse) and Table 3.1 (the ten ellipses), pp. 53 to 56
  - paper: "P. A. Toft, The Radon Transform: Theory and Implementation, PhD thesis, Department of Mathematical Modelling, Technical University of Denmark, 1996"
    locator: the modified phantom with higher contrast (general locator)
---

The Shepp-Logan phantom is a test image for [tomographic reconstruction](/tomographic-reconstruction-problem/). It is a sum of ten ellipses, each with a constant density, and it models a cross section of a human head: a skull, the brain, two ventricles and some small tumors. Shepp and Logan introduced it in 1974 to compare reconstruction methods. Each ellipse has a [Radon transform](/radon-transform/) in closed form, so the exact [sinogram](/sinogram/) of the phantom is known at every angle and every detector position. This lets a test compare a reconstruction with the true image, with no error from the simulation of the data.

## Definition

An ellipse with density $\rho$, center $c = (x_0, y_0)$, semi-axes $A$ and $B$, and rotation angle $\alpha$ is the function that equals $\rho$ at the points $x$ with
$$\frac{\big((x - c)\cdot(\cos\alpha, \sin\alpha)\big)^2}{A^2} + \frac{\big((x - c)\cdot(-\sin\alpha, \cos\alpha)\big)^2}{B^2} \le 1$$
and 0 at all other points. So $A$ is the semi-axis along the direction at the angle $\alpha$ from the $x$ axis, counterclockwise, and $B$ is the other one. The **Shepp-Logan phantom** is the sum of the ten ellipses of the table below, on the square $[-1, 1]^2$. These are the values of Kak and Slaney, Table 3.1. The table gives the semi-axes, and the angle in degrees.

| ellipse | center $(x_0, y_0)$ | $A$ | $B$ | $\alpha$ | $\rho$ | modified $\rho$ |
|---|---|---|---|---|---|---|
| a, outer edge of the skull | (0, 0) | 0.92 | 0.69 | 90 | 2.0 | 1.0 |
| b, brain | (0, -0.0184) | 0.874 | 0.6624 | 90 | -0.98 | -0.8 |
| c, ventricle | (0.22, 0) | 0.31 | 0.11 | 72 | -0.02 | -0.2 |
| d, ventricle | (-0.22, 0) | 0.41 | 0.16 | 108 | -0.02 | -0.2 |
| e | (0, 0.35) | 0.25 | 0.21 | 90 | 0.01 | 0.1 |
| f | (0, 0.1) | 0.046 | 0.046 | 0 | 0.01 | 0.1 |
| g | (0, -0.1) | 0.046 | 0.046 | 0 | 0.01 | 0.1 |
| h | (-0.08, -0.605) | 0.046 | 0.023 | 0 | 0.01 | 0.1 |
| i | (0, -0.605) | 0.023 | 0.023 | 0 | 0.01 | 0.1 |
| j | (0.06, -0.605) | 0.046 | 0.023 | 90 | 0.01 | 0.1 |

Kak and Slaney name the density column a refractive index, because their chapter treats any kind of ray. In CT the densities stand for X-ray attenuation in arbitrary units. The values add where ellipses overlap, so the phantom takes only a few values:

- 2.0 on the skull, the ring between ellipses a and b.
- 1.02 in the brain, and 1.02 at the center $(0, 0)$, where only a and b hold the point: $2 - 0.98 = 1.02$.
- 1.0 in the ventricles c and d.
- 1.03 in the small ellipses e to j, and 1.04 where f lies in e.
- 1.01 where e or g overlaps the ventricle d.
- 0 outside the skull.

These are the labels of Kak and Slaney, Fig. 3.4. The head is 1.38 wide in $x$ and 1.84 high in $y$.

**Pixels.** An $n \times n$ image of the phantom covers the square $[-1, 1]^2$. Pixel $(i, j)$ has row $i$ from the top and column $j$ from the left, and its center is at $x_j = -1 + (2j+1)/n$ and $y_i = 1 - (2i+1)/n$. So $y$ goes up, as in the figure of Shepp and Logan, and the tumors h, i and j are at the bottom of the image. The value of the image at a pixel is the phantom at the pixel center.

**The modified phantom.** Toft (1996) kept the ten ellipses and changed the densities to those of the last column. The value at the center is $1 - 0.8 = 0.2$, the ventricles are 0, and the small ellipses are 0.3 or 0.4. The structure is the same, but the contrast inside the brain is ten times higher in absolute terms.

**The projections in closed form.** Use the Radon convention $\mathcal{R}f(\theta, s) = \int f(s\,\omega + t\,\omega^\perp)\,dt$ with $\omega = (\cos\theta, \sin\theta)$. A centered ellipse with $\alpha = 0$ has the projection
$$p_0(\theta, s) = \frac{2\rho A B}{a(\theta)^2}\sqrt{a(\theta)^2 - s^2} \quad \text{for } |s| \le a(\theta), \qquad a(\theta)^2 = A^2\cos^2\theta + B^2\sin^2\theta,$$
and 0 for $|s| > a(\theta)$ (Kak and Slaney, equation 5). Here $a(\theta)$ is the half-width of the shadow of the ellipse. A shift by $c$ and a rotation by $\alpha$ give
$$p(\theta, s) = p_0(\theta - \alpha,\; s - c\cdot\omega(\theta)),$$
which is Kak and Slaney, equation 6, with $c\cdot\omega(\theta) = |c|\cos(\gamma - \theta)$ for the polar angle $\gamma$ of $c$. The projection of the phantom is the sum of the ten terms. It costs $O(1)$ per ray, with no quadrature.

## Examples and non-examples

**The values on two lines.** At $\theta = 0$ the line $s = 0$ is the vertical axis $x = 0$. It passes through a, b, e, f, g and i, and the sum of the ten terms is $\mathcal{R}f(0, 0) = 1.97426$. A numerical integral of the phantom along the axis gives the same value. At $\theta = \pi/2$ the line $s = 0$ is the horizontal axis, which crosses the skull where it is thinner and passes through both ventricles, and $\mathcal{R}f(\pi/2, 0) = 1.45071$.

**The mass.** The integral of an ellipse is $\rho\pi A B$. The sum over the table is $\int f\,dx = 2.20176$. Each row of the exact sinogram has this integral, which gives a quick check of a projector. The modified phantom has the mass 0.49526.

**The test in practice.** The [filtered back-projection](/filtered-back-projection/) and [direct Fourier reconstruction](/direct-fourier-reconstruction/) pages build the sinogram from the formulas above, with 32 angles and 47 detector bins, and reconstruct a $32 \times 32$ image. Filtered back-projection with the Ram-Lak kernel gives 1.0217 at the pixel $(16, 16)$, whose center is $(1/32, -1/32)$, where the true value is 1.02. Direct Fourier reconstruction with bilinear interpolation gives 1.048 there.

**Low contrast.** The brain, the ventricles and the tumors differ by 0.01 to 0.02, against the skull at 2.0. An image shown on the full range $[0, 2]$ shows only the skull. To see the inside, show the window $[1.0, 1.05]$ or a similar one, or use the modified phantom. The low contrast makes the phantom a hard test: a method must show differences of 1 percent next to a strong edge. Errors near the skull, such as the ringing that the [ramp filter](/ramp-filter/) causes at a sharp edge, can be larger than these differences and hide the tumors.

**Non-example: a pixel image as the ground truth.** A sampled image of the phantom is not the phantom. If the test computes the data from the pixel image with the same discrete projector that the reconstruction uses, the test checks the solver against its own model and hides the error of the discretization. This is sometimes called the inverse crime. Compute the data from the closed form, or from a much finer grid, and compare the result with the phantom at the pixel centers.

**Non-example: the modified phantom as the same test.** The modified phantom has the same edges but other densities. Results on the two phantoms are not comparable, and an error that is 1 percent of the brain value in one is a different fraction in the other. State which one a table uses.

## Related definitions

- [Radon transform](/radon-transform/): the transform whose closed form for an ellipse gives the exact data.
- [Sinogram](/sinogram/): the image of the projections. The head fills a band whose half-width goes between 0.69 at $\theta = 0$ and 0.92 at $\theta = \pi/2$.
- [Filtered back-projection](/filtered-back-projection/): the method Shepp and Logan tested on the phantom, with the kernel that now has their name.
- [Ramp filter](/ramp-filter/): the Shepp-Logan kernel, from the same paper, is one discrete form of it.
- [PSNR](/psnr/): a common figure for the error of a reconstruction against the phantom.

## References
