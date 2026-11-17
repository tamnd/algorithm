---
tag: P9J3VF
kind: problem
slug: penetration-depth
name: Penetration depth
aliases:
- penetration depth computation
area: graphics-and-signals/rigid-body-simulation
level: core
summary: The shortest translation that separates two overlapping solids, which gives the contact normal and the overlap distance.
prereqs: [minkowski-sum, convex-collision-detection]
see_also: [expanding-polytope-algorithm, gjk-algorithm, separating-axis-theorem, contact-manifold, collision-impulse, signed-distance-function, configuration-space, approximate-convex-decomposition]
sources:
  - paper: doi:10.1007/BF01190153
    title: David Dobkin, John Hershberger, David Kirkpatrick and Subhash Suri, Computing the intersection-depth of polyhedra, Algorithmica 9(6), 1993, 518 to 533
    locator: the definition of the intersection depth as the shortest translation that separates two convex polyhedra, and its computation
  - book: isbn:9781558607323
    title: Christer Ericson, Real-Time Collision Detection, Morgan Kaufmann, 2005
    locator: the chapter on convexity-based methods (the Minkowski difference, GJK and penetration depth)
---

The penetration depth of two overlapping solids is the length of the shortest translation that makes them disjoint, apart from contact on their boundaries. Its direction is the contact normal, and its length tells how far the solids overlap. A physics engine needs both to push the solids apart and to apply a [contact impulse](/collision-impulse/) along the right direction. For two convex solids the problem has a clean form: the depth is the distance from the origin to the boundary of their [Minkowski difference](/minkowski-sum/). For nonconvex solids, the shortest translation can be far from any local overlap, and the exact problem is much harder.

## In plain words

Two solid objects overlap, for example because a simulation step moved them too far. You want the smallest push, in one straight direction, that moves one object until the two only touch.

The length of that push says how deep they overlap. Its direction says which way the contact pushes. For two round balls, you push along the line between the centers. For boxes and other flat-sided shapes, the best push is along one of a few special directions. For shapes with holes and dents, the best push can go in a surprising direction, and it is hard to find.

## Definition

**Input.** Two compact solids $A, B \subset \mathbb{R}^d$, with $d = 2$ or $3$, whose interiors overlap. Usually they are convex polygons, convex polyhedra, or other convex shapes given by a support function. In the general version they are polygons or polyhedral meshes.

**Output.** The penetration depth
$$\operatorname{PD}(A, B) = \min \{ |v| : \operatorname{int}(A + v) \cap \operatorname{int}(B) = \emptyset \}$$
and a vector $v$ that attains it. The unit vector $v / |v|$ is the contact normal. Many uses also want a pair of witness points, one on each boundary, whose difference is $v$.

**Convex form.** $A + v$ and $B$ have overlapping interiors exactly when $-v$ is in the interior of $A - B = \{a - b\}$. So for convex solids $\operatorname{PD}(A, B)$ is the distance from the origin to the boundary of $A - B$, and the minimizing $v$ is the negative of the closest boundary point. If the solids are disjoint, the distance from the origin to $A - B$ is their distance. The two together give the signed distance.

**Cost model.** For exact methods, the [real RAM](/real-ram/) on polygons or polyhedra with $m$ and $n$ vertices. For support-function methods, the number of support queries and the size of the work polytope, with a tolerance on the depth.

## Variants

- **Translational depth.** The definition above. It is the common version in simulation.
- **Directional depth.** The shortest translation along a given direction, for example the direction of the relative velocity. It is a ray cast inside $A - B$.
- **Generalized depth.** The smallest rigid motion, with rotation, that separates the solids, under a metric on motions. It is more faithful for long objects and much harder to compute.
- **Signed distance.** The distance when the solids are apart and minus the depth when they overlap, as one continuous function of the placement.
- **Local depth.** For each contact region, a depth and a normal at that region alone. Engines and deformable models often use local depths, sampled from a [signed distance field](/signed-distance-function/), because the global minimum can jump from one region to another.
- **Penetration volume.** The volume of $A \cap B$ instead of a distance.

## Examples

| $A$ | $B$ | depth | normal |
|---|---|---|---|
| the disk with the center $(0, 0)$ and the radius 1 | the disk with the center $(1.5, 0)$ and the radius 1 | $1 + 1 - 1.5 = 0.5$ | along $(1, 0)$ |
| the square $[0, 2] \times [0, 2]$ | the square $[1.5, 3.5] \times [0.5, 2.5]$ | 0.5 | along $(1, 0)$ |
| the triangle $(0, 0), (4, 0), (0, 4)$ | the triangle $(1, 1), (3, 1), (1, 3)$ | $\sqrt{2} \approx 1.414$ | along $(1, 1) / \sqrt{2}$ |

