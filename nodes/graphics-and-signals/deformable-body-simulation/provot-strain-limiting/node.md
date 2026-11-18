---
tag: SR6S3F
kind: algorithm
slug: provot-strain-limiting
name: Provot's strain limiting
aliases:
- inverse dynamic constraints
area: graphics-and-signals/deformable-body-simulation
level: core
summary: After each step, shorten springs stretched beyond a limit such as ten percent by moving their end points, to avoid the super-elastic look of soft springs.
solves: [cloth-simulation]
model: real-ram
complexity:
  vars: {n: "the number of particles", m: "the number of limited springs", k: "the number of sweeps"}
  time: {sweep: "Θ(m)", correction: "Θ(k m)", step: "Θ(n + k m)"}
  space: {extra: "Θ(n)"}
properties: {deterministic: true, exact: false, order_dependent: true, converges_when_feasible: true}
history:
  year: 1995
  people: [Xavier Provot]
  note: Provot kept soft springs for a stable explicit step and corrected the positions of over-stretched springs after the step, at Graphics Interface 1995.
prereqs: [mass-spring-system]
see_also: [cloth-simulation, position-based-dynamics, robust-cloth-collision, baraff-witkin-cloth, fast-mass-spring, impact-zones, gauss-seidel-method, projective-dynamics]
sources:
  - paper: doi:10.20380/GI1995.17
    title: "Xavier Provot, Deformation constraints in a mass-spring model to describe rigid cloth behavior, Graphics Interface 95, 147-154, 1995"
    locator: "Section 3 (the super-elastic effect), Section 4, equation (3) (the critical stiffness), Section 5 (the correction rules) and Section 6 (results with a 10% limit, one and two passes)"
  - paper: doi:10.1145/566654.566623
    title: "Robert Bridson, Ronald Fedkiw and John Anderson, Robust treatment of collisions, contact and friction for cloth animation, ACM Transactions on Graphics 21(3), 594-603, 2002"
    locator: "Section 4 (strain limiting: the case where Provot's method does not converge, and a version on velocities with Jacobi iteration)"
---

Provot's strain limiting is a correction that runs after each step of a [mass-spring](/mass-spring-system/) cloth. The springs are kept soft so that an explicit step stays stable. A soft spring stretches too much under load, so after the step every spring that is longer than $(1 + \tau)$ times its rest length, with $\tau$ about 10%, is shortened by moving its end points along the spring. Provot (1995) called this an inverse dynamic procedure and used it to make cloth that looks stiff with springs that are not. The same idea, a projection of positions onto constraints, is at the core of later [position-based dynamics](/position-based-dynamics/).

## In plain words

Real cloth hardly stretches. A spring model of cloth needs very stiff springs to match that, and stiff springs force tiny time steps. With softer springs the steps can be larger, but a hanging cloth then stretches like rubber near the points that hold it.

Provot's fix is to let the soft springs move the cloth as usual, and then check every spring. If a spring is more than 10% longer than its rest length, its two ends are pulled toward each other until it is exactly 10% longer. If one end is pinned, only the other end moves. If both ends are pinned, nothing can be done.

Fixing one spring can stretch its neighbour again, so one pass over the springs does not fix all of them. Repeating the pass helps, and it settles down whenever the limits can all hold at once.

## The problem

Given particle positions $\mathbf x_i$ after an explicit step of a mass-spring system, a list of springs $(a, b, L)$ and a limit $\tau$, move the free particles so that every spring has the length $l \le (1 + \tau) L$, with small moves. This is a step inside [cloth simulation](/cloth-simulation/). The force model, the stiffness and the time step stay as they were; the correction only changes positions (and then the velocities that follow from them).

## The algorithm

```pseudo id=main
PROVOT-STRAIN-LIMIT(x, springs, tau)
L1  repeat for the given number of sweeps (or until no spring is longer than (1 + tau) L)
L2      for each spring (a, b, L) in the list order:
L3          d <- x_b - x_a, l <- |d|, r <- (1 + tau)(1 - sigma) L
L4          if l <= r or both a and b are fixed: skip the spring
L5          e <- (l - r) d / l                          ▷ the excess, as a vector
L6          if a and b are free: x_a <- x_a + s_a e, x_b <- x_b - s_b e   ▷ s_a = s_b = 1/2
L7          else if a is free: x_a <- x_a + e
L8          else: x_b <- x_b - e
PROVOT-STEP(x, v, dt)
L9  x* <- the positions after one explicit step of the spring system
L10 x_new <- PROVOT-STRAIN-LIMIT(x*, springs, tau)
L11 v_new <- (x_new - x) / dt
```

