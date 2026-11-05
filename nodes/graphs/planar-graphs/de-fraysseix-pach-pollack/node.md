---
tag: FQHSKN
kind: algorithm
slug: de-fraysseix-pach-pollack
name: de Fraysseix-Pach-Pollack algorithm
aliases:
- shift method
- shift algorithm
area: graphs/planar-graphs
level: advanced
summary: Linear-time straight-line drawing on a (2n-4) by (n-2) grid using the shift method.
solves: [planar-straight-line-drawing]
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: O(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, needs_embedding: true, recursive: false}
history:
  year: 1990
  people: [Hubert de Fraysseix, János Pach, Richard Pollack, Marek Chrobak, Thomas H. Payne]
  note: de Fraysseix, Pach and Pollack gave the shift method with an O(n log n) bound in 1988 and 1990; Chrobak and Payne made it linear in 1995.
prereqs: [canonical-ordering, maximal-planar-graph, rotation-system, fary-theorem]
see_also: [planar-straight-line-drawing, schnyder-drawing, schnyder-woods, graph-drawing, tutte-spring-theorem, planar-embedding, doubly-connected-edge-list, st-numbering]
sources:
  - paper: doi:10.1007/BF02122694
    title: Hubert de Fraysseix, János Pach and Richard Pollack, How to draw a planar graph on a grid, Combinatorica 10(1), 41 to 51 (1990)
    locator: the canonical ordering, the shift method with the sets M(v), and the (2n-4) by (n-2) grid bound
  - paper: "Marek Chrobak and Thomas H. Payne, A linear-time algorithm for drawing a planar graph on a grid, Information Processing Letters 54(4), 241 to 246 (1995)"
    locator: the relative offsets in a tree that make the shifts cost O(1) each
  - paper: doi:10.1007/BF02086606
    title: Goos Kant, Drawing planar graphs using the canonical ordering, Algorithmica 16(1), 4 to 32 (1996)
    locator: the extension to 3-connected graphs and convex drawings
  - book: "Giuseppe Di Battista, Peter Eades, Roberto Tamassia and Ioannis G. Tollis, Graph Drawing, Algorithms for the Visualization of Graphs, Prentice Hall, 1999"
    locator: the chapter on straight-line drawings of planar graphs (the shift method)
  - book: "Takao Nishizeki and Md. Saidur Rahman, Planar Graph Drawing, World Scientific, 2004"
    locator: Chapter 4, Straight line drawing (the shift method and its linear-time implementation)
---

