---
tag: RRDHJZ
kind: theorem
slug: grangeat-formula
name: Grangeat's formula
aliases:
- Grangeat relation
area: imaging-and-inverse-problems/tomographic-reconstruction
level: advanced
summary: "The radial derivative of the 3D Radon transform is given by a weighted derivative of cone-beam line integrals, which links cone-beam data to plane integrals."
model: real-ram
prereqs: [radon-transform, x-ray-transform, radon-inversion-formula]
see_also: [tuy-condition, feldkamp-davis-kress, katsevich-algorithm, radon-inversion-formula, fan-to-parallel-rebinning, back-projection-operator, fourier-slice-theorem, x-ray-transform]
sources:
  - paper: doi:10.1007/BFb0084509
    title: "P. Grangeat, Mathematical framework of cone beam 3D reconstruction via the first derivative of the Radon transform, in Mathematical Methods in Tomography, Lecture Notes in Mathematics, Springer, 1991 (ISBN 9783540549703)"
    locator: pp. 66 to 97
  - paper: doi:10.1137/0143035
    title: H. K. Tuy, An inversion formula for cone-beam reconstruction, SIAM Journal on Applied Mathematics 43(3), 1983
    locator: pp. 546 to 552 (the inversion formula for sources on a curve that meets almost every plane through the object)
  - book: isbn:9780898714937
    title: F. Natterer, The Mathematics of Computerized Tomography, SIAM Classics in Applied Mathematics 32, 2001
    locator: Section II.2, inversion formulas (the inversion formula for plane integrals in three dimensions)
---

Grangeat's formula connects the two transforms of 3D tomography. A cone-beam scanner measures the integrals of $f$ along the rays from one source point $a$, which is the [X-ray transform](/x-ray-transform/) restricted to the rays through $a$. The 3D [Radon transform](/radon-transform/) integrates $f$ over planes. The rays from $a$ that lie in one plane through $a$ fill that plane, but their sum is a weighted plane integral with the weight $1/|x - a|$, not the plane integral itself. Grangeat's formula removes the weight with one derivative: a derivative of the cone-beam data across the plane gives the derivative of the plane integral in the direction normal to the plane. The [Radon inversion formula](/radon-inversion-formula/) in three dimensions needs only this derivative and one more, so every plane through a source point gives the data that the inversion needs on that plane. This is the reason for the [Tuy condition](/tuy-condition/).

## Statement

Conventions: for $f$ on $\mathbb{R}^3$, a source point $a$ and $\beta \in \mathbb{R}^3 \setminus \{0\}$, the cone-beam transform is
$$D_f(a, \beta) = \int_0^\infty f(a + t\beta)\,dt.$$
It is homogeneous of degree $-1$ in $\beta$: $D_f(a, c\beta) = c^{-1} D_f(a, \beta)$ for $c > 0$. For a unit $\beta$ it is the integral of $f$ along the ray from $a$ in the direction $\beta$. The Radon transform is $\mathcal{R}f(\alpha, \rho) = \int_{x\cdot\alpha = \rho} f\,dA$ for $\alpha \in S^2$. For a unit $\alpha$, $C_\alpha = \{\theta \in S^2 : \theta\cdot\alpha = 0\}$ is the great circle normal to $\alpha$, with the arc length $d\theta$.