For the squares, $B - A$ is the box $[-0.5, 3.5] \times [-1.5, 2.5]$, and the origin is $0.5$ from its left side, $1.5$ from its bottom side and farther from the others, so moving $B$ by $0.5$ to the right is the shortest push. The overlaps on the two axes are $0.5$ and $1.5$, and the depth is the smaller one. For the triangles, $B$ lies inside $A$ and touches the long side $x + y = 4$. On the direction $(1, 1)$, $A$ covers $x + y \in [0, 4]$ and $B$ covers $[2, 4]$, so $B$ must move until $x + y \ge 4$ on all of it, which is a push of $2 / \sqrt{2} = \sqrt{2}$. Along the two axes the push would be 3.

## Known algorithms

**Separating axes for polygons and boxes.** For two convex polygons, each edge of $A - B$ is parallel to an edge of $A$ or of $B$. The distance from the origin to the line of an edge with the outer normal $u$ is the overlap of the projections of $A$ and $B$ on $u$. So the smallest overlap over all edge normals of both polygons is the depth, and the [separating axis test](/separating-axis-theorem/) computes it in $O((m + n)^2)$ time, or in $O(m + n)$ with a merged walk over the normals in angular order. The same argument holds for any set of directions that contains all facet normals of $A - B$. For two boxes in 3D, the 15 axes of the box test give the exact depth.

**The Minkowski difference.** In the plane, the Minkowski sum of two convex polygons has at most $m + n$ edges and is computed in $O(m + n)$ time, so the depth takes $O(m + n)$ time. In 3D, $A - B$ is the convex hull of the $m n$ differences of vertices, and it can have $\Theta(m n)$ faces. A hull of these points gives the depth in $O(m n \log(m n))$ time. Dobkin, Hershberger, Kirkpatrick and Suri defined the intersection depth of two convex polyhedra and gave algorithms to compute it exactly.

**The expanding polytope algorithm.** The [expanding polytope algorithm](/expanding-polytope-algorithm/) starts from the simplex in which [GJK](/gjk-algorithm/) found the origin, and grows a polytope inside $A - B$ toward its nearest face, with support queries only. It works for curved convex shapes too, and it stops at a tolerance. It is the usual method in physics engines.

**Nonconvex solids.** Split each solid into convex pieces, by an exact or an [approximate convex decomposition](/approximate-convex-decomposition/). The depth of the union is not the largest depth of a pair of pieces, because a push that separates one pair of pieces can push another pair into contact. An exact method must find the closest point to the origin outside the union of all the pairwise Minkowski differences, which is costly. Practical methods use local depths at each contact region, or sample a [signed distance field](/signed-distance-function/).

## Bounds

For convex polygons, the depth takes $O(m + n)$ time, by the Minkowski sum. For convex polyhedra, the difference can have $\Theta(m n)$ faces, so a method that builds it needs $\Omega(m n)$ time in the worst case. Support-function methods such as EPA give no bound in terms of $m$ and $n$ that is smaller than the size of the difference, but on typical shapes they need few support queries. For nonconvex polyhedra the union of the pairwise differences can be much larger, and exact methods are rarely used in simulation.

## Reductions

- **To a nearest point on a boundary.** For convex solids, the depth is the distance from the origin to the boundary of $A - B$, from the inside.
- **To distance.** The signed distance joins the depth and the [distance of two convex solids](/convex-collision-detection/) in one function, and GJK with EPA computes both.
- **From overlap testing.** The depth is positive exactly when the interiors overlap, so a depth method also decides overlap.
- **To a configuration space query.** The placements $v$ of $A$ that overlap $B$ form the obstacle $B - A$ in the [configuration space](/configuration-space/) of translations, and the depth is the distance from the current placement to the boundary of this obstacle.

## Applications

- **Contact response.** A penalty method applies a force that grows with the depth along the normal. A projection method moves the solids apart by the depth. Impulse methods use the normal to build the [contact manifold](/contact-manifold/) and the [collision impulse](/collision-impulse/).
- **Recovery after a missed contact.** When a discrete step lets two solids overlap, the depth tells how to separate them before the next step.
- **Haptics.** A haptic device renders a force that depends on how deep the probe is in an object.
- **Motion planning and tolerance checks.** The depth measures how far a placement is from being free, which guides a planner out of collision and measures interference in an assembly.

## References