The de Fraysseix-Pach-Pollack algorithm draws a maximal [planar graph](/planar-graph/) with $n \ge 3$ vertices with straight-line edges, no crossings, and all vertices at integer points of a $(2n - 4) \times (n - 2)$ grid. It adds the vertices in a [canonical ordering](/canonical-ordering/), places each new vertex at the apex of two lines of slope $+1$ and $-1$ over the part of the outline it attaches to, and makes room by shifting parts of the drawing to the right. With the relative offsets of Chrobak and Payne it runs in $O(n)$ time. It gives an algorithmic proof of [Fáry's theorem](/fary-theorem/) in which all coordinates are integers of size $O(n)$.

## In plain words

Start with one small triangle on a base line. Add the other points one by one, in an order where each new point connects to a run of points along the current top outline.

Each new point goes at the top of a roof: one line goes up at 45 degrees from the left end of the run, another from the right end, and the point sits where they meet. From there it can see every point of the run.

The roof may be too flat, so that the new point would touch the outline. So before placing it, the algorithm pushes the right part of the drawing one step to the right, and the far right part two steps. Everything that hangs below a pushed point moves with it, so nothing crosses. The final picture fits in a box about twice as wide as the number of points.

## The problem

Given a maximal planar graph $G$ with $n \ge 3$ vertices, with its embedding given as a [rotation system](/rotation-system/) (for each vertex, its neighbours in counterclockwise order) and an outer face $v_1, v_2, v_n$ listed counterclockwise, find integer coordinates for the vertices such that the straight segments for the edges meet only at common endpoints, and the drawing has the given rotation system. A planar graph that is not maximal is first triangulated, in linear time, by adding edges inside faces; the added edges are deleted from the drawing at the end (see [planar straight-line drawing](/planar-straight-line-drawing/)). The input is a combinatorial embedding, not coordinates.

## The algorithm

Write the contour of the current drawing as $c_1 = v_1, c_2, \ldots, c_t = v_2$, from left to right. For each contour vertex $c$, the set $M(c)$ holds the vertices that move together with $c$; when the algorithm shifts $c$ to the right, it shifts all of $M(c)$.

```pseudo id=main
DFPP(G, v1, v2, vn)                    ▷ G maximal planar, given by a rotation system
L1  compute a canonical ordering v1, v2, ..., vn
L2  place v1 at (0, 0), v3 at (1, 1), v2 at (2, 0); contour ← v1, v3, v2
L3  for k ← 4 to n do
L4      w_p, ..., w_q ← the neighbours of v_k on the contour, from left to right
L5      shift every vertex of M(w_{p+1}) by 1 to the right
L6      shift every vertex of M(w_q) by 1 more to the right
L7      place v_k at the intersection of the line of slope +1 through w_p and the line of slope −1 through w_q
L8      M(w_i) ← M(w_i) ∪ {v_k} for i ≤ p; M(v_k) ← {v_k} ∪ M(w_{p+1})
L9      w_{p+1}, ..., w_{q−1} leave the contour (they are covered by v_k)
L10     contour ← c_1, ..., w_p, v_k, w_q, ..., c_t
L11 compute the final x-coordinates (only needed with relative offsets)
L12 return the coordinates
```

**Line L7 in numbers.** With $w_p = (x_p, y_p)$ and $w_q = (x_q, y_q)$, the new vertex is

$$x = \frac{x_p + x_q + y_q - y_p}{2}, \qquad y = \frac{x_q - x_p + y_p + y_q}{2}.$$

Both are integers, because every contour edge has slope $+1$ or $-1$, so $x_q - x_p + y_q - y_p$ is even, and lines L5 and L6 add 2 to $x_q - x_p$.

**Why shift.** Before the shift, $w_p$ and $w_q$ might be joined by contour edges of slope exactly $+1$ next to $w_p$, so that the line of slope $+1$ through $w_p$ runs along the contour and $v_k$ would see $w_{p+1}$ on a contour edge. After the shift, every covered vertex lies strictly below both lines, so $v_k$ sees each of $w_p, \ldots, w_q$ along a free segment.

**The sets $M$.** The set $M(c)$ is the set of vertices that are "under or to the right of" $c$ in the sense of the construction: $c$, the vertices covered by $c$ and, recursively, the vertices they cover, and everything at or after the next contour vertex. Shifting $M(w_{p+1})$ moves the covered part together with all of the right side, so the shapes hanging below the contour move rigidly.

**Linear time (Chrobak and Payne).** Shifting the sets $M$ explicitly costs $O(n)$ per step and $O(n^2)$ in total. Instead, store for each vertex an x-offset relative to a parent in a tree: a contour vertex's parent is its left neighbour on the contour, and a covered vertex's parent is the vertex that covered it (for the first covered vertex) or its left neighbour in the covered chain. Then $M(c)$ is the set of descendants of $c$, and a shift of $M(c)$ is one addition to the offset of $c$. In the implementation, lines L5 and L6 add 1 to the offsets of $w_{p+1}$ and $w_q$; line L7 sums the offsets of $w_{p+1}, \ldots, w_q$ to get $x_q - x_p$, which costs one step per covered vertex; lines L8 to L10 rewrite the offsets of $w_{p+1}$ and $w_q$ relative to $v_k$; and line L11 sums offsets from the root $v_1$ down the tree with an explicit stack. The canonical ordering of line L1 comes from the peeling procedure on the [canonical ordering](/canonical-ordering/) page, which also records $w_p$ and $w_q$ for each vertex.

## Example

**$K_4$.** Take the triangle $0, 1, 2$ (counterclockwise) with vertex 3 inside: the rotation system is $0: (1, 3, 2)$, $1: (2, 3, 0)$, $2: (0, 3, 1)$, $3: (0, 1, 2)$. The canonical ordering is $0, 1, 3, 2$. Place $0 = (0,0)$, $3 = (1,1)$, $1 = (2,0)$. Vertex 2 attaches to the whole contour $0, 3, 1$, so $w_p = 0$, $w_q = 1$: shift $M(3) = \{3, 1\}$ by 1 and $M(1) = \{1\}$ by 1 more, giving $3 = (2,1)$ and $1 = (4,0)$. Then $2 = ((0 + 4 + 0 - 0)/2, (4 - 0 + 0 + 0)/2) = (2, 2)$. The grid is $4 \times 2 = (2n - 4) \times (n - 2)$.

**The octahedron.** Take the octahedron with outer face $0, 1, 2$ and inner triangle $3, 4, 5$, where 3 is adjacent to 0 and 1, 4 to 1 and 2, and 5 to 2 and 0 (the drawing on the [canonical ordering](/canonical-ordering/) page). The implementation's canonical ordering is $0, 1, 3, 5, 4, 2$. The trace, with all coordinates after the step:

| step | $v_k$ | $w_p, \ldots, w_q$ | shifted by 1 | shifted by 2 | $v_k$ placed at | contour |
|---|---|---|---|---|---|---|
| start | 0, 3, 1 | | | | $(0,0)$, $(1,1)$, $(2,0)$ | 0, 3, 1 |
| $k = 4$ | 5 | 0, 3 | | 3, 1 | $(2, 2)$ | 0, 5, 3, 1 |
| $k = 5$ | 4 | 5, 3, 1 | 3 | 1 | $(3, 3)$ | 0, 5, 4, 1 |
| $k = 6$ | 2 | 0, 5, 4, 1 | 5, 3, 4 | 1 | $(4, 4)$ | 0, 2, 1 |

At $k = 4$, $p + 1 = q$, so $M(w_{p+1}) = M(w_q) = M(3) = \{3, 1\}$ moves by 2: $3 = (3,1)$, $1 = (4,0)$. At $k = 5$, $M(3) = \{3, 1\}$ moves by 1 and $M(1)$ by 1 more: $3 = (4,1)$, $1 = (6,0)$. At $k = 6$, $M(5) = \{5, 3, 1, 4\}$ moves by 1 and $M(1)$ by 1 more. The final coordinates are

| vertex | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| $(x, y)$ | $(0,0)$ | $(8,0)$ | $(4,4)$ | $(5,1)$ | $(4,3)$ | $(3,2)$ |

inside the $8 \times 4$ grid. The tests check these coordinates, check that no two edges cross, and check that the counterclockwise order of neighbours at each vertex equals the input rotation system.

**Inputs that are not triangulations.** A single vertex, an edge, a tree, $K_5$ and $K_{3,3}$ are rejected: the implementation traces the faces of the rotation system and requires that every face is a triangle and that $n - m + f = 2$. The tests try all 7776 rotation systems of $K_5$ (with one fixed neighbour first at each vertex) and all 64 of $K_{3,3}$. To draw a tree or any other planar graph, triangulate it first.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). After step $k$ the drawing of $G_k$ satisfies three invariants: the contour is x-monotone ($x(c_1) < x(c_2) < \cdots < x(c_t)$); each contour edge has slope $+1$ or $-1$; and for every nondecreasing sequence $0 \le \delta_1 \le \cdots \le \delta_t$, shifting each vertex of $M(c_i) \setminus M(c_{i+1})$ by $\delta_i$ keeps every bounded face a positively oriented triangle. Line L5 and L6 are such a shift. After it, every covered vertex lies strictly below the two lines of slope $\pm 1$ through $w_p$ and $w_q$, so the new triangles $v_k w_i w_{i+1}$ are positively oriented. A straight-line drawing of a triangulated disk whose bounded faces are all positively oriented triangles and whose outer boundary is a simple polygon has no crossings, by a winding number count. At the end the outer boundary is the triangle $v_1, v_2, v_n$.

