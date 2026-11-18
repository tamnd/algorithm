---
tag: BJ4E1Y
kind: algorithm
slug: impact-zones
name: Impact zones
aliases:
- rigid impact zones
area: graphics-and-signals/deformable-body-simulation
level: advanced
summary: Group vertices involved in unresolved simultaneous collisions and move each group rigidly, or project it to a collision-free state, until no collisions remain.
solves: [cloth-simulation]
model: real-ram
complexity:
  vars: {n: "the number of nodes", m: "the number of edges", p: "the number of passes that find collisions"}
  time: {pass: "Θ(n m)", total: "O(p n m)", worst_case: "O(n^2 m)"}
  space: {zones: "Θ(n + m)"}
properties: {deterministic: true, exact: false, collision_free_result: true, linear_momentum_conserving: true, angular_momentum_conserving: false}
history:
  year: 1997
  people: [Xavier Provot, Robert Bridson, Ronald Fedkiw, John Anderson]
  note: Provot proposed impact zones in 1997, and Bridson, Fedkiw and Anderson gave a corrected rigid motion in 2002 and used the method as the failsafe of their collision pipeline.
prereqs: [continuous-collision-detection, disjoint-set]
see_also: [robust-cloth-collision, elementary-ccd-tests, incremental-potential-contact, bounding-volume-hierarchy, linear-complementarity-problem, baraff-witkin-cloth, provot-strain-limiting, cloth-simulation]
sources:
  - paper: doi:10.1007/978-3-7091-6874-5_13
    title: "Xavier Provot, Collision and self-collision handling in cloth model dedicated to design garments, Computer Animation and Simulation 97, Eurographics, Springer, pages 177 to 189, 1997"
    locator: "the impact zones (as described and corrected by Bridson et al. 2002, Section 7.5)"
  - paper: doi:10.1145/566654.566623
    title: "Robert Bridson, Ronald Fedkiw and John Anderson, Robust treatment of collisions, contact and friction for cloth animation, ACM Transactions on Graphics 21(3), pages 594 to 603, 2002"
    locator: "Section 7.4 (iterated geometric collisions and the switch to a failsafe), Section 7.5 (rigid impact zones, the corrected rigid motion)"
  - paper: doi:10.1145/1360612.1360622
    title: "David Harmon, Etienne Vouga, Rasmus Tamstorf and Eitan Grinspun, Robust treatment of simultaneous collisions, ACM Transactions on Graphics 27(3), 2008"
    locator: "the abstract (a failsafe that cancels impact but not sliding motion)"
---

Impact zones are the last line of defence of a cloth collision method. When a step has many collisions at once, applying impulses one collision at a time can go on for a long time, because fixing one collision can cause another. Provot (1997) suggested a failsafe: put all nodes of the collisions that remain into groups, the *impact zones*, and move each group as one rigid body. Bridson, Fedkiw and Anderson (2002) showed that Provot's formulas did not give a true rigid motion, corrected them, and used the zones after a few passes of impulses. A rigid zone cannot collide with itself, so the zones only grow, and the loop ends with a step that has no collisions.

## In plain words

Imagine a crumpled sheet in which many folds hit each other in the same instant. Pushing the folds apart one pair at a time may never finish, because every push can cause a new hit.

Impact zones take a blunt approach: every group of points that collides is glued together for this step and moves as one solid piece. A solid piece cannot pass through itself, so the problem inside the group is gone. If a glued group still hits another part of the cloth, the two are glued together too. In the worst case the whole cloth moves as one solid piece for one step, and that motion has no collisions.

The price is that the glued points stop moving relative to each other for that step. The group keeps its total momentum, so it still drifts and turns in a believable way.

## The problem

Given node positions $\mathbf x_i$ with no contact, masses $m_i$, velocities $\mathbf v_i$ for a step of length $\Delta t$, and the edges of the cloth, find new velocities such that the straight paths $\mathbf x_i + s\, \Delta t\, \mathbf v_i$, $s \in [0, 1]$, have no contact: no node lies on an edge that does not contain it at any time. The page works in 2D, where the cloth is a set of curves and a node-edge test covers every contact. In 3D the tests are node-triangle and edge-edge, as in [robust cloth collision](/robust-cloth-collision/).

## The algorithm