**The correction (L3 to L8).** These are Provot's three rules from Section 5 of the paper. If both ends are free, both move toward the middle by half of the excess. If one end is fixed, the free end takes the whole excess. If both are fixed, the spring is left alone. Each correction uses the positions left by the corrections before it, so the result depends on the order of the springs, which Provot did not consider. The code also has a mass split $s_a = w_a / (w_a + w_b)$ with inverse masses $w$, which keeps the centre of mass; Provot's cloth had equal masses, where the two splits agree.

**The slack $\sigma$.** Provot's rule has $\sigma = 0$. The code accepts a small $\sigma > 0$, for example $10^{-3}$, which aims a little below the limit. Then repeated sweeps stop after a finite number of sweeps with every spring inside the limit (Corollary 5 of the proof page). The value $10^{-3}$ is a tuning constant of this code, not of the paper.

**Which springs.** Provot used $\tau = 10\%$ on the structural springs, and in a second version on the structural and shear springs (Section 6). The code takes the list of springs to correct as a parameter.

**Velocities (L11).** The code sets each velocity to the straight move from the old to the new position, so the next step does not undo the correction. This is a choice of this code.

## Example

**One sweep by hand.** Three free particles lie on a line at $0$, $1.5$ and $3.5$, joined by two springs of rest length 1, with $\tau = 0.1$, so the limit is $1.1$.

| | $x_0$ | $x_1$ | $x_2$ | first spring | second spring |
|---|---|---|---|---|---|
| start | 0 | 1.5 | 3.5 | 1.5 | 2.0 |
| after the first spring | 0.2 | 1.3 | 3.5 | 1.1 | 2.2 |
| after the second spring | 0.2 | 1.85 | 2.95 | 1.65 | 1.1 |

The first correction moves both ends by $0.2$. The second spring is now longer, $2.2$, and its correction moves its ends by $0.55$ each. That stretches the first spring to $1.65$, a strain of 65%. Repeated sweeps with $\sigma = 10^{-3}$ stop after 6 sweeps, with both springs inside the limit.

**A hanging cloth, measured.** A 9 by 9 grid with a spacing of $0.1$ m, particles of $0.01$ kg, structural and shear springs of $50$ N/m and a damping of $0.05$ N s/m along each spring hangs from its two top corners under gravity. It runs for 1000 steps of $\Delta t = 0.002$ s with symplectic Euler. The table gives the largest strain of a structural spring over the run, with the correction on the structural springs and $\tau = 0.1$.

| correction | largest structural strain |
|---|---|
| none | 72.5% |
| one sweep per step | 12.8% |
| two sweeps per step | 11.2% |
| sweeps until done, $\sigma = 10^{-3}$ | 10.0% (never above the limit) |

Without the correction the cloth near the corners stretches like rubber. With one sweep it stays close to the limit but above it. Two sweeps are better, as Provot also observed (Section 6), and repeated sweeps meet the limit.

## Correctness

The claims are about the positions; they are proved in [proofs/correctness.md](proofs/correctness.md).

1. **One correction (proved).** After lines L5 to L8 the spring has the length $(1 + \tau)(1 - \sigma) L$ and the same direction. The equal split keeps the midpoint of the pair; the mass split keeps its centre of mass.
2. **A projection (proved).** One correction moves the free positions to the closest point of the set $\{|x_b - x_a| \le r\}$, in the plain norm for the equal split and in the mass norm for the mass split. That set is convex.
3. **Repeated sweeps converge when the limits can hold (proved).** If some placement of the free particles meets every limit, the sweeps are cyclic projections onto closed convex sets with a common point, and they converge to a point that meets every limit. Provot (Section 6) wrote that the repeated procedure seemed to converge; this is the reason. With $\sigma > 0$ they stop after finitely many sweeps. Pins at their rest positions are enough, because the rest shape meets every limit.
4. **They cannot converge otherwise (proved).** If the pins force a stretch, no placement meets the limits. A chain of $n$ springs between pins at the distance $1.3\,nL$ always has a spring at least 30% too long. Bridson, Fedkiw and Anderson (2002, Section 4) name this case.
5. **One sweep gives no bound (proved by the example).** A later correction can undo an earlier one.

