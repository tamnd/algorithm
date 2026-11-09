---
tag: C2Q4A8
kind: problem
slug: flip-distance
name: Flip distance
aliases:
- Triangulation flip distance
- rotation distance
- edge flip distance
area: geometry/triangulations
level: research
summary: Minimum number of edge flips needed to transform one triangulation into another; NP-hard.
model: real-ram
prereqs: [edge-flip, flip-graph, triangulation-of-point-set]
see_also: [flip-graph-diameter-theorem, tree-rotation, binary-tree, lawson-flip-algorithm, polygon-triangulation, catalan-triangulation-theorem, number-of-triangulations, delaunay-triangulation]
sources:
  - paper: "Anna Lubiw and Vinayak Pathak, Flip distance between two triangulations of a point set is NP-complete, Computational Geometry 49, 17 to 23 (2015)"
    locator: NP-completeness for point sets by a reduction from vertex cover (source problem to be checked)
  - paper: "Alexander Pilz, Flip distance between triangulations of a planar point set is APX-hard, Computational Geometry 47(5), 589 to 604 (2014)"
    locator: APX-hardness for point sets
  - paper: "Oswin Aichholzer, Wolfgang Mulzer and Alexander Pilz, Flip distance between triangulations of a simple polygon is NP-complete, Discrete and Computational Geometry 54(2), 368 to 389 (2015)"
    locator: NP-completeness for simple polygons
  - paper: "Daniel D. Sleator, Robert E. Tarjan and William P. Thurston, Rotation distance, triangulations, and hyperbolic geometry, Journal of the American Mathematical Society 1(3), 647 to 681 (1988)"
    locator: common diagonals are never flipped in a shortest sequence for convex polygons, and the diameter 2n - 10
  - paper: "Sean Cleary and Katherine St. John, Rotation distance is fixed-parameter tractable, Information Processing Letters 109(16), 918 to 922 (2009)"
    locator: a kernel of size 5k for convex polygons
  - paper: "Iyad Kanj, Eric Sedgwick and Ge Xia, Computing the flip distance between triangulations, Discrete and Computational Geometry 58(2), 313 to 344 (2017)"
    locator: a fixed-parameter algorithm for point sets
  - paper: "Ferran Hurtado, Marc Noy and Jorge Urrutia, Flipping edges in triangulations, Discrete and Computational Geometry 22(3), 333 to 346 (1999)"
    locator: Θ(n^2) flips are sometimes needed for point sets and polygons
---

The flip distance between two triangulations of the same point set or polygon is the smallest number of [edge flips](/edge-flip/) that turns one into the other, that is, their distance in the [flip graph](/flip-graph/). For points in convex position it equals the rotation distance between two binary trees, and its complexity is a famous open problem: no polynomial algorithm and no NP-hardness proof are known. For general point sets the problem is NP-complete (Lubiw and Pathak; Pilz, who proved APX-hardness), and for simple polygons as well (Aichholzer, Mulzer and Pilz). It is fixed-parameter tractable in the distance, and easy to approximate within a factor 2 for convex polygons.

## In plain words

You have two ways to cut the same set of dots into triangles. One move erases a shared side of two triangles that form a convex four-sided piece and draws the other diagonal. How few moves turn the first cutting into the second?

For dots around a circle, nobody knows a fast method, and nobody has proved that there is none. For dots placed anywhere, the question is as hard as the hardest search problems. Counting the lines that are in one cutting but not the other gives a quick estimate that is off by at most a factor of two around a circle.

## Definition

**Input.** Two triangulations $T_1$ and $T_2$ of the same finite point set $S$ in the plane, or of the same simple polygon, and in the decision version an integer $k$.

**Output.** The flip distance $d(T_1, T_2)$, the length of a shortest sequence $T_1 = U_0, U_1, \ldots, U_d = T_2$ in which each $U_{i+1}$ is obtained from $U_i$ by one flip. The decision version asks whether $d(T_1, T_2) \le k$. The distance is finite because the flip graph is connected.

**Basic bounds.** Each flip removes one edge and adds one, so $d(T_1, T_2) \ge |T_1 \setminus T_2|$, the number of edges of $T_1$ that are not in $T_2$. For a convex polygon, flipping every diagonal not at a vertex $v$ into one at $v$ reaches the fan at $v$ in $n - 3 - \deg(v)$ flips, so $d(T_1, T_2) \le 2n - 6 - \deg_{T_1}(v) - \deg_{T_2}(v)$, where the degrees count diagonals.

## Variants