```pseudo id=main
RIGID-IMPACT-ZONES(x, v, m, edges, dt)
L1  make each node its own zone                              ▷ a disjoint-set structure
L2  loop:
L3      C <- all node-edge collisions on the paths x + s dt v, s in [0, 1]
L4      if C is empty: return v
L5      for each collision (i, (a, b)) in C: unite the zones of i, a and b
L6      for each zone Z that took part in a collision of C:
L7          x_cm, v_cm <- mass-weighted means over Z ;  L <- sum m_i r_i x (v_i - v_cm) ;  I <- sum m_i |r_i|^2
L8          omega <- L / I                                    ▷ a scalar in 2D, I^-1 L in 3D
L9          for i in Z: y_i <- x_cm + dt v_cm + R(dt omega) r_i   ▷ r_i = x_i - x_cm
L10             v_i <- (y_i - x_i) / dt
```

**The collision test (L3).** A node $\mathbf p$ is on the line of a moving edge $\mathbf a \mathbf b$ when $(\mathbf b - \mathbf a) \times (\mathbf p - \mathbf a) = 0$. On straight paths this is a quadratic in $s$. The code solves it, keeps the roots in $[0, 1]$, and checks at each root that $\mathbf p$ is between $\mathbf a$ and $\mathbf b$. The code tests all node-edge pairs; a real code uses a [bounding volume hierarchy](/bounding-volume-hierarchy/) or [spatial hashing](/spatial-hashing/) first.

**The rigid motion (L7 to L10).** This is Section 7.5 of Bridson et al. The zone keeps its centre of mass velocity $\mathbf v_{cm}$, and its angular velocity $\omega = I^{-1} L$ is the one that keeps the angular momentum. To make the step itself rigid, the end positions are the start positions rotated by the angle $\Delta t\, \omega$ about the centre of mass and moved by $\Delta t\, \mathbf v_{cm}$, and the new velocity is the mean velocity over the step. In 3D the part of $\mathbf r_i$ along $\omega$ does not rotate; in 2D that part is empty.

**Choices of this code.** Only zones that took part in a collision of the pass get a new motion. If the rotation angle $\Delta t\, |\omega|$ is $\pi$ or more, the zone only translates, because the proof needs an angle below $\pi$.

## Example

**One node falls on an edge, by hand.** An edge joins $(0, 0)$ and $(1, 0)$, both at rest, and a node at $(0.5, 0.1)$ falls with $2$ m/s, with $\Delta t = 0.1$ s and all masses $1$ kg. The node reaches the edge at $s = 0.5$. Line L5 makes one zone of the three nodes. Its centre is $(0.5, 0.0\overline 3)$, its mean velocity is $(0, -2/3)$ m/s, and the relative velocities are $(0, 2/3)$, $(0, 2/3)$ and $(0, -4/3)$ at offsets $(-0.5, -0.0\overline 3)$, $(0.5, -0.0\overline 3)$ and $(0, 0.0\overline 6)$. The angular momentum is $-0.5 \cdot \frac23 + 0.5 \cdot \frac23 + 0 = 0$, so $\omega = 0$ and all three nodes move down with $2/3$ m/s. The momentum $2$ kg m/s is kept, and the next pass finds no collision. If the node falls at $(0.8, 0.1)$ instead, the same steps give $L = -0.4$, $I \approx 0.567$ and $\omega \approx -0.71$ rad/s, so the zone also turns.

**Two chains, measured.** A chain of 10 nodes at rest and a chain of 10 nodes $0.05$ m above it, falling with about $1$ m/s, with $\Delta t = 0.1$ s, have 18 collisions in the first pass. All 20 nodes end in one zone after one pass, and the second pass finds no collision. Both chains then move together as one rigid body for that step: the failsafe resolves the collisions but freezes the cloth into a clump, which is why Bridson et al. use it only after the impulses fail.

**One chain with random velocities, measured.** For eight chains of 12 nodes with random velocities up to $1.5$ m/s, four have no collision, three need one pass with one zone of 3 nodes, and one needs one pass with a zone of 5 nodes.

## Correctness

The claims are proved in [proofs/correctness.md](proofs/correctness.md).

