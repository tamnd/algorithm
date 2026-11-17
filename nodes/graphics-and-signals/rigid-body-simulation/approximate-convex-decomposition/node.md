---
tag: 1SYCDG
kind: algorithm
slug: approximate-convex-decomposition
name: Approximate convex decomposition
aliases:
- ACD
area: graphics-and-signals/rigid-body-simulation
level: advanced
summary: Split a nonconvex mesh into a few nearly convex parts whose concavity is below a tolerance, so that convex collision tests apply to each part.
solves: [convex-decomposition]
model: real-ram
complexity:
  vars: {n: the number of vertices of the polygon, r: the number of reflex vertices}
  time: {worst: O((r + 1) (n + r) log(n + r)), cuts: O(r)}
  space: {extra: O(n + r)}
properties: {deterministic: true, online: false, recursive: false, exact: true}
history:
  year: 2004
  people: [Jyh-Ming Lien, Nancy M. Amato]
  note: Lien and Amato defined the concavity of a polygon by the pockets of its convex hull and cut only the notches that are too concave, which gives far fewer pieces than an exact convex decomposition.
prereqs: [convex-hull, convex-decomposition, simple-polygon, point-to-segment-distance]
see_also: [hertel-mehlhorn, convex-collision-detection, gjk-algorithm, collision-detection, bounding-volume-hierarchy, minkowski-sum, hausdorff-distance, medial-axis]
sources:
  - paper: doi:10.1016/j.comgeo.2005.10.005
    title: Jyh-Ming Lien and Nancy M. Amato, Approximate convex decomposition of polygons, Computational Geometry 35(1-2), 2006, 100 to 123
    locator: the pockets and bridges of the convex hull, the concavity measures, and the resolution of the most concave notch
  - paper: doi:10.1145/1236246.1236265
    title: Jyh-Ming Lien and Nancy M. Amato, Approximate convex decomposition of polyhedra, Proceedings of the 2007 ACM Symposium on Solid and Physical Modeling, 121 to 131
    locator: the extension of the method to polyhedra
  - paper: doi:10.1137/0213031
    title: Bernard Chazelle, Convex partitions of polyhedra, a lower bound and worst-case optimal algorithm, SIAM Journal on Computing 13(3), 1984, 488 to 507
    locator: the quadratic lower bound on the number of convex pieces of a polyhedron
  - paper: "Khaled Mamou and Faouzi Ghorbel, A simple and efficient approach for 3D mesh approximate convex decomposition, IEEE International Conference on Image Processing (ICIP 2009), 3501 to 3504"
    locator: the hierarchical approximate convex decomposition of a mesh by the decimation of its dual graph
  - paper: doi:10.1145/3528223.3530103
    title: Xinyue Wei, Minghua Liu, Zhan Ling and Hao Su, Approximate convex decomposition for 3D meshes with collision-aware concavity and tree search, ACM Transactions on Graphics 41(4), 2022, article 42
    locator: the collision-aware concavity, the cuts by planes, and the tree search over the cuts
---

Approximate convex decomposition splits a nonconvex shape into a small number of pieces that are each nearly convex. The concavity of a piece measures how far its boundary goes into its convex hull. The method cuts only the parts that are more concave than a tolerance $\tau$, and leaves small dents in place. Then the convex hulls of the pieces replace the shape in [collision detection](/collision-detection/), so that fast tests for convex shapes, such as [GJK](/gjk-algorithm/), apply to each piece. An exact [convex decomposition](/convex-decomposition/) is the case $\tau = 0$. It can need many more pieces, and in 3D the number can grow with the square of the number of reflex edges. This page uses a 2D polygon, where the ideas are the same as for meshes and every step can be checked.

## In plain words

A collision test is fast for shapes with no dents, such as a box or a ball. Real objects, such as a chair or a cup, have dents and holes.

You can cut the object into pieces with no dents at all, but you can need very many pieces. Most of the dents are small, and a small dent hardly changes where two objects touch.

So measure each dent by how deep it goes. Cut only at the deepest dent. Check the two new pieces again, and cut them only if they still have a dent deeper than your limit. A larger limit gives fewer pieces that are a little less exact.

## The problem

