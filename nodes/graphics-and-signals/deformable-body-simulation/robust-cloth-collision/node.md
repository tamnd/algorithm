---
tag: QXMR1R
kind: algorithm
slug: robust-cloth-collision
name: Bridson-Fedkiw-Anderson cloth collision handling
aliases:
- robust cloth collision handling
area: graphics-and-signals/deformable-body-simulation
level: advanced
summary: Handle cloth contact with repulsion forces for proximity, continuous collision impulses for fast motion, and rigid impact zones as a final safeguard.
solves: [cloth-simulation]
model: floating-point-model
complexity:
  vars: {n: "the number of nodes", t: "the number of triangles", e: "the number of edges", P: "the number of impulse passes", Z: "the number of impact zone passes"}
  time: {pass: "Θ(n t + e^2)", total: "O((1 + P + Z) (n t + e^2))", worst_case: "O(n (n t + e^2))"}
  space: {pairs: "Θ(n t + e^2)"}
properties: {deterministic: true, exact: false, collision_free_result: true, linear_momentum_conserving: true, angular_momentum_conserving: false, order_dependent: true}
history:
  year: 2002
  people: [Robert Bridson, Ronald Fedkiw, John Anderson]
  note: Bridson, Fedkiw and Anderson combined repulsion impulses, continuous collision impulses and corrected rigid impact zones into one pipeline for cloth at SIGGRAPH 2002.
prereqs: [continuous-collision-detection, elementary-ccd-tests, impact-zones]
see_also: [incremental-potential-contact, bounding-volume-hierarchy, spatial-hashing, coulomb-friction-law, baraff-witkin-cloth, provot-strain-limiting, cloth-simulation, linear-complementarity-problem]
sources:
  - paper: doi:10.1145/566654.566623
    title: "Robert Bridson, Ronald Fedkiw and John Anderson, Robust treatment of collisions, contact and friction for cloth animation, ACM Transactions on Graphics 21(3), pages 594 to 603, 2002"
    locator: "Section 5 (the pipeline), Section 6 (proximity and the coplanarity cubic), Section 7.1 to 7.5 (impulse weights, repulsions, friction, iterated collisions, rigid impact zones)"
  - paper: doi:10.1007/978-3-7091-6874-5_13
    title: "Xavier Provot, Collision and self-collision handling in cloth model dedicated to design garments, Computer Animation and Simulation 97, Eurographics, Springer, pages 177 to 189, 1997"
    locator: "the impact zones and the cubic for the coplanarity of moving points (as cited by Bridson et al. 2002, Sections 6 and 7.5)"
  - paper: doi:10.1145/1360612.1360622
    title: "David Harmon, Etienne Vouga, Rasmus Tamstorf and Eitan Grinspun, Robust treatment of simultaneous collisions, ACM Transactions on Graphics 27(3), 2008"
    locator: "the abstract (a failsafe that cancels impact but not sliding motion)"
---

Cloth is thin, it folds onto itself, and it moves fast. A simulation that only checks for overlap at the end of a step lets cloth pass through cloth. Bridson, Fedkiw and Anderson (2002) gave a collision method for triangle cloth with three stages. Cheap repulsion impulses keep nearby pieces apart and add friction. Continuous collision tests then find every crossing on the straight paths of the step and stop it with an impulse. If crossings remain after a few passes, rigid impact zones remove them for certain. The result is a step with no intersection, whatever the internal cloth model did.

## In plain words

Think of a shirt that is folding onto itself during one frame. The cloth solver has proposed where every point goes. This method checks that proposal before it is used.

First, points that are already very close get a small push apart, and sliding pieces rub with friction. This takes care of most contact.

Second, the method follows each point on a straight line through the frame and asks if a point passes through a triangle or an edge passes through an edge. Each such crossing gets a push that stops the approach. A push can cause a new crossing, so this is repeated a few times.

Third, if crossings still remain, the points of each crossing are glued together and move as one solid piece for this frame. A solid piece cannot pass through itself, so this always ends with no crossing.

## The problem

