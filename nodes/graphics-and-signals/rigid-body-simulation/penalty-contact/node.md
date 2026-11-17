---
tag: VCKTJD
kind: technique
slug: penalty-contact
name: Penalty method for contact
aliases:
- penalty-based contact
- spring contact model
area: graphics-and-signals/rigid-body-simulation
level: intro
summary: Push overlapping bodies apart with a stiff spring force proportional to the penetration depth, plus damping along the normal.
prereqs: [symplectic-euler-method, penetration-depth, newton-euler-equations]
see_also: [mass-spring-system, coefficient-of-restitution, collision-impulse, baumgarte-stabilization, incremental-potential-contact, signed-distance-function, a-stability, backward-euler-method]
sources:
  - paper: doi:10.1145/54852.378528
    title: "Matthew Moore and Jane Wilhelms, Collision detection and response for computer animation, Computer Graphics (SIGGRAPH 88) 22(4), 289-298, 1988"
    locator: the spring method of collision response (general locator)
  - paper: doi:10.1115/1.3423596
    title: "K. H. Hunt and F. R. E. Crossley, Coefficient of restitution interpreted as damping in vibroimpact, Journal of Applied Mechanics 42(2), 440-445, 1975"
    locator: the nonlinear damping term that vanishes at zero penetration (general locator)
---

The penalty method treats contact as a stiff spring. When two bodies overlap by a depth $d > 0$, it applies a force $k d$ along the contact normal that pushes them apart, often with a damping force against the normal relative velocity. Nothing stops the bodies from overlapping; the spring only makes overlap expensive, so a stiffer spring gives a smaller overlap. The method is the simplest way to add contact to any integrator, and it gives forces at all times, which makes it easy to couple with other forces. The price is the step size: a stiff spring needs a small time step, or an explicit integrator gains energy and the bodies fly apart. The stiffness $k$ and the damping $c$ are tuning, not material constants, unless they are fitted to a contact model such as Hertz contact.

## In plain words

Two objects that touch push each other away. This method pretends that there is a strong spring at each place where they touch. The deeper one object sinks into the other, the harder the spring pushes back. A weak spring lets objects sink in a lot. A strong spring keeps them almost apart, but it shakes very fast, and a computer that takes large time steps cannot follow such fast shaking. Then the objects jump away with more speed than they had. So a strong spring needs many small steps. A second part, like the shock absorber of a car, slows the shaking down and makes the bounce smaller.

## When it applies

- Any method that computes forces and integrates them, such as an explicit or [symplectic Euler](/symplectic-euler-method/) integrator, a [mass-spring system](/mass-spring-system/), cloth, or soft bodies, where a contact force is just one more force.
- Cases where small overlaps are acceptable and a distance or depth is cheap, for example from a [signed distance function](/signed-distance-function/) or a [penetration depth](/penetration-depth/) query.
- Contact between many points of deformable bodies, where an impulse solver over all contacts would be costly.

It is a poor fit for stiff stacks of rigid bodies with large time steps, where impulse or complementarity methods such as [projected Gauss-Seidel](/projected-gauss-seidel/) are used instead.

## The template

For a contact between $A$ and $B$ with unit normal $n$ from $B$ to $A$ ($y$ up), depth $d$ and normal relative velocity $v_{rel} = n \cdot (v_A(p) - v_B(p))$:

1. Find the contacts and their depths $d > 0$, for example with a narrow phase [collision detection](/collision-detection/) query.
2. Compute the normal force $f_n = k d - c \, v_{rel}$; with Hunt and Crossley's nonlinear damping, $f_n = k d^q + \lambda d^q \dot d$ with $\dot d = -v_{rel}$.
3. Clamp $f_n$ at zero, so the contact never pulls. This step is a choice; without it, a linear damper pulls the bodies together near the end of the contact.
4. Apply $f_n n$ to $A$ at $p$ and $-f_n n$ to $B$, with the torques about the centers of mass.
5. Integrate all forces over the step. With symplectic Euler, update the velocities first and then move the bodies with the new velocities.

```pseudo id=main
PENALTY-STEP(bodies, k, c, Δt)
L1  for each contact (A, B, p, n, d) with d > 0
L2    f ← max(0, k d - c n·(v_A(p) - v_B(p)))
L3    add f n to A at p, and -f n to B at p
L4  for each body: v ← v + Δt M⁻¹ F
L5  for each body: x ← x + Δt v
```

**The step limit (proved).** For one body of mass $m$ on a spring of stiffness $k$ that stays in contact, the equation is $\ddot x = -\omega^2 x$ with $\omega = \sqrt{k/m}$. Symplectic Euler maps $(x, v)$ to $(x + \Delta t v', v')$ with $v' = v - \Delta t \omega^2 x$. The matrix of this map has determinant 1 and trace $2 - \omega^2 \Delta t^2$, so its eigenvalues have modulus 1 and the motion stays bounded if and only if $|2 - \omega^2 \Delta t^2| < 2$, that is

