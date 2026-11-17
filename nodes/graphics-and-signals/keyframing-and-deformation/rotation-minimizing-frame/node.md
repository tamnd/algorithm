---
tag: SJDRMY
kind: definition
slug: rotation-minimizing-frame
name: Rotation minimizing frame
aliases:
- Bishop frame
- parallel transport frame
area: graphics-and-signals/keyframing-and-deformation
level: core
summary: A moving frame along a space curve whose normal vectors do not rotate about the tangent, which avoids the twist of the Frenet frame.
prereqs: [frenet-frame]
see_also: [double-reflection-method, sweep-surface, discrete-elastic-rods, arc-length-parametrization, angular-velocity, runge-kutta-methods, unit-quaternion-rotation]
sources:
  - paper: doi:10.1080/00029890.1975.11993807
    title: "Richard L. Bishop, There is more than one way to frame a curve, The American Mathematical Monthly 82(3), 246-251, 1975"
    locator: the relatively parallel adapted frame, its equations, and its existence on every regular C2 curve
  - paper: doi:10.1016/0167-8396(86)90039-7
    title: "Fopke Klok, Two moving coordinate frames for sweeping along a 3D trajectory, Computer Aided Geometric Design 3(3), 217-229, 1986"
    locator: the rotation minimizing frame for sweeping, defined by a differential equation
  - paper: doi:10.1145/1330511.1330513
    title: "Wenping Wang, Bert Jüttler, Dayue Zheng and Yang Liu, Computation of rotation minimizing frames, ACM Transactions on Graphics 27(1), Article 2, 2008"
    locator: "Section 3.1 (the definition by a differential equation) and Section 4 (the double reflection method)"
---

A rotation minimizing frame is an orthonormal frame $(r, s, t)$ that moves along a space curve, with $t$ the unit tangent, such that the normal vectors $r$ and $s$ do not turn about the tangent.
Its angular velocity has no component along $t$, so the frame turns only as much as the tangent forces it to.
Bishop (1975) called it a relatively parallel frame and showed that it exists on every regular curve with a continuous second derivative, also where the [Frenet frame](/frenet-frame/) is not defined.
Klok (1986) gave the name rotation minimizing frame and used it to sweep cross sections along a path.
In graphics it frames [sweep surfaces](/sweep-surface/), tubes, ribbons and camera paths, and in simulation it is the reference frame of the twist of a rod, as in [discrete elastic rods](/discrete-elastic-rods/).
The [double reflection method](/double-reflection-method/) computes it from sample points.

## Definition

Let $x(u)$ be a regular $C^2$ curve in $\mathbb{R}^3$, with the speed $\sigma = |x'| > 0$ and the unit tangent $t = x'/\sigma$.
A **unit normal field** along $x$ is a $C^1$ map $r(u)$ with $|r| = 1$ and $r \cdot t = 0$.

**Rotation minimizing normal field.** A unit normal field $r$ is rotation minimizing if $r'$ is parallel to $t$ at every $u$.
Differentiating $r \cdot t = 0$ gives $r' \cdot t = -r \cdot t'$, so the condition is the linear differential equation

$$r' = -(r \cdot t')\,t.$$

**Rotation minimizing frame.** A rotation minimizing frame is a right-handed orthonormal frame $(r, s, t)$ with $s = t \times r$ in which $r$ is rotation minimizing.
Then $s$ is rotation minimizing too.

**Bishop's equations.** With the arc length $\ell$ and derivatives with respect to it written with a dot, a rotation minimizing frame satisfies

$$\dot t = k_1 r + k_2 s, \qquad \dot r = -k_1 t, \qquad \dot s = -k_2 t,$$

where $k_1 = \dot t \cdot r$ and $k_2 = \dot t \cdot s$ are the normal curvatures with respect to the frame, and $k_1^2 + k_2^2 = \kappa^2$, the square of the curvature.

**Angular velocity.** The angular velocity of the frame is $\omega = k_1\,s - k_2\,r$ with respect to arc length, which has no component along $t$.
Any frame $(r_\theta, s_\theta, t)$ that rotates the rotation minimizing one about $t$ by an angle $\theta(\ell)$ has the angular velocity $\omega + \dot\theta\,t$, whose length is at least $|\omega| = \kappa$.
So among all orthonormal frames that contain the tangent, the rotation minimizing frames have the smallest angular speed at every point, which gives the name.