Given a triangle mesh with node positions $\mathbf x_j$ that have no intersection, masses $m_j$, and candidate mean velocities $\mathbf v_j$ from the cloth solver for a step of length $\Delta t$, find new mean velocities such that the straight paths $\mathbf x_j + t\, \mathbf v_j$, $t \in [0, \Delta t]$, have no contact. A contact is a node on a triangle that does not contain it, or two edges with no common node that touch. The step then ends at $\mathbf x_j + \Delta t\, \mathbf v_j$, and the solver turns the mean velocity into the end velocity (Section 7.6 of the paper, not part of this page). The cloth also has a thickness $h$: pairs closer than $h$ at the start get repulsions.

## The algorithm

Each pair has four nodes and four weights $c_j$ that sum to $0$: $(1, -w_1, -w_2, -w_3)$ for a node and a triangle with barycentric weights $w$, and $(1 - a, a, -(1 - b), -b)$ for two edges with closest points at the fractions $a$ and $b$. The relative velocity is $\sum c_j \mathbf v_j$. To change it by $\Delta\mathbf u$, node $j$ gets $c_j \Delta \mathbf u / (m_j W)$ with $W = \sum c_j^2/m_j$, and the effective mass is $m_{\rm eff} = 1/W$.

```pseudo id=main
ROBUST-CLOTH-COLLISIONS(x, v, m, mesh, dt, h, k, mu, P)
L1  for each point-triangle and edge-edge pair closer than h at x:              ▷ repulsions
L2      n, c, d <- unit normal, node weights, overlap h - distance ;  vN <- (sum c_j v_j) . n
L3      if vN < 0: apply the inelastic impulse that sets vN to 0
L4      if vN < 0.1 d / dt: raise vN by min(dt k d / m_eff, 0.1 d / dt - vN)     ▷ spring
L5      lower the tangential relative speed by min(mu dvN, |vT|)                ▷ friction
L6  repeat at most P times:                                                     ▷ collisions
L7      C <- pairs that meet on the paths x + t v, t in [0, dt]                  ▷ cubic, proximity
L8      if C is empty: return v
L9      for each (pair, t) in C: if vN < 0 for the normal at time t: set vN to 0
L10 loop:                                                                       ▷ failsafe
L11     C <- pairs with nodes in two or more zones that meet on the paths
L12     if C is empty: return v
L13     merge the four nodes of each pair of C into one zone ; move each changed zone rigidly
```

**Repulsions (L1 to L5).** Section 7.2 of the paper. A pair that approaches gets a fully inelastic impulse, because cloth contact loses most of its energy. A spring of stiffness $k$ acts on the overlap $d = h - $ distance, but it may only raise the normal velocity to $0.1 d/\Delta t$, so that it never pushes a pair out of the overlap in one step. Bridson et al. match $k$ to the stretch stiffness of the cloth (a heuristic). Friction follows Coulomb's law (Section 7.3): the normal impulse $\Delta v_N$ allows a tangential change of at most $\mu\, \Delta v_N$, and the tangential speed never changes sign.

**Continuous detection (L7, L11).** Section 6. Four moving points meet only when they are coplanar, so the code solves the cubic $(\mathbf x_{21}(t) \times \mathbf x_{31}(t)) \cdot \mathbf x_{41}(t) = 0$. The cubic is monotone between its critical points, so each root comes from bisection on a sign change, and the critical points are kept as times too. At each time in increasing order the code tests proximity with the tolerance $10^{-6}$ m of the paper, by barycentric weights for a node and a triangle and by the closest points for two edges. See [elementary CCD tests](/elementary-ccd-tests/).

**Collision impulses (L9).** Section 7.4. Each collision gets an inelastic impulse with the normal of the collision time. The impulse changes the velocity for the whole step, so the pair then keeps about its start distance.

**Failsafe (L10 to L13).** Section 7.5 and the page [impact zones](/impact-zones/). The zone keeps its linear and angular momentum, $\boldsymbol\omega = \mathbf I^{-1}\mathbf L$, and its end positions are the start positions rotated by $\Delta t |\boldsymbol\omega|$ about $\boldsymbol\omega$ and moved by $\Delta t\, \mathbf v_{cm}$.

**Choices of this code.** The impulses act one pair at a time; the paper also allows a parallel update with a relaxation of $0.25$. The spring cap is written for the relative velocity with the effective mass, which for equal masses is the weighting of Section 7.1. The code tests all pairs after a box test, not a bounding volume hierarchy, and it has no proximity test at the end of the step and no adaptive step. In the failsafe it skips pairs with all four nodes in one zone, because a rigid zone has no internal contact. If a zone would turn by $\pi$ or more, or its inertia tensor is singular, it only translates. If a cubic is zero for all $t$, the code tests 65 evenly spaced times.