The input is a simple polygon $P$ with $n$ vertices and a tolerance $\tau \ge 0$. The output is a set of simple polygons with disjoint interiors whose union is $P$, each with a concavity of at most $\tau$, and with few pieces. Let $H$ be the convex hull of a polygon $X$. The parts of $H$ outside $X$ are the pockets, and the edge of $H$ that closes a pocket is its bridge. The concavity of a vertex of $X$ is $0$ on the hull, and otherwise its distance to the bridge of its pocket. The concavity of $X$ is the largest concavity of its vertices. This is the straight-line concavity of Lien and Amato. Their paper also uses a measure by shortest paths inside the pocket, and newer 3D methods use other measures. The measure and $\tau$ are choices, and the answer depends on them.

## The algorithm

```pseudo id=main
ACD(P, τ)
L1  Q ← [P]
L2  while Q is not empty
L3      take a piece X from Q
L4      compute the convex hull of X and the concavity of each vertex of X
L5      if the concavity of X is at most τ then add X to the output and continue
L6      v ← the reflex vertex of X with the largest concavity
L7      extend each edge at v beyond v to its first hit q on the boundary of X, and keep the shorter cut vq
L8      split X along vq into two pieces, and add both to Q
L9  return the output
```

Line L4 uses Andrew's monotone chain for the hull. The hull vertices appear in the order of $X$, so the vertices between two consecutive hull vertices form a pocket, with the bridge between those two hull vertices. Line L7 is a choice of this page. An edge extension starts into the interior at a reflex vertex, so the cut is always valid, and each piece gets an angle of at most $\pi$ at $v$. Lien and Amato resolve a notch by a cut that they choose with a score. The code uses exact rational arithmetic, so the hit points, the areas and the comparisons with $\tau$ have no rounding. It compares squared distances with $\tau^2$.

## Example

Take a rectangle from $(0, 0)$ to $(8, 6)$ with two dents: the polygon $(0,0), (3,0), (4,1), (5,0), (8,0), (8,6), (6,6), (5,2), (3,6), (0,6)$, with the area 41. Its hull is the rectangle. There are two pockets. The reflex vertex $(4, 1)$ has the bridge from $(0, 0)$ to $(8, 0)$ and the concavity 1. The reflex vertex $(5, 2)$ has the bridge from $(8, 6)$ to $(0, 6)$ and the concavity 4. The other vertices have the concavity 0.

| $\tau$ | pieces | what happens |
|---|---|---|
| 4 or more | 1 | no cut |
| from about 0.728 up to 4 | 2 | one cut at $(5, 2)$ |
| less than about 0.728 | 3 | a second cut at $(4, 1)$, and all pieces are convex |

With $\tau = 1$, the loop cuts at $(5, 2)$. The extension of the edge from $(6, 6)$ to $(5, 2)$ hits the edge from $(4, 1)$ to $(5, 0)$ at $(23/5, 2/5)$, with the length $1.649$. The extension of the edge from $(3, 6)$ to $(5, 2)$ hits $(6, 0)$, with the length $2.236$. Line L7 keeps the first cut. The right piece $(23/5, 2/5), (5, 0), (8, 0), (8, 6), (6, 6)$ is convex, with the area $82/5$. The left piece, with the area $123/5$, still holds the dent at $(4, 1)$. Its bridge is now the segment from $(3, 0)$ to $(23/5, 2/5)$, because the cut took $(5, 0)$ out of this piece, so the concavity of the dent is now $3/\sqrt{17} \approx 0.728$. This is at most 1, so the loop stops with two pieces. With $\tau = 0.5$, the loop also cuts at $(4, 1)$, along the extension of the edge from $(3, 0)$, which hits the vertex $(5, 2)$. This gives a triangle with the area $3/5$ and a convex pentagon with the area 24. The areas always add up to 41.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). A reflex vertex is never on the hull, so it has a positive concavity, and a polygon with the concavity 0 is convex. At a reflex vertex, both edge extensions start into the interior, so the cut to the first boundary hit is a chord, and it splits the piece into two simple polygons with the same union. The cut gives the vertex an angle of at most $\pi$ in both pieces and makes no new reflex vertex. So each cut lowers the total number of reflex vertices by at least one. The loop stops after at most $r$ cuts with at most $r + 1$ pieces, and it outputs a piece only when its concavity is at most $\tau$. The proof does not depend on which reflex vertex or which extension the code picks.

