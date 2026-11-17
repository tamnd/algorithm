---
tag: 0Z69Y4
kind: definition
slug: coefficient-of-restitution
name: Coefficient of restitution
aliases:
- Newton's restitution law
- restitution coefficient
area: graphics-and-signals/rigid-body-simulation
level: intro
summary: The ratio of the relative normal velocity after a collision to that before it, from 0 for a perfectly plastic to 1 for an elastic collision.
prereqs: [newton-euler-equations, dot-product]
see_also: [collision-impulse, impulse-based-simulation, coulomb-friction-law, penalty-contact, zeno-behavior, painleve-paradox, rigid-contact-complementarity, shock-propagation]
sources:
  - book: isbn:9780521632867
    title: "W. J. Stronge, Impact Mechanics, Cambridge University Press, 2000"
    locator: "the definitions of the kinematic, kinetic and energetic coefficients of restitution, and the treatment of collisions with friction (general locator)"
  - paper: doi:10.1098/rspa.1990.0125
    title: "W. J. Stronge, Rigid body collisions with friction, Proceedings of the Royal Society of London A 431(1881), 169-181, 1990"
    locator: the energetic coefficient of restitution and its difference from the kinematic and kinetic forms when friction acts
  - paper: doi:10.1137/s0036144599360110
    title: "David E. Stewart, Rigid-body dynamics with friction and impact, SIAM Review 42(1), 3-39, 2000"
    locator: the discussion of restitution laws for rigid body impact with friction (general locator)
  - paper: doi:10.1145/199404.199436
    title: "Brian Mirtich and John Canny, Impulse-based simulation of rigid bodies, Symposium on Interactive 3D Graphics, 181-188, 1995"
    locator: "Section 4 (the collision with compression and restitution phases, and Poisson's hypothesis)"
---

The coefficient of restitution $e$ is the number that a rigid body simulation uses to decide how strongly two bodies bounce apart after a collision. Rigid bodies cannot deform, so the short phase of compression and recovery inside a real collision is not part of the model; $e$ stands in for all of it. Under Newton's law, the relative normal velocity after the collision is $-e$ times the value before it: $e = 0$ is a perfectly plastic collision, in which the bodies stay together along the normal, and $e = 1$ is an elastic one. The value is a measured, empirical number for a pair of materials. It changes with the impact speed, the shape and the material, so a constant $e$ is a model, not a law of nature. When friction acts, there are three different definitions, and they give different results.

## Definition

Two bodies $A$ and $B$ touch at a point $p$ with unit normal $n$ from $B$ to $A$, with $y$ up as in the rest of this area. The relative normal velocity is

$$v_{rel} = n \cdot (v_A(p) - v_B(p)), \qquad v_X(p) = v_X + \omega_X \times (p - x_X),$$

and the bodies approach when $v_{rel} < 0$. Let $v_{rel}^-$ be its value just before the collision and $v_{rel}^+$ the value just after. A collision lasts for an instant, in which a normal impulse $p_n \ge 0$ acts. It has a compression phase, which ends when $v_{rel} = 0$, and a restitution phase, which ends at separation.

- **Kinematic (Newton).** $v_{rel}^+ = -e \, v_{rel}^-$.
- **Kinetic (Poisson).** $p_n^{total} = (1 + e) \, p_n^{c}$, where $p_n^{c}$ is the normal impulse of the compression phase; equivalently the restitution phase gives $e$ times the impulse of the compression phase.
- **Energetic (Stronge).** $e^2 = -W_r / W_c$, where $W_c < 0$ is the work of the normal impulse in the compression phase and $W_r \ge 0$ is its work in the restitution phase.

In all three forms $0 \le e \le 1$ is the usual range. The kinematic form is the one used by the [collision impulse](/collision-impulse/) of most engines, $j = -(1 + e) v_{rel}^- / K$ with the effective mass $1/K$ along the normal.

**Without friction the three forms agree (proved).** Without friction, the impulse acts along $n$ only, so $v_{rel}$ is an affine function of the normal impulse, $v_{rel} = v_{rel}^- + K p_n$ with $K > 0$. Compression ends at $p_n^c = -v_{rel}^- / K$. Poisson's law gives $p_n^{total} = (1 + e) p_n^c$, so $v_{rel}^+ = -e v_{rel}^-$, which is Newton's law. The work along the normal is $\int v_{rel} \, dp_n$; it is $-(v_{rel}^-)^2 / (2K)$ in compression and $(v_{rel}^+)^2 / (2K)$ in restitution, so Stronge's $e$ is the same $e$. The loss of kinetic energy is then $(1 - e^2)(v_{rel}^-)^2 / (2K)$, which is never negative for $e \le 1$.