**The grid.** Each step adds 2 to $x(v_2)$, so $x(v_2) = 2 + 2(n - 3) = 2n - 4$. The last vertex attaches to $w_p = v_1$ and $w_q = v_2$, so $y(v_n) = (2n - 4)/2 = n - 2$. Every contour vertex satisfies $|y(c_j) - y(c_i)| \le x(c_j) - x(c_i)$ along the contour, so all vertices lie in the triangle with corners $(0,0)$, $(2n - 4, 0)$ and $(n - 2, n - 2)$.

## Complexity

- **Canonical ordering (line L1).** Linear: each vertex enters the contour once, and its edges are scanned once at that moment to count chords; see [canonical ordering](/canonical-ordering/). Finding the position of $w_p$ in the rotation of $v_k$ costs $O(\deg v_k)$, $O(m) = O(n)$ in total.
- **Shifts (lines L5 and L6).** With relative offsets, $O(1)$ each.
- **Placement (line L7).** Summing the offsets of $w_{p+1}, \ldots, w_q$ costs $O(q - p)$. The $q - p - 1$ covered vertices leave the contour forever, so the total over all steps is $O(n)$.
- **Final coordinates (line L11).** One traversal of the tree, $O(n)$.

The total is $O(n)$ time and $\Theta(n)$ extra space. The explicit sets $M$ of the original description give $O(n^2)$ time; de Fraysseix, Pach and Pollack brought it to $O(n \log n)$, and Chrobak and Payne to $O(n)$. Coordinates are at most $2n - 4$, so they fit in a word.

