---
tag: XP59A1
kind: concept
slug: triangulation-dual-tree
name: Dual tree of a polygon triangulation
aliases:
- Triangulation dual graph
area: geometry/triangulations
level: intro
summary: The dual graph of a polygon triangulation is a tree with maximum degree three.
prereqs: [polygon-triangulation, tree, planar-dual-graph]
see_also: [two-ears-theorem, ear, art-gallery-theorem, catalan-triangulation-theorem, binary-tree, polygon-with-holes-triangulation]
sources:
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 1, Section 1.2, Triangulation, Theory (the dual of a triangulation is a tree of degree at most 3, and Meisters' theorem from its leaves)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 3, Section 3.1, Guarding and Triangulations (the dual graph and the 3-coloring by depth-first search)
  - paper: "Steve Fisk, A short proof of Chvátal's watchman theorem, Journal of Combinatorial Theory, Series B 24(3), 374 (1978)"
    locator: the 3-coloring of a triangulated polygon
---

The dual tree of a [polygon triangulation](/polygon-triangulation/) has one node for each triangle and one edge for each diagonal, joining the two triangles on its sides. For a simple polygon this graph is always a tree, and no node has more than three neighbors, because a triangle has only three sides. Many arguments and algorithms about polygons walk this tree: the [two ears theorem](/two-ears-theorem/), the 3-coloring behind the [art gallery theorem](/art-gallery-theorem/), and shortest paths inside a polygon.

## In plain words

Cut a polygon into triangles along straight cuts. Put a dot in each triangle, and join two dots when their triangles share a cut. The result never has a loop: each cut splits the polygon into two parts, so there is only one way to go from one triangle to another. Each dot has at most three lines, one per side of its triangle. A dot at the end of a branch is a triangle with two sides on the boundary, which is an ear that can be cut off.

## The idea

Let $P$ be a simple polygon with $n \ge 3$ vertices and let $T$ be a triangulation of $P$ by diagonals, with $n - 2$ triangles and $n - 3$ diagonals. The **dual graph** $G(T)$ has the triangles as nodes; two triangles are adjacent if they share a diagonal. It is the [planar dual](/planar-dual-graph/) of the triangulation with the node for the outer face removed.

**Claim.** $G(T)$ is a tree with $n - 2$ nodes, every node has degree at most 3, and for $n \ge 4$ the leaves are exactly the triangles $v_{i-1} v_i v_{i+1}$ of ears $v_i$.

- *Connected.* The interior of $P$ is connected, and a path inside it from one triangle to another passes from triangle to triangle through diagonals (it can be moved off the vertices).
- *No cycle.* A diagonal $d$ splits $P$ into two polygons, and every triangle lies on one side. Removing the edge of $d$ from $G(T)$ separates the triangles on the two sides, so every edge is a bridge, and a connected graph in which every edge is a bridge is a tree. Equivalently, it has $n - 2$ nodes and $n - 3$ edges and is connected.
- *Degree.* A triangle has three sides, and a node's degree is the number of its sides that are diagonals.
- *Leaves.* A leaf has one diagonal side and two polygon sides, which are consecutive polygon edges $v_{i-1} v_i$ and $v_i v_{i+1}$. Its third side $v_{i-1} v_{i+1}$ is a diagonal, so $v_i$ is an ear. Every tree with at least two nodes has at least two leaves, which gives the two ears theorem once a triangulation is known to exist.

**Degree counts.** Let $t_1, t_2, t_3$ be the numbers of triangles with 1, 2 and 3 diagonal sides, for $n \ge 4$. Counting nodes and degrees gives $t_1 + t_2 + t_3 = n - 2$ and $t_1 + 2 t_2 + 3 t_3 = 2(n - 3)$. Subtracting twice the first from the second gives $t_1 = t_3 + 2$: the number of ears in the triangulation is two more than the number of interior triangles, whose three sides are all diagonals.

**Rooting.** Fix a polygon edge $e$ and root the tree at the triangle on $e$. Each triangle then has a left and a right child, across its two sides other than the one toward the root, either of which may be missing (a polygon edge). This turns triangulations of a convex polygon into binary trees with $n - 2$ nodes, a bijection that gives the [Catalan count](/catalan-triangulation-theorem/).

**Beyond simple polygons.** For a [polygon with holes](/polygon-with-holes-triangulation/), the dual graph is connected but not a tree: each hole adds one independent cycle, since the triangles around a hole form a ring. For a triangulation of a point set, each interior point is surrounded by a cycle of triangles. For a triangulated region with connected interior, the dual graph is a tree exactly when the region has no holes and no vertex lies in its interior.

## Examples

- **A notched rectangle.** For $v_0 = (0,0)$, $v_1 = (6,0)$, $v_2 = (6,4)$, $v_3 = (4,4)$, $v_4 = (3,1)$, $v_5 = (2,4)$, $v_6 = (0,4)$, [ear clipping](/ear-clipping/) gives the triangles $A = v_5 v_6 v_0$, $B = v_4 v_5 v_0$, $C = v_4 v_0 v_1$, $D = v_4 v_1 v_2$, $E = v_4 v_2 v_3$. The diagonals $v_5 v_0$, $v_4 v_0$, $v_4 v_1$, $v_4 v_2$ give the dual edges $A B$, $B C$, $C D$, $D E$. The tree is a path with leaves $A$ and $E$, the ears at $v_6$ and $v_3$. Here $t_1 = 2$ and $t_3 = 0$.
- **A star.** In a convex hexagon $v_0 \ldots v_5$, take the diagonals $v_0 v_2$, $v_2 v_4$, $v_4 v_0$. The middle triangle $v_0 v_2 v_4$ is adjacent to all three others. The tree is a star with one node of degree 3 and three leaves, so $t_3 = 1$, $t_1 = 3$.
- **A fan.** All diagonals from $v_0$ in a convex polygon give a path; the fan is the triangulation whose dual is a path with the ears at $v_1$ and $v_{n-1}$.

## Where it is used

- **Two ears and ear clipping.** The leaves are ears; see the [two ears theorem](/two-ears-theorem/) and [ear clipping](/ear-clipping/).
- **Art gallery theorem.** Fisk's proof 3-colors the vertices of a triangulated polygon by walking the dual tree: color the first triangle, and each new triangle across a diagonal has two colored corners and one free corner that gets the third color. The smallest color class has at most $\lfloor n/3 \rfloor$ vertices and sees the whole polygon; see the [art gallery theorem](/art-gallery-theorem/).
- **Shortest paths in a polygon.** The triangles between the triangles holding two points form a unique path in the dual tree, the sleeve, and the funnel algorithm finds the shortest path through it in linear time (Lee and Preparata; Guibas, Hershberger, Leven, Sharir and Tarjan).
- **Polygon partitioning.** [Hertel-Mehlhorn](/hertel-mehlhorn/) removes diagonals from a triangulation while the pieces stay convex; the dual tree organizes the pieces.
- **Counting.** Rooted dual trees are binary trees, which gives the [Catalan count](/catalan-triangulation-theorem/) for convex polygons.

## References
