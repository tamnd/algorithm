---
tag: 9KMKQ5
kind: problem
slug: art-gallery-problem
name: Art gallery problem
aliases:
- Minimum guard problem
- guarding polygons
- minimum guard problem
- museum problem
- point guard problem
- polygon guarding problem
- vertex guard problem
area: geometry/polygons
level: core
summary: Find the minimum number of guards placed in a polygon so that every point is visible to some guard.
prereqs: [simple-polygon, visibility-polygon, np-hard]
see_also: [art-gallery-theorem, minimum-guard-np-hardness, orthogonal-art-gallery-theorem, polygon-kernel, lee-preparata-algorithm, set-cover, watchman-route-problem, lee-visibility-polygon-algorithm]
sources:
  - book: "Joseph O'Rourke, Art Gallery Theorems and Algorithms, Oxford University Press, 1987"
    locator: Chapters 1 and 9 (the worst-case bounds, and the NP-hardness of the minimum guard problems)
  - paper: "D. T. Lee and Arthur K. Lin, Computational complexity of art gallery problems, IEEE Transactions on Information Theory 32(2), 1986, 276 to 282"
    locator: the reduction from 3-SAT for vertex, edge and point guards in simple polygons
  - paper: "Joseph O'Rourke and Kenneth J. Supowit, Some NP-hard polygon decomposition problems, IEEE Transactions on Information Theory 29(2), 1983, 181 to 190"
    locator: the minimum guard problem for polygons with holes
  - paper: "Mikkel Abrahamsen, Anna Adamaszek and Tillmann Miltzow, The art gallery problem is complete for the existential theory of the reals, Proceedings of the 50th ACM Symposium on Theory of Computing, 2018"
    locator: the main theorem (point guards in a simple polygon), and the remarks on irrational guards
  - paper: "Stephan Eidenbenz, Christoph Stamm and Peter Widmayer, Inapproximability results for guarding polygons and terrains, Algorithmica 31(1), 2001, 79 to 113"
    locator: APX-hardness for simple polygons and the logarithmic bound for polygons with holes
  - paper: "Subir Kumar Ghosh, Approximation algorithms for art gallery problems in polygons, Discrete Applied Mathematics 158(6), 2010, 718 to 722"
    locator: the O(log n) approximation for vertex and edge guards by set cover
---

The art gallery problem asks for the fewest guards that together see every point of a polygon. A guard sees a point when the segment between them stays inside the polygon. The worst case over all simple polygons with $n$ vertices is settled by the [art gallery theorem](/art-gallery-theorem/): $\lfloor n/3 \rfloor$ guards always suffice and are sometimes needed. Finding the minimum for a given polygon is much harder: it is [NP-hard](/minimum-guard-np-hardness/) even for simple polygons, hard to approximate, and for guards placed anywhere it is complete for the existential theory of the reals, so it is not even known to be in NP. One guard suffices exactly when the [kernel](/polygon-kernel/) is not empty, which takes $O(n)$ time to decide.

## In plain words

A museum is a room with straight walls and a complicated shape. You want to place as few cameras as possible so that every spot of the floor is seen by at least one camera. A camera sees in every direction but not through walls.

For a room with no bad corners, one camera anywhere is enough. A room with long side alcoves needs a camera looking into each alcove. In general, finding the smallest number of cameras for a given room is one of the hard problems: no fast method is known, and there is good reason to believe none exists.

## Definition

**Notation.** A polygon is a cyclic list of vertices $v_0, \ldots, v_{n-1}$ with edges $v_i v_{i+1}$, indices modulo $n$, and a point is $p = (x, y)$. For a [simple polygon](/simple-polygon/) $P$, $R$ is its closed region. A point $x \in R$ *sees* $y \in R$ if the closed segment $xy$ lies in $R$; touching the boundary is allowed. The set of points that $x$ sees is its [visibility polygon](/visibility-polygon/) $V(x)$.

**Input.** A simple polygon $P$ with $n$ vertices, with integer or rational coordinates, and for the decision version an integer $k$.

**Output.** A set $G$ of guards of minimum size with $\bigcup_{g \in G} V(g) = R$. In the decision version, whether some $G$ with $|G| \le k$ exists.

**Guard types.**

- *Point guards:* $G$ may be any finite subset of $R$.
- *Vertex guards:* $G$ must be a subset of the vertices.
- *Edge guards:* each guard is an edge, and it sees a point if some point of the edge sees it.

Write $\mathrm{opt}_p(P) \le \mathrm{opt}_v(P)$ for the point guard and vertex guard optima.

## Variants

- **Polygons with holes.** The region has polygonal holes. Fisk's bound no longer applies, and $\lfloor (n + h)/3 \rfloor$ point guards suffice for $h$ holes.
- **Orthogonal polygons.** All edges are horizontal or vertical. The worst case drops to $\lfloor n/4 \rfloor$; see the [orthogonal art gallery theorem](/orthogonal-art-gallery-theorem/). The minimum is still NP-hard.
- **One guard.** Deciding whether $\mathrm{opt}_p(P) = 1$ is deciding whether $P$ is [star-shaped](/star-shaped-polygon/), that is, whether its [kernel](/polygon-kernel/) is not empty.
- **Mobile guards.** A single guard who walks along a closed route and must see everything from some point of it: the [watchman route problem](/watchman-route-problem/), which is solvable in polynomial time in a simple polygon.
- **Guarding the boundary only.** The guards must see every point of the boundary, not every point of the interior. This can need fewer guards.
- **Outside and both sides.** The fortress problem guards the outside of a polygon, and the prison yard problem guards both sides.
- **Terrains.** Guards on a 1.5D terrain (an $x$-monotone chain) must see every point of it from above.

## Examples