- **Convex polygons, rotation distance.** For a convex $(n + 2)$-gon, triangulations correspond to binary trees with $n$ internal nodes and flips to [rotations](/tree-rotation/). The distance is the rotation distance of the trees, which arises in the analysis of self-adjusting search trees.
- **Point sets in general position.** NP-complete and APX-hard.
- **Simple polygons.** Only diagonals of the polygon are allowed. NP-complete.
- **Simultaneous flips.** Flip a set of edges at once, as long as no two of them bound a common triangle; the distance becomes $O(\log n)$ for convex polygons and $O(n)$ for point sets (Galtier, Hurtado, Noy, Pérennes and Urrutia; to be checked).
- **Other graphs.** Flips in combinatorial triangulations of the sphere, in triangulations of surfaces, and in pseudotriangulations each give a flip distance of their own.

## Examples

- **Convex hexagon, distance 2.** The fan at $v_0$ (diagonals $v_0 v_2$, $v_0 v_3$, $v_0 v_4$) and the fan at $v_3$ (diagonals $v_3 v_1$, $v_3 v_5$, $v_3 v_0$) share $v_0 v_3$, which cuts the hexagon into two quadrilaterals. One flip in each turns one fan into the other, and since two edges differ, $d = 2$.
- **Convex hexagon, distance 4.** The triangulations with diagonals $v_1 v_5$, $v_2 v_4$, $v_2 v_5$ and with $v_0 v_3$, $v_0 v_4$, $v_1 v_3$ share no diagonal and are at distance 4, the diameter of the flip graph of the hexagon. Here the lower bound $|T_1 \setminus T_2| = 3$ is not tight.
- **The diameter for small convex polygons.** Breadth-first search over all triangulations gives the largest flip distance 4 for $n = 6$ (14 triangulations), 5 for $n = 7$ (42) and 7 for $n = 8$ (132).
- **Points with a reflex chain.** Hurtado, Noy and Urrutia give $n$ points, two concave chains facing each other, with two triangulations at distance $\Omega(n^2)$, because each flip can change the edges between the chains only locally.

## Known algorithms

| setting | result |
|---|---|
| any, small input | breadth-first or A* search in the flip graph; exact, exponential |
| convex polygon | exact complexity open; FPT with a kernel of size $5k$ (Cleary and St. John), improved to $2k$ (Lucas) |
| convex polygon | factor 2 approximation in linear time |
| point set | NP-complete, APX-hard; FPT in $k$ (Kanj, Sedgwick and Xia) |
| simple polygon | NP-complete |

**Common diagonals in convex polygons.** Sleator, Tarjan and Thurston proved that if $T_1$ and $T_2$ share a diagonal, then no shortest flip sequence flips it. So the problem splits along common diagonals into independent polygons. This is the basis of the kernels, and of the factor 2 approximation: in each piece with $n_i$ vertices and no common diagonal, the fan bound gives at most $2(n_i - 3)$ flips, twice the lower bound $n_i - 3$. For point sets the property fails: some shortest sequences must flip a common edge away and back, which is one reason the general problem is harder.

## Bounds

- **Convex polygons.** The diameter of the flip graph is exactly $2n - 10$ for $n \ge 13$; see the [flip graph diameter theorem](/flip-graph-diameter-theorem/). The decision problem is in NP, and its hardness is open.
- **Point sets and polygons.** The distance is $O(n^2)$, through the Delaunay triangulation or a canonical triangulation, and $\Theta(n^2)$ in the worst case.
- **Hardness.** NP-complete for point sets and simple polygons; for point sets, no polynomial approximation scheme unless P = NP.

## Reductions

- **From vertex cover.** Lubiw and Pathak, and Pilz, encode a graph by a point set with double chains for the vertices and edges, so that a short flip sequence corresponds to a small vertex cover.
- **From rectilinear Steiner arborescence.** Aichholzer, Mulzer and Pilz reduce this NP-hard problem to flip distance in simple polygons.
- **To rotation distance.** For convex polygons, flip distance and rotation distance of binary trees are the same problem, through the [dual tree](/triangulation-dual-tree/).

## Applications

- **Self-adjusting data structures.** Rotation distance measures how far one binary search tree is from another; see [tree rotation](/tree-rotation/).
- **Phylogenetics and RNA folding.** Distances between trees and secondary structures are defined by local moves of the same kind.
- **Mesh optimization.** The [Lawson flip algorithm](/lawson-flip-algorithm/) uses $O(n^2)$ flips to reach the Delaunay triangulation, which bounds the distance of any triangulation to it.

## References