The tests check one correction against hand values, the projection against a brute force search over random allowed points, the centre of mass to $10^{-10}$ relative, the hand example, the finite end of the sweeps with pins at rest, the case that cannot converge, and the hanging cloth.

## Complexity

One correction costs $O(1)$, so a sweep costs $\Theta(m)$ for $m$ limited springs, and $k$ sweeps cost $\Theta(k m)$ on top of the explicit step of $\Theta(n + m)$. The extra space is $\Theta(n)$ for the new positions. Provot measured the cost of the correction at about 15% above the plain spring model (Section 6); that is a measurement on his scenes. The number of sweeps until the end in Corollary 5 has no useful bound in general: the convergence of cyclic projections can be slow.

## Properties

- **Explicit and simple.** No linear system, no stiffness matrix. Each correction is a few lines.
- **Order dependent.** The Gauss-Seidel order changes the result and can bias the cloth toward the springs visited last.
- **Not momentum conserving with pins.** A pinned particle does not move, so the free end takes the whole correction. Away from the pins, the mass split keeps the linear momentum of each pair.
- **Only stretch.** The rule shortens long springs and leaves short springs alone, so compression is not limited.
- **A heuristic, not a force law.** The correction moves positions without a force, so no law of motion controls its effect on the energy. It is a heuristic for the look of stiff cloth, and the limit $\tau$ is a tuning value.

## Variants and improvements

- **Velocity filter.** Bridson, Fedkiw and Anderson (2002, Section 4) apply momentum-conserving impulses to the velocities so that no spring is deformed by more than 10% at the end of the step, and also limit the change of strain per step. They use [Jacobi iteration](/jacobi-method/) to avoid the bias of Gauss-Seidel order; convergence is not guaranteed, but they report one or two iterations per step.
- **Strain limiting on triangles.** Later work limits the principal stretches of each triangle instead of spring lengths.
- **Position-based dynamics.** [Position-based dynamics](/position-based-dynamics/) and [extended position-based dynamics](/extended-position-based-dynamics/) use the same projection for every constraint and drop the soft forces altogether.
- **Exact inextensibility.** Fast projection methods solve for the positions that meet all length constraints at once, with a Newton-like step on the constraints, instead of one spring at a time.

## When to use it

Use it with an explicit mass-spring cloth whose springs must stay soft for a stable step, to keep the stretch inside a few percent. It is cheap and easy to add after any integrator. Pair it with repeated sweeps when the scene is pinned near its rest shape.

Do not rely on it when pins or obstacles force a stretch: the sweeps then cannot meet the limits and the cloth may jitter. For stiff cloth with large steps, an implicit method such as [Baraff-Witkin cloth](/baraff-witkin-cloth/) or [fast mass-spring simulation](/fast-mass-spring/) is the usual choice.

## Pitfalls

- **Forgetting the velocities.** If only the positions are corrected, the velocity still carries the stretch, and the next step stretches the cloth again.
- **One sweep and a hard limit.** A single sweep leaves springs above the limit, as the example shows. Code that assumes all springs are inside the limit after one sweep is wrong.
- **Infeasible pins.** Pins that are moved apart by an animator can make the limits impossible. Cap the number of sweeps.
- **Floating point.** With $\sigma = 0$ a corrected spring has the length $(1 + \tau) L$ only up to rounding; the hand example gives a strain of $0.1 + 9 \times 10^{-17}$. A strict check needs a small slack.
- **Mixing with collision handling.** The correction can push particles into an obstacle. Run collision handling after it, or include the contacts in the same sweeps.

## Implementations

## History

Xavier Provot presented the method at Graphics Interface 1995, in a paper on a mass-spring model of cloth. He measured the super-elastic effect on a grid hung by two corners, related the stiffness to the time step, and proposed to correct the positions of the over-stretched springs after each step. He tested it with a 10% limit and found that running the correction twice gave better results. In 2002 Bridson, Fedkiw and Anderson pointed out that the method cannot converge when the boundaries force a stretch, and moved the limit to the velocities. The projection of positions onto constraints became the base of position-based dynamics.

## References