$$\Delta t < \frac{2}{\omega} = 2 \sqrt{\frac{m}{k}}.$$

For several bodies the limit is set by the largest frequency of the stiffness matrix; for a chain of masses on springs this frequency is below $2\omega$, so $\Delta t < 1/\omega$ is always enough there. The limit holds only while the spring is engaged. Entering and leaving contact in the middle of a step is not covered by this argument, and it can add energy at step sizes below the limit (see the measurements below).

**Damping and restitution (computed).** With a linear damper and damping ratio $\zeta = c / (2\sqrt{k m}) < 1$, ignoring gravity during the contact and letting the contact last until the depth is zero again, the bounce has the coefficient of restitution $e = \exp(-\zeta\pi/\sqrt{1 - \zeta^2})$; for $\zeta = 0.2$, $e = 0.526621$. This $e$ does not depend on the impact speed, and the force jumps to $c |v_{rel}|$ at first touch. Hunt and Crossley (1975) proposed damping proportional to $d^q \dot d$, which vanishes at zero depth.

## Classic examples

**A ball dropped on the floor.** A ball of mass $m = 1$ falls from $1$ m and meets a floor spring of stiffness $k = 100$ N/m at $4.42945$ m/s, with $g = 9.81$ m/s² and no damping. The values below are computed from the exact solution of the spring with gravity.

| quantity | $k = 100$ | $k = 10^5$ |
|---|---|---|
| $\omega = \sqrt{k/m}$ | 10 rad/s | 316.228 rad/s |
| step limit $2/\omega$ | 0.2 s | 0.0063246 s |
| largest depth | 0.551778 m | 0.014106 m |
| time in contact | 0.357750 s | 0.009979 s |
| depth at rest, $m g / k$ | 0.0981 m | $9.81 \cdot 10^{-5}$ m |

The soft spring lets the ball sink by half a meter. The stiff one keeps the overlap near 1 cm, but its contact lasts 10 ms, so a step of $1/60$ s sees at most one step of it.

**What happens at larger steps (measurement).** The same drop with symplectic Euler, from rest at 1 m, should come back to 1 m. The height of the bottom of the ball at the top of the first bounce:

| $k$ | $\Delta t$ | bounce height |
|---|---|---|
| 100 | 1/600 s | 0.9999 m |
| 100 | 1/60 s | 0.9934 m |
| 100 | 1/30 s | 1.0165 m |
| 100 | 1/10 s | 1.2563 m |
| $10^5$ | 1/600 s | 0.9938 m |
| $10^5$ | 1/60 s | 105.9 m |

All the steps for $k = 100$ are below the limit of 0.2 s, but at $1/10$ s the ball gains a quarter of its energy at the moments of entering and leaving contact, and at $1/30$ s it already gains a little. For $k = 10^5$, a step of $1/60$ s is above the limit, and the ball is shot up about a hundred times higher than it fell.

## Variations

- **Nonlinear springs.** $f = k d^{3/2}$ follows the Hertz model of two elastic spheres, from the theory of elasticity, with $k$ set by the radii and the materials. The barrier of [incremental potential contact](/incremental-potential-contact/) grows without bound as the distance goes to zero, so overlap cannot occur.
- **Implicit integration.** [Backward Euler](/backward-euler-method/) is [A-stable](/a-stability/), so a linear spring does not make it unstable for any stiffness, but it damps the motion and needs a linear solve per step.
- **Friction.** A tangential spring anchored at the first contact point models stick, and a slip rule moves the anchor when the spring force passes $\mu f_n$. The anchor stiffness is tuning.
- **Velocity-level penalties.** A bias velocity proportional to the depth, as in [Baumgarte stabilization](/baumgarte-stabilization/), is the same idea applied inside an impulse solver.

## Pitfalls

- **Energy gain.** Too stiff a spring for the step, or a step that crosses the contact boundary, adds energy. Check the step limit for the stiffest contact and the smallest mass.
- **Mass ratios.** The limit depends on $m/k$. A light body against a stiff contact sets the step for the whole scene.
- **Pulling dampers.** A linear damper pulls near the end of the contact unless the force is clamped at zero.
- **Tunneling.** A thin or fast body can pass through in one step before the spring sees any depth; use [continuous collision detection](/continuous-collision-detection/) or smaller steps.
- **Stacks sink.** Each layer sinks by its load over $k$, so a tall stack visibly sinks unless $k$ is large, and large $k$ brings back the step limit.

## References