## Example

**A node falls on a triangle, by hand.** The triangle has the corners $(0, 0, 0)$, $(1, 0, 0)$ and $(0, 1, 0)$ at rest, and a node at $(0.25, 0.25, 0.1)$ falls with $2$ m/s, with $\Delta t = 0.1$ s, all masses $1$ kg and $h = 0.005$ m. The node is $0.1$ m away, so L1 finds no close pair. The cubic gives the coplanar time $t = 0.05$ s, where the node is at the barycentric weights $(0.5, 0.25, 0.25)$, inside the triangle. The weights of the pair are $(1, -0.5, -0.25, -0.25)$, so $W = 1 + 0.25 + 0.0625 + 0.0625 = 11/8$. The normal relative velocity is $-2$ m/s, and L9 changes it by $+2$: the node gets $2 \cdot 8/11 = 16/11$ m/s and its velocity becomes $-6/11 \approx -0.545$ m/s; the corners get $-8/11$, $-4/11$ and $-4/11$ m/s. The momentum is $-6/11 - 8/11 - 4/11 - 4/11 = -2$ kg m/s, as before, and the relative normal velocity is $-6/11 - (0.5 \cdot (-8/11) + 0.25 \cdot (-4/11) \cdot 2) = 0$. The second pass of L7 finds no collision. For equal masses this is the impulse $\tilde I = 2I/(1 + \sum w_i^2) = 16/11$ of Section 7.1 with $I = 1$.

**A sheet falls through a sheet, measured.** Two sheets of $5 \times 5$ nodes and 32 triangles each, $0.1$ m apart in the grid and $0.05$ m apart in height, have 3008 point-triangle pairs and 5786 edge-edge pairs. The lower sheet is at rest. The nodes of the upper sheet fall with speeds from about $0.2$ to $1.2$ m/s, so without handling the upper sheet ends half through the lower one with $\Delta t = 0.1$ s (the exact test finds an intersection). With $h = 0.005$ m, $k = 50$ N/m, $\mu = 0.3$ and masses of $0.01$ kg, the first pass of L7 finds 75 collisions, and after their impulses the second pass finds none. The mean vertical velocity is then $-0.31$ m/s for the lower sheet and $-0.39$ m/s for the upper sheet. With $P = 0$ the failsafe alone does the work: one pass makes one zone of 38 nodes, which moves as one rigid body for the step.

**Close sheets, measured.** Two sheets of $4 \times 4$ nodes $0.004$ m apart, with $h = 0.005$ m and $\Delta t = 0.01$ s, have 66 close pairs at the start. After the repulsions the slowest node of the upper sheet falls with $0.023$ m/s instead of $0.047$ m/s, and the first pass of L7 finds no collision.

**Self-collision, measured.** One sheet of $5 \times 5$ nodes with random velocities up to $1.5$ m/s and $P = 1$: with the seed 11 the impulses meet 19 collisions and one failsafe pass makes two zones of 4 nodes; with the seed 12 they meet 11 collisions and two failsafe passes make one zone of 8 nodes.

## Correctness

The claims are proved in [proofs/correctness.md](proofs/correctness.md).

1. **Momentum (proved).** Every impulse changes the relative velocity of its pair by exactly the asked amount and keeps the linear momentum, because the weights sum to zero. For equal masses it is the weighting of Section 7.1. The rigid zones keep the momentum too.
2. **One repulsion (proved).** For one pair alone, after L3 and L4 the normal relative velocity is at least $0$ and the spring part raises it to at most $0.1 d/\Delta t$. Friction never reverses the sliding direction. With many pairs, later impulses can change earlier ones.
3. **Detection (proved).** A contact makes the four nodes coplanar, so its time is a root of the cubic, and the list of times holds every root of the cubic in $[0, 1]$ when the cubic is not zero.
4. **Termination and result (proved).** The failsafe merges at least two zones in each pass that finds a collision, so it ends after at most $n - 1$ such passes. A rigid zone has no internal contact when it turns by less than $\pi$. So the paths have no contact, and the end state has no intersection when the start state has none.
5. **Plausibility (heuristic, not claimed).** The stiffness $k$, the cap $0.1 d/\Delta t$, the relaxation and the number of passes are tuning choices. The page does not claim that the result is the motion of real cloth.

