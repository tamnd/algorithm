---
tag: K96B4X
kind: theorem
slug: tuy-condition
name: Tuy condition
aliases:
- Tuy-Smith data sufficiency condition
area: imaging-and-inverse-problems/tomographic-reconstruction
level: advanced
summary: "Exact cone-beam reconstruction is possible when every plane through the object meets the source trajectory, which a single circle fails."
model: real-ram
prereqs: [x-ray-transform, grangeat-formula, radon-inversion-formula]
see_also: [feldkamp-davis-kress, katsevich-algorithm, limited-angle-tomography, interior-tomography, radon-transform, fan-beam-filtered-back-projection, back-projection-operator, tomographic-reconstruction-problem]
sources:
  - paper: doi:10.1137/0143035
    title: H. K. Tuy, An inversion formula for cone-beam reconstruction, SIAM Journal on Applied Mathematics 43(3), 1983
    locator: pp. 546 to 552 (the hypotheses on the curve, the inversion formula, and the proof with tempered distributions in the appendix)
  - paper: doi:10.1109/TMI.1985.4307689
    title: B. D. Smith, Image reconstruction from cone-beam projections, necessary and sufficient conditions and reconstruction methods, IEEE Transactions on Medical Imaging 4(1), 1985
    locator: pp. 14 to 25
  - paper: doi:10.1137/0145039
    title: D. V. Finch, Cone beam reconstruction with sources on a curve, SIAM Journal on Applied Mathematics 45(4), 1985
    locator: pp. 665 to 673 (inversion for many curves that do not satisfy Tuy's conditions, for example planar circles of sufficiently large radius)
  - paper: doi:10.1007/BFb0084509
    title: "P. Grangeat, Mathematical framework of cone beam 3D reconstruction via the first derivative of the Radon transform, in Mathematical Methods in Tomography, Lecture Notes in Mathematics, Springer, 1991"
    locator: pp. 66 to 97
---

The Tuy condition is the test that a source trajectory must pass for exact cone-beam reconstruction: every plane that meets the object must also meet the trajectory. The reason is the 3D [Radon inversion formula](/radon-inversion-formula/), which needs the integrals of the object over all planes, and the [Grangeat formula](/grangeat-formula/), which gets the derivative of the integral over a plane from one source point only if the plane passes through that source point. A single circle fails the test, because the planes that are almost parallel to the plane of the circle miss it. That is why the [Feldkamp-Davis-Kress](/feldkamp-davis-kress/) algorithm on a circular orbit is only approximate away from the mid-plane. A helix passes the test, and the [Katsevich algorithm](/katsevich-algorithm/) reconstructs exactly from helical data. Tuy stated the condition, with a transversality part, in 1983, and gave an inversion formula under it.

## Statement

Conventions: $\Omega \subset \mathbb{R}^3$ is a bounded open set that contains the object. The sources are on a curve $\Phi : \Lambda \to \mathbb{R}^3$, $\Lambda$ an interval. For a source point $a$ and $\beta \ne 0$ the cone-beam data are $D_f(a, \beta) = \int_0^\infty f(a + t\beta)\,dt$, as on the [Grangeat formula](/grangeat-formula/) page. For a unit $\beta$ this is the integral of $f$ along the ray from $a$ in the direction $\beta$. The plane with the unit normal $\alpha$ at the signed distance $\rho$ from the origin is $\{x : x\cdot\alpha = \rho\}$.

**Definition (Tuy's conditions).** The curve $\Phi$ satisfies Tuy's conditions for $\Omega$ when:

1. the curve is outside $\overline{\Omega}$;
2. the curve is bounded and continuous, and differentiable almost everywhere;
3. for every $x \in \Omega$ and every $\beta \in S^2$ there is a $\lambda \in \Lambda$ with $\Phi(\lambda)\cdot\beta = x\cdot\beta$ and $\Phi'(\lambda)\cdot\beta \ne 0$.

Condition 3 says that every plane that meets $\Omega$ meets the curve, and that it crosses the curve at a point where the curve is not tangent to the plane.

**Theorem 1 (Tuy 1983, cited).** Under Tuy's conditions, a function $f$ with support in $\Omega$ is determined by the cone-beam data $D_f(\Phi(\lambda), \cdot)$, $\lambda \in \Lambda$, and Tuy gives the formula
$$f(x) = \int_0^{2\pi}\!\!\int_{-\pi/2}^{\pi/2} \cos\varphi\,\frac{1}{2\pi i\,\Phi'(\lambda)\cdot\beta}\,\frac{\partial G}{\partial\lambda}(\beta, \lambda)\,d\varphi\,d\theta,$$
where $\beta = \beta(\theta, \varphi)$ is the unit vector with the spherical coordinates $(\theta, \varphi)$, $\lambda = \lambda(x, \beta)$ is a solution of condition 3, and $G(\cdot, \lambda)$ is the Fourier transform, in Tuy's convention, of the function $\alpha \mapsto D_f(\Phi(\lambda), \alpha)$, which is homogeneous of degree $-1$. Section 2 of the paper derives the formula formally, and the appendix proves it with tempered distributions.

**Theorem 2 (the plane condition is sufficient).** Let $\Gamma \subset \mathbb{R}^3$ be any set of source points, and let $f$ be smooth with a compact support in $\Omega$. Suppose that every plane that meets $\Omega$ contains a point of $\Gamma$. For $\alpha \in S^2$ and a plane $x\cdot\alpha = \rho$ that meets $\Omega$, choose $a \in \Gamma$ with $a\cdot\alpha = \rho$, and put
$$\Psi(\alpha, \rho) = \int_{C_\alpha} (\alpha\cdot\nabla_\beta)\,D_f(a, \beta)\Big|_{\beta = \theta}\,d\theta, \qquad C_\alpha = \{\theta \in S^2 : \theta\cdot\alpha = 0\}.$$
Then $\Psi$ does not depend on the choice of $a$, and for every $x \in \Omega$
$$f(x) = -\frac{1}{8\pi^2}\int_{S^2} \frac{\partial\Psi}{\partial\rho}(\alpha, x\cdot\alpha)\,d\alpha.$$
In particular the data $D_f(a, \theta)$ for $a \in \Gamma$ and $\theta \in S^2$ determine $f$. Theorem 2 needs no curve, no transversality and no condition on the position of the sources.

**Theorem 3 (a circle fails).** Let the sources be on the circle $\Phi(\lambda) = (R\cos\lambda, R\sin\lambda, 0)$. The plane $x\cdot\alpha = \rho$ misses the circle if and only if $|\rho| > R\sqrt{\alpha_1^2 + \alpha_2^2}$. So for every $\Omega$ that contains a point off the plane $x_3 = 0$, some planes that meet $\Omega$ miss the circle. For the point $x = (0, 0, z)$ the set of normals $\alpha$ of the planes through $x$ that miss the circle is the pair of polar caps $|\alpha_3| > R/\sqrt{R^2 + z^2}$, a fraction $1 - R/\sqrt{R^2 + z^2}$ of the sphere. For a point in the plane $x_3 = 0$ with $|x| < R$ no plane through it misses the circle.

**Theorem 4 (a helix passes).** Let the sources be on the infinite helix $\Phi(\lambda) = (R\cos\lambda, R\sin\lambda, H\lambda)$, $H > 0$. Every plane that meets the open cylinder $x_1^2 + x_2^2 < R^2$ meets the helix. So Theorem 2 applies to every bounded $\Omega$ inside this cylinder.

**Example.** For a circle with $R = 3$ the fractions of missed normals in Theorem 3 at $x = (0, 0, z)$ are $0.00345$ at $z = 0.25$, $0.01361$ at $z = 0.5$ and $0.05132$ at $z = 1$. A Monte Carlo count with 200000 uniform random normals and the seed 1 gave $0.00344$, $0.01370$ and $0.05181$.

## In plain words

A cone-beam scanner sends rays out from a source that moves along a path around the object. Exact reconstruction in space needs the total of the object over every flat sheet that cuts it. A single source position gives this information only for the sheets that pass through that source position. So the path must touch every sheet that cuts the object. A path that goes once around the object in one flat ring misses the sheets that lie almost flat above and below the ring, and the parts of the object far from the ring are then not exactly known. A path that winds up like a spring touches every sheet, so it allows exact reconstruction. Tuy also asked that the path cross each sheet instead of only touching it, because his formula divides by the speed at which the path crosses.

## Proof

**Theorem 1** is cited. The proof in the paper uses the Fourier transform of the homogeneous function $D_f(\Phi(\lambda), \cdot)$ and condition 3 to change the variable from $\lambda$ to the distance of the plane, which is where the factor $1/(\Phi'(\lambda)\cdot\beta)$ comes from.

**Theorem 2.** The data on the sphere give $D_f(a, \beta)$ for all $\beta \ne 0$ by the homogeneity, $D_f(a, \beta) = D_f(a, \beta/|\beta|)/|\beta|$, so $\Psi$ is computable from the data. By Theorem 1 of the [Grangeat formula](/grangeat-formula/) page, which holds for every source point, $\Psi(\alpha, \rho) = \partial_\rho\mathcal{R}f(\alpha, \rho)$ whenever $a\cdot\alpha = \rho$. The right side does not depend on $a$, so $\Psi$ does not depend on the choice of $a$. Fix $x \in \Omega$ and $\alpha$. Since $\Omega$ is open, the point $x + (\rho - x\cdot\alpha)\alpha$ is in $\Omega$ for all $\rho$ in an open interval $I$ around $x\cdot\alpha$, so the plane $y\cdot\alpha = \rho$ meets $\Omega$ for $\rho \in I$. By the hypothesis it contains a point of $\Gamma$, so $\Psi(\alpha, \rho) = \partial_\rho\mathcal{R}f(\alpha, \rho)$ on all of $I$, and $\partial_\rho\Psi(\alpha, x\cdot\alpha) = \partial_\rho^2\mathcal{R}f(\alpha, x\cdot\alpha)$. Theorem 3 of the [Radon inversion formula](/radon-inversion-formula/) page, $f(x) = -\frac{1}{8\pi^2}\int_{S^2}\partial_\rho^2\mathcal{R}f(\alpha, x\cdot\alpha)\,d\alpha$, gives the formula. For uniqueness, if $f_1$ and $f_2$ have the same data, then $f_1 - f_2$ has zero data, so $\Psi = 0$ and $f_1 - f_2 = 0$ on $\Omega$, and both are zero outside $\Omega$. $\square$

**Theorem 3.** On the circle, $\Phi(\lambda)\cdot\alpha = R(\alpha_1\cos\lambda + \alpha_2\sin\lambda)$, which takes exactly the values in $[-R r_\alpha, R r_\alpha]$ with $r_\alpha = \sqrt{\alpha_1^2 + \alpha_2^2}$. So the plane misses the circle if and only if $|\rho| > R r_\alpha$. Let $p \in \Omega$ with $p_3 \ne 0$. The plane $x_3 = p_3$ has $\alpha = e_3$, $r_\alpha = 0$ and $\rho = p_3 \ne 0$, so it meets $\Omega$ at $p$ and misses the circle. For $x = (0, 0, z)$ and the plane through $x$ with the normal $\alpha$, $\rho = z\alpha_3$, and the plane misses the circle if and only if $|z\alpha_3| > R\sqrt{1 - \alpha_3^2}$, which is $|\alpha_3| > R/\sqrt{R^2 + z^2}$. By Archimedes' theorem on the sphere, the area of the two caps $|\alpha_3| > c$ is the fraction $1 - c$ of the whole sphere. For $x$ with $x_3 = 0$ and $|x| < R$, a plane through $x$ either is the plane $x_3 = 0$, which contains the circle, or meets the plane $x_3 = 0$ in a line through $x$, which meets the circle because $x$ is inside it. $\square$

**Theorem 4.** Let the plane be $x\cdot\alpha = \rho$ and put $h(\lambda) = \Phi(\lambda)\cdot\alpha - \rho = R(\alpha_1\cos\lambda + \alpha_2\sin\lambda) + H\alpha_3\lambda - \rho$. If $\alpha_3 \ne 0$, the term $H\alpha_3\lambda$ grows without bound and the other terms are bounded, so $h$ takes both signs, and $h$ has a zero by the intermediate value theorem. If $\alpha_3 = 0$, the plane is vertical, and it meets the open cylinder only if $|\rho| < R\sqrt{\alpha_1^2 + \alpha_2^2} = R$. Then $R\cos(\lambda - \lambda_\alpha) = \rho$ has a solution, where $\lambda_\alpha$ is the angle of $(\alpha_1, \alpha_2)$. $\square$

## Consequences

- **Circular orbits are not exact (theorem).** By Theorem 3, every circular orbit misses planes through every point off its plane, so the 3D Radon data on these planes are not in the cone-beam data, and the route of Theorem 2 fails there. The [Feldkamp-Davis-Kress](/feldkamp-davis-kress/) algorithm is exact in the mid-plane, which agrees with the last part of Theorem 3, and for objects that do not change along the axis.
- **Errors grow with the cone angle (heuristic plus measurement).** The fraction of missed normals in Theorem 3 grows from 0 in the mid-plane as $z^2/(2R^2)$ for small $z$. On the [Feldkamp-Davis-Kress](/feldkamp-davis-kress/) page the error for a thin blob also grows with the height above the mid-plane. The two facts agree, but the fraction does not predict the size of the error.
- **Helical and other complete orbits (theorem).** By Theorem 4 a long enough helix gives exact reconstruction for an object inside its cylinder, and the [Katsevich algorithm](/katsevich-algorithm/) does it with a filtered back projection. A circle plus a line along the axis, or two circles in planes that are not parallel, are other orbits that meet more planes, and each one must be checked with the plane test.
- **Exactness is not stability (heuristic).** Theorem 2 needs the second derivative of the plane integrals, the same order as the 3D Radon inversion, so its noise growth is that of the inversion formula. When planes are missed, the edges of $f$ whose normals are in the missed set are not visible in the data, which is the same effect as in [limited-angle tomography](/limited-angle-tomography/).

## Tightness

- **The condition is not necessary for uniqueness (theorem, cited).** Finch 1985 gives an inversion procedure that applies to many curves that do not satisfy Tuy's conditions, for example planar circles of sufficiently large radius, and gives Sobolev estimates for the inversion in some cases. So a failure of the plane test does not always mean that the data do not determine $f$. It means that the route of Theorem 2 through the Radon transform is not available.
- **Transversality is a condition of the formula (theorem).** Tuy's formula divides by $\Phi'(\lambda)\cdot\beta$, so condition 3 asks for a crossing that is not tangent. Theorem 2 does not divide by it and does not need it. The infinite helix shows that the difference is real: for $\alpha = (0, H, -R)/\sqrt{H^2 + R^2}$, the plane through the origin with the normal $\alpha$ meets the helix only at $\Phi(0)$, where $h(\lambda) = c\,(\sin\lambda - \lambda)$ with $c \ne 0$, so $h'(0) = 0$. At that point the helix is tangent to the plane.
- **Bounded curves and a finite helix (theorem and heuristic).** Condition 2 asks for a bounded curve, so in practice the helix is finite. A finite helix misses the planes that are close to horizontal and pass above its top end or below its bottom end (theorem, by the formula for $h$). So it fails the plane test for a long object that sticks out of both ends, which is the long object problem of helical CT. For an object that stays well inside the ends, enough turns pass the test (heuristic: the proof of Theorem 4 then finds the zero of $h$ within a bounded range of $\lambda$).
- **The sources outside the object (theorem).** Condition 1 keeps the sources outside $\overline{\Omega}$, which is the case in X-ray CT. Theorem 2 does not use it, because the Grangeat relation holds for every source point.

## History

Tuy published the conditions and the inversion formula in 1983. His paper notes that earlier work of Gel'fand and Kirillov on the same inversion needed an unbounded curve, and he replaced this by a bounded curve with the plane condition. Smith in 1985 discussed necessary and sufficient conditions on the source positions together with reconstruction methods, and the plane condition is often called the Tuy-Smith condition. In the same year Finch gave inversion results for curves that fail the condition. Grangeat's 1991 relation between cone-beam data and the derivative of the 3D Radon transform made the role of the planes direct, and it is the route of the proof of Theorem 2.

## References