**A convex polygon.** Every point sees every other point, so $\mathrm{opt}_p = \mathrm{opt}_v = 1$.

**An L-shape.** $(0,0), (4,0), (4,2), (2,2), (2,4), (0,4)$ is the union of the rectangles $[0,4] \times [0,2]$ and $[0,2] \times [0,4]$. The reflex vertex $(2,2)$ lies in both, and a rectangle is convex, so this one vertex sees everything: $\mathrm{opt}_v = 1$. The kernel is the square $[0,2] \times [0,2]$.

**A comb.** $(0,0), (5,0), (4,10), (3,1), (2,1), (1,10)$ has two teeth with tips $(1, 10)$ and $(4, 10)$. A point that sees a tip has $x$ within $1/9$ of the base of that tooth, so no point sees both tips, and $\mathrm{opt}_p = 2 = \lfloor 6/3 \rfloor$. The comb with $k$ teeth has $3k$ vertices and needs $k$ guards; this is the lower bound of the [art gallery theorem](/art-gallery-theorem/).

**The 3-coloring can be far from optimal.** For a convex polygon with $n = 30$ vertices, Fisk's method places $10$ guards, while one is enough. The theorem bounds the worst case, not the optimum.

## Known algorithms

| version | method | time | guarantee |
|---|---|---|---|
| any guards, worst-case bound | triangulate and 3-color (Fisk; Avis and Toussaint) | $O(n)$ after triangulation | at most $\lfloor n/3 \rfloor$ vertex guards |
| one point guard | kernel by [Lee and Preparata](/lee-preparata-algorithm/) | $O(n)$ | exact |
| vertex or edge guards | [set cover](/set-cover/) over the cells of the arrangement of visibility polygons (Ghosh) | polynomial | $O(\log n)$ times optimal |
| vertex guards in a simple polygon | King and Kirkpatrick | polynomial | $O(\log \log \mathrm{opt})$ times optimal |
| vertex guards | integer programming over the arrangement cells | exponential in the worst case | exact, practical for thousands of vertices |
| point guards | decision procedures for the existential theory of the reals | exponential | exact |

For vertex guards, the problem is a finite [set cover](/set-cover/) instance. Compute the visibility polygon of each vertex in $O(n)$ time each (for example by [Lee's algorithm](/lee-visibility-polygon-algorithm/)). Their edges cut $R$ into $O(n^4)$ cells, and a vertex sees either all or none of each cell. Choosing vertices to cover all cells is set cover, which the greedy algorithm approximates within $O(\log n)$. Point guards are harder because the candidate positions are not finite: the optimal guards can be forced to irrational coordinates. Practical exact methods iterate between a finite candidate set and a finite set of witness points, with integer programming at each round.

## Bounds

- **Worst case.** $\max_P \mathrm{opt}_p(P) = \max_P \mathrm{opt}_v(P) = \lfloor n/3 \rfloor$ over simple polygons with $n$ vertices, by the [art gallery theorem](/art-gallery-theorem/).
- **NP-hardness.** Lee and Lin (1986) showed that the decision version is NP-hard for vertex guards, edge guards and point guards in simple polygons, by a reduction from 3-SAT. O'Rourke and Supowit (1983) had shown it for polygons with holes. See [minimum guard NP-hardness](/minimum-guard-np-hardness/).
- **Membership.** For vertex guards the problem is in NP: a guard set can be checked by computing the visibility polygons and testing that their union is $R$, in polynomial time. For point guards, Abrahamsen, Adamaszek and Miltzow (2018) proved that it is complete for $\exists\mathbb{R}$, the existential theory of the reals, so it is in NP only if $\mathrm{NP} = \exists\mathbb{R}$. The same authors showed that some polygons with integer vertices need guards at irrational points to reach the optimum.
- **Approximation.** The problem is APX-hard for simple polygons, so it has no polynomial-time approximation scheme unless $\mathrm{P} = \mathrm{NP}$. For polygons with holes it cannot be approximated within a factor $c \ln n$ for some constant $c > 0$ under standard assumptions (Eidenbenz, Stamm and Widmayer, 2001).
- **Arithmetic.** With integer input, visibility polygons of vertices have vertices with rational coordinates whose numerators and denominators have polynomially many bits, so the vertex guard algorithms run in exact arithmetic.

## Reductions

- **From 3-SAT.** Lee and Lin encode variables as pockets of the polygon where a guard must choose one of two positions, and clauses as pockets that are seen only if one of the chosen literals is true.
- **To set cover.** Vertex and edge guards reduce to set cover over the finite arrangement of visibility polygons, as above. Ghosh's approximation and the integer programming methods use this.
- **One guard to linear programming.** A point $x$ sees all of $R$ if and only if it lies to the left of every edge of a counterclockwise polygon, so $\mathrm{opt}_p = 1$ is the feasibility of $n$ linear inequalities in two variables. Lee and Preparata solve it in $O(n)$ time using the order of the edges; [Megiddo's algorithm](/megiddo-fixed-dimension-lp/) for linear programming in fixed dimension also takes $O(n)$ time.
- **To the existential theory of the reals.** Whether $k$ point guards suffice is a sentence with $2k$ real variables over polynomial constraints, which gives an exact, if slow, algorithm.

## Applications

- **Surveillance and sensor placement.** Placing cameras, motion sensors or lights in a building; the visibility model is a first approximation that ignores range and angle limits.
- **Wireless networks.** Placing antennas in an indoor environment where walls block the signal.
- **Robotics.** Choosing viewpoints for a robot that scans a building, and planning a [watchman route](/watchman-route-problem/) that sees everything.
- **Terrain guarding.** Placing watchtowers or relay stations on a terrain profile.
- **Computer graphics.** Choosing a small set of viewpoints that together see a whole scene, for example for image-based rendering or for precomputing visibility.

## References