1. **Rigid and momentum (proved).** The end positions of a zone are a rigid image of the start positions, and the zone keeps its linear momentum exactly. Rigid input velocities give back their angular velocity.
2. **Angular momentum (proved, not kept).** The mean velocities have the angular momentum $L \sin\varphi/\varphi$ with $\varphi = \Delta t\, \omega$, so it is kept only up to $O(\varphi^2)$.
3. **No self-collision of a zone (proved).** At every time of the step, the nodes of a rigid zone are an invertible affine image of their start positions when $|\varphi| < \pi$, so a zone without contact at the start has none during the step.
4. **Termination (proved).** Every pass with a collision merges at least two zones, so the loop ends after at most $n - 1$ such passes, and the result has no collision on the paths and no crossing at the end.
5. **Plausibility (not claimed).** The method does not give the motion of real cloth; the zones remove all relative motion inside them for the step.

The tests check the collision time against fine sampling and bisection, a collinear case, the rigid motion, the momentum and the angular momentum factor, the fallback for large angles, two chains that pass through each other and random self-collisions of a chain. After each run they check the paths with the collision test, the end state with an exact test in rational arithmetic, the linear momentum to $10^{-10}$, the rigidity of each zone, and the zones against the connected components of all collisions found.

## Complexity

A pass of this code tests every node against every edge, $\Theta(n m)$, and moves the zones in $\Theta(n)$ time. The disjoint-set operations cost $O(\alpha(n))$ each, amortized, with path halving and union by size. With $p$ passes the cost is $O(p\, n\, m)$, and $p \le n - 1$, so the worst case is $O(n^2 m)$. With a bounding volume hierarchy, a pass costs about the number of nearby pairs instead of $n m$. In practice the impulses before the failsafe remove most collisions, and the zones stay small (Bridson et al., Section 7.5; an observation, not a bound).

## Properties

- **Always ends.** The zones only grow, and one rigid zone has no collision.
- **Collision free.** The result has no contact on the paths, in exact arithmetic.
- **Dissipative.** All relative motion in a zone is lost, which can look like sticky cloth.
- **Linear momentum.** Kept exactly in each zone. Angular momentum is kept only to $O(\varphi^2)$.
- **Order free.** All collisions of a pass are handled together, so the result does not depend on the order of the collision list.

## Variants and improvements

- **Provot's zones (1997).** The original formulas for the zone motion did not give a rigid motion, so a zone could still deform during the step. Bridson et al. corrected them (Section 7.5).
- **Inelastic projection.** Harmon, Vouga, Tamstorf and Grinspun (2008) replace the rigid motion by a failsafe that cancels the approaching motion but keeps sliding, which removes much less energy, and they add an approximation of Coulomb friction.
- **Barrier methods.** [Incremental potential contact](/incremental-potential-contact/) keeps the cloth free of intersections by a barrier energy inside the time step, so no failsafe is needed.
- **Contact as a complementarity problem.** Simultaneous contacts can also be posed as a [linear complementarity problem](/linear-complementarity-problem/) on the impulses.

## When to use it

Use impact zones as the failsafe of a collision pipeline that must never let cloth pass through itself, after a few passes of local impulses have not removed every collision. Use it alone only when stickiness is acceptable, because the zones freeze the cloth into clumps.

Do not use it as the main contact method, and prefer an inelastic projection when the sliding of cloth on cloth matters.

## Pitfalls

- **Contact at the start.** The proof needs a start state with no contact. If the input already intersects, the rigid motion keeps the intersection.
- **Large rotations.** For $\Delta t\, |\omega| \ge \pi$ the path of a rigid zone is not an invertible affine image of the start, and a zone can pass through itself. The code then only translates the zone.
- **Rounding.** In floating point a node can end on an edge by rounding. Real codes add a small thickness and test proximity, not only exact contact.
- **Angular velocity in 3D.** $I^{-1} L$ needs the inertia tensor of the current positions. For collinear nodes the tensor is singular, and the angular velocity along the line has no effect and must be set to zero.
- **Recomputing old zones.** Giving an unchanged zone a new rigid motion from its mean velocities shrinks its rotation by $\sin\varphi/\varphi$ every pass. The code recomputes only zones that took part in a collision.

## Implementations

## History

Xavier Provot described impact zones in 1997 for garment design, as a way to handle many collisions at once in cloth that bunches together, where friction prevents most relative motion. Bridson, Fedkiw and Anderson (2002) used the idea as the failsafe of their robust collision method, after the repulsion forces and iterated collision impulses, and noted that Provot's formulas for the angular velocity were flawed. Harmon, Vouga, Tamstorf and Grinspun (2008) replaced the rigid motion by an inelastic projection that keeps sliding motion.

## References
