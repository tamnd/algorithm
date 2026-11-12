---
tag: 5W3KF8
kind: definition
slug: sweep-surface
name: Sweep surface
aliases:
- generalized cylinder
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: The surface swept by a profile curve carried along a spine curve by a moving frame. The frame sets the twist, and a rotation minimizing frame avoids the spin of the Frenet frame.
prereqs: [parametric-surface, frenet-frame]
see_also: [frenet-frame, surface-of-revolution, ruled-surface, offset-curve, arc-length-parametrization, parametric-curve, nurbs, surface-tessellation]
sources:
  - paper: doi:10.1145/1330511.1330513
    title: Wenping Wang, Bert Juttler, Dayue Zheng and Yang Liu, Computation of Rotation Minimizing Frames, ACM Transactions on Graphics 27(1), Article 2 (2008)
    locator: the double reflection method and its fourth order global error
  - paper: doi:10.1080/00029890.1975.11993807
    title: Richard L. Bishop, There is More than One Way to Frame a Curve, The American Mathematical Monthly 82(3), 246-251 (1975)
    locator: relatively parallel adapted frames, which are the rotation minimizing frames, and their relation to the Frenet frame
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: Section 10.3, Skinned Surfaces, and Section 10.4, Swept Surfaces (the trajectory, the section curve and the choice of orientation)
---

A sweep surface is the surface that a profile curve traces when it moves along a second curve, the spine. At each point of the spine a frame of three vectors places the profile in space, so the surface depends on the spine, the profile and the frame. Pipes, tubes, cables, hair strands, rails and extruded cross sections are all sweeps, and in computer vision the same shape is called a generalized cylinder. The hard part is the frame: the [Frenet frame](/frenet-frame/) of the spine spins with the torsion and fails on straight pieces, and a rotation minimizing frame has neither problem.

## Definition

Let $c : [u_0, u_1] \to \mathbb{R}^3$ be a regular spine curve with unit tangent $t(u)$, and let $p(v) = (x(v), y(v))$ be a plane profile curve. A moving frame along $c$ is a pair of unit vectors $r(u), s(u)$ such that $(t, r, s)$ is orthonormal and right handed at each $u$. The sweep surface is

$$S(u, v) = c(u) + x(v)\, r(u) + y(v)\, s(u).$$

The profile lies in the normal plane of the spine at each $u$. Common variants multiply the profile by a scale $\sigma(u)$ or turn it by a twist angle $\alpha(u)$ in the normal plane, or both, which gives $S = c + M(u)\, p(v)$ with $M(u)$ a $3 \times 2$ matrix built from the frame. A constant frame gives a translational surface $c(u) + p(v)$, and with a straight spine this is the general cylinder.

**Frames.** Any two frames along the same spine differ by a rotation about $t$ by an angle $\theta(u)$, so the choice of frame is a choice of twist.

- The [Frenet frame](/frenet-frame/) $(T, N, B)$ uses the principal normal $N$ and the binormal $B$. It needs $c' \times c'' \ne 0$, so it is not defined on straight pieces and it flips at inflections. In arc length, $N' = -\kappa T + \tau B$, so the frame turns about $T$ at the rate of the torsion $\tau$.
- A rotation minimizing frame (RMF) has $r'$ parallel to $t$ at each point, so the normal vectors do not turn about the tangent at all (Bishop 1975). It is defined for every regular spine, and it is unique once $r(u_0)$ is given. In arc length $s$ the RMF is the Frenet frame turned by $\theta(s) = \theta_0 - \int_0^s \tau\, d\sigma$, where the Frenet frame is defined.
- A frame from a fixed up vector, which takes $r$ as the part of a world vector normal to $t$, is cheap, but it fails where $t$ is parallel to that vector.

**Regularity of a tube.** For a circular profile of radius $\rho$, an arc-length spine and the angle $\varphi$ measured from the principal normal, $|S_s \times S_\varphi| = \rho\, (1 - \kappa \rho \cos \varphi)$. So the tube is regular while $\rho < 1/\kappa$ at every point, and where $\rho > 1/\kappa$ the inner side folds through itself. Thin profiles on gently bent spines are safe; a fat tube on a tight bend is not.

### Rotation minimizing frame by double reflection

The method of Wang, Juttler, Zheng and Liu (2008) takes sample points $x_i = c(u_i)$ and unit tangents $t_i$ and builds the frame at each sample by two reflections.

