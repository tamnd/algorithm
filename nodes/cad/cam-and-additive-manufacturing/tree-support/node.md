---
tag: YRE332
kind: algorithm
slug: tree-support
name: Tree support generation
aliases:
- branching supports
area: cad/cam-and-additive-manufacturing
level: advanced
summary: Builds supports as trees that start at the overhang points and merge downward within the critical angle, as in Vanek and coauthors, which saves material.
solves: [support-structure-generation]
model: real-ram
complexity:
  vars: {n: number of points that need support}
  time: {worst: "O(n^2 log n)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 2014
  people: [Juraj Vanek, Jorge A. Garcia Galicia, Bedrich Benes]
  note: Vanek, Garcia Galicia and Benes presented Clever Support at SGP 2014, with a top-down sweep that merges support cones into trees and lands branches on the plate or on the part.
prereqs: [support-structure-generation, euclidean-steiner-tree-problem]
see_also: [build-orientation, euclidean-minimum-spanning-tree, steiner-tree-problem, sweep-line-technique, slicing-for-additive-manufacturing, binary-heap]
sources:
  - paper: doi:10.1111/cgf.12437
    title: Juraj Vanek, Jorge A. Garcia Galicia and Bedrich Benes, Clever Support, Efficient Support Structure Generation for Digital Fabrication, Computer Graphics Forum 33(5), 2014, 117 to 125 (Proceedings of SGP 2014)
    locator: the detection of the points that need support, the sweep that merges cones, and the measurements of material and print time
  - book: isbn:978-3-030-56126-0
    title: Ian Gibson, David Rosen, Brent Stucker and Mahyar Khorasani, Additive Manufacturing Technologies, 3rd edition, Springer, 2021
    locator: the chapters on material extrusion and on design for additive manufacturing (overhangs and supports)
---

Tree support generation builds the supports of a 3D print as trees. Each point of the part that needs support is a leaf. Branches go down from the leaves, merge where they meet, and end in a few trunks on the build plate. Each branch is a straight strut that is no more tilted than the printer can build, so the struts themselves need no support. Compared with a vertical pillar under each point, a tree uses much less material. The method was made popular by the Clever Support paper of Vanek, Garcia Galicia and Benes (2014). Its main step is a sweep from the top down: the two points whose support cones meet highest are merged first, at the point where their cones meet. This page gives that greedy merge with exact arithmetic, for supports that stand on the plate. It solves one form of the [support structure generation](/support-structure-generation/) problem heuristically, with no claim of optimal length.

## In plain words

Some parts of a print hang over empty space, and the printer cannot put material on air. So each such point needs something below it. The simple answer is a straight pillar from the point to the plate. That works, but it uses a lot of material if there are many points.

A printer can build a strut that leans a little, up to a limit. So the support of a point can be any strut inside an upside-down cone below it. If the cones of two points meet, both points can share one strut below the meeting point, like two branches of a tree. Start at the top and always join the two branches that can meet highest, as long as this saves material. At the end, every branch that is still alone goes straight down to the plate.

## The problem

The input is a set of points $p_1, \dots, p_n$ with $z > 0$ that need support, and a cone slope $k > 0$. A strut from $a$ down to $b$ is allowed if $a_z > b_z$ and its horizontal length is at most $k\,(a_z - b_z)$. The slope $k = \tan\beta$ comes from the largest angle $\beta$ from the vertical that the printer can build without support. For material extrusion a common rule of thumb is $\beta = 45^\circ$, so $k = 1$. It is a rule of thumb, not a law, and it depends on the material, the speed and the cooling.

The output is a set of nodes, which includes the input points, and a set of allowed struts. Each node has at most one strut below it, and the path of struts down from each input point ends on the plate $z = 0$. The cost is the total length of the struts. Here the struts may cross the part: this version does not test them against the mesh. Real supports must avoid the part or land on it, see the variants below.

**Which points need support.** The points come from the mesh of the part. A facet with outward normal $n$ faces down if $n_z < 0$. It is tilted from the horizontal by the angle $\varphi$ with $\cos\varphi = -n_z / \|n\|$, and it needs support if $\varphi < 90^\circ - \beta$, that is, if
$$n_z < 0 \quad\text{and}\quad n_z^2 > \sin^2\!\beta\; \|n\|^2.$$
For $\beta = 45^\circ$ this is $2 n_z^2 > \|n\|^2$, an exact test on integers. A facet at exactly $45^\circ$ passes as self-supporting. The code samples each overhang facet on a grid of barycentric points, and it adds every vertex that is strictly lower than all its neighbours, because such a point starts a new island in the layer where it appears. Points on the plate need nothing.

## The algorithm

MERGE$(p, q)$, for $p_z \ge q_z$, finds the highest point $m$ that lies in both cones. Let $D$ be the horizontal distance of $p$ and $q$. If $D \le k\,(p_z - q_z)$, then $q$ lies in the cone of $p$, and the highest common point is $q$ itself. Otherwise the cones meet first on the vertical plane through $p$ and $q$, at horizontal distance $s = (k(p_z - q_z) + D)/2$ from $p$ and at height $(p_z + q_z - D/k)/2$.

```pseudo id=main
TREE-SUPPORT(P, k)                    ▷ points P that need support, cone slope k
L1  A ← P; E ← empty                    ▷ active points, struts
L2  H ← max-heap of MERGE(p, q) for the pairs of A that save length
L3  while H is not empty do
L4      (m, p, q) ← extract the event with the highest m_z
L5      if p ∉ A or q ∉ A then continue           ▷ stale event
L6      remove p and q from A
L7      if m = q then add strut (p, q) to E        ▷ q lies in the cone of p
L8      else add struts (p, m) and (q, m) to E      ▷ reuse m if it is already in A
L9      add m to A
L10     for each r ∈ A with r ≠ m do
L11         if MERGE(m, r) saves length then insert it into H
L12 for each p ∈ A do add strut (p, (p_x, p_y, 0)) to E   ▷ trunks to the plate
L13 return E

MERGE(p, q)                           ▷ p_z ≥ q_z
L14 D ← horizontal distance of p and q
L15 if D ≤ k (p_z − q_z) then return (q, |p − q| < p_z)
L16 s ← (k (p_z − q_z) + D) / 2
L17 m_xy ← p_xy + (q_xy − p_xy) · s / D, rounded to a fine grid
L18 m_z ← min(p_z − |m − p|_xy / k, q_z − |m − q|_xy / k)
L19 saves ← m_z > 0 and |p − m| + |q − m| + m_z < p_z + q_z
L20 return (m, saves)
```

The test "saves length" compares the struts of a merge with the cheapest way to finish both points, two trunks of lengths $p_z$ and $q_z$. In the case of line L15, $p$ goes to $q$, and $q$ still needs its own support, so the test is $|p - q| < p_z$. The heap holds events for pairs, and line L5 skips events whose points were already merged. Each merge happens at the height of its event, and a new point $m$ can only merge lower than $m_z$, because any common point lies in the cone of $m$. So the events come out in decreasing height, which is the sweep of a horizontal plane from the top down.

**Exact arithmetic.** The horizontal distances are square roots, so they are not rational. Line L17 rounds $m$ to a grid, and line L18 then sets $m_z$ with an upper bound of each square root (from math.isqrt) in place of the root. This lowers $m$ a little, and it keeps $m$ exactly inside both cones, so every strut is allowed. Line L19 compares a sum of two square roots with a rational $C = p_z + q_z - m_z$ exactly: $\sqrt{A} + \sqrt{B} < C$ holds if and only if $C > 0$, $C^2 - A - B > 0$ and $4AB < (C^2 - A - B)^2$. A test in floating point can accept a merge that makes the tree longer when the two sides are almost equal, or reject a strut that is exactly at the limit angle.

## Example

Take $k = 1$ and the points $a = (0, 0, 6)$, $b = (4, 0, 6)$, $c = (3, 0, 3)$ and $d = (12, 0, 4)$. Vertical pillars would have length $6 + 6 + 3 + 4 = 19$.

| step | event | value |
|---|---|---|
| L2 | $(a, b)$ | $D = 4 > 0$, $s = 2$, $m = (2, 0, 4)$; $2\sqrt8 + 4 \approx 9.66 < 12$, saves |
| L2 | $(b, c)$ and $(a, c)$ | $D = 1 \le 3$ and $D = 3 \le 3$: $c$ is in both cones, events at height 3 |
| L2 | $(b, d)$ | $D = 8$, $s = 5$, $m = (9, 0, 1)$; $\sqrt{50} + \sqrt{18} + 1 \approx 12.31 > 10$, not inserted |
| L4 to L9 | $(a, b)$ at height 4 | struts $a \to m$ and $b \to m$, $A = \{c, d, m\}$ with $m = (2, 0, 4)$ |
| L10, L11 | $(m, c)$ | $D = 1 \le 1$: $c$ is in the cone of $m$, and $\sqrt2 < 4$, so it saves |
| L4 to L9 | $(m, c)$ at height 3 | strut $m \to c$, $A = \{c, d\}$ |
| L4, L5 | $(b, c)$ and $(a, c)$ | stale, skipped |
| L11 | $(c, d)$ | $D = 9$, $m_z = (4 + 3 - 9)/2 < 0$, not inserted |
| L12 | trunks | $c \to (3, 0, 0)$ and $d \to (12, 0, 0)$ |

The tree is $a \to (2, 0, 4) \leftarrow b$, then $(2, 0, 4) \to c \to (3, 0, 0)$, and the separate trunk $d \to (12, 0, 0)$. Its length is $2\sqrt8 + \sqrt2 + 3 + 4 = 5\sqrt2 + 7 \approx 14.07$, against 19 for pillars. Every strut leans at most $45^\circ$: for example $a \to m$ goes 2 across and 2 down.

On 200 random integer points in $[0, 60]^2 \times [1, 30]$ (seed 1, $k = 1$), the code of this page builds 333 struts of total length about 1206, against 3076 for pillars, in about 1.5 s of Python. This is one toy measurement and says nothing about real parts.

## Correctness

Every strut is allowed: the struts of line L7 join $p$ to a point $q$ inside its cone with $q_z < p_z$ (otherwise $D \le 0$ and $p = q$), the struts of line L8 go to a point that line L18 places inside both cones and strictly below both, and the trunks of line L12 are vertical. Each node gets exactly one strut below it, when it leaves the active set, and every node in the active set at the end gets a trunk. So the path down from each input point is unique and ends on the plate. The total length never exceeds the length of vertical pillars, because every merge is accepted only when it lowers the sum of the strut length built so far and the heights of the active points. The full proof is below.

The method is a heuristic. It does not find the shortest tree. The shortest tree is a [Steiner tree](/euclidean-steiner-tree-problem/) with a slope rule and with free points on the plate, and the Euclidean Steiner tree problem is NP-hard already in the plane.

## Complexity

Line L2 computes $\binom{n}{2}$ events and puts them in a [binary heap](/binary-heap/) in $O(n^2 \log n)$ time. There are at most $n - 1$ merges, because each one makes the active set smaller by one, and each merge adds at most $n$ events. So the heap receives $O(n^2)$ events, and each is extracted at most once, in $O(\log n)$ time. The total is $O(n^2 \log n)$ time and $O(n^2)$ space for the heap. The exact arithmetic adds a factor that depends on the size of the numbers, which grow with the grid of line L17.

A faster version keeps only near pairs, for example the pairs within a distance from a grid or a [k-d tree](/kd-tree/), because two points that are far apart compared with their heights cannot merge above the plate.

## Properties

- **Every point is supported.** Each input point has a path of allowed struts to the plate.
- **A forest.** Each node has one strut below it, so the supports form trees with their roots on the plate.
- **Never longer than pillars.** The total length is at most $\sum_i (p_i)_z$, and strictly less if one merge happens.
- **Top-down order.** Merges happen in decreasing height.
- **Exact decisions.** The cone test, the saving test and the overhang test are exact on integer or rational input.
- **Heuristic.** The length is not optimal, and the result depends on the order of merges.

## Variants and improvements

- **Clever Support.** Vanek, Garcia Galicia and Benes (2014) first choose the build orientation for a small overhang area, find the points that need support from the facets and from a scan of the layers, and then run the sweep. At each step they compare the meeting point of two cones with the point where a cone first hits the part, and they take the higher one. So a branch can also end on the part. They report that, on their test models and a MakerBot Replicator 2, the trees saved on average about 40% of the support material and about 29% of the print time compared with the supports of the printer software. These are measured numbers on their models.
- **Avoiding the part.** A strut that would pass through the part must be bent or rerouted. Common tools test each strut against the mesh, or grow branches in a distance field of the part.
- **Branch thickness.** Real branches get thicker toward the root, because they carry more weight. This changes the cost from length to volume.
- **Other support shapes.** Pillars, lines and grids under the overhang, and scaffolds with horizontal bridges, are other answers to the same problem, see [support structure generation](/support-structure-generation/).

## When to use it

Use tree supports when a part has many small overhangs over open space, such as figures, organic shapes or parts with islands, and when support material and removal time matter. For large flat overhangs, a dense support under the whole area gives a better bottom surface, because a tree touches the part only at points. For parts that are mostly flat with small overhangs near the plate, simple pillars are often enough.

## Pitfalls

- **Struts through the part.** A support that ignores the mesh can pass through the part, which is not printable. This page's code has that limit on purpose.
- **Too few sample points.** A facet sampled only at its vertices can sag between them. The sampling step must match the largest span that the material can bridge.
- **Floating point angle tests.** A facet at exactly the critical angle is common in designed parts. Compare squares of exact numbers.
- **The angle is not a constant of nature.** The self-supporting angle depends on the printer, the material and the speed. Make it a parameter.
- **Local minima.** A vertex below all its neighbours needs support even if no facet near it is an overhang.
- **Thin trunks.** A long thin trunk can bend or break during printing. Real tools set a minimum diameter and add a base.

## Implementations

## History

Early support generators for stereolithography and material extrusion placed vertical walls, lines or grids under every overhang. Vanek, Garcia Galicia and Benes presented Clever Support at the Symposium on Geometry Processing in 2014, published in Computer Graphics Forum. It showed that a sweep that merges support cones into trees saves much material and time on extrusion printers. Tree supports later became an option of common slicers. The trees of these tools differ from the paper in how they avoid the part and how they choose the merge points.

## References