**Theorem 1 (Grangeat's formula).** Let $f$ be a Schwartz function on $\mathbb{R}^3$, let $a \in \mathbb{R}^3$ and let $\alpha \in S^2$. Then
$$\frac{\partial}{\partial\rho}\mathcal{R}f(\alpha, \rho)\Big|_{\rho = a\cdot\alpha} = \int_{C_\alpha} (\alpha\cdot\nabla_\beta)\,D_f(a, \beta)\Big|_{\beta = \theta}\,d\theta.$$

The right side uses only the rays from $a$ that are in the plane $x\cdot\alpha = a\cdot\alpha$ and the rays close to it, because the derivative in $\beta$ along $\alpha$ tilts each ray out of the plane.

**Theorem 2 (flat detector form).** Let $e_u, e_v, e_w$ be an orthonormal frame, and let the flat detector be at the distance $D > 0$ from the source $a$, with its point $(u, v)$ at $a + u e_u + v e_v - D e_w$. Let $g(u, v)$ be the integral of $f$ along the ray from $a$ through the point $(u, v)$. Let $f$ be smooth with a compact support in the open half-space $\{x : (x - a)\cdot e_w < 0\}$ in front of the source. Fix a unit vector $n = n_u e_u + n_v e_v$ and $m = -n_v e_u + n_u e_v$, and for $s \in \mathbb{R}$ let $L_s$ be the detector line $\{s n + \ell m : \ell \in \mathbb{R}\}$. Put
$$\alpha_s = \frac{D n + s e_w}{\sqrt{D^2 + s^2}}, \qquad \cos\zeta = \frac{D}{\sqrt{D^2 + s^2}}, \qquad G(s) = \int_{-\infty}^{\infty} \frac{D}{\sqrt{D^2 + s^2 + \ell^2}}\,g(s n + \ell m)\,d\ell.$$
Then $\alpha_s$ is the unit normal of the plane through $a$ and $L_s$, and
$$\frac{\partial}{\partial\rho}\mathcal{R}f(\alpha_s, \rho)\Big|_{\rho = a\cdot\alpha_s} = \frac{1}{\cos^2\zeta}\,G'(s).$$

So the data on one detector give the radial derivative of the plane integrals on all planes through the source that meet the detector. The steps are a weight $D/\sqrt{D^2 + u^2 + v^2}$, a line integral along each detector line, and a derivative across the lines.

**Example.** Take $f(x) = e^{-\pi|x|^2}$. Every plane at the distance $\rho$ from the origin gives $\mathcal{R}f(\alpha, \rho) = e^{-\pi\rho^2}$, so the left side of Theorem 1 is $-2\pi\rho\,e^{-\pi\rho^2}$. For the right side, $\nabla f(x) = -2\pi x f(x)$, and on the plane $x\cdot\alpha = a\cdot\alpha = \rho$ the factor $\alpha\cdot x$ is the constant $\rho$. So
$$\int_{C_\alpha}\int_0^\infty t\,(\alpha\cdot\nabla f)(a + t\theta)\,dt\,d\theta = -2\pi\rho\int_{C_\alpha}\int_0^\infty f(a + t\theta)\,t\,dt\,d\theta = -2\pi\rho\,\mathcal{R}f(\alpha, \rho),$$
which is the left side. With $a = (0, -3, 0)$ and $\alpha = (0, -0.1, \sqrt{0.99})$, $\rho = 0.3$ and both sides are $-0.6\pi\,e^{-0.09\pi} = -1.42072$.

## In plain words

A cone-beam scanner sends rays out from one point. The rays that lie in one flat sheet through that point cover the whole sheet, so it seems that their sum gives the total of the object over the sheet. It does not, because the rays spread out like the spokes of a wheel: they are dense near the source and sparse far from it, so the sum counts near parts more than far parts. Grangeat found a correction. Tilt the sheet a little, take the change in the ray sums, and the uneven counting cancels. What remains is the change of the true sheet total when the sheet moves. The inversion formula in space needs exactly this change of the sheet totals, so the rays from the sources give everything that it needs.

## Proof

**Theorem 1.** For a fixed $\theta$, differentiate under the integral sign:
$$(\alpha\cdot\nabla_\beta)\,D_f(a, \beta)\Big|_{\beta = \theta} = \int_0^\infty t\,(\alpha\cdot\nabla f)(a + t\theta)\,dt.$$
This is allowed because $\nabla f$ is a Schwartz function, so $t\,|\nabla f(a + t\beta)|$ has an integrable bound that is uniform for $\beta$ near the unit sphere. Integrate over $\theta \in C_\alpha$. The map $(t, \theta) \mapsto x = a + t\theta$ is polar coordinates centered at $a$ in the plane $E = \{x : x\cdot\alpha = a\cdot\alpha\}$, with $dA = t\,dt\,d\theta$. So the right side of Theorem 1 is $\int_E (\alpha\cdot\nabla f)\,dA$. On the other side, $\mathcal{R}f(\alpha, \rho) = \int_{\alpha^\perp} f(\rho\alpha + y)\,dy$, and differentiation under the integral sign gives $\partial_\rho\mathcal{R}f(\alpha, \rho) = \int_{\alpha^\perp} (\alpha\cdot\nabla f)(\rho\alpha + y)\,dy$. At $\rho = a\cdot\alpha$ the plane $\rho\alpha + \alpha^\perp$ is $E$. $\square$

**Theorem 2.** Put $P(s, \ell) = s n + \ell m - D e_w$, so the detector point $(u, v) = s n + \ell m$ is at $a + P$, and $|P|^2 = D^2 + s^2 + \ell^2$. The ray integral is $g = |P|\,D_f(a, P)$ by the homogeneity, so the integrand of $G$ is $D\,D_f(a, P)$ and $G(s) = D\int D_f(a, P(s, \ell))\,d\ell$.

The normal. $\alpha_s\cdot P = (D s - s D)/\sqrt{D^2 + s^2} = 0$ and $\alpha_s\cdot m = 0$, so $\alpha_s$ is normal to the plane through $a$ and $L_s$, and $|\alpha_s| = 1$.

The support. If $\beta\cdot e_w \ge 0$, every point $a + t\beta$ with $t \ge 0$ has $(x - a)\cdot e_w \ge 0$ and is outside the support. Since the support is compact, $D_f(a, \cdot)$ and its gradient are zero on a neighbourhood of the closed half-space $\{\beta : \beta\cdot e_w \ge 0\}$ of directions. In particular $D_f(a, P(s, \ell)) = 0$ for all large $|\ell|$, because $P/|P|$ then comes close to $\pm m$.

The derivative. $\partial_s P = n$, so $G'(s) = D\int (n\cdot\nabla_\beta)D_f(a, P)\,d\ell$. Let $p_0 = s n - D e_w$ be the point of the line $\ell \mapsto P(s, \ell)$ closest to the origin, with $|p_0| = \sqrt{D^2 + s^2}$, and let $c = p_0/|p_0|$. A direct check gives
$$n = \frac{D\,\alpha_s + s\,c}{\sqrt{D^2 + s^2}}.$$

The term with $c$ is zero. $D_f(a, \cdot)$ is homogeneous of degree $-1$, so Euler's relation gives $P\cdot\nabla_\beta D_f(a, P) = -D_f(a, P)$. With $P = p_0 + \ell m$ and $m\cdot\nabla_\beta D_f(a, P) = \partial_\ell D_f(a, P)$,
$$\int p_0\cdot\nabla_\beta D_f(a, P)\,d\ell = -\int D_f(a, P)\,d\ell - \int \ell\,\partial_\ell D_f(a, P)\,d\ell = 0,$$
by integration by parts, with no boundary terms because $D_f(a, P) = 0$ for large $|\ell|$.

The term with $\alpha_s$. The points $\theta = P/|P|$ for $\ell \in \mathbb{R}$ run once over the open half of $C_{\alpha_s}$ with $\theta\cdot e_w < 0$. The angle element of a line at the distance $|p_0|$ from the origin is $d\theta = |p_0|\,d\ell/|P|^2$. The gradient $\nabla_\beta D_f(a, \cdot)$ is homogeneous of degree $-2$, so $(\alpha_s\cdot\nabla_\beta)D_f(a, \theta) = |P|^2\,(\alpha_s\cdot\nabla_\beta)D_f(a, P)$. On the other half of $C_{\alpha_s}$ the integrand is zero by the support step. So
$$\int_{C_{\alpha_s}} (\alpha_s\cdot\nabla_\beta)D_f(a, \theta)\,d\theta = |p_0|\int (\alpha_s\cdot\nabla_\beta)D_f(a, P)\,d\ell.$$

Together,
$$G'(s) = \frac{D^2}{\sqrt{D^2 + s^2}}\int (\alpha_s\cdot\nabla_\beta)D_f(a, P)\,d\ell = \frac{D^2}{D^2 + s^2}\int_{C_{\alpha_s}} (\alpha_s\cdot\nabla_\beta)D_f(a, \theta)\,d\theta = \cos^2\zeta\;\partial_\rho\mathcal{R}f(\alpha_s, a\cdot\alpha_s),$$
by Theorem 1. $\square$

**Measurement.** A Python check with the Gaussian of the example, $a = (0, -3, 0)$, $D = 3$, $e_w = (0, -1, 0)$, $e_u = (1, 0, 0)$, $e_v = (0, 0, 1)$ and $n$ at the angle $0.7$ from $e_u$. The ray integrals use the closed form with the error function. The Gaussian does not have a compact support, but the rays away from the detector carry less than $10^{-12}$. The right side of Theorem 1, with 4000 midpoint nodes on $C_\alpha$ and a central difference in $\beta$, gives $-1.420716$ for $\rho = 0.3$. Theorem 2 with the trapezoid rule on $|\ell| \le 12$ and a central difference in $s$ gives these values.

| $s$ | $\rho = a\cdot\alpha_s$ | $G'(s)/\cos^2\zeta$ | $-2\pi\rho\,e^{-\pi\rho^2}$ |
|---|---|---|---|
| 0.3 | 0.29851 | -1.4176282 | -1.4176282 |
| -0.5 | -0.49320 | 1.4431947 | 1.4431947 |
| 1.2 | 1.11417 | -0.1417175 | -0.1417175 |

## Consequences

- **Exact cone-beam inversion (theorem).** The 3D [Radon inversion formula](/radon-inversion-formula/) is $f(x) = -\frac{1}{8\pi^2}\int_{S^2}\partial_\rho^2\mathcal{R}f(\alpha, x\cdot\alpha)\,d\alpha$. It needs $\partial_\rho\mathcal{R}f(\alpha, \rho)$ as a function of $\rho$ near $x\cdot\alpha$, for every $\alpha$. Theorem 1 gives $\partial_\rho\mathcal{R}f(\alpha, \rho)$ from the source points $a$ with $a\cdot\alpha = \rho$. So if every plane that meets the support of $f$ contains a source point, the cone-beam data determine $f$, and the two formulas give $f$. This is the [Tuy condition](/tuy-condition/), and the [Tuy condition](/tuy-condition/) page proves it on this route.
- **Grangeat's algorithm (theorem plus a design choice).** Theorem 2 turns each detector image into the values of $\partial_\rho\mathcal{R}f$ on a family of planes through the source. A rebinning step moves these values to a regular grid in $(\alpha, \rho)$, and the 3D inversion formula finishes the job. This is the 3D analog of [fan-to-parallel rebinning](/fan-to-parallel-rebinning/).
- **Why the derivative (theorem).** Without the derivative the sum of the rays in a plane is $\int_{C_\alpha} D_f(a, \theta)\,d\theta = \int_E f(x)\,|x - a|^{-1}\,dA$, by the same polar coordinates. The weight $|x - a|^{-1}$ depends on the source, so different sources give different weighted integrals over the same plane, and these cannot be put together directly.
- **The circular orbit (theorem).** A circle in the plane $x_3 = 0$ misses every plane $x_3 = c$ with $c \ne 0$, so Theorem 1 gives no value of $\partial_\rho\mathcal{R}f$ on these planes and on the planes close to them. The [Feldkamp-Davis-Kress](/feldkamp-davis-kress/) algorithm uses a circular orbit and is exact only in special cases.
- **The helix (theorem).** A helix meets every plane that meets a cylinder inside it, so helical data satisfy the hypothesis of the first item. The [Katsevich algorithm](/katsevich-algorithm/) is an exact filtered back projection for this trajectory that does not need a rebinning to Radon space.

## Tightness

- **The factor $1/\cos^2\zeta$ (measurement).** Without it the detector form is wrong by the factor $\cos^2\zeta = D^2/(D^2 + s^2)$. For $D = 3$ and $s = 1.2$ this is $0.862$, an error of 14 percent in the table above.
- **The support in front of the source (theorem).** Theorem 2 needs $D_f(a, \cdot) = 0$ on the directions away from the detector, because the detector sees only half of each great circle and the integration by parts needs $D_f(a, P) = 0$ for large $|\ell|$. Theorem 1 has no such condition: it holds for every source point, also for a point inside the support.
- **The whole detector line (theorem).** $G(s)$ integrates along the whole line $L_s$. If the projection of the object is larger than the detector, as for a long object in a helical scan, the integral on some lines is incomplete, and Theorem 2 gives a wrong value on the planes through these lines.
- **Smoothness (theorem).** The proof differentiates under the integral sign, which needs $\nabla f$ with an integrable bound along the rays. For an $f$ with jumps both sides are distributions in $\rho$, and the identity holds in that sense.

## History

Tuy published an inversion formula for cone-beam data from sources on a curve in 1983. Grangeat derived the relation between the cone-beam data and the first radial derivative of the 3D Radon transform, and a reconstruction framework built on it. He published it in 1991 as a chapter of the volume Mathematical Methods in Tomography, in the Lecture Notes in Mathematics series. Unlike Tuy's formula, his relation turns cone-beam data into Radon data plane by plane, so the well-known 3D Radon inversion can do the rest.

## References
