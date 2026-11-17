---
tag: P8GDCY
kind: algorithm
slug: impulse-based-simulation
name: Impulse-based simulation
aliases:
- Mirtich-Canny impulse-based dynamics
area: graphics-and-signals/rigid-body-simulation
level: core
summary: Simulate all contact, including resting contact, as a series of collision impulses, with friction resolved by integrating along the impulse.
solves: [rigid-body-simulation-problem]
model: real-ram
complexity:
  vars: {n: the number of bodies, c: the number of collision events}
  time: {next_event_brute_force: O(n^2), one_collision: O(1), total_brute_force: O(c n^2)}
  space: {total: O(n)}
properties: {deterministic: true, online: true, recursive: false, in_place: true}
history:
  year: 1995
  people: [Brian Mirtich, John Canny]
  note: Mirtich and Canny modeled every contact, resting, rolling and sliding, as trains of collisions, with Poisson's hypothesis, Coulomb friction integrated along the collision, and microcollisions for contacts that are almost at rest.
prereqs: [collision-impulse, coulomb-friction-law, coefficient-of-restitution, newton-euler-equations]
see_also: [projected-gauss-seidel, baraff-contact-force-algorithm, penalty-contact, friction-cone, conservative-advancement, lin-canny-closest-features, priority-queue, rigid-body-simulation-problem]
sources:
  - paper: doi:10.1145/199404.199436
    title: "Brian Mirtich and John Canny, Impulse-based simulation of rigid bodies, Proceedings of the 1995 Symposium on Interactive 3D Graphics, 181-188"
    locator: "Section 3 (collision heap and time of impact bounds), Section 4 (Poisson's hypothesis, the collision parameter p_z, sliding and sticking modes) and Section 4.5 (static contact and microcollisions, v_e = sqrt(2 g eps_c))"
  - paper: doi:10.1145/54852.378530
    title: "James K. Hahn, Realistic animation of rigid bodies, SIGGRAPH 88, Computer Graphics 22(4), 299-308, 1988"
    locator: impulse-based collision response, an earlier use of impulses in animation
  - paper: doi:10.1098/rspa.1990.0125
    title: "W. J. Stronge, Rigid body collisions with friction, Proceedings of the Royal Society of London A 431(1881), 169-181, 1990"
    locator: the kinematic, kinetic and energetic coefficients of restitution for collisions with friction
---

Impulse-based simulation treats every contact between [rigid bodies](/rigid-body-simulation-problem/) as a collision. Between collisions each body follows a ballistic path. When two bodies come within a small distance $\varepsilon_c$, the collision envelope, and approach, the simulator applies one impulse that resolves the collision, with [Coulomb friction](/coulomb-friction-law/) and Poisson's hypothesis for restitution. A body that rests on a table is then a body that makes many tiny bounces. Mirtich and Canny (1995) built the method, with a heap of time of impact bounds and with microcollisions, which keep resting bodies from creeping.

## In plain words

Most simulators treat a box on a table as a special case: the box touches the table, so the simulator computes a force that holds it up. This method has no such case. The box falls a tiny distance, hits the table, bounces up a tiny distance, and falls again. Each hit is handled like any other collision.

This makes the simulator simple. It needs only two parts: a part that finds the next collision, and a part that computes what one collision does. Between collisions, nothing touches, so each body flies freely under gravity.

The collision part is careful about friction. During a hit, the touching points can slide, then stop, then stay stuck or slide the other way. The method follows these changes along the hit instead of guessing the end result.

## The problem

The input is a set of rigid bodies with their masses, inertia, positions and velocities, gravity $g$, a coefficient of restitution $e$, a friction coefficient $\mu$, the envelope $\varepsilon_c$ and an end time. The output is the state at the end time, such that no two bodies overlap and the collisions obey the collision model below.

The collision model has three assumptions, all stated by Mirtich and Canny in Section 4.1. A collision takes no time, so positions do not change during it. Poisson's hypothesis holds: with $p_{mc}$ the normal impulse up to the point of maximum compression, where the normal relative velocity is zero, the total normal impulse is $(1 + e) p_{mc}$. Coulomb friction holds at every instant of the collision. These are empirical models. This page works in 2D, with discs on a ground line, where the collision can be integrated exactly; Mirtich and Canny work with convex polyhedra in 3D.

Notation for one contact: $n$ is the unit normal from $B$ to $A$, $t = (n_y, -n_x)$ is the tangent, and $u = (u_t, u_n)$ is the velocity of the contact point of $A$ minus that of $B$. The impulse $p = (p_t, p_n)$ acts on $A$, and $-p$ on $B$. By the [Newton-Euler equations](/newton-euler-equations/), $u = u^- + K p$ with the symmetric $2 \times 2$ matrix $K_{de} = \sum_X m_X^{-1} (d \cdot e) + I_X^{-1} (r_X \times d)(r_X \times e)$, which is positive definite when at least one body moves.

## The algorithm