The tests check the cubic against the volume, the collision time against fine sampling of the volume with bisection, the closest points of two edges against an enumeration of all cases, the barycentric weights against area ratios, the impulse weights and momentum, the spring and friction formulas, and the rigid motion of a zone against a rotation matrix. On the sheet scenes they check the paths with the collision test, the end state with an exact test in rational arithmetic, the momentum to $10^{-10}$ and the rigidity of each zone.

## Complexity

Let $n$ be the number of nodes, $t$ the number of triangles and $e$ the number of edges. This code tests all $\Theta(n t + e^2)$ pairs in each pass, and each test costs $O(1)$: a box test, a cubic, at most a fixed number of bisection steps and a few proximity tests. There is one repulsion pass, at most $P$ collision passes and $Z \le n - 1$ failsafe passes, so the total is $O((1 + P + Z)(n t + e^2))$, and the worst case is $O(n (n t + e^2))$. Bridson et al. use a hierarchy of bounding boxes instead, so that a pass costs about the number of nearby pairs. They report that the repulsions catch almost all collisions, so few collision passes are needed and the zones stay small and rare; this is an observation of the paper, not a bound.

## Properties

- **No intersection at the end.** In exact arithmetic and when no cubic is zero, the step ends with no intersection.
- **Momentum.** The linear momentum is kept exactly. The angular momentum is not kept by the failsafe.
- **Order dependent.** The repulsions and collision impulses act one pair at a time, so the result depends on the order of the pairs.
- **Inelastic.** Contacts lose their normal approach speed, as the paper intends for cloth.
- **Independent of the cloth model.** The method only changes the mean velocities, so it can follow any internal solver, such as [Baraff-Witkin cloth](/baraff-witkin-cloth/).

## Variants and improvements

- **Parallel update.** All impulses of a pass are computed from the same velocities and added with a relaxation such as $0.25$ (Section 7.2 and 7.4).
- **Inelastic projection.** Harmon, Vouga, Tamstorf and Grinspun (2008) replace the rigid zones by a failsafe that cancels the approach but keeps sliding, so much less motion is lost.
- **Barrier methods.** [Incremental potential contact](/incremental-potential-contact/) keeps the cloth apart with a barrier energy inside the solver and needs no failsafe.
- **Exact root tests.** The floating-point cubic can give false negatives near degenerate cases. Later work, listed on [elementary CCD tests](/elementary-ccd-tests/), gives exact or conservative tests.

## When to use it

Use it after any cloth solver that must never let cloth pass through cloth or through itself, for example in garments with many folds. It adds friction and thickness at the same time, which matters for folds and wrinkles.

Do not expect it to fix a start state that already intersects. If sliding contact must look smooth, prefer an inelastic projection or a barrier method to the rigid zones.

## Pitfalls

- **Coplanar motion.** If four nodes stay in one plane, for example two pieces of a flat sheet that slide in their plane, the cubic is zero and gives no time. This code then tests 65 times, which can miss a short contact.
- **Rounding.** A floating-point cubic can miss a root near a double root. The tolerance $10^{-6}$ m and the thickness $h$ make this rare, not impossible.
- **Too many collision passes.** Impulses can create new collisions without end. Limit the passes and leave the rest to the failsafe.
- **Unequal masses.** The weights of Section 7.1 assume equal masses. With other masses, use the effective mass so that the momentum stays exact.
- **Sticky clumps.** Large zones freeze the cloth for the step. If zones are large and frequent, the repulsions are too weak or the step is too long.

## Implementations

## History

Moore and Wilhelms (1988) found contact times of moving points from the times at which they are coplanar, and Provot (1997) and Doghri et al. (1998) reduced this to the roots of a cubic, as Bridson et al. note in Section 6. Provot (1997) also proposed impact zones. Bridson, Fedkiw and Anderson (2002) combined repulsion impulses with friction, continuous collision impulses and a corrected rigid motion for the zones, and made the step free of intersection in a way that does not depend on the cloth model. Harmon, Vouga, Tamstorf and Grinspun (2008) replaced the rigid zones by an inelastic projection that keeps sliding motion.

## References