## Properties

- **Grid size.** Width $2n - 4$, height $n - 2$, area below $2n^2$. Every planar graph with $n \ge 3$ vertices has such a drawing, and the nested triangles graph needs width and height about $2n/3$, so quadratic area is necessary in the worst case.
- **Embedding preserving.** The drawing realizes the given rotation system and outer face.
- **Flat shapes.** Contour edges have slope $\pm 1$ when drawn, and later shifts stretch them, so many faces become long and thin. The drawings are hard to read for large graphs.
- **Deterministic.** The output depends only on the rotation system, the outer face and the tie-breaking in the canonical ordering.

## Variants and improvements

- **Chrobak-Payne.** The linear-time version used here.
- **Smaller grids.** Chrobak and Kant reduced the grid to $(n - 2) \times (n - 2)$ with a variant of the shift method for 3-connected graphs. [Schnyder drawings](/schnyder-drawing/) from [Schnyder woods](/schnyder-woods/) give $(n - 2) \times (n - 2)$ by barycentric coordinates and are simpler to implement.
- **Convex drawings.** Kant's canonical ordering for 3-connected graphs gives drawings with convex faces on a $(2n - 4) \times (n - 2)$ grid.
- **Other drawing styles.** The canonical ordering also drives visibility representations, orthogonal drawings and polyline drawings.

## When to use it

Use it when integer coordinates of size $O(n)$ are required, for example for exact geometric computation, for a proof that a straight-line drawing exists, or as a starting layout that another method improves. For drawings meant to be read by people, the very flat angles are a drawback, and [force-directed layouts](/force-directed-layout/), [Tutte embeddings](/tutte-spring-theorem/) for 3-connected graphs, or Schnyder drawings followed by post-processing are more common.

## Pitfalls

- **Rotation direction.** The method needs the outer face listed counterclockwise and rotations counterclockwise. Mixing conventions produces a mirror ordering and a drawing with crossings. The implementation checks the outer face orientation.
- **Not triangulated input.** The canonical ordering needs a maximal planar graph. Triangulate first, and do it without creating multiple edges: adding a chord inside a face can duplicate an edge that exists elsewhere.
- **Choosing the wrong neighbour range.** $w_p$ and $w_q$ must be the leftmost and rightmost contour neighbours of $v_k$. They are the contour neighbours of $v_k$ at the moment it is removed during peeling; recomputing them from the forward contour by scanning is quadratic.
- **Recursion.** The final pass over the offset tree visits a path of length up to $n$ for nested triangles; use an explicit stack.
- **Parity.** Skipping the second shift of line L6 breaks the parity argument, and coordinates become half-integers.

## Implementations

## History

De Fraysseix, Pach and Pollack presented the shift method at STOC 1988 and published it in Combinatorica in 1990. It answered a question of Rosenstiehl and Tarjan whether every planar graph has a straight-line drawing on a polynomial grid. Schnyder found a different method with an $(n - 2) \times (n - 2)$ grid at about the same time, published at SODA 1990. Chrobak and Payne gave the linear-time implementation in 1995, and Kant extended the canonical ordering to 3-connected graphs in 1996.

## References