```pseudo id=main
RMF-DOUBLE-REFLECTION(x[0..n], t[0..n], r0)
L1  r ← unit(r0 − (r0 · t[0]) t[0]);  output (t[0], r, t[0] × r)
L2  for i ← 0 to n − 1
L3      v1 ← x[i+1] − x[i];  c1 ← v1 · v1
L4      rL ← r − (2 (v1 · r) / c1) v1;  tL ← t[i] − (2 (v1 · t[i]) / c1) v1
L5      v2 ← t[i+1] − tL;  c2 ← v2 · v2
L6      r ← rL − (2 (v2 · rL) / c2) v2          ▷ keep r ← rL when c2 = 0
L7      output (t[i+1], r, t[i+1] × r)
```

The first reflection, in the plane that bisects $x_i x_{i+1}$, maps the frame to the next point. The second, in the plane normal to $t_{i+1} - t^L$, turns the reflected tangent onto the true tangent $t_{i+1}$. Two reflections make a rotation, so each frame is orthonormal and right handed up to rounding. Each step costs a constant number of operations, so $n$ steps cost $O(n)$ in the real RAM model, and a grid of $n + 1$ stations and $m$ profile points costs $O(n + nm)$, which is $O(nm)$. The paper proves a global error of order four in the step size. For the helix below the observed errors drop by a factor near 16 at each halving of the step, which agrees with that order.

## Examples and non-examples

- **A helix: Frenet against RMF.** Take $c(t) = (2 \cos t, 2 \sin t, t)$. Its speed is $\sqrt 5$, its curvature $\kappa = 2/5$ and its torsion $\tau = 1/5$. The RMF that starts at the Frenet frame is the Frenet frame turned by $\theta = -\tau s = -t/\sqrt 5$. Over $t \in [0, 4\pi]$ the Frenet frame turns by $4\pi/\sqrt 5 \approx 5.62$ radians against the RMF, nearly a full turn, which shows on a striped tube as a visible twist. The double reflection method with $n$ equal steps on this interval has a maximum error in $r$ of about $8.0 \times 10^{-5}$ for $n = 25$, $5.0 \times 10^{-6}$ for $n = 50$, $3.1 \times 10^{-7}$ for $n = 100$, $1.9 \times 10^{-8}$ for $n = 200$ and $1.2 \times 10^{-9}$ for $n = 400$.
- **A plane spine.** For a spine in a plane, $\tau = 0$, so the RMF is the Frenet frame up to a constant turn wherever the Frenet frame is defined. The double reflection method reproduces this for an ellipse, and it keeps working through the inflections of an S-shaped plane curve, where the Frenet normal flips.
- **A straight spine.** The Frenet frame is not defined. The RMF is a constant frame, and the sweep of a circle is a circular cylinder.
- **A surface of revolution.** Sweep a profile around a circle in the $xy$ plane. The circle is plane, so its RMF is its Frenet frame, with $r$ along the radius and $s$ along the $z$ axis, and the sweep is the [surface of revolution](/surface-of-revolution/) of the profile shifted by the circle radius.
- **A tube that folds.** A circle of radius $2$ swept around the unit circle has $\kappa \rho = 2 > 1$. The inner half of each profile circle passes through the axis, and every profile circle contains the two points $(0, 0, \pm\sqrt 3)$, since the distance from $(\cos \theta, \sin \theta, 0)$ to $(0, 0, \sqrt 3)$ is $2$. The surface is a spindle torus that crosses itself there.
- **Non-example: a closed spine with an open frame.** On a closed space curve the RMF after one loop is in general the start frame turned by some angle $\alpha$, so the tube has a seam. A common fix adds the twist $-\alpha u / (u_1 - u_0)$ to spread the correction along the spine. The result is no longer rotation minimizing, but it closes.
- **Non-example: skinning.** Skinning fits a surface through several given cross-section curves, one at each of several stations (Piegl and Tiller, Section 10.3). There is no single profile and no moving frame, so it is a different construction, even though the results can look alike.
- **Non-example: an offset surface.** A tube of radius $\rho$ is the set of points at distance $\rho$ from the spine, a kind of offset. The offset of a surface by a distance, as in the [offset curve](/offset-curve/) case, moves each point along its normal and is a different construction.

## Related definitions

- [Frenet frame](/frenet-frame/): the frame that the curvature and torsion of the spine define, and the reference for the RMF angle.
- [Arc-length parametrization](/arc-length-parametrization/): the parameter in which the frame equations take their simplest form.
- [Surface of revolution](/surface-of-revolution/) and [ruled surface](/ruled-surface/): sweeps with a circular spine, and surfaces swept by a straight line.
- [NURBS](/nurbs/): the form CAD systems use for sweeps. A sweep with an RMF is in general not exactly a NURBS surface, so systems fit one to sampled sections.
- [Surface tessellation](/surface-tessellation/): a sweep is usually drawn as the grid of stations times profile points.

## References