## Complexity

There are at most $r$ cuts, so the loop runs at most $2r + 1$ times. A cut adds at most one vertex, so a piece has at most $n + r$ vertices. Each round costs $O(m \log m)$ for the hull of a piece with $m$ vertices and $O(m)$ for the concavities and the cut. The total is $O((r + 1)(n + r)\log(n + r))$ in the real RAM. The code uses Fractions, and the size of the numbers grows with the depth of the cuts, which this bound does not count. In practice the cost is in the number of pieces, because every collision query then runs on each pair of pieces.

## Properties

- **A valid partition for any choice.** Any reflex vertex and any edge extension give a correct partition. The rule changes only the number and the shape of the pieces.
- **At most r + 1 pieces.** For $\tau = 0$ the output is a convex partition with at most $r + 1$ pieces. [Hertel and Mehlhorn](/hertel-mehlhorn/) give a partition within four times the optimum, and the optimum can be found in polynomial time for a polygon without holes.
- **Fewer pieces for a larger tolerance.** On 100 random star-shaped polygons with 16 integer vertices and a mean of 6.36 reflex vertices, the mean number of pieces was 7.33 for $\tau = 0$, 6.4 for $\tau = 1$, 4.92 for $\tau = 4$ and 3.58 for $\tau = 8$. The mean concavity of the input was 15.2. These are measured values for this cut rule. For a greedy rule like this one, a larger $\tau$ does not give fewer pieces for every input.
- **Not optimal.** The method is greedy and does not minimize the number of pieces for a given $\tau$.

## Variants and improvements

- **Shortest-path concavity.** Lien and Amato also measure the concavity by the shortest path from the vertex to the bridge inside the pocket. This is larger for pockets that curl, and costs more to compute.
- **Polyhedra.** Lien and Amato (2007) extend the concavity measure and the cuts to polyhedra.
- **Hierarchical clustering.** Mamou and Ghorbel (2009) build the pieces of a mesh from the bottom up. They merge adjacent parts in the dual graph of the triangles while the merged part stays nearly convex.
- **Collision-aware concavity.** Wei, Liu, Ling and Su (2022) measure the concavity by the distance between the shape and its hull from both the boundary and the interior. They cut the mesh with planes and choose the planes by a tree search, not by one greedy step.
- **Use the hulls.** A physics engine stores the convex hull of each piece, not the piece itself. The hulls fill the dents that the method left, and with this measure each pocket vertex is at most $\tau$ from its bridge.

## When to use it

Use approximate convex decomposition to make collision shapes for a nonconvex rigid body before the simulation starts. The convex hulls of the pieces go into a [bounding volume hierarchy](/bounding-volume-hierarchy/), and each pair of pieces that overlap goes to a [convex collision test](/convex-collision-detection/). Choose $\tau$ from the size of the smallest gap or dent that must stay visible in contacts. Use an exact convex decomposition when the pieces must match the shape exactly, for example for a [Minkowski sum](/minkowski-sum/).

## Pitfalls

- **Units.** The concavity is a length. A fixed $\tau$ gives very different results on a small object and on a large one, so scale $\tau$ to the size of the object.
- **Too many pieces for small $\tau$.** Each piece costs time in every collision query. Very small values of $\tau$ give a large number of pieces with little gain.
- **The hulls can overlap other parts.** The hull of a piece covers its dents, so a thin gap between two parts of the object can close. A slot or a handle can become solid.
- **Rounding.** In floating point the hit point of a cut can fall just outside the polygon or make a tiny sliver piece. Exact arithmetic, or snapping the hit to a nearby vertex, avoids this.
- **Simple input.** The 2D method needs a simple polygon. A mesh for the 3D methods must be closed and without self-intersections, or the concavity is not well defined.

## Implementations

## History

Exact convex decomposition was studied first. Chazelle (1984) showed that some polyhedra with $r$ reflex edges need $\Omega(r^2)$ convex pieces, so an exact decomposition of a detailed mesh can be very large. Lien and Amato proposed approximate convex decomposition for polygons in 2004, with the journal version in 2006, and extended it to polyhedra in 2007. Mamou and Ghorbel (2009) gave a hierarchical method for meshes, and Wei, Liu, Ling and Su (2022) gave a method with a collision-aware concavity and a tree search over the cuts.

## References
