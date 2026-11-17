---
tag: XKE6M3
kind: model
slug: coulomb-friction-law
name: Coulomb friction law
aliases:
- Coulomb friction model
- dry friction
- Amontons-Coulomb friction
area: graphics-and-signals/rigid-body-simulation
level: intro
summary: The tangential contact force is at most mu times the normal force and opposes sliding; it reaches the bound when the contact slides.
prereqs: [newton-euler-equations, dot-product]
see_also: [friction-cone, collision-impulse, impulse-based-simulation, projected-gauss-seidel, painleve-paradox, rigid-contact-complementarity, stewart-trinkle-time-stepping, baraff-contact-force-algorithm]
sources:
  - paper: doi:10.1137/s0036144599360110
    title: "David E. Stewart, Rigid-body dynamics with friction and impact, SIAM Review 42(1), 3-39, 2000"
    locator: "the statement of Coulomb's law as a set-valued relation, the friction cone, and Painleve's paradox (general locator)"
  - paper: doi:10.1145/127719.122722
    title: "David Baraff, Coping with friction for non-penetrating rigid body simulation, Computer Graphics (SIGGRAPH 91) 25(4), 31-41, 1991"
    locator: the NP-hardness of consistent contact forces with Coulomb friction
  - url: https://box2d.org/files/ErinCatto_IterativeDynamics_GDC2005.pdf
    title: "Erin Catto, Iterative Dynamics with Temporal Coherence, Game Developers Conference, 2005"
    locator: "Section 4.3 (friction rows bounded by a constant, mu m_c g)"
---

Coulomb's law of friction is the usual model of dry friction between rigid bodies in simulation. At a contact with normal force $f_n \ge 0$, the friction force $f_t$ lies in the tangent plane and is bounded by $\mu f_n$, where $\mu$ is the friction coefficient. If the contact does not slide, any friction force within the bound is allowed, and the dynamics decide which one acts. If the contact slides, the friction force is at the bound and points against the sliding velocity. The law is empirical, and $\mu$ is a measured number for a pair of surfaces; a real $\mu$ changes with speed, load, temperature and wear. The law is simple to state, but it makes rigid body dynamics hard: the force is a set-valued function of the sliding velocity, and with it some problems have no solution or many.

## The machine

A contact between bodies $A$ and $B$ has a point $p$, a unit normal $n$ from $B$ to $A$ ($y$ up, as in the rest of this area) and the relative velocity $u = v_A(p) - v_B(p)$. Split it into the normal part $u_n = n \cdot u$ and the sliding velocity $u_t = u - u_n n$. The contact force on $A$ is $f = f_n n + f_t$ with $f_t \cdot n = 0$. Coulomb's law is

$$\|f_t\| \le \mu f_n, \qquad \text{and if } u_t \ne 0: \quad f_t = -\mu f_n \frac{u_t}{\|u_t\|}.$$

- **Stick (static friction).** $u_t = 0$, and $f_t$ is any vector with $\|f_t\| \le \mu f_n$.
- **Slip (dynamic friction).** $u_t \ne 0$, and $f_t$ is at the bound, against the sliding.

The same law holds for impulses during a collision. The set of allowed forces $\{f : \|f_t\| \le \mu f_n\}$ is the [friction cone](/friction-cone/) (the robotics pages use $z$ up). A second statement of slip is the maximum dissipation principle: among the forces of the cone, the sliding contact chooses the one that removes energy fastest, $f_t$ minimizes $f_t \cdot u_t$. Some models use a static coefficient $\mu_s$ for stick and a smaller dynamic $\mu_d$ for slip.

## What it counts

The law fixes the force from three numbers: the normal force, the coefficient, and the direction of sliding. It does not depend on the area of contact or the sliding speed. It is a law of the model, fitted to experiments, not a consequence of the rigid body equations. The coefficient $\mu$ is a measurement for a pair of surfaces, and a simulator that uses one constant value is using a fitted model.

## Relation to other models

- **Linearized cones.** Engines and time stepping methods replace the circular cone by a polygon with $k$ edges, for example a box in 2 tangent directions, so that the problem becomes a [linear complementarity problem](/linear-complementarity-problem/). [Stewart-Trinkle time stepping](/stewart-trinkle-time-stepping/) does this with a polyhedral cone. The polygon makes the friction depend on the direction of sliding relative to the axes.
- **Box friction with a fixed bound.** [Projected Gauss-Seidel](/projected-gauss-seidel/) as described by Catto (2005, Section 4.3) bounds each friction row by the constant $\mu m_c g$, where $m_c$ is a share of the mass, instead of $\mu f_n$. This keeps the bounds fixed and is tuning. Later engines use $\pm \mu \lambda_n$ with the current normal impulse.
- **Regularized friction.** A penalty model replaces stick by a stiff tangential spring, or replaces the jump at $u_t = 0$ by a steep smooth function of $u_t$. Then a stuck body creeps slowly, and the step size must be small.
- **Impulses.** [Collision impulses](/collision-impulse/) and [impulse-based simulation](/impulse-based-simulation/) apply the law to the impulse of one collision, with stick and slip during the collision. With friction, the restitution laws differ (see the [coefficient of restitution](/coefficient-of-restitution/)).

## Known results in the model

**A block on a slope (computed).** A block of mass $m = 1$ rests on a slope at $30°$, with $g = 9.81$ m/s². Gravity has the component $m g \sin 30° = 4.905$ N along the slope and $m g \cos 30° = 8.495709$ N into it, so $f_n = 8.495709$ N. The block sticks if and only if $\mu \ge \tan 30° = 0.577350$.

| $\mu$ | bound $\mu f_n$ | friction needed to stick | outcome |
|---|---|---|---|
| 0.6 | 5.097426 N | 4.905 N | stick, $f_t = 4.905$ N |
| 0.5 | 4.247855 N | 4.905 N | slip, $a = g(\sin 30° - \mu \cos 30°) = 0.657145$ m/s² |

With $\mu = 0.5$ the block slides $0.328573$ m in the first second from rest. With $\mu = 0.6$ the friction force is not $\mu f_n$: in stick, the law gives only a bound, and the force is what keeps the block at rest.

**Existence and uniqueness can fail (proved in the literature).** For rigid bodies with Coulomb friction, the contact forces at an instant may not exist or may not be unique; this is [Painleve's paradox](/painleve-paradox/), and Stewart (2000) surveys it. Formulations at the level of impulses over a time step, such as Stewart-Trinkle time stepping, recover existence.

**Consistent forces with friction are NP-hard (proved).** Baraff (1991) showed that deciding whether consistent contact forces exist under Coulomb friction is NP-hard. His later pivoting method extends to friction, but its static friction version is not proved to terminate (see [Baraff's contact force algorithm](/baraff-contact-force-algorithm/)).

**Not proved.** Convergence of projected Gauss-Seidel with the bounds $\pm \mu \lambda_n$ (the bounds move with the normal impulse, so the problem is not a symmetric program); see the proof of [projected Gauss-Seidel](/projected-gauss-seidel/).

## References