**With friction they differ.** Friction couples the tangential and normal directions through the effective mass matrix, and the friction impulse can change sign or stop during the collision. Then the ratio of velocities, the ratio of impulses and the ratio of work are no longer the same number (Stronge 1990). Stronge argues that the energetic form is the one that keeps the energy balance consistent; with the kinematic form, a collision with friction can end with more kinetic energy than it began with. The examples below show this.

## Examples and non-examples

**A dropped ball (law and model).** A ball falls from $h = 1$ m onto a static floor, with $g = 9.81$ m/s². It hits at $v = \sqrt{2 g h} = 4.42945$ m/s. With $e = 0.5$ it leaves at $2.21472$ m/s and rises to $e^2 h = 0.25$ m. The first fall takes $t_0 = \sqrt{2h/g} = 0.451524$ s, and each later bounce takes $e$ times as long as the one before it, so the infinitely many bounces end at

$$T = t_0 \frac{1 + e}{1 - e} = 1.354571 \text{ s}.$$

This is [Zeno behavior](/zeno-behavior/): infinitely many collisions in finite time. A simulator with a fixed step cannot follow it, so engines set $e = 0$ below a small approach speed. That threshold is tuning.

**A measured value is not a constant (measurement).** The value of $e$ comes from tests such as drops at several heights, and it depends on the impact speed as well as on the materials and the shapes. A simulator that uses one value of $e$ is using a model fitted to one range of speeds.

**Newton's law with friction adds energy (example, computed).** A 2D rod of mass $m = 1$ and moment of inertia $I = 1/3$ hits the floor ($n = (0, 1)$) with the tip at the arm $r = (3/5, -4/5)$ from its center. Its center moves with $v = (-1/2, -1)$ and $\omega = 0$, so the tip moves with $u^- = (-1/2, -1)$. The tip velocity changes by $K p$ for an impulse $p$, with

$$K = \begin{pmatrix} 73/25 & 36/25 \\ 36/25 & 52/25 \end{pmatrix}.$$

Take $e = 1$ in Newton's law and ask that the tip stop sliding: $u^+ = (0, 1)$. Then $p = K^{-1}(u^+ - u^-) = (-23/50, 32/25)$, which is inside the friction cone for $\mu \ge 23/64 \approx 0.36$. The rod leaves with $v^+ = (-24/25, 7/25)$ and $\omega^+ = 6/5$. Its kinetic energy goes from $0.625$ to $0.74$: a gain of $23/200$. With the same $\mu = 1/2$, Poisson's law with the friction integrated over the collision (as in [impulse-based simulation](/impulse-based-simulation/)) gives the total impulse $(-271/730, 11/10)$ and $u^+ = (0, 55/73)$, and the energy changes by $-25/584$, a loss. The two laws give different outcomes for the same $e$, and only one of them loses energy.

**Not a coefficient of restitution.** The ratio of speeds of the centers of mass is not $e$ unless the collision is central and frictionless; $e$ is defined on the relative velocity at the contact point along the normal. A value of $e$ above 1 is not a restitution value of passive materials; it adds energy and only appears as an artifact, for example of position correction (see [Baumgarte stabilization](/baumgarte-stabilization/)).

## Related definitions

- [Collision impulse](/collision-impulse/) applies Newton's law at one contact point.
- [Impulse-based simulation](/impulse-based-simulation/) follows Mirtich and Canny (1995), who integrate the collision in a compression and a restitution phase and use Poisson's hypothesis.
- [Coulomb friction](/coulomb-friction-law/) gives the tangential impulse that makes the three forms differ.
- [Penalty contact](/penalty-contact/) replaces $e$ by a spring and a damper; for a linear damper with damping ratio $\zeta$, the bounce has $e = \exp(-\zeta\pi/\sqrt{1 - \zeta^2})$, independent of the impact speed.
- [Rigid contact complementarity](/rigid-contact-complementarity/) and the [Painleve paradox](/painleve-paradox/) treat impact with friction in robotics, where $z$ is up.
- Stewart (2000) surveys restitution laws and their problems for rigid bodies with friction and impact.

## References