```pseudo id=main
SIMULATE(bodies, t_end)
L1  t ← 0
L2  loop
L3    (τ, A, B) ← the earliest time from now at which a pair is within ε_c and approaching
L4    if t + τ > t_end then move all bodies on ballistic paths to t_end; return
L5    move all bodies on ballistic paths by τ; t ← t + τ
L6    build n, t, the arms r_A, r_B, the matrix K and the contact velocity u
L7    if |u_n| < v_e and q = K⁻¹(-2u) lies in the friction cone then p ← q        ▷ microcollision
L8    else p ← COLLIDE(K, u, μ, e′), with e′ = 1 if |u_n| < v_e, else e′ = e
L9    apply p to A and -p to B

COLLIDE(K, u, μ, e)
L10 p ← 0; target ← none
L11 repeat
L12   d ← (d_t, 1): slide d_t = -μ sgn u_t; stick d_t = -K_tn/K_tt if u_t = 0 and |K_tn| ≤ μ K_tt; else slide again d_t = -μ sgn K_tn
L13   δ ← the smallest step in p_n to the next event: u_t reaches 0, u_n reaches 0, or p_n reaches target
L14   p ← p + δ d; u ← u + δ K d
L15   if u_n reached 0 then target ← (1 + e) p_n          ▷ maximum compression
L16 until p_n = target
L17 return p
```

The threshold $v_e = \sqrt{2 g \varepsilon_c}$ is the speed that a body at rest gains when it falls through the envelope (Mirtich and Canny, eq. 12). A microcollision reverses the whole contact velocity. It is used only when that impulse lies inside the [friction cone](/friction-cone/), so that friction could provide it.

COLLIDE follows Mirtich and Canny in using $p_n$ as the collision parameter: it starts at zero and only grows, while time inside the collision is not known. While the contact slides, the friction impulse grows at $\mu$ times the normal impulse against the slip. In 2D the slip direction is just a sign, so within one phase $u$ is a straight line in $p_n$, and each event takes one division. In 3D the slip direction turns during the collision, and Mirtich and Canny integrate a nonlinear differential equation numerically instead of L12 to L14.

Line L8 with $e' = 1$ is a choice of this page, not of the paper: a slow contact whose reversing impulse is outside the cone slides, and keeping its normal speed makes the bounces deliver, on average, a normal impulse equal to the weight. Without it, the bounces of a sliding disc shrink geometrically and pile up in a finite time while the disc still slides.

## Example

**One collision.** A rod of mass 1 and length 2 ($I = 1/3$) hits the ground with its lower tip at the arm $r = (3/5, -4/5)$ from its center, with $n = (0, 1)$. Then $K = \begin{pmatrix} 73/25 & 36/25 \\ 36/25 & 52/25 \end{pmatrix}$. The rod moves with $v = (-1/2, -1)$ and $\omega = 0$, so $u^- = (-1/2, -1)$. Take $\mu = 1/2$ and $e = 1$.

| phase | mode | $d_t$ | ends at | $p$ at the end | $u$ at the end |
|---|---|---|---|---|---|
| 1 | slide | $1/2$ | $u_t = 0$ | $(5/58, 5/29)$ | $(0, -15/29)$ |
| 2 | stick | $-36/73$ | $u_n = 0$ | $(-1/10, 11/20)$ | $(0, 0)$ |
| 3 | stick | $-36/73$ | $p_n = 11/10$ | $(-271/730, 11/10)$ | $(0, 55/73)$ |

The test $|K_{tn}| \le \mu K_{tt}$ is $36/25 \le 73/50$, so the tip stays stuck after the slip stops. The kinetic energy changes by $p \cdot u^- + \tfrac12 p^T K p = -25/584$. For the same rod, Newton's law $u_n^+ = -e\, u_n^-$ with a full stop of the slip gives the impulse $(-23/50, 32/25)$ and adds $23/200$ to the energy (see [coefficient of restitution](/coefficient-of-restitution/)). With $\mu = 1/5$ the test fails ($36/25 > 73/125$), and the tip slides again in the other direction for the rest of the collision.

**A disc with backspin.** A disc of mass 1 and radius $0.5$ falls from $0.1$ above the envelope with $v = (2, 0)$ and spin $\omega_0$, with $\mu = 0.5$, $e = 0.5$ and $\varepsilon_c = 10^{-3}$. At every contact the impulse acts at the contact point, so the angular momentum about that point, $I\omega - m R v_x$, does not change, and the flights do not change it either. When the slip stops, $v_x = (2 v_0 - R \omega_0)/3$, the same rolling speed as the continuous Coulomb model. The measured runs over 2 s:

| $\omega_0$ | rolling speed | events in 2 s | slip stops at |
|---|---|---|---|
| 4 | $2/3$ | 94 | about 0.286 s |
| 12 | $-2/3$ | 94 | about 0.536 s |

With $\omega_0 = 12$ the disc rolls back. The continuous model with the normal force $mg$ from the first contact at $0.143$ s predicts the stops at $0.415$ s and $0.686$ s: the impulse model stops the slip earlier because the landing impulse is much larger than the weight.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Its main steps are proved properties of the 2D model:

- COLLIDE ends after at most three phases. The slip can stop at most once; after it stops, the contact either stays stuck or slides the other way forever. The normal velocity increases in every phase except a slide phase that is about to stop, which uses that $K$ is positive definite.
- The result satisfies $p_n = (1 + e) p_{mc}$, $|p_t| \le \mu p_n$, friction against the slip in every slide phase, and $u_n^+ \ge 0$.
- A microcollision changes $u$ to $-u$ and does no work: $\Delta T = \tfrac12 p \cdot (u^- + u^+) = 0$. Mirtich and Canny state this property in Section 4.5.
- Between events the motion is exact, and the loop finds the first time at which some pair is within $\varepsilon_c$ and approaching.
- A single disc at rest has a bounded event rate: after the first slow event, its approach speed is fixed in $[e v_e, v_e)$, so events are at least $2 e v_e / g$ apart, and the gap stays below $2\varepsilon_c$.

## Complexity

One collision costs $O(1)$: at most three phases of constant work in 2D. Finding the next event by brute force costs $O(n^2)$ per event, as on this page. Mirtich and Canny keep the pairs in a heap ordered by a lower bound on the time of impact, recompute bounds only for pairs that involve a body that just collided, and cut the candidate pairs with a hierarchy of spatial hash tables, so that bodies far apart are never tested. The total cost is the number of events times the cost per event, and the number of events is the weak point: it depends on the scene, and for resting contact it grows as $\varepsilon_c$ shrinks, since one resting disc makes up to $g / (2 e v_e)$ events per second. For a stack of bodies, the event rate is a measurement, not a bound.

## Properties

- Every contact is a collision, so there is no list of contact states to keep and no switching between resting and colliding modes.
- Bodies never touch: collisions happen at the gap $\varepsilon_c$. Resting bodies hover in $[\varepsilon_c, 2\varepsilon_c)$.
- The Coulomb law holds within each collision, including the stops and reversals of slip.
- Linear momentum is conserved in collisions between moving bodies, and angular momentum too, because both impulses act at the same point.
- With $e = 1$ and $\mu = 0$, the kinetic energy is conserved.
- The friction result is not that of a continuous contact force with the same $\mu$; see the second example.

## Variants and improvements

- **3D.** The sliding direction rotates during the collision. Mirtich and Canny integrate the relative velocity numerically and solve a quartic when the slip stops and must resume; they conjecture that the outward sliding direction is unique.
- **Other restitution laws.** Newton's law on velocities, Poisson's law on impulses and Stronge's energetic coefficient agree without friction and differ with it. Newton's law with friction can add energy (the rod example). Stronge's energetic coefficient compares the work of the normal force in restitution with that in compression.
- **Simultaneous contacts.** Treating the contacts of a stack one at a time is slow and can be order dependent. [Projected Gauss-Seidel](/projected-gauss-seidel/) with accumulated impulses solves all contacts of a step together, and [shock propagation](/shock-propagation/) orders them from the ground up.
- **Time stepping.** Instead of exact event times, a fixed step can collect all contacts within the envelope and resolve them together, as in [Stewart-Trinkle time stepping](/stewart-trinkle-time-stepping/). That bounds the work per unit time but gives up the exact order of the collisions.

## When to use it

Use it for scenes with many brief collisions and few long contacts: a pool break or parts in a vibratory feeder, two examples of Mirtich and Canny. Avoid it for tall stacks, bodies at rest in large numbers, and joints: the event rate for resting contact is high, and joints are not collisions. A [penalty](/penalty-contact/) or constraint-based method, or a time-stepping method with a velocity solver, is the usual choice there.

## Pitfalls

- **Zeno behaviour.** With $e < 1$ and exact event times, a body that bounces with friction can make infinitely many collisions in a finite time. The microcollision rule and the slow sliding rule above prevent it for one disc, but a body that starts exactly at the envelope with zero velocity, or a contrived stack, can still produce events with speeds that tend to zero.
- **Creep on a ramp.** Without microcollisions, a block on a ramp creeps down even when $\mu$ is large, because it falls during every flight. Mirtich and Canny show that microcollisions stop it.
- **The envelope is a tuning value.** A large $\varepsilon_c$ makes resting bodies hover visibly; a small one raises the event rate. The threshold $v_e$ follows from it and from $g$.
- **Sign of the normal.** COLLIDE assumes $u_n < 0$ at the start and the normal from $B$ to $A$. A wrong sign gives an impulse that pulls.
- **Rounding at the stop.** In floating point, set $u_t$ to zero exactly at the stop event; otherwise the next phase may see a tiny slip of either sign.

## Implementations

## History

Hahn (1988) and Moore and Wilhelms (1988) used impulses for collisions in computer animation, next to other methods for resting contact. Baraff's analytical methods (1989 to 1994) computed contact forces with complementarity instead. Mirtich and Canny (1995) took the other road and handled all contact with impulses. They built on the impact analysis of Routh, with Keller (1986) and Bhatt and Koechling (1994) for frictional impacts, and on the Lin-Canny closest features algorithm for distances. Stronge (1990) analyzed the coefficients of restitution for collisions with friction.

## References