**Existence and uniqueness.** The defining equation is linear with continuous coefficients, so for each start vector $r(u_0) \perp t(u_0)$ there is exactly one solution on the whole curve.
The solution keeps $|r| = 1$ and $r \perp t$.
Two rotation minimizing frames of the same curve differ by a rotation about $t$ by a constant angle.

**Relation to the Frenet frame.** Where the curvature $\kappa$ is positive, the Frenet frame $(T, N, B)$ is defined, with the torsion $\tau$.
Writing $r = \cos\theta\,N + \sin\theta\,B$ and using the Frenet formulas gives the condition $\dot\theta = -\tau$, so

$$\theta(\ell) = \theta(\ell_0) - \int_{\ell_0}^{\ell}\tau\,d\ell.$$

The Frenet frame turns about the tangent at the rate $\tau$, and the rotation minimizing frame does not.

**Parallel transport.** The equation says that $r(u)$, as a tangent vector of the unit sphere at the point $t(u)$, is moved by parallel transport along the curve of tangents $t(u)$ on the sphere.
For this reason the frame is also called the parallel transport frame.

## Examples and non-examples

- **A straight line.** The tangent is constant, $t' = 0$, so every constant unit normal gives a rotation minimizing frame. The Frenet frame does not exist there.
- **A plane curve.** For a curve in a plane with the unit normal $n$, the constant field $r = n$ is rotation minimizing, because $r' = 0$. The frame is $(n, t \times n, t)$ up to a sign, so $s$ is the normal of the curve in the plane. On the curve $y = x^3$, the Frenet normal flips from one side to the other at the inflection point $x = 0$, while the rotation minimizing frame is smooth there.
- **A circle.** The torsion is 0, so the Frenet frame is rotation minimizing.
- **A helix.** For $x(u) = (a\cos u, a\sin u, bu)$, the torsion is $\tau = b/(a^2 + b^2)$ and the arc length of one turn is $2\pi\sqrt{a^2 + b^2}$. So the rotation minimizing frame falls behind the Frenet frame by the angle $2\pi b/\sqrt{a^2 + b^2}$ per turn, which is $2.810$ radians, about 161 degrees, for $a = 1$ and $b = 1/2$. The [double reflection method](/double-reflection-method/) reproduces this angle to the fourth order in the step.
- **A curve on a sphere.** For a curve on a sphere with the center $p$ and the radius $\rho$, the radial field $r = (x - p)/\rho$ is rotation minimizing, because $r' = x'/\rho$ is parallel to $t$.
- **A closed curve.** After one loop, the rotation minimizing frame comes back turned about the tangent by some angle $\alpha$. By the parallel transport view and the Gauss-Bonnet theorem, $\alpha$ equals, up to the sign and modulo $2\pi$, the area that the closed curve of tangents encloses on the unit sphere. A frame for a closed tube must spread this angle along the curve.
- **Non-example: the Frenet frame of a helix.** It turns about the tangent at the rate $\tau \ne 0$, so its normal $N$ is not rotation minimizing.
- **Non-example: a fixed up vector.** The frame whose $r$ is the projection of a fixed vector, such as the vertical, onto the normal plane is not rotation minimizing in general. It is often the better choice for a camera, but it turns about the tangent and fails where the tangent is parallel to the fixed vector.

## Related definitions

- **[Frenet-Serret frame](/frenet-frame/).** The frame of tangent, principal normal and binormal. It is defined only where $\kappa > 0$, and it turns about the tangent at the rate of the torsion.
- **Relatively parallel frame.** Bishop's name for a rotation minimizing frame, as one example of a frame along a curve that is adapted to the tangent.
- **Parallel transport.** The transport of a tangent vector of a surface along a curve on it with no turning, as measured in the surface. The rotation minimizing frame is parallel transport on the unit sphere along the curve of tangents.
- **[Angular velocity](/angular-velocity/).** The vector $\omega$ with $\dot e = \omega \times e$ for each vector $e$ of a moving frame. A rotation minimizing frame has $\omega \cdot t = 0$.
- **Twist of a rod.** In [discrete elastic rods](/discrete-elastic-rods/), the material frame of a rod is described by its angle to a rotation minimizing reference frame, and the twist energy depends on the derivative of that angle.
- **[Sweep surface](/sweep-surface/).** A surface made by moving a cross section along a curve. A rotation minimizing frame gives a sweep with no artificial twist.
- **[Double reflection method](/double-reflection-method/).** A fourth-order method to compute the frame at sample points, by two reflections per step.

## References
